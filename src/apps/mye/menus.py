from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Evaluación
mye_children = (
    ViewMenuItem(
        "Cooperantes",
        reverse_lazy("cooperante_list"),
        weight=10,
        icon="fa-users"),
    ViewMenuItem(
        "Proyectos",
        reverse_lazy("proyecto_list"),
        weight=20,
        icon="fa-object-group"),
    ViewMenuItem(
        "Listado de solicitudes",
        reverse_lazy("solicitud_list"),
        weight=40,
        icon="fa-folder-open-o"),
    ViewMenuItem(
        "Listado de validaciones",
        reverse_lazy("validacion_list"),
        weight=50,
        icon="fa-check-square-o"),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Evaluación",
        '#',
        weight=10,
        icon="fa-search",
        group="mye",
        children=mye_children))

# Consulta
consulta_children = (
    ViewMenuItem(
        "Cooperantes",
        reverse_lazy("cooperante_list"),
        weight=10,
        icon="fa-users"),
    ViewMenuItem(
        "Proyectos",
        reverse_lazy("proyecto_list"),
        weight=20,
        icon="fa-object-group"),
    ViewMenuItem(
        "Listado de solicitudes",
        reverse_lazy("solicitud_list"),
        weight=40,
        icon="fa-folder-open-o"),
    ViewMenuItem(
        "Informe de entregas",
        reverse_lazy("equipamiento_informe"),
        weight=50,
        icon="fa-list-alt"),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Evaluación",
        '#',
        weight=10,
        icon="fa-search",
        group="consulta",
        children=consulta_children))
