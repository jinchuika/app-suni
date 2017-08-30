from django.conf.urls import url
from apps.kalite import api_views


punteo_api_list = api_views.PunteoViewSet.as_view({
    'get': 'list'})
punteo_api_detail = api_views.PunteoViewSet.as_view({
    'get': 'retrieve',
    'post': 'update',
    'patch': 'partial_update'})

evaluacion_api_list = api_views.EvaluacionViewSet.as_view({
    'get': 'list'})
evaluacion_api_detail = api_views.EvaluacionViewSet.as_view({
    'get': 'retrieve',
    'post': 'update',
    'patch': 'partial_update'})

visita_api_list = api_views.VisitaViewSet.as_view({
    'get': 'list'})
visita_api_detail = api_views.VisitaViewSet.as_view({
    'get': 'retrieve',
    'post': 'update',
    'patch': 'partial_update'})

calendario_api_list = api_views.VisitaCalendarViewSet.as_view({
    'get': 'list'})

grado_api = api_views.GradoViewSet.as_view({
    'get': 'list',
    'post': 'create'})
grado_api_detail = api_views.GradoViewSet.as_view({
    'get': 'retrieve',
    'post': 'update',
    'patch': 'partial_update'})

ejerciciosgrado_api = api_views.EjerciciosGradoViewSet.as_view({
    'get': 'list',
    'post': 'create'})
ejerciciosgrado_api_detail = api_views.EjerciciosGradoViewSet.as_view({
    'get': 'retrieve',
    'post': 'update',
    'patch': 'partial_update'})


urlpatterns = [
    url(r'^api/punteo/$', punteo_api_list, name='punteo_api_list'),
    url(r'^api/punteo/(?P<pk>\d+)/$', punteo_api_detail, name='punteo_api_detail'),

    url(r'^api/evaluacion/$', evaluacion_api_list, name='evaluacion_api_list'),
    url(r'^api/evaluacion/(?P<pk>\d+)/$', evaluacion_api_detail, name='evaluacion_api_detail'),

    url(r'^api/visita/$', visita_api_list, name='visita_api_list'),
    url(r'^api/calendario/$', calendario_api_list, name='kalite_calendario_api_list'),
    url(r'^api/visita/(?P<pk>\d+)/$', visita_api_detail, name='visita_api_detail'),

    url(r'^api/grado/$', grado_api, name='grado_api'),
    url(r'^api/grado/(?P<pk>\d+)/$', grado_api_detail, name='grado_api_detail'),

    url(r'^api/ejerciciosgrado/$', ejerciciosgrado_api, name='ejerciciosgrado_api'),
    url(r'^api/ejerciciosgrado/(?P<pk>\d+)/$', ejerciciosgrado_api_detail, name='ejerciciosgrado_api_detail'),
]
