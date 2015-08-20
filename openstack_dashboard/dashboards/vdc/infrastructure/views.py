import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse  # noqa
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View  # noqa

from horizon import exceptions
from horizon import views

from openstack_dashboard import api
from openstack_dashboard.usage import quotas

from openstack_dashboard.dashboards.project.network_topology.instances \
    import tables as instances_tables
from openstack_dashboard.dashboards.project.network_topology.ports \
    import tables as ports_tables
from openstack_dashboard.dashboards.project.network_topology.routers \
    import tables as routers_tables

from openstack_dashboard.dashboards.project.instances import\
    console as i_console
from openstack_dashboard.dashboards.project.instances import\
    views as i_views
from openstack_dashboard.dashboards.project.instances.workflows import\
    create_instance as i_workflows
from openstack_dashboard.dashboards.project.networks import\
    views as n_views
from openstack_dashboard.dashboards.project.networks import\
    workflows as n_workflows
from openstack_dashboard.dashboards.project.routers import\
    views as r_views

class IndexView(views.HorizonTemplateView):
    template_name = 'vdc/infrastructure/index.html'
    page_title = _("Infrastructure")

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


class JSONView(View):

    @property
    def add_resource_url(self, view, resources):
        tenant_id = self.request.user.tenant_id
        for resource in resources:
            if (resource.get('tenant_id')
                    and tenant_id != resource.get('tenant_id')):
                continue
            resource['url'] = reverse(view, None, [str(resource['id'])])

    def _get_servers(self, request):
        # Get nova data
        try:
            servers, more = api.nova.server_list(request)
        except Exception:
            servers = []
        data = []
        console_type = getattr(settings, 'CONSOLE_TYPE', 'AUTO')
        # lowercase of the keys will be used at the end of the console URL.
        for server in servers:
            try:
                console = i_console.get_console(
                    request, console_type, server)[0].lower()
            except exceptions.NotAvailable:
                console = None

            server_data = {'name': server.name,
                           'status': server.status,
                           'task': getattr(server, 'OS-EXT-STS:task_state'),
                           'id': server.id}
            if console:
                server_data['console'] = console
            data.append(server_data)
        #self.add_resource_url('horizon:project:instances:detail', data)
        return data

    def _get_networks(self, request):
        # Get neutron data
        # if we didn't specify tenant_id, all networks shown as admin user.
        # so it is need to specify the networks. However there is no need to
        # specify tenant_id for subnet. The subnet which belongs to the public
        # network is needed to draw subnet information on public network.
        try:
            neutron_networks = api.neutron.network_list_for_tenant(
                request,
                request.user.tenant_id)
        except Exception:
            neutron_networks = []
        networks = [{'name': network.name,
                     'id': network.id,
                     'subnets': [{'cidr': subnet.cidr}
                                 for subnet in network.subnets],
                     'router:external': network['router:external']}
                    for network in neutron_networks]
        self.add_resource_url('horizon:project:networks:detail',
                              networks)

        # Add public networks to the networks list
        if self.is_router_enabled:
            try:
                neutron_public_networks = api.neutron.network_list(
                    request,
                    **{'router:external': True})
            except Exception:
                neutron_public_networks = []
            my_network_ids = [net['id'] for net in networks]
            for publicnet in neutron_public_networks:
                if publicnet.id in my_network_ids:
                    continue
                try:
                    subnets = [{'cidr': subnet.cidr}
                               for subnet in publicnet.subnets]
                except Exception:
                    subnets = []
                networks.append({
                    'name': publicnet.name,
                    'id': publicnet.id,
                    'subnets': subnets,
                    'router:external': publicnet['router:external']})

        return sorted(networks,
                      key=lambda x: x.get('router:external'),
                      reverse=True)


    def get(self, request, *args, **kwargs):
        data = {'servers': self._get_servers(request)}
        json_string = json.dumps(data, ensure_ascii=False)
        return HttpResponse(json_string, content_type='text/json')
