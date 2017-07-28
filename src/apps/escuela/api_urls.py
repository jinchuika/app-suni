from django.conf.urls import url
from apps.escuela import api_views

escuela_api_list = api_views.EscuelaViewSet.as_view({
    'get': 'list'})
escuela_api_detail = api_views.EscuelaViewSet.as_view({
    'get': 'retrieve'})

urlpatterns = [
    url(r'^api/escuela/list/$', escuela_api_list, name='escuela_api_list'),
    url(r'^api/escuela/(?P<pk>\d+)/$', escuela_api_detail, name='escuela_api_detail'),
]
