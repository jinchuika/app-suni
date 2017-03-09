from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Administración
tpe_children = (
    ViewMenuItem(
        "Garantías",
        reverse_lazy("garantia_list"),
        weight=10,
        icon="fa-gavel"),
    ViewMenuItem(
        "Lista de entregas",
        reverse_lazy("equipamiento_list"),
        weight=80,
        icon="fa-list"),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Equipamiento",
        reverse_lazy('list_c'),
        weight=10,
        icon="fa-desktop",
        group="tpe",
        children=tpe_children))
