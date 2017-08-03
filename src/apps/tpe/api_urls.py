from django.conf.urls import url
from apps.tpe import api_views

reparacion_api_list = api_views.TicketReparacionViewSet.as_view({
    'get': 'list'})

urlpatterns = [
    url(r'^api/reparacion/list/$', reparacion_api_list, name='reparacion_api_list'),
]
