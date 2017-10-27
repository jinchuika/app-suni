from django.conf.urls import url
from apps.ie import api_views

organizacion_api_list = api_views.OrganizacionViewSet.as_view({
    'get': 'list'})

laboratorio_api_list = api_views.LaboratorioViewSet.as_view({
    'get': 'list'})

escuela_api_list = api_views.EscuelaViewSet.as_view({
    'get': 'list'})

geo_api_list = api_views.GeografiaViewSet.as_view({
    'get': 'list'})

urlpatterns = [
    url(r'^organizacion/$', organizacion_api_list, name='ie_organizacion_api_list'),
    url(r'^laboratorio/$', laboratorio_api_list, name='ie_laboratorio_api_list'),
    url(r'^escuela/$', escuela_api_list, name='ie_escuela_api_list'),
    url(r'^geo/$', geo_api_list, name='ie_geo_api_list'),
]
