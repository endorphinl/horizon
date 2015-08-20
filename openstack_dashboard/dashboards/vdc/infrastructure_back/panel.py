from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.vdc import dashboard

class Infrastructure(horizon.Panel):
    name = _("Infrastructure")
    slug = "infrastructure"


dashboard.Vdc.register(Infrastructure)
