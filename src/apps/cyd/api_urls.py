from django.conf.urls import url
from apps.cyd import api_views


sede_api_list = api_views.SedeViewSet.as_view({
    'get': 'list'})
sede_api_list_informe = api_views.SedeViewSetInforme.as_view({
    'get': 'list'})
sede_desactivar = api_views.SedeViewSet.as_view({
    'post':'desactivar_sede'})
participante_desactivar = api_views.SedeViewSet.as_view({
    'post':'desactivar_participante'})
actualizar_control_academico = api_views.SedeViewSet.as_view({
    'post':'actualizar_control_academico'})
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
grupo_desactivar = api_views.GrupoViewSet.as_view({
    'post':'desactivar_grupo'})
curso_desactivar = api_views.GrupoViewSet.as_view({
    'post':'desactivar_curso'})
grupo_crear = api_views.GrupoViewSet.as_view({
    'post':'crear_grupos'})
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

calendario_escuela_api_list = api_views.EscuelaCalendarioViewSet.as_view({
    'get': 'list'})

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
recordatorio_api_detail = api_views.RecordatorioViewSet.as_view({
'get': 'list',
'post': 'create',
'patch': 'partial_update',
'delete': 'destroy'
})
urlpatterns = [
    url(r'^api/sede/list/$', sede_api_list, name='sede_api_list'),
    url(r'^api/sede/listinforme/$', sede_api_list_informe, name='sede_api_list_informe'),
    url(r'^api/sede/desactivar_sede/$', sede_desactivar, name='sede_desactivar'),
    url(r'^api/sede/(?P<pk>\d+)/$', sede_api_detail, name='sede_api_detail'),
    url(r'^api/asesoria/list/$', asesoria_api_list, name='asesoria_api_list'),
    url(r'^api/asesoria/add/$', asesoria_api, name='asesoria_api_add'),
    url(r'^api/asesoria/calendario/$', asesoria_api_calendario, name='asesoria_api_calendario'),
    url(r'^api/asesoria/(?P<pk>\d+)/$', asesoria_api, name='asesoria_api_detail'),
    url(r'^api/grupo/list/$', grupo_api_list, name='grupo_api_list'),
    url(r'^api/grupo/desactivar_grupo/$', grupo_desactivar, name='grupo_desactivar'),
    url(r'^api/grupo/crear/$', grupo_crear, name='grupo_crear'),
    url(r'^api/controlacademico/grupo/actualizar/$', actualizar_control_academico, name='actualizar_control_academico'),

    url(r'^api/grupo/(?P<pk>\d+)/$', grupo_api_detail, name='grupo_api_detail'),

    url(r'^api/calendario/list/$', calendario_api_list, name='calendario_api_list'),
    url(r'^api/calendario/escuela/list/$', calendario_escuela_api_list, name='calendario_esucela_api_list'),
    url(r'^api/calendario/(?P<pk>\d+)/$', calendario_api_detail, name='calendario_api_detail'),

    url(r'^api/asignacion/$', asignacion_api_list, name='asignacion_api_list'),
    url(r'^api/asignacion/add/$', asignacion_api_add, name='asignacion_api_add'),
    url(r'^api/asignacion/(?P<pk>\d+)/$', asignacion_api_detail, name='asignacion_api_detail'),

    url(r'^api/participante/list/$', participante_api_list, name='participante_api_list'),
    url(r'^api/participante/(?P<pk>\w+)/$', participante_api_detail, name='participante_api_detail'),
    url(r'^api/participante/(?P<pk>\d+)/update/$', participante_api_update, name='participante_api_update'),
    url(r'^api/sede/desactivar/$', participante_desactivar, name='participante_desactivar'),

    url(r'^api/nota_asistencia/(?P<pk>\d+)/update/$', nota_asistencia_api_update, name='nota_asistencia_api_update'),
    url(r'^api/nota_hito/(?P<pk>\d+)/update/$', nota_hito_api_update, name='nota_hito_api_update'),
    url(r'^api/curso/desactivar_curso/$', curso_desactivar, name='curso_desactivar'),
    url(r'^api/recordatorios/$',recordatorio_api_detail, name='recordatorio_api_detail')
]
