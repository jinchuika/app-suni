from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Escuelas
escuela_children = (
    ViewMenuItem(
        "Crear escuela",
        reverse_lazy("escuela_add"),
        weight=10,
        icon="fa-plus-square-o",
        perm='escuela.add_escuela'),
    ViewMenuItem(
        "Buscar escuela",
        reverse_lazy("escuela_buscar"),
        weight=10,
        icon="fa-search"),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Escuelas",
        '#',
        weight=10,
        icon="fa-building-o",
        children=escuela_children))
