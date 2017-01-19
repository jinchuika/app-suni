from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Menú de capacitación
cyd_children = (
    ViewMenuItem(
        "Cursos",
        reverse_lazy("curso_list"),
        weight=10,
        icon="fa-book"),
    ViewMenuItem(
        "Sedes",
        reverse_lazy("sede_list"),
        weight=10,
        icon="fa-map"),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Capacitación",
        '#',
        weight=10,
        icon="fa-graduation-cap",
        group="cyd",
        children=cyd_children))
