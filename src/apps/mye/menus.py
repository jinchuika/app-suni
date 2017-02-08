from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Administración
mye_children = (
    ViewMenuItem(
        "Cooperantes",
        reverse_lazy("cooperante_list"),
        weight=10,
        icon="fa-users"),
    ViewMenuItem(
        "Proyectos",
        reverse_lazy("proyecto_list"),
        weight=10,
        icon="fa-object-group"),
    ViewMenuItem(
        "Informe",
        reverse_lazy("informe_mye"),
        weight=10,
        icon="fa-book"),
    )

Menu.add_item(
    "user",
    ViewMenuItem(
        "Monitoreo",
        reverse_lazy('list_c'),
        weight=10,
        icon="fa-search",
        group="mye",
        children=mye_children))
