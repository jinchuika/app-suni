from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Donantes`
crm_children = (
    ViewMenuItem(
        "Donantes",
        reverse_lazy("donante_list"),
        weight=12,
        group="crm",
        icon="fa fa-user-o"
    ),
    ViewMenuItem(
        "Ofertas",
        reverse_lazy("oferta_list"),
        weight=12,
        group="crm",
        icon="fa fa-recycle"
    ),
    ViewMenuItem(
        "Informe Proveedores",
        reverse_lazy("informe_gastos"),
        weight=12,
        group="crm,crm_informe_proveedores",
        icon="fas fa-columns"
    )
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Donantes",
        reverse_lazy('donante_list'),
        weight=10,
        icon="fa fa-truck",
        group="crm,crm_informe_proveedores",
        children=crm_children
    )
)
