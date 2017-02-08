from django.conf.urls import url
from apps.mye.views import *

urlpatterns = [
    url(r'^$', CooperanteList.as_view(), name='list_c'),
    url(r'^cooperante/all/$', CooperanteList.as_view(), name='cooperante_list'),
    url(r'^cooperante/add/$', CooperanteCrear.as_view(), name='cooperante_add'),
    url(r'^cooperante/(?P<pk>\d+)/$', CooperanteDetalle.as_view(), name='cooperante_detail'),
    url(r'^cooperante/(?P<pk>\d+)/editar/$', CooperanteUpdate.as_view(), name='cooperante_update'),

    url(r'^proyecto/all/$', ProyectoList.as_view(), name='proyecto_list'),
    url(r'^proyecto/add/$', ProyectoCrear.as_view(), name='proyecto_add'),
    url(r'^proyecto/(?P<pk>\d+)/$', ProyectoDetalle.as_view(), name='proyecto_detail'),
    url(r'^proyecto/(?P<pk>\d+)/editar/$', ProyectoUpdate.as_view(), name='proyecto_update'),

    url(r'^solicitud/version/(?P<pk>\d+)/$', SolicitudVersionDetalle.as_view(), name='solicitud_version_detail'),
    url(r'^solicitud/version/add/$', SolicitudVersionCrear.as_view(), name='solicitud_version_add'),

    url(r'^solicitud/add/$', SolicitudCrearView.as_view(), name='solicitud_add'),
    url(r'^solicitud/(?P<pk>\d+)/$', SolicitudUpdate.as_view(), name='solicitud_update'),

    url(r'^validacion/add/$', ValidacionCrearView.as_view(), name='validacion_add'),
    url(r'^validacion/(?P<pk>\d+)/$', ValidacionUpdate.as_view(), name='validacion_update'),

    url(r'^informe/$', InformeMyeView.as_view(), name='informe_mye'),
    url(r'^informe/q/$', InformeMyeBackend.as_view(), name='informe_mye_backend'),
    url(r'^validacion_comentario/add/$', ValidacionComentarioCrear.as_view(), name='validacion_comentario_add'),
]

