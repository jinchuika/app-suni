from django.conf.urls import url
#from apps.inventario import views as inventario_v
from apps.beqt import views as beqt_v
urlpatterns = [
    # Creacion de asignaciones de técnico
    url(
        r'^asignacion/add/$',
        beqt_v.AsignacionTecnicoCreateView.as_view(),
        name='asignaciontecnico_beqt_add'
    ),
    # Listado de asignaciones de técnico
    url(
        r'^asignacion/list/$',
        beqt_v.AsignacionTecnicoListView.as_view(),
        name='asignaciontecnico_beqt_list'
    ),
    # Edición de asignaciones de técnico
    url(
        r'^asignacion/(?P<pk>\d+)/edit/$',
        beqt_v.AsignacionTecnicoUpdateView.as_view(),
        name='asignaciontecnico_beqt_update'
    ),   
      
   
 
    # Detalle de laptop
    url(
        r'^laptop/(?P<triage>[\w\d-]+)/$',
        beqt_v.LaptopDetailView.as_view(),
        name='laptop_beqt_detail'
    ),
    # Actualizacion de Laptop
    url(
        r'^laptop/(?P<triage>[\w\d-]+)/edit/$',
        beqt_v.LaptopUptadeView.as_view(),
        name='laptop_beqt_edit'
    ),
    # Detalle de hdd
    url(
        r'^hdd/(?P<triage>[\w\d-]+)/$',
        beqt_v.HDDDetailView.as_view(),
        name='hdd_beqt_detail'
    ),
    # Actualizacion de HHD
    url(
        r'^hdd/(?P<triage>[\w\d-]+)/edit/$',
        beqt_v.HDDUptadeView.as_view(),
        name='hdd_beqt_edit'
    ),

  

    # Detalle de access point
    url(
        r'^ap/(?P<triage>[\w\d-]+)/$',
        beqt_v.DispositivoAccessPointDetailView.as_view(),
        name='ap_beqt_detail'
    ),
    # Actualizacion de access point
    url(
        r'^ap/(?P<triage>[\w\d-]+)/edit/$',
        beqt_v.DispositivoAccessPointUptadeView.as_view(),
        name='ap_beqt_edit'
    ),

    # Detalle de tablet
    url(
        r'^tablet/(?P<triage>[\w\d-]+)/$',
        beqt_v.TabletDetailView.as_view(),
        name='tablet_beqt_detail'
    ),
    # Actualizacion de tablet
    url(
        r'^tablet/(?P<triage>[\w\d-]+)/edit/$',
        beqt_v.TabletUptadeView.as_view(),
        name='tablet_beqt_edit'
    ),
     # Detalle de switch
    url(
        r'^red/(?P<triage>[\w\d-]+)/$',
        beqt_v.DispositivoRedDetailView.as_view(),
        name='red_beqt_detail'
    ),
    # Actualizacion de switch
    url(
        r'^red/(?P<triage>[\w\d-]+)/edit/$',
        beqt_v.DispositivoRedUptadeView.as_view(),
        name='red_beqt_edit'
    ),
     # Detalle de cargador de tablet
    url(
        r'^tablet/cargador/(?P<triage>[\w\d-]+)/$',
        beqt_v.TabletCargadorDetailView.as_view(),
        name='cargador_tablet_beqt_detail'
    ),
    # Actualizacion de cargador de tablet
    url(
        r'^tablet/cargador/(?P<triage>[\w\d-]+)/edit/$',
        beqt_v.TabletCargadorUptadeView.as_view(),
        name='cargador_tablet_beqt_edit'
    ),
    # Detalle de cargador de laptop
    url(
        r'^laptop/cargador/(?P<triage>[\w\d-]+)/$',
        beqt_v.LaptopCargadorDetailView.as_view(),
        name='cargador_laptop_beqt_detail'
    ),
     # Detalle de estuche de tablet
    url(
        r'^tablet/estuche/(?P<triage>[\w\d-]+)/$',
        beqt_v.TabletEstucheDetailView.as_view(),
        name='tablet_estuche_beqt_detail'
    ),
    # Actualizacion de estuche de tablet
    url(
        r'^tablet/estuche/(?P<triage>[\w\d-]+)/edit/$',
        beqt_v.TabletEstucheUptadeView.as_view(),
        name='tablet_estuche_beqt_edit'
    ),
   
    # Actualizacion de cargador de laptop
    url(
        r'^laptop/cargador/(?P<triage>[\w\d-]+)/edit/$',
        beqt_v.LaptopCargadorUptadeView.as_view(),
        name='laptop_cargador_beqt_edit'
    ),

     # Detalle de regleta
    url(
        r'^regleta/(?P<triage>[\w\d-]+)/$',
        beqt_v.RegletaDetailView.as_view(),
        name='regleta_beqt_detail'
    ),
    # Actualizacion de regleta
    url(
        r'^regleta/(?P<triage>[\w\d-]+)/edit/$',
        beqt_v.RegletaUptadeView.as_view(),
        name='regleta_beqt_edit'
    ),
        # Detalle de ups
    url(
        r'^ups/(?P<triage>[\w\d-]+)/$',
        beqt_v.UpsDetailView.as_view(),
        name='ups_beqt_detail'
    ),
    # Actualizacion de ups
     url(
        r'^ups/(?P<triage>[\w\d-]+)/edit/$',
        beqt_v.UpsUptadeView.as_view(),
        name='ups_beqt_edit'
    ),
    # Creacion de Solicitudes de movimiento
    url(
        r'^dispositivo/solicitudmovimiento/add/$',
        beqt_v.SolicitudMovimientoCreateView.as_view(),
        name='solicitudmovimiento_beqt_add'
    ),
    
    # Actualización de Solicitudes de movimiento
    url(
        r'^dispositivo/solicitudmovimiento/(?P<pk>\d+)/edit/$',
        beqt_v.SolicitudMovimientoUpdateView.as_view(),
        name='solicitudmovimiento_beqt_update'
    ),
    # Detalle de Solicitudes de movimiento
    url(
        r'^dispositivo/solicitudmovimiento/(?P<pk>\d+)/$',
        beqt_v.SolicitudMovimientoDetailView.as_view(),
        name='solicitudmovimiento_beqt_detail'
    ),
    # Lista de Solicitudes de movimiento
    url(
        r'^dispositivo/solicitudmovimiento/list/$',
        beqt_v.SolicitudMovimientoListView.as_view(),
        name='solicitudmovimiento_beqt_list'
    ),
    # Listado de Dispositivos
    url(
        r'^dispositivo/list/$',
        beqt_v.DispositivoListView.as_view(),
        name='dispositivo_beqt_list'
    ),
    # Tipo de Dispositivo
    url(
        r'^dispositivo/tipo/$',
        beqt_v.DispositivoTipoCreateView.as_view(),
        name='dispositivotipo_beqt_add'
    ),
    # Impresion de QR
    url(
        r'^dispositivo/reporteqr/(?P<triage>[\w\d-]+)/$',
        beqt_v.DispositivoQRprint.as_view(),
        name='reportedispositivo_beqt_qr'
    ),
    # impresion de Qr por listado
    url(
        r'^dispositivo/listadoqrtarima/(?P<pk>\d+)/$',
        beqt_v.DispositivosTarimaQr.as_view(),
        name='reportelistado_beqt_qr'
    ),
    # Listado de Dispositivos en Tarimas
    url(
        r'^dispositivo/tarima/list/$',
        beqt_v.DispositivosTarimaListView.as_view(),
        name='dispositivo_beqt_tarima'
    )
]
