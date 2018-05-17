from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem


def prueba_externo(user):
    return not user.perfil.externo

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
        perm='escuela.add_escuela'),
        )
Menu.add_item(
    "user",
    ViewMenuItem(
        "Escuelas",
        reverse_lazy('escuela_crear'),
        weight=10,
        icon="fa-building-o",
        test=prueba_externo,
        children=escuela_children))
