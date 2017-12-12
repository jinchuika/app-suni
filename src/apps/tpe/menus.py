from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Equipamiento
tpe_children = (
    ViewMenuItem(
        "Lista de entregas",
        reverse_lazy("equipamiento_list"),
        weight=60,
        icon="fa-list"),
    ViewMenuItem(
        "Informe de monitoreo",
        reverse_lazy("monitoreo_list"),
        weight=70,
        icon="fa-phone"),
    ViewMenuItem(
        "Mapa de escuelas",
        reverse_lazy("equipamiento_map"),
        weight=80,
        icon="fa-map-o"),
    ViewMenuItem(
        "Informe de entregas",
        reverse_lazy("equipamiento_informe"),
        weight=90,
        icon="fa-list-alt"),
    ViewMenuItem(
        "Calendario",
        reverse_lazy("calendario_tpe"),
        weight=75,
        icon="fa-calendar"),
    ViewMenuItem(
        "Evaluación",
        reverse_lazy("evaluacionmonitoreo_list"),
        weight=95,
        icon="fa-check"),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Equipamiento",
        reverse_lazy('list_c'),
        weight=10,
        icon="fa-desktop",
        group="tpe",
        children=tpe_children))

# Garantías
garantia_children = (
    ViewMenuItem(
        "Lista de Garantías",
        reverse_lazy("garantia_list"),
        weight=10,
        icon="fa-gavel"),
    ViewMenuItem(
        "Tickets de soporte",
        reverse_lazy("ticket_informe"),
        weight=10,
        icon="fa-ticket"),
    ViewMenuItem(
        "Reparaciones",
        reverse_lazy("ticket_reparacion_informe"),
        weight=10,
        icon="fa-plug"),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Garantías",
        reverse_lazy('list_c'),
        weight=10,
        icon="fa-wrench",
        group="garantia",
        children=garantia_children))
