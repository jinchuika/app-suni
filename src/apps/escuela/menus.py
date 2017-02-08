from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Escuelas
escuela_children = (
    ViewMenuItem(
        "Buscar escuela",
        reverse_lazy("escuela_buscar"),
        weight=11,
        icon="fa-search"),
    ViewMenuItem(
        "Crear escuela",
        reverse_lazy("escuela_add"),
        weight=12,
        icon="fa-plus-square-o",
        perm='escuela.add_escuela'),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Escuelas",
        reverse_lazy('escuela_crear'),
        weight=10,
        icon="fa-building-o",
        children=escuela_children))
