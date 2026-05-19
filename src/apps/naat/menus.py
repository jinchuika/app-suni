from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Naat
naat_children = (
    # ViewMenuItem(
    #     "Crear participante",
    #     reverse_lazy("participante_naat_add"),
    #     weight=30,
    #     icon="fa-user"),
    ViewMenuItem(
        "Calendario",
        reverse_lazy("sesion_naat_calendar"),
        weight=10,
        icon="fa-calendar"),
    ViewMenuItem(
        "Procesos de Naat",
        reverse_lazy("proceso_naat_list"),
        weight=20,
        icon="fa-cubes"),
    ViewMenuItem(
        "Tareas Naat",
        reverse_lazy("participantes_tareas_naat"),
        weight=12,
        icon="fa-tasks"),
    ViewMenuItem(
        "Informe avances Naat",
        reverse_lazy("informe_naat_participantes"),
        weight=12,
        group="cyd_admin,cyd_informes,cyd_capacitador_informe",
        icon="fa-share-alt"),    
        )

Menu.add_item(
    "user",
    ViewMenuItem(
        "Naat",
        '#',
        weight=10,
        icon="fa-sun-o",
        group="naat",
        children=naat_children)
        )
