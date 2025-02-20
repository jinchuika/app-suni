from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# KA Lite
kalite_children = (
    ViewMenuItem(
        "Rúbricas",
        reverse_lazy("rubrica_list"),
        weight=10,
        icon="fa-list",
        group="kalite"
    ),
    ViewMenuItem(
        "Tipos de visita",
        reverse_lazy("tipovisita_list"),
        weight=5,
        icon="fa-list",
        group="kalite"
    ),
    ViewMenuItem(
        "Calendario",
        reverse_lazy("kalite_calendario"),
        weight=40,
        icon="fa-calendar",
        group="kalite,kalite_calendario"
    ),
    ViewMenuItem(
        "Informe",
        reverse_lazy("visita_kalite_informe"),
        weight=40,
        icon="fa-th",
        group="kalite"
    ),
    ViewMenuItem(
        "Gráficos",
        reverse_lazy("visita_kalite_dashboard"),
        weight=50,
        icon="fa-bar-chart",
        group="kalite"
    ),
)

Menu.add_item(
    "user",
    ViewMenuItem(
        "KA Lite",
        '#',
        weight=35,
        icon="fa-leaf",
        group="kalite,kalite_calendario",
        children=kalite_children
    )
)
