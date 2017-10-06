from django.conf.urls import url
from apps.tpe import api_views

reparacion_api_list = api_views.TicketReparacionViewSet.as_view({
    'get': 'list'})

evaluacionmonitoreo_api = api_views.EvaluacionMonitoreoViewSet.as_view({
    'get': 'list',
    'post': 'update'})
evaluacionmonitoreo_api_detail = api_views.EvaluacionMonitoreoViewSet.as_view({
    'get': 'retrieve',
    'post': 'update',
    'patch': 'partial_update'})

urlpatterns = [
    url(r'^api/reparacion/list/$', reparacion_api_list, name='reparacion_api_list'),

    url(r'^api/evaluacionmonitoreo/$', evaluacionmonitoreo_api, name='evaluacionmonitoreo_api'),
    url(r'^api/evaluacionmonitoreo/(?P<pk>\d+)/$', evaluacionmonitoreo_api_detail, name='evaluacionmonitoreo_api_detail'),
]
