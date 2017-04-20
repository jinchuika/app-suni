from django.conf.urls import url
from apps.tpe.views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^equipamiento/list/$', cache_page(5)(EquipamientoListView.as_view()), name='equipamiento_list'),
    url(r'^equipamiento/add/$', EquipamientoCrearView.as_view(), name='equipamiento_add'),
    url(r'^equipamiento/(?P<pk>\d+)/$', EquipamientoUpdateView.as_view(), name='equipamiento_update'),
    url(r'^equipamiento/mapa/$', EquipamientoMapView.as_view(), name='equipamiento_map'),

    url(r'^garantia/list/$', cache_page(5)(GarantiaListView.as_view()), name='garantia_list'),
    url(r'^garantia/add/$', GarantiaCreateView.as_view(), name='garantia_add'),
    url(r'^garantia/(?P<pk>\d+)/$', GarantiaDetailView.as_view(), name='garantia_detail'),

    url(r'^garantia/(?P<pk>\d+)/ticket/(?P<ticket_id>\d+)/$', GarantiaDetailView.as_view(), name='ticket_detail'),
    url(r'^ticket/add/$', TicketCreateView.as_view(), name='ticket_soporte_add'),
    url(r'^ticket/(?P<pk>\d+)/edit/$', TicketCierreView.as_view(), name='ticket_soporte_update'),
    url(r'^ticketregistro/add/(?P<ticket_id>\d+)/$', TicketRegistroCreateView.as_view(), name='ticket_registro_add'),
    url(r'^ticketreparacion/add/(?P<ticket_id>\d+)/$', TicketReparacionCreateView.as_view(), name='ticket_reparacion_add'),

    url(r'^reparacion/list/$', cache_page(5)(ReparacionListView.as_view()), name='reparacion_list'),
    url(r'^reparacion/(?P<pk>\d+)/edit/$', cache_page(0)(ReparacionUpdateView.as_view()), name='reparacion_update'),
    url(r'^reparacion/repuesto/add/$', ReparacionRepuestoCreateView.as_view(), name='reparacion_repuesto_add'),
    url(r'^reparacion/repuesto/autorizar/(?P<pk>\d+)/$', ReparacionRepuestoUpdateView.as_view(), name='reparacion_repuesto_autorizar'),

    url(r'^monitoreo/add/(?P<equipamiento_id>\d+)/$', MonitoreoCreateView.as_view(), name='monitoreo_add'),
    url(r'^monitoreo/list/$', cache_page(5)(MonitoreoListView.as_view()), name='monitoreo_list'),
]
