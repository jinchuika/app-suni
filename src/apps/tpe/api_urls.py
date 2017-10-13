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

urlpatterns = [
    url(r'^api/reparacion/list/$', reparacion_api_list, name='reparacion_api_list'),

    url(r'^api/monitoreo/$', monitoreo_api, name='monitoreo_api'),
    url(r'^api/monitoreo/(?P<pk>\d+)/$', monitoreo_api_detail, name='monitoreo_api_detail'),

    url(r'^api/evaluacionmonitoreo/$', evaluacionmonitoreo_api, name='evaluacionmonitoreo_api'),
    url(r'^api/evaluacionmonitoreo/(?P<pk>\d+)/$', evaluacionmonitoreo_api_detail, name='evaluacionmonitoreo_api_detail'),
]
