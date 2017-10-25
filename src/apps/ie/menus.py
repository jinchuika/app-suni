from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Nación Digital
ie_children = (
    ViewMenuItem(
        "Informe laboratorios",
        reverse_lazy("laboratorio_list"),
        weight=10,
        icon="fa-list"),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Nación digital",
        '#',
        weight=40,
        icon="fa-cubes",
        group="nacion_digital",
        children=ie_children))
