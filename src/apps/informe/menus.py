from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Informe`
informe_children = (
    ViewMenuItem(
        "Informe General",
        reverse_lazy("informe_nuevo"),
        weight=12,
        icon="fa fa-line-chart"
    ),
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
