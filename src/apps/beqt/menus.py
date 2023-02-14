from django.core.urlresolvers import reverse_lazy
from django.urls import reverse
from menu import Menu
from apps.main.menus import ViewMenuItem


# BEQT
# Entrada
entrada_children = (
    ViewMenuItem(
        "Listado de Entradas de Beqt",
        reverse_lazy('entrada_beqt_list'),
        weight=12,
        icon="fa-list green-color",
    ),
    ViewMenuItem(
        "Agregar Entrada de Beqt",
        reverse_lazy('entrada_beqt_add'),
        weight=12,
        perm="inventario.add_entrada",
        icon="fa-pencil-square-o",
    ),
)
# Solicitudes de Movimiento
solicitudes_children = (
    ViewMenuItem(
        "Listado de Solicitudes de Beqt",
        reverse_lazy('solicitudmovimiento_beqt_list'),
        weight=12,
        icon="fa-list-ul",
    ),
    ViewMenuItem(
        "Solicitud Movimiento de Beqt",
        reverse_lazy('solicitudmovimiento_beqt_add'),
        weight=12,
        group="beqt_cc,beqt_tecnico",
        icon="fa-clock-o",
    ),
)
# Dispositivos
dispositivos_children = (
    ViewMenuItem(
        "Tipos de Dispositivos de Beqt",
        reverse_lazy('dispositivotipo_beqt_add'),
        weight=12,
        group="inv_admin",
        icon="fa-gear",
    ),
    
    ViewMenuItem(
        "Dispositivos de beqt",
        reverse_lazy('dispositivo_beqt_list'),
        weight=12,
        icon=" fa-mobile-phone",
    ),   
)
# Salidas
salidas_children = (
    ViewMenuItem(
        "Salidas Pendientes Beqt",
        reverse_lazy('controlcalidad_beqt_list'),
        weight=12,
        icon="fa-list-ul",
    ),
    ViewMenuItem(
        "Agregar Salida de Beqt",
        reverse_lazy('salidainventario_beqt_add'),
        weight=12,
        group="beqt_cc",
        icon="fa-pencil-square-o",
    ),
    ViewMenuItem(
        "Revisiones de contabilidad para Beqt",
        reverse_lazy('revisionsalida_beqt_list'),
        weight=12,
        group="inv_conta",
        icon="fa-check",
    ),
    ViewMenuItem(
        "Agregar Revision Beqt",
        reverse_lazy('revisionsalida_beqt_add'),
        weight=12,
        group="inv_conta",
        icon="fa-plus-square",
    ),   
)



# Administrador
admin_children = (
    ViewMenuItem(
        "Asignacion Usuarios",
        reverse_lazy('asignaciontecnico_beqt_list'),
        weight=12,
        group="inv_admin",
        icon="fa-user-plus",
    ),
    ViewMenuItem(
        "Tipos de Dispositivos",
        reverse_lazy('dispositivotipo_beqt_add'),
        weight=12,
        group="inv_admin",
        icon="fa-gear",
    ),
    ViewMenuItem(
        "Informe de Entradas",
        reverse_lazy('contabilidad_entrada'),
        weight=12,
        icon="fa-file-pdf-o",
    ),
    ViewMenuItem(
        "Dispositivos x Entrada",
        reverse_lazy('contabilidad_entrada_dispositivo'),
        weight=12,
        icon="fa-sign-in",
    ),
    ViewMenuItem(
        "Informe de Salidas",
        reverse_lazy('contabilidad_salidas'),
        weight=12,
        icon="fa-file-pdf-o",
    ),   
    ViewMenuItem(
        "Resumen",
        reverse_lazy('contabilidad_resumen'),
        weight=12,
        icon="fa-file-pdf-o",
    ),
)

##################################################################
# CREACION DE MENÚS
##################################################################
Menu.add_item(
    "user",
    ViewMenuItem(
        "Entrada Beqt",
        reverse_lazy('entrada_beqt_list'),
        weight=10,
        icon="fa-sign-in",
        group="inv_conta,beqt",
        tipo="beqt",
        children=entrada_children
    )
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Solicitudes Beqt",
        reverse_lazy('solicitudmovimiento_beqt_add'),
        weight=10,
        icon="fa-exchange",
        group="beqt_tecnico,beqt_cc,beqt",
        tipo="beqt",
        children=solicitudes_children
    )
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Dispositivos Beqt",
        reverse_lazy('dispositivo_beqt_list'),
        weight=10,
        icon="fa-desktop",
        group="beqt",
        tipo="beqt",
        children=dispositivos_children
    )
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Salidas Beqt",
        reverse_lazy('salidainventario_beqt_add'),
        weight=10,
        icon="fa-sign-out",
        group="inv_conta,beqt",
        tipo="beqt",
        children=salidas_children
    )
)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Inventario Beqt",
        reverse_lazy('entrada_beqt_list'),
        weight=10,
        icon="fa-user",
        group="inv_conta",
        tipo="beqt",
        children=admin_children
    )
)
