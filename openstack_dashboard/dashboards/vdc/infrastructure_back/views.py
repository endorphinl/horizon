#from horizon import views
from horizon import tabs 
from openstack_dashboard.dashboards.vdc.infrastructure import tabs as vdc_tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = vdc_tabs.MypanelTabs
    # A very simple class-based view...
    template_name = 'vdc/infrastructure/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context
