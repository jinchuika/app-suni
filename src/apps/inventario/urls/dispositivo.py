from django.conf.urls import url
from apps.inventario import views as inventario_v

urlpatterns = [
    # Creacion de asignaciones de técnico
    url(
        r'^asignacion/add/$',
        inventario_v.AsignacionTecnicoCreateView.as_view(),
        name='asignaciontecnico_add'
    ),
    # Listado de asignaciones de técnico
    url(
        r'^asignacion/list/$',
        inventario_v.AsignacionTecnicoListView.as_view(),
        name='asignaciontecnico_list'
    ),
    # Edición de asignaciones de técnico
    url(
        r'^asignacion/(?P<pk>\d+)/edit/$',
        inventario_v.AsignacionTecnicoUpdateView.as_view(),
        name='asignaciontecnico_update'
    ),
    # Edición de falla de dispositivo
    url(
        r'^falla/(?P<pk>\d+)/edit/$',
        inventario_v.DispositivoFallaUpdateView.as_view(),
        name='dispositivofalla_update'
    ),

    # Listado de Teclados
    url(
        r'^teclado/(?P<triage>[\w\d-]+)/edit/$',
        inventario_v.TecladoUpdateView.as_view(),
        name='teclado_update'
        ),
    # Detalle de cada teclado
    url(
        r'^teclado/(?P<triage>[\w\d-]+)/$',
        inventario_v.TecladoDetailView.as_view(),
        name='teclado_detail'
        ),
    # Creación de fallas de dispositivos
    url(
        r'^falla/add/$',
        inventario_v.DispositivoFallaCreateView.as_view(),
        name='dispositivofalla_add'
    ),
    #  Detalles de cada monitor
    url(
        r'^monitor/(?P<triage>[\w\d-]+)/$',
        inventario_v.MonitorDetailView.as_view(),
        name='monitor_detail'
    ),
    # Detalle de mouse
    url(
        r'^mouse/(?P<triage>[\w\d-]+)/$',
        inventario_v.MouseDetailView.as_view(),
        name='mouse_detail'
    ),
    # Detalle de cpu
    url(
        r'^cpu/(?P<triage>[\w\d-]+)/$',
        inventario_v.CPUDetailView.as_view(),
        name='cpu_detail'
    ),
    # Detalle de laptop
    url(
        r'^laptop/(?P<triage>[\w\d-]+)/$',
        inventario_v.LaptopDetailView.as_view(),
        name='laptop_detail'
    ),
    # Detalle de hdd
    url(
        r'^hdd/(?P<triage>[\w\d-]+)/$',
        inventario_v.HDDDetailView.as_view(),
        name='hdd_detail'
    ),
    # Detalle de red
    url(
        r'^red/(?P<triage>[\w\d-]+)/$',
        inventario_v.DispositivoRedDetailView.as_view(),
        name='red_detail'
    ),
    # Detalle de tablet
    url(
        r'^tablet/(?P<triage>[\w\d-]+)/$',
        inventario_v.TabletDetailView.as_view(),
        name='tablet_detail'
    ),
    # Creacion de Solicitudes de movimiento
    url(
        r'^dispositivo/solicitudmovimiento/add/$',
        inventario_v.SolicitudMovimientoCreateView.as_view(),
        name='solicitudmovimiento_add'
    ),
    # Actualización de Solicitudes de movimiento
    url(
        r'^dispositivo/solicitudmovimiento/(?P<pk>\d+)/edit/$',
        inventario_v.SolicitudMovimientoUpdateView.as_view(),
        name='solicitudmovimiento_update'
    ),
    # Detalle de Solicitudes de movimiento
    url(
        r'^dispositivo/solicitudmovimiento/(?P<pk>\d+)/$',
        inventario_v.SolicitudMovimientoDetailView.as_view(),
        name='solicitudmovimiento_detail'
    ),
    # Lista de Solicitudes de movimiento
    url(
        r'^dispositivo/solicitudmovimiento/list/$',
        inventario_v.SolicitudMovimientoListView.as_view(),
        name='solicitudmovimiento_list'
    )
]
