from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Naat
naat_children = (
    ViewMenuItem(
        "Crear participante",
        reverse_lazy("participante_naat_add"),
        weight=20,
        icon="fa-user"),
    ViewMenuItem(
        "Calendario",
        reverse_lazy("sesion_naat_calendar"),
        weight=10,
        icon="fa-calendar"),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Naat",
        '#',
        weight=10,
        icon="fa-sun-o",
        group="naat",
        children=naat_children))
