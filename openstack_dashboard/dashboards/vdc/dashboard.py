from django.utils.translation import ugettext_lazy as _

import horizon

class Manage(horizon.PanelGroup):
    slug = "manage"
    name = _("Manage")
    panels = ('infrastructure',)

class Vdc(horizon.Dashboard):
    name = _("VDC")
    slug = "vdc"
    panels = (Manage,)  # Add your panels here.
    default_panel = 'infrastructure'  # Specify the slug of the dashboard's default panel.


horizon.register(Vdc)
