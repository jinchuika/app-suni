from django.core.urlresolvers import reverse_lazy
from django.urls import reverse
from menu import Menu
from apps.main.menus import ViewMenuItem


# Inventario
# Entrada
entrada_children = (
    ViewMenuItem(
        "Listado de Entradas",
        reverse_lazy('entrada_list'),
        weight=12,
        icon="fa-list",
    ),
    ViewMenuItem(
        "Agregar Entrada",
        reverse_lazy('entrada_add'),
        weight=12,
        perm="inventario.add_entrada",
        icon="fa-pencil-square-o",
    ),
)
# Solicitudes de Movimiento
solicitudes_children = (
    ViewMenuItem(
        "Listado de Solicitudes",
        reverse_lazy('solicitudmovimiento_list'),
        weight=12,
        icon="fa-list-ul",
    ),
    ViewMenuItem(
        "Solicitud Movimiento",
        reverse_lazy('solicitudmovimiento_add'),
        weight=12,
        group="inv_cc,inv_tecnico",
        icon="fa-clock-o",
    ),
    ViewMenuItem(
        "Devoluciones",
        reverse_lazy('devolucion_add'),
        weight=12,
        group="inv_cc,inv_tecnico",
        icon="fa-road",
    ),
)
# Dispositivos
dispositivos_children = (
    ViewMenuItem(
        "Tipos de Dispositivos",
        reverse_lazy('dispositivotipo_add'),
        weight=12,
        group="inv_admin",
        icon="fa-gear",
    ),
    ViewMenuItem(
        "Sistema Operativo",
        reverse_lazy('versionsistema_list'),
        group="inv_bodega",
        weight=12,
        icon="fa-linux",
    ),
    ViewMenuItem(
        "Softwate",
        reverse_lazy('software_list'),
        weight=12,
        group="inv_bodega",
        icon="fa-firefox",
    ),
    ViewMenuItem(
        "Dispositivos",
        reverse_lazy('dispositivo_list'),
        weight=12,
        icon=" fa-mobile-phone",
    ),
    ViewMenuItem(
        "Dispositivos por tarima  ",
        reverse_lazy('dispositivo_tarima'),
        group="inv_bodega",
        weight=12,
        icon="fa-desktop",
    ),
    ViewMenuItem(
        "Asignacion Repuestos",
        reverse_lazy('repuesto_list'),
        weight=12,
        icon="fa-archive",
    ),
)
# Salidas
salidas_children = (
    ViewMenuItem(
        "Salidas Pendientes",
        reverse_lazy('controlcalidad_list'),
        weight=12,
        icon="fa-list-ul",
    ),
    ViewMenuItem(
        "Agregar Salida",
        reverse_lazy('salidainventario_add'),
        weight=12,
        group="inv_cc,inv_bodega",
        icon="fa-pencil-square-o",
    ),
    ViewMenuItem(
        "Revisiones",
        reverse_lazy('revisionsalida_list'),
        weight=12,
        group="inv_conta",
        icon="fa-check",
    ),
    ViewMenuItem(
        "Agregar Revision",
        reverse_lazy('revisionsalida_add'),
        weight=12,
        group="inv_conta",
        icon="fa-plus-square",
    ),
    ViewMenuItem(
        "Prestamos",
        reverse_lazy('prestamo_list'),
        weight=12,
        group="inv_bodega",
        icon="fa-refresh",
    ),
)
# Desechos
desecho_children = (
    ViewMenuItem(
        "Empresa de Desecho",
        reverse_lazy('desechoempresa_list'),
        weight=12,
        icon="fa-recycle",
    ),
    ViewMenuItem(
        "Salidas de Desecho",
        reverse_lazy('desechosalida_add'),
        weight=12,
        icon="fa-archive",
    ),

)
# Contabilidad
contabilidad_children = (
    ViewMenuItem(
        "Periodo Fiscal",
        reverse_lazy('periodo_add'),
        weight=12,
        group="inv_conta",
        icon="fa-calendar-check-o",
    ),
    ViewMenuItem(
        "Precio Estándar",
        reverse_lazy('precioestandar_list'),
        weight=12,
        group="inv_conta,inv_admin",
        icon="fa-money",
    ),
    ViewMenuItem(
        "Informe x Periodo Fiscal",
        reverse_lazy('precioestandar_informe'),
        weight=12,
        group="inv_conta",
        icon="fa-file-pdf-o",
    ),
)

# Administrador
admin_children = (
    ViewMenuItem(
        "Asignacion Usuarios",
        reverse_lazy('asignaciontecnico_list'),
        weight=12,
        group="inv_admin",
        icon="fa-user-plus",
    ),
    ViewMenuItem(
        "Tipos de Dispositivos",
        reverse_lazy('dispositivotipo_add'),
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
        "Informe de Salidas",
        reverse_lazy('contabilidad_salidas'),
        weight=12,
        icon="fa-file-pdf-o",
    ),
    ViewMenuItem(
        "Informe Desecho",
        reverse_lazy('contabilidad_desecho'),
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
        "Entrada",
        reverse_lazy('entrada_list'),
        weight=10,
        icon="fa-sign-in",
        group="inventario,inv_conta",
        children=entrada_children
    )
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Solicitudes",
        reverse_lazy('entrada_list'),
        weight=10,
        icon="fa-exchange",
        group="inv_tecnico,inv_cc,inventario",
        children=solicitudes_children
    )
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Dispositivos",
        reverse_lazy('entrada_list'),
        weight=10,
        icon="fa-desktop",
        group="inventario",
        children=dispositivos_children
    )
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Salidas",
        reverse_lazy('entrada_list'),
        weight=10,
        icon="fa-sign-out",
        group="inventario,inv_conta",
        children=salidas_children
    )
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Desecho",
        reverse_lazy('entrada_list'),
        weight=10,
        icon="fa-trash-o",
        group="inv_bodega,inv_monitoreo",
        children=desecho_children
    )
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Contabilidad",
        reverse_lazy('entrada_list'),
        weight=10,
        icon="fa-archive",
        group="inv_conta,inv_admin",
        children=contabilidad_children
    )
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Inventario",
        reverse_lazy('entrada_list'),
        weight=10,
        icon="fa-user",
        group="inv_admin,inv_conta,inv_tecnico,inv_bodega",
        children=admin_children
    )
)
