from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Inventario
# Entrada
entrada_children = (
    ViewMenuItem(
        "Listado de entradas",
        reverse_lazy('entrada_list'),
        weight=12,
        icon="fa-list",
    ),
    ViewMenuItem(
        "Entradas en creacion",
        reverse_lazy('entrada_add'),
        weight=12,
        icon="fa-pencil-square-o",
    ),
)
# Dispositivos
dispositivos_children = (
    ViewMenuItem(
        "Solicitud movimiento",
        reverse_lazy('solicitudmovimiento_add'),
        weight=12,
        icon="fa-road",
    ),
    ViewMenuItem(
        "Solicitud pendientes",
        reverse_lazy('solicitudmovimiento_list'),
        weight=12,
        icon="fa-clock-o",
    ),
    ViewMenuItem(
        "Tipos de dispositivos",
        reverse_lazy('dispositivotipo_add'),
        weight=12,
        icon="fa-gear",
    ),
    ViewMenuItem(
        "Sistema operativo",
        reverse_lazy('versionsistema_list'),
        weight=12,
        icon="fa-linux",
    ),
    ViewMenuItem(
        "Softwate",
        reverse_lazy('software_list'),
        weight=12,
        icon="fa-firefox",
    ),
    ViewMenuItem(
        "Dispositivos",
        reverse_lazy('dispositivo_list'),
        weight=12,
        icon=" fa-mobile-phone",
    ),
)
# Repuestos
repuestos_children = (
    ViewMenuItem(
        "Asignacion de repuestos",
        reverse_lazy('repuesto_list'),
        weight=12,
        icon="fa-archive",
    ),

)
# Salidas
salidas_children = (
    ViewMenuItem(
        "Salida informe",
        reverse_lazy('entrada_list'),
        weight=12,
        icon="fa-list-ol",
    ),
    ViewMenuItem(
        "Salida pendientes",
        reverse_lazy('salidainventario_add'),
        weight=12,
        icon="fa-list-ul",
    ),
    ViewMenuItem(
        "Control de calidad",
        reverse_lazy('controlcalidad_list'),
        weight=12,
        icon="fa-check",
    ),

)
# Desechos
desecho_children = (
    ViewMenuItem(
        "Empresa de desecho",
        reverse_lazy('desechoempresa_add'),
        weight=12,
        icon="fa-recycle",
    ),
    ViewMenuItem(
        "Listado salidas de desecho",
        reverse_lazy('desechoempresa_list'),
        weight=12,
        icon="fa-archive",
    ),

)
# Contabilidad
contabilidad_children = (
    ViewMenuItem(
        "Informes",
        reverse_lazy('entrada_list'),
        weight=12,
        icon="fa-list",
    ),
)

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
        group="inventario",
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
        group="inventario",
        children=contabilidad_children
    )
)
