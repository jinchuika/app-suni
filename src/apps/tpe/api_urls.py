from rest_framework import routers
from django.conf.urls import url
from apps.tpe import api_views

reparacion_api_list = api_views.TicketReparacionViewSet.as_view({
    'get': 'list'})

monitoreo_api = api_views.MonitoreoViewSet.as_view({
    'get': 'list',
    'post': 'create'})

monitoreo_api_detail = api_views.MonitoreoViewSet.as_view({
    'get': 'retrieve',
    'post': 'update',
    'patch': 'partial_update'})

evaluacionmonitoreo_api = api_views.EvaluacionMonitoreoViewSet.as_view({
    'get': 'list',
    'post': 'update'})
evaluacionmonitoreo_api_detail = api_views.EvaluacionMonitoreoViewSet.as_view({
    'get': 'retrieve',
    'post': 'update',
    'patch': 'partial_update'})

router = routers.DefaultRouter()
router.register(r'equipamiento', api_views.EquipamientoViewSet, base_name='equipamiento')
router.register(r'equipamiento-informe', api_views.EquipamientoFullViewSet, base_name='equipamiento-informe')
router.register(r'equipamiento-calendar', api_views.EquipamientoCalendarViewSet, base_name='equipamiento-calendar')
router.register(r'evaluacion-monitoreo', api_views.EvaluacionMonitoreoFullViewSet, base_name='evaluacion-monitoreo')

urlpatterns = [
    url(r'^reparacion/list/$', reparacion_api_list, name='reparacion_api_list'),

    url(r'^monitoreo/$', monitoreo_api, name='monitoreo_api'),
    url(r'^monitoreo/(?P<pk>\d+)/$', monitoreo_api_detail, name='monitoreo_api_detail'),

    url(r'^evaluacionmonitoreo/$', evaluacionmonitoreo_api, name='evaluacionmonitoreo_api'),
    url(r'^evaluacionmonitoreo/(?P<pk>\d+)/$', evaluacionmonitoreo_api_detail, name='evaluacionmonitoreo_api_detail'),
]

urlpatterns += router.urls
