from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Evaluacion 
evaluacion_children = (
    ViewMenuItem(
        "Listado de Formulario",
        reverse_lazy("formulario_list"),
        weight=12,
        icon="fa fa-files-o"
    ),
    ViewMenuItem(
        "Añadir Formulario",
        reverse_lazy("formulario_add"),
        weight=12,
        icon="fa fa-plus-circle"
    ),
    ViewMenuItem(
        "Informe Evaluación",
        reverse_lazy("informe_estadisticas"),
        weight=12,
        icon="fa fa-bar-chart"
    ),
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Evaluacion",
        reverse_lazy('formulario_list'),
        weight=10,
        icon="fa fa-list",
        group="eva_tpe,eva_admin,eva_capacitacion",
        children=evaluacion_children
    )
)
