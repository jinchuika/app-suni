from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Informe`
informe_children = (
    ViewMenuItem(
        "Informe",
        reverse_lazy("informe"),
        weight=12,
        icon="fa fa-calendar-plus-o"
    )
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Informe",
        reverse_lazy('informe'),
        weight=10,
        icon="fa fa-chrome",
        group="",
        children=informe_children
    )
)
