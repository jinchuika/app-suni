from django.conf.urls import url, include
from apps.tpe.views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^equipamiento/list/$', cache_page(5)(EquipamientoListView.as_view()), name='equipamiento_list'),
    url(r'^equipamiento/informe/$', cache_page(5)(EquipamientoInformeView.as_view()), name='equipamiento_informe'),
    url(r'^equipamiento/list/home$', cache_page(5)(EquipamientoListHomeView.as_view()), name='equipamiento_list_home'),
    url(r'^equipamiento/calendario/home$', cache_page(5)(EquipamientoCalendarHomeView.as_view()), name='equipamiento_calendario_home'),
    url(r'^equipamiento/add/$', EquipamientoCrearView.as_view(), name='equipamiento_add'),
    url(r'^equipamiento/(?P<pk>\d+)/$', EquipamientoUpdateView.as_view(), name='equipamiento_update'),
    url(r'^equipamiento/mapa/$', EquipamientoMapView.as_view(), name='equipamiento_map'),

    url(r'^garantia/list/$', cache_page(5)(GarantiaListView.as_view()), name='garantia_list'),
    url(r'^garantia/add/$', GarantiaCreateView.as_view(), name='garantia_add'),
    url(r'^garantia/(?P<pk>\d+)/$', GarantiaDetailView.as_view(), name='garantia_detail'),

    url(r'^garantia/(?P<pk>\d+)/ticket/(?P<ticket_id>\d+)/$', GarantiaDetailView.as_view(), name='ticket_detail'),
    url(r'^ticket/add/$', TicketCreateView.as_view(), name='ticket_soporte_add'),
    url(r'^ticket/informe/$', cache_page(5)(TicketInformeView.as_view()), name='ticket_informe'),
    url(r'^ticket/list/$', cache_page(5)(TicketCalendarView.as_view()), name='ticket_list_calendar'),
    url(r'^ticket/(?P<pk>\d+)/edit/$', TicketCierreView.as_view(), name='ticket_soporte_update'),
    url(r'^ticket/print_detalle/$', GarantiaPrintDetalle.as_view(), name='ticket_print_detalle'),
    url(r'^ticketregistro/add/(?P<ticket_id>\d+)/$', TicketRegistroCreateView.as_view(), name='ticket_registro_add'),
    url(r'^ticketregistro/(?P<pk>\d+)/$', TicketRegistroUpdateView.as_view(), name='ticket_registro_update'),
    url(r'^ticketregistro/print_detalle/$', TicketVisitaPrintDetalle.as_view(), name='ticket_registro_print_detalle'),
    url(r'^ticketreparacion/add/(?P<ticket_id>\d+)/$', TicketReparacionCreateView.as_view(), name='ticket_reparacion_add'),
    url(r'^tickettransporte/add/(?P<ticket_id>\d+)/$', TicketTransporteCreateView.as_view(), name='ticket_transporte_add'),
    url(r'^ticketreparacion/list/$', cache_page(5)(TicketReparacionInformeView.as_view()), name='ticket_reparacion_informe'),

    url(r'^ticket/(?P<pk>\d+)/recepcion/$', TicketRecepcionPrintView.as_view(), name='ticket_recepcion_print'),
    url(r'^ticket/(?P<pk>\d+)/entrega/$', TicketEntregaPrintView.as_view(), name='ticket_entrega_print'),

    url(r'^reparacion/list/$', cache_page(5)(ReparacionListView.as_view()), name='reparacion_list'),
    url(r'^reparacion/(?P<pk>\d+)/edit/$', cache_page(0)(ReparacionUpdateView.as_view()), name='reparacion_update'),
    url(r'^reparacion/repuesto/add/$', ReparacionRepuestoCreateView.as_view(), name='reparacion_repuesto_add'),
    url(r'^reparacion/repuesto/autorizar/(?P<pk>\d+)/$', ReparacionRepuestoUpdateView.as_view(), name='reparacion_repuesto_autorizar'),

    url(r'^monitoreo/add/(?P<equipamiento_id>\d+)/$', MonitoreoCreateView.as_view(), name='monitoreo_add'),
    url(r'^monitoreo/list/$', cache_page(5)(MonitoreoListView.as_view()), name='monitoreo_list'),

    url(r'^monitoreo/(?P<pk>\d+)/evaluacion/$', MonitoreoUpdateView.as_view(), name='monitoreo_update'),
    url(r'^monitoreo/(?P<pk>\d+)/$', MonitoreoDetailView.as_view(), name='monitoreo_detail'),

    url(r'^calendario/$', CalendarioTPEView.as_view(), name='calendario_tpe'),
    url(r'^api/', include('apps.tpe.api_urls', namespace='tpe_api')),
]
