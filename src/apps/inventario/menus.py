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
        perm="inventario.add_solicitudmovimiento",
        icon="fa-clock-o",
    ),
    ViewMenuItem(
        "Devoluciones",
        reverse_lazy('devolucion_add'),
        weight=12,
        perm="inventario.add_solicitudmovimiento",
        icon="fa-road",
    ),
)
# Dispositivos
dispositivos_children = (
    ViewMenuItem(
        "Tipos de Dispositivos",
        reverse_lazy('dispositivotipo_add'),
        weight=12,
        perm="inventario.add_dispositivotipo",
        icon="fa-gear",
    ),
    ViewMenuItem(
        "Dispositivos x Tarima",
        reverse_lazy('reportelistado_qr'),
        weight=12,
        group="inv_bodega",
        icon="fa-gear",
    ),
    ViewMenuItem(
        "Sistema Operativo",
        reverse_lazy('versionsistema_list'),
        perm="inventario.add_versionsistema",
        weight=12,
        icon="fa-linux",
    ),
    ViewMenuItem(
        "Softwate",
        reverse_lazy('software_list'),
        weight=12,
        perm="inventario.add_software",
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
        weight=12,
        icon="fa-desktop",
    ),
)
# Repuestos
repuestos_children = (
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
        perm="inventario.add_salidainventario",
        icon="fa-pencil-square-o",
    ),
    ViewMenuItem(
        "Revisiones",
        reverse_lazy('revisionsalida_list'),
        weight=12,
        group="inventario_conta",
        icon="fa-check",
    ),
    ViewMenuItem(
        "Agregar Revision",
        reverse_lazy('revisionsalida_add'),
        weight=12,
        group="inventario_conta",
        icon="fa-plus-square",
    ),
)
# Desechos
desecho_children = (
    ViewMenuItem(
        "Empresa de Desecho",
        reverse_lazy('desechoempresa_add'),
        weight=12,
        icon="fa-recycle",
    ),
    ViewMenuItem(
        "Salidas de Desecho",
        reverse_lazy('desechoempresa_list'),
        weight=12,
        icon="fa-archive",
    ),

)
# Contabilidad
contabilidad_children = (
    ViewMenuItem(
        "Periodo Fiscal",
        reverse_lazy('desechoempresa_list'),
        weight=12,
        perm="conta.add_periodofiscal",
        icon="fa-calendar-check-o",
    ),
)

# Administrador
admin_children = (
    ViewMenuItem(
        "Asignacion Usuarios",
        reverse_lazy('asignaciontecnico_list'),
        weight=12,
        perm="inventario.add_asignaciontecnico",
        icon="fa-user-plus",
    ),
    ViewMenuItem(
        "Precio Estándar",
        reverse('asignaciontecnico_list'),
        weight=12,
        perm="conta.add_precioestandar",
        icon="fa-money",
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
        group="inventario",
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
        group="inventario",
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
        "Repuestos",
        reverse_lazy('entrada_list'),
        weight=10,
        icon="fa-wrench",
        group="inventario",
        children=repuestos_children
    )
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Salidas",
        reverse_lazy('entrada_list'),
        weight=10,
        icon="fa-sign-out",
        group="inventario",
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
        group="inventario_bodega",
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
        group="inventario_conta",
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
        group="inventario_admin",
        children=admin_children
    )
)
