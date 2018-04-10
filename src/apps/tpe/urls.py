from django.conf.urls import url, include
from apps.tpe import views as tpe_v
from django.views.decorators.cache import cache_page

urlpatterns = [
    # Listado de entregas
    url(
        r'^equipamiento/list/$',
        cache_page(5)(tpe_v.EquipamientoListView.as_view()),
        name='equipamiento_list'),

    # Informe de equipamientos
    url(
        r'^equipamiento/informe/$',
        cache_page(5)(tpe_v.EquipamientoInformeView.as_view()),
        name='equipamiento_informe'),

    # Listado de equipamientos a ser mostrados en el home
    url(
        r'^equipamiento/list/home$', cache_page(5)(tpe_v.EquipamientoListHomeView.as_view()),
        name='equipamiento_list_home'),

    # Creación de equipamientos
    url(
        r'^equipamiento/add/$',
        tpe_v.EquipamientoCrearView.as_view(),
        name='equipamiento_add'),

    # Edición de equipamientos
    url(
        r'^equipamiento/(?P<pk>\d+)/$',
        tpe_v.EquipamientoUpdateView.as_view(),
        name='equipamiento_update'),

    # Mapa de equipamientos
    url(
        r'^equipamiento/mapa/$',
        tpe_v.EquipamientoMapView.as_view(),
        name='equipamiento_map'),

    # Listado de garantias
    url(
        r'^garantia/list/$',
        cache_page(5)(tpe_v.GarantiaListView.as_view()),
        name='garantia_list'),

    # Creación de garantías
    url(
        r'^garantia/add/$',
        tpe_v.GarantiaCreateView.as_view(),
        name='garantia_add'),

    # Detalle de garantías
    url(
        r'^garantia/(?P<pk>\d+)/$',
        tpe_v.GarantiaDetailView.as_view(),
        name='garantia_detail'),

    # Detalle de tickets
    url(
        r'^garantia/(?P<pk>\d+)/ticket/(?P<ticket_id>\d+)/$',
        tpe_v.GarantiaDetailView.as_view(),
        name='ticket_detail'),

    # Creación de tickets
    url(
        r'^ticket/add/$',
        tpe_v.TicketCreateView.as_view(),
        name='ticket_soporte_add'),

    # Informe de tickets
    url(
        r'^ticket/informe/$',
        cache_page(5)(tpe_v.TicketInformeView.as_view()),
        name='ticket_informe'),

    # Listado de tickets para mostrar en el calendario
    url(
        r'^ticket/list/$',
        cache_page(5)(tpe_v.TicketCalendarView.as_view()),
        name='ticket_list_calendar'),

    # Para para cerrar un ticket
    url(
        r'^ticket/(?P<pk>\d+)/edit/$',
        tpe_v.TicketCierreView.as_view(),
        name='ticket_soporte_update'),

    # Impresión de detalle de garantías
    url(
        r'^ticket/print_detalle/$',
        tpe_v.GarantiaPrintDetalle.as_view(),
        name='ticket_print_detalle'),

    # Creación de registro para un ticket de soporte
    url(
        r'^ticketregistro/add/(?P<ticket_id>\d+)/$',
        tpe_v.TicketRegistroCreateView.as_view(),
        name='ticket_registro_add'),

    # Actualización de registro de tickets de soporte
    url(
        r'^ticketregistro/(?P<pk>\d+)/$',
        tpe_v.TicketRegistroUpdateView.as_view(),
        name='ticket_registro_update'),

    # Impresión de visita técnica
    url(
        r'^ticketregistro/print_detalle/$',
        tpe_v.TicketVisitaPrintDetalle.as_view(),
        name='ticket_registro_print_detalle'),

    # Creación de reparación para ticket de soporte
    url(
        r'^ticketreparacion/add/(?P<ticket_id>\d+)/$',
        tpe_v.TicketReparacionCreateView.as_view(),
        name='ticket_reparacion_add'),

    # Creación de transporte para ticket de soporte
    url(
        r'^tickettransporte/add/(?P<ticket_id>\d+)/$',
        tpe_v.TicketTransporteCreateView.as_view(),
        name='ticket_transporte_add'),

    # Informe de reparaciones de tickets de soporte
    url(
        r'^ticketreparacion/list/$',
        cache_page(5)(tpe_v.TicketReparacionInformeView.as_view()),
        name='ticket_reparacion_informe'),

    # Impresión de recepción de equipo para ticket de soporte
    url(
        r'^ticket/(?P<pk>\d+)/recepcion/$',
        tpe_v.TicketRecepcionPrintView.as_view(),
        name='ticket_recepcion_print'),

    # Impresión de entrega de equipo para ticket de soporte
    url(
        r'^ticket/(?P<pk>\d+)/entrega/$',
        tpe_v.TicketEntregaPrintView.as_view(),
        name='ticket_entrega_print'),

    # Listado de reparaciones de equipo
    url(
        r'^reparacion/list/$',
        cache_page(5)(tpe_v.ReparacionListView.as_view()),
        name='reparacion_list'),

    # Lista de dispositivos reparados
    url(
        r'^dispositivoreparacion/list/$',
        cache_page(5)(tpe_v.DispositivoReparacionListView.as_view()),
        name='dispositivo_reparacion_list'),

    # Edición de reparaciones
    url(
        r'^reparacion/(?P<pk>\d+)/edit/$',
        cache_page(0)(tpe_v.ReparacionUpdateView.as_view()),
        name='reparacion_update'),

    # Creación de solicitud de repuesto de reparación
    url(
        r'^reparacion/repuesto/add/$',
        tpe_v.ReparacionRepuestoCreateView.as_view(),
        name='reparacion_repuesto_add'),

    # Autorización de repuestos para reparación de garantías
    url(
        r'^reparacion/repuesto/autorizar/(?P<pk>\d+)/$',
        tpe_v.ReparacionRepuestoUpdateView.as_view(),
        name='reparacion_repuesto_autorizar'),

    # Creación de registro de monitoreo
    url(
        r'^monitoreo/add/(?P<equipamiento_id>\d+)/$',
        tpe_v.MonitoreoCreateView.as_view(),
        name='monitoreo_add'),

    # Listado de registros de monitoreo
    url(
        r'^monitoreo/list/$',
        cache_page(5)(tpe_v.MonitoreoListView.as_view()),
        name='monitoreo_list'),

    # Edición de registros de monitoreo
    url(
        r'^monitoreo/(?P<pk>\d+)/evaluacion/$',
        tpe_v.MonitoreoUpdateView.as_view(),
        name='monitoreo_update'),

    # Detalle de registro de monitoreo
    url(
        r'^monitoreo/(?P<pk>\d+)/$',
        tpe_v.MonitoreoDetailView.as_view(),
        name='monitoreo_detail'),

    # Informe de evaluaciones al monitoreo
    url(
        r'^evaluacionmonitoreo/list/$',
        cache_page(5)(tpe_v.EvaluacionMonitoreoInformeView.as_view()),
        name='evaluacionmonitoreo_list'),

    # Calendario de TPE
    url(
        r'^calendario/$',
        tpe_v.CalendarioTPEView.as_view(),
        name='calendario_tpe'),

    # Visitas a escuelas
    url(
        r'^visita/add/$',
        tpe_v.VisitaInformeView.as_view(),
        name='visita_monitoreo_add'
        ),

    # Listado de visitas
    url(
        r'visita/list/$',
        tpe_v.VisitaListView.as_view(),
        name='visita_list'
        ),

    # Detalles de las visitas
    url(
        r'visita/(?P<pk>\d+)/$',
        tpe_v.VisitaDetailView.as_view(),
        name='visita_monitoreo_detail'
        ),

    # Detalles de las vistas
    url(
        r'visita/(?P<pk>\d+)/editar/$',
        tpe_v.VisitaUpdateView.as_view(),
        name='visita_monitoreo_update'
        ),

    # Calendario de visitas
    url(
        r'visita/calendario/$',
        tpe_v.CalendarioTPEView.as_view(),
        name='visita_calendario'),

    # Impresion de reportes de visita
    url(
        r'visita/print_detalle/(?P<pk>\d+)/$',
        tpe_v.VisitaDetallePrintView.as_view(),
        name='visita_monitoreo_print'
        ),

    # API REST
    url(
        r'^api/',
        include('apps.tpe.api_urls', namespace='tpe_api')),
]
