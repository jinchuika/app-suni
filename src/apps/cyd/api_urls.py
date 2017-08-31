from django.conf.urls import url
from apps.cyd import api_views


sede_api_list = api_views.SedeViewSet.as_view({
    'get': 'list'})
sede_api_detail = api_views.SedeViewSet.as_view({
    'get': 'retrieve',
    'post': 'create',
    'patch': 'partial_update'})
asesoria_api_list = api_views.AsesoriaViewSet.as_view({
    'get': 'list'})
asesoria_api = api_views.AsesoriaViewSet.as_view({
    'get': 'retrieve',
    'post': 'create',
    'patch': 'partial_update',
    'delete': 'destroy'})
asesoria_api_calendario = api_views.AsesoriaCalendarViewSet.as_view({
    'get': 'list'})

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

asignacion_api_list = api_views.AsignacionViewSet.as_view({
    'get': 'list'})
asignacion_api_add = api_views.AsignacionViewSet.as_view({
    'post': 'create'})
asignacion_api_detail = api_views.AsignacionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update'})

participante_api_list = api_views.ParticipanteViewSet.as_view({
    'get': 'list'})
participante_api_detail = api_views.ParticipanteViewSet.as_view({
    'get': 'retrieve'})
participante_api_update = api_views.ParticipanteAPIViewSet.as_view({
    'patch': 'partial_update'})

nota_asistencia_api_update = api_views.NotaAsistenciaViewSet.as_view({
    'patch': 'partial_update'})
nota_hito_api_update = api_views.NotaHitoViewSet.as_view({
    'patch': 'partial_update'})

urlpatterns = [
    url(r'^api/sede/list/$', sede_api_list, name='sede_api_list'),
    url(r'^api/sede/(?P<pk>\d+)/$', sede_api_detail, name='sede_api_detail'),
    url(r'^api/asesoria/list/$', asesoria_api_list, name='asesoria_api_list'),
    url(r'^api/asesoria/add/$', asesoria_api, name='asesoria_api_add'),
    url(r'^api/asesoria/calendario/$', asesoria_api_calendario, name='asesoria_api_calendario'),
    url(r'^api/asesoria/(?P<pk>\d+)/$', asesoria_api, name='asesoria_api_detail'),
    url(r'^api/grupo/list/$', grupo_api_list, name='grupo_api_list'),
    url(r'^api/grupo/(?P<pk>\d+)/$', grupo_api_detail, name='grupo_api_detail'),

    url(r'^api/calendario/list/$', calendario_api_list, name='calendario_api_list'),
    url(r'^api/calendario/(?P<pk>\d+)/$', calendario_api_detail, name='calendario_api_detail'),

    url(r'^api/asignacion/$', asignacion_api_list, name='asignacion_api_list'),
    url(r'^api/asignacion/add/$', asignacion_api_add, name='asignacion_api_add'),
    url(r'^api/asignacion/(?P<pk>\d+)/$', asignacion_api_detail, name='asignacion_api_detail'),

    url(r'^api/participante/list/$', participante_api_list, name='participante_api_list'),
    url(r'^api/participante/(?P<pk>\w+)/$', participante_api_detail, name='participante_api_detail'),
    url(r'^api/participante/(?P<pk>\d+)/update/$', participante_api_update, name='participante_api_update'),

    url(r'^api/nota_asistencia/(?P<pk>\d+)/update/$', nota_asistencia_api_update, name='nota_asistencia_api_update'),
    url(r'^api/nota_hito/(?P<pk>\d+)/update/$', nota_hito_api_update, name='nota_hito_api_update'),
]
