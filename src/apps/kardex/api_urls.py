from django.conf.urls import url
from apps.kardex import api_views


entrada_api_list = api_views.EntradaViewSet.as_view({
    'get': 'list'})
entrada_api_detail = api_views.EntradaViewSet.as_view({
    'get': 'retrieve',
    'post': 'update',
    'patch': 'partial_update'})

proveedor_api_list = api_views.ProveedorViewSet.as_view({
    'get': 'list'})
proveedor_api_detail = api_views.ProveedorViewSet.as_view({
    'get': 'retrieve',
    'post': 'update',
    'patch': 'partial_update'})

equipo_api_list = api_views.EquipoViewSet.as_view({
    'get': 'list'})
equipo_api_detail = api_views.EquipoViewSet.as_view({
    'get': 'retrieve'})

urlpatterns = [
    url(r'^api/entrada/$', entrada_api_list, name='entrada_api_list'),
    url(r'^api/entrada/(?P<pk>\d+)/$', entrada_api_detail, name='entrada_api_detail'),

    url(r'^api/proveedor/$', proveedor_api_list, name='proveedor_api_list'),
    url(r'^api/proveedor/(?P<pk>\d+)/$', proveedor_api_detail, name='proveedor_api_detail'),

    url(r'^api/equipo/$', equipo_api_list, name='equipo_api_list'),
    url(r'^api/equipo/(?P<pk>\d+)/$', equipo_api_detail, name='equipo_api_detail'),
]
