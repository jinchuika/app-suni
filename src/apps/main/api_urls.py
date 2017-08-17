from django.conf.urls import url
from apps.main import api_views

departamento_api_list = api_views.DepartamentoViewSet.as_view({
    'get': 'list'})
departamento_api_detail = api_views.DepartamentoViewSet.as_view({
    'get': 'retrieve'})

municipio_api_list = api_views.MunicipioViewSet.as_view({
    'get': 'list'})
municipio_api_detail = api_views.MunicipioViewSet.as_view({
    'get': 'retrieve'})

urlpatterns = [
    url(r'^api/departamento/list/$', departamento_api_list, name='departamento_api_list'),
    url(r'^api/departamento/(?P<pk>\d+)/$', departamento_api_detail, name='departamento_api_detail'),

    url(r'^api/municipio/list/$', municipio_api_list, name='municipio_api_list'),
    url(r'^api/municipio/(?P<pk>\d+)/$', municipio_api_detail, name='municipio_api_detail'),
]
