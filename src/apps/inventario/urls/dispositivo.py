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
    #  Actualizacion de cada monitor
    url(
        r'^monitor/(?P<triage>[\w\d-]+)/edit/$',
        inventario_v.MonitorUptadeView.as_view(),
        name='monitor_edit'
    ),
    # Detalle de mouse
    url(
        r'^mouse/(?P<triage>[\w\d-]+)/$',
        inventario_v.MouseDetailView.as_view(),
        name='mouse_detail'
    ),
    # Actualizacion de mouse
    url(
        r'^mouse/(?P<triage>[\w\d-]+)/edit/$',
        inventario_v.MouseUptadeView.as_view(),
        name='mouse_edit'
    ),
    # Detalle de cpu
    url(
        r'^cpu/(?P<triage>[\w\d-]+)/$',
        inventario_v.CPUDetailView.as_view(),
        name='cpu_detail'
    ),
    # Actualizacion de Dispositivosinventario/entrada/imprimir_qr.html
    url(
        r'^cpu/(?P<triage>[\w\d-]+)/edit/$',
        inventario_v.CPUptadeView.as_view(),
        name='cpu_edit'
    ),
    # Detalle de laptop
    url(
        r'^laptop/(?P<triage>[\w\d-]+)/$',
        inventario_v.LaptopDetailView.as_view(),
        name='laptop_detail'
    ),
    # Actualizacion de Laptop
    url(
        r'^laptop/(?P<triage>[\w\d-]+)/edit/$',
        inventario_v.LaptopUptadeView.as_view(),
        name='laptop_edit'
    ),
    # Detalle de hdd
    url(
        r'^hdd/(?P<triage>[\w\d-]+)/$',
        inventario_v.HDDDetailView.as_view(),
        name='hdd_detail'
    ),
    # Actualizacion de HHD
    url(
        r'^hdd/(?P<triage>[\w\d-]+)/edit/$',
        inventario_v.HDDUptadeView.as_view(),
        name='hdd_edit'
    ),

    # Detalle de red
    url(
        r'^red/(?P<triage>[\w\d-]+)/$',
        inventario_v.DispositivoRedDetailView.as_view(),
        name='red_detail'
    ),
    # Actualizacion de red
    url(
        r'^red/(?P<triage>[\w\d-]+)/edit/$',
        inventario_v.DispositivoRedUptadeView.as_view(),
        name='red_edit'
    ),
    # Detalle de tablet
    url(
        r'^tablet/(?P<triage>[\w\d-]+)/$',
        inventario_v.TabletDetailView.as_view(),
        name='tablet_detail'
    ),
    # Actualizacion de tablet
    url(
        r'^tablet/(?P<triage>[\w\d-]+)/edit/$',
        inventario_v.TabletUptadeView.as_view(),
        name='tablet_edit'
    ),
    # Creacion de Solicitudes de movimiento
    url(
        r'^dispositivo/solicitudmovimiento/add/$',
        inventario_v.SolicitudMovimientoCreateView.as_view(),
        name='solicitudmovimiento_add'
    ),
    # Creacion de Devoluciones
    url(
        r'^dispositivo/devolucion/add/$',
        inventario_v.DevolucionCreateView.as_view(),
        name='devolucion_add'
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
    ),
    # Listado de Dispositivos
    url(
        r'^dispositivo/list/$',
        inventario_v.DispositivoListView.as_view(),
        name='dispositivo_list'
    ),
    # Tipo de Dispositivo
    url(
        r'^dispositivo/tipo/$',
        inventario_v.DispositivoTipoCreateView.as_view(),
        name='dispositivotipo_add'
    ),
    # Impresion de QR
    url(
        r'^dispositivo/reporteqr/(?P<triage>[\w\d-]+)/$',
        inventario_v.DispositivoQRprint.as_view(),
        name='reportedispositivo_qr'
    ),
    # impresion de Qr por listado
    url(
        r'^dispositivo/listadoqrtarima/(?P<pk>\d+)/$',
        inventario_v.DispositivosTarimaQr.as_view(),
        name='reportelistado_qr'
    ),
    # Listado de Dispositivos en Tarimas
    url(
        r'^dispositivo/tarima/list/$',
        inventario_v.DispositivosTarimaListView.as_view(),
        name='dispositivo_tarima'
    )
]
