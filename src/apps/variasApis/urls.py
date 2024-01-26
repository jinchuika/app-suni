from apps.variasApis import views as varias_v 
from django.conf.urls import url, include
urlpatterns = [
 # Creacion de periodos fiscales

  url(
    r'^todo/$',
    varias_v.SubirTodo.as_view(),
    name='revision_datos'
 ),
 url(
    r'^informe/$',
    varias_v.RevionErrores.as_view(),
    name='revisar_errores'
 ),
  url(
    r'^subir/asignaciones/$',
    varias_v.SubirAsignacionesJson.as_view(),
    name='subir_asignaciones'
 ),
 url(
    r'^subir/notaasistencia/$',
    varias_v.SubirNotasAsistenciaJson.as_view(),
    name='subir_nota_asistencia'
 ),
 url(
    r'^subir/notahito/$',
    varias_v.SubirNotasHitosJson.as_view(),
    name='subir_nota_hito'
 )
]

