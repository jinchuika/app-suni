from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Informe`
informe_children = (
    ViewMenuItem(
        "Informe General",
        reverse_lazy("informe"),
        weight=12,
        icon="fa fa-line-chart"
    ),
    ViewMenuItem(
        "KA Lite",
        reverse_lazy("visita_kalite_informe"),
        weight=13,
        icon="fa fa-leaf"
    ),
    ViewMenuItem(
        "Inventario",
        reverse_lazy("contabilidad_resumen"),
        weight=14,
        icon="fa fa-truck"
    )
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Informes Funsepa",
        reverse_lazy('informe'),
        weight=8,
        icon="fa fa-file-pdf-o",
        group="informes",
        children=informe_children
    )
)
