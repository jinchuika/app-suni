from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Menú de capacitación
cyd_children = (
    ViewMenuItem(
        "Cursos",
        reverse_lazy("curso_list"),
        weight=10,
        icon="fa-book"),
    ViewMenuItem(
        "Sedes",
        reverse_lazy("sede_list"),
        weight=10,
        icon="fa-map"),
    ViewMenuItem(
        "Grupos",
        reverse_lazy("grupo_list"),
        weight=10,
        icon="fa-users"),)

cyd_participantes_children = (
    ViewMenuItem(
        "Nuevo",
        reverse_lazy("participante_add"),
        weight=10,
        icon="fa-plus"),
    ViewMenuItem(
        "Ingresar listado",
        reverse_lazy("participante_importar"),
        weight=20,
        icon="fa-list"),
    ViewMenuItem(
        "Buscar participante",
        reverse_lazy("participante_buscar"),
        weight=20,
        icon="fa-search"),)

cyd_control_academico_children = (
    ViewMenuItem(
        "Control Académico",
        reverse_lazy("control_academico_grupo"),
        weight=12,
        icon="fa-book"),)

cyd_calendario_children = (
    ViewMenuItem(
        "Capacitación",
        reverse_lazy("cyd_calendario"),
        weight=10,
        icon="fa-calendar"),)

cyd_informes_children = (
    ViewMenuItem(
        "Control academico",
        reverse_lazy("informe_control_academico"),
        weight=12,
        icon="fa-list-ol"),
        
     ViewMenuItem(
        "Asistencia",
        reverse_lazy("informe_asistencia"),
        weight=12,
        icon="fa-file-pdf-o"),
    
    ViewMenuItem(
        "Finalizacion proyecto",
        reverse_lazy("informe_finalizacion_proyecto"),
        weight=12,
        icon="fa-check-circle"),
    
    ViewMenuItem(
        "Capacitador",
        reverse_lazy("informe_capacitador"),
        weight=12,
        icon="fa-file-pdf-o"),
    
    ViewMenuItem(
        "Escuela",
        reverse_lazy("informe_escuela"),
        weight=12,
        icon="fa-file-pdf-o"),
    
    ViewMenuItem(
        "Listado escuela",
        reverse_lazy("informe_escuela_lista"),
        weight=12,
        icon="fa-file-pdf-o"),
    
    ViewMenuItem(
        "Grupo",
        reverse_lazy("informe_grupo"),
        weight=12,
        icon="fa-file-pdf-o"),
    
    ViewMenuItem(
        "Asistencia periodo",
        reverse_lazy("informe_asistencia_periodos"),
        weight=12,
        icon="fa-file-pdf-o"),
    
    ViewMenuItem(
        "Escuela sede",
        reverse_lazy("informe_escuela_sede"),
        weight=12,
        icon="fa-file-pdf-o"),
    
    ViewMenuItem(
        "Escuela capacitada",
        reverse_lazy("informe_escuela_capacitadas"),
        weight=12,
        icon="fa-file-pdf-o"),
        
        
        )

Menu.add_item(
    "user",
    ViewMenuItem(
        "Capacitación",
        '#',
        weight=10,
        icon="fa-graduation-cap",
        group="cyd",
        children=cyd_children),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Participantes",
        '#',
        weight=10,
        icon="fa-user",
        group="cyd",
        children=cyd_participantes_children),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Control Académico",
        '#',
        weight=10,
        icon="fa-book",
        group="cyd",
        children=cyd_control_academico_children),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Calendario",
        '#',
        weight=10,
        icon="fa-calendar",
        group="cyd",
        children=cyd_calendario_children),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Informes",
        '#',
        weight=10,
        icon="fa-file-pdf-o",
        group="cyd",
        children=cyd_informes_children),)