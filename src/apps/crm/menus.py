from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Donantes`
crm_children = (
    ViewMenuItem(
        "Donantes",
        reverse_lazy("donante_list"),
        weight=12,
        icon="fa fa-user-o"
    ),
    ViewMenuItem(
        "Ofertas",
        reverse_lazy("oferta_list"),
        weight=12,
        icon="fa fa-recycle"
    )
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Donantes",
        reverse_lazy('donante_list'),
        weight=10,
        icon="fa fa-truck",
        group="crm",
        children=crm_children
    )
)
