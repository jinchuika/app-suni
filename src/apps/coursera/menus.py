from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Donantes`
coursera_children = (
    ViewMenuItem(
        "Monitoreo",
        reverse_lazy("monitoreo_add"),
        weight=12,
        icon="fa fa-calendar-plus-o"
    ),
    ViewMenuItem(
        "Informe",
        reverse_lazy("informe"),
        weight=12,
        icon="fa fa-bar-chart"
    )
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Coursera",
        reverse_lazy('monitoreo_add'),
        weight=10,
        icon="fa fa-chrome",
        group="coursera",
        children=coursera_children
    )
)
