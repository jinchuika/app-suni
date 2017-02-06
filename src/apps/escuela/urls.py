from django.conf.urls import url
from apps.escuela.views import *

urlpatterns = [
    url(r'^$', EscuelaCrear.as_view(), name='escuela_crear'),
    url(r'^add/', EscuelaCrear.as_view(), name='escuela_add'),
    url(r'^buscar/$', EscuelaBuscar.as_view(), name='escuela_buscar'),
    url(r'^buscar/q/$', EscuelaBuscarBackend.as_view(), name='escuela_buscar_backend'),

    url(r'^(?P<pk>\d+)/solicitud/(?P<id_solicitud>\d+)/$', EscuelaDetail.as_view(), name='escuela_solicitud_update'),
    url(r'^(?P<pk>\d+)/equipamiento/(?P<id_equipamiento>\d+)/$', EscuelaDetail.as_view(), name='escuela_equipamiento_update'),
    url(r'^(?P<pk>\d+)/validacion/(?P<id_validacion>\d+)/$', EscuelaDetail.as_view(), name='escuela_validacion_update'),
    url(r'^(?P<pk>\d+)/$', EscuelaDetail.as_view(), name='escuela_detail'),
    url(r'^(?P<pk>\d+)/editar$', EscuelaEditar.as_view(), name='escuela_update'),

    url(r'^(?P<id_escuela>\d+)/contacto/(?P<pk>\d+)/', EscContactoEditar.as_view(), name='escuela_contacto_edit'),
    url(r'^(?P<id_escuela>\d+)/contacto/$', EscContactoCrear.as_view(), name='escuela_contacto_add'),

    url(r'^(?P<pk>\d+)/cooperante/$', EscuelaCooperanteUpdate.as_view(), name='escuela_cooperante_add'),
    url(r'^(?P<pk>\d+)/proyecto/$', EscuelaProyectoUpdate.as_view(), name='escuela_proyecto_add'),
]
