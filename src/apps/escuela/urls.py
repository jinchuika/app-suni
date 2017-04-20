from django.conf.urls import url
from apps.escuela.views import *
from apps.tpe.views import EquipamientoDetailView
from apps.mye.views import ValidacionDetailView

urlpatterns = [
    url(r'^$', EscuelaCrear.as_view(), name='escuela_crear'),
    url(r'^add/', EscuelaCrear.as_view(), name='escuela_add'),
    url(r'^buscar/$', EscuelaBuscar.as_view(), name='escuela_buscar'),

    url(r'^(?P<pk>\d+)/solicitud/(?P<id_solicitud>\d+)/$', EscuelaDetail.as_view(), name='escuela_solicitud_update'),

    url(r'^(?P<pk>\d+)/$', EscuelaDetail.as_view(), name='escuela_detail'),
    url(r'^(?P<pk>\d+)/editar$', EscuelaEditar.as_view(), name='escuela_update'),

    url(r'^(?P<pk>\d+)/equipamiento/(?P<id_equipamiento>\d+)/edit$', EscuelaDetail.as_view(), name='escuela_equipamiento_update'),
    url(r'^(?P<pk>\d+)/equipamiento/(?P<id_equipamiento>\d+)/$', EquipamientoDetailView.as_view(), name='escuela_equipamiento_detail'),

    url(r'^(?P<pk>\d+)/validacion/(?P<id_validacion>\d+)/edit$', EscuelaDetail.as_view(), name='escuela_validacion_update'),
    url(r'^(?P<pk>\d+)/validacion/(?P<id_validacion>\d+)/$', ValidacionDetailView.as_view(), name='escuela_validacion_detail'),

    url(r'^(?P<id_escuela>\d+)/contacto/(?P<pk>\d+)/', EscContactoEditar.as_view(), name='escuela_contacto_edit'),
    url(r'^(?P<id_escuela>\d+)/contacto/$', EscContactoCrear.as_view(), name='escuela_contacto_add'),

    url(r'^(?P<pk>\d+)/cooperante/$', EscuelaCooperanteUpdate.as_view(), name='escuela_cooperante_add'),
    url(r'^(?P<pk>\d+)/proyecto/$', EscuelaProyectoUpdate.as_view(), name='escuela_proyecto_add'),
]
