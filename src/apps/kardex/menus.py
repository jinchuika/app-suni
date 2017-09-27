from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Kardex
kardex_children = (
    ViewMenuItem(
        "Equipo",
        reverse_lazy("kardex_equipo_list"),
        weight=10,
        icon="fa-desktop"),
    ViewMenuItem(
        "Entradas",
        reverse_lazy("kardex_entrada"),
        weight=20,
        icon='fa-sign-in'),
    ViewMenuItem(
        "Salidas",
        reverse_lazy("kardex_salida"),
        weight=40,
        icon="fa-sign-out"),
    ViewMenuItem(
        "Proveedores",
        reverse_lazy("kardex_proveedor_list"),
        weight=50,
        icon="fa-truck"),
    ViewMenuItem(
        "Informe",
        reverse_lazy("kardex_informe"),
        weight=60,
        icon="fa-list-alt"),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Kardex",
        reverse_lazy('list_c'),
        weight=40,
        icon="fa-cog",
        group="kardex",
        children=kardex_children))
