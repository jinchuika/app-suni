from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Donantes`
crm_children = (
    ViewMenuItem(
        "Ingresar Donante",
        reverse_lazy("donantes_add"),
        weight=12,
        icon="fa-list"
    ),
    ViewMenuItem(
        "Ingresar Oferta",
        reverse_lazy("oferta_add"),
        weight=12,
        icon="fa-wrench"
    )
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Donantes",
        reverse_lazy('donantes_add'),
        weight=10,
        icon="fa-desktop",
        children=crm_children
    )
)
