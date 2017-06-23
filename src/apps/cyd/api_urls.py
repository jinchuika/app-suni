from django.conf.urls import url
from apps.cyd import api_views


grupo_api_list = api_views.GrupoViewSet.as_view({
    'get': 'list'})
grupo_api_detail = api_views.GrupoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update'})
calendario_api_list = api_views.CalendarioViewSet.as_view({
    'get': 'list'})
calendario_api_detail = api_views.CalendarioViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update'})

urlpatterns = [
    url(r'^api/grupo/list/$', grupo_api_list, name='grupo_api_list'),
    url(r'^api/grupo/(?P<pk>\d+)/$', grupo_api_detail, name='grupo_api_detail'),
    url(r'^api/calendario/list/$', calendario_api_list, name='calendario_api_list'),
    url(r'^api/calendario/(?P<pk>\d+)/$', calendario_api_detail, name='calendario_api_detail')
]
