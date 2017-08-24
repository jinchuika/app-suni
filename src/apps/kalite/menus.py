from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# KA Lite
kalite_children = (
    ViewMenuItem(
        "Rúbricas",
        reverse_lazy("rubrica_list"),
        weight=10,
        icon="fa-list"),
    ViewMenuItem(
        "Tipos de visita",
        reverse_lazy("tipovisita_list"),
        weight=5,
        icon="fa-list",
        perm='kalite.add_tipovisita'),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "KA Lite",
        reverse_lazy('list_c'),
        weight=35,
        icon="fa-leaf",
        children=kalite_children))
