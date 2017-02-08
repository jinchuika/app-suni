from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Kardex
kardex_children = (
    ViewMenuItem(
        "Equipo",
        reverse_lazy("kardex_equipo"),
        weight=10,
        icon="fa-desktop"),
    ViewMenuItem(
        "Entradas",
        reverse_lazy("kardex_entrada"),
        weight=20,
        icon='fa-arrow-up'),
    ViewMenuItem(
        "Salidas",
        reverse_lazy("kardex_salida"),
        weight=40,
        icon="fa-arrow-down"),
    ViewMenuItem(
        "Proveedores",
        reverse_lazy("kardex_proveedor"),
        weight=50,
        icon="fa-truck"),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Kardex",
        reverse_lazy('kardex_equipo'),
        weight=40,
        icon="fa-cog",
        group="kardex",
        children=kardex_children))
