from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Menú de capacitación
cyd_children = (
    ViewMenuItem(
        "Cursos",
        reverse_lazy("curso_list"),
        weight=10,
        icon="fa-users"),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Capacitación",
        '',
        weight=10,
        icon="fa-book",
        children=cyd_children))
