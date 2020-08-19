from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Bienestar`
bienestar_children = (
    ViewMenuItem(
        "Bienestar",
        reverse_lazy("bienestar_informe"),
        weight=12,
        icon="fa fa-area-chart"
    ),
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Bienestar",
        reverse_lazy('bienestar_informe'),
        weight=10,
        icon="fa fa-area-chart",
        group="bienestar",
        children=bienestar_children
    )
)
