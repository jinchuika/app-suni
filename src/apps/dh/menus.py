from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem


# Dejando huella
dh_children = (
    ViewMenuItem(
        "Calendario",
        reverse_lazy("evento_dh_calendario"),
        weight=10,
        icon="fa-calendar"),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Dejando Huella",
        reverse_lazy('list_c'),
        weight=10,
        icon="fa-heart",
        group="dejando_huella",
        children=dh_children))
