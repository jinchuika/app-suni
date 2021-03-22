from django.conf.urls import url, include
from apps.mye.views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    # Listado de Cooperantes
    url(
        r'^cooperante/list/$',
        CooperanteList.as_view(),
        name='cooperante_list'
        ),
    # Ingreso de  la informacion de los Cooperantes
    url(
        r'^cooperante/add/$',
        CooperanteCrear.as_view(),
        name='cooperante_add'
        ),
    # Detalles del Cooperante en especifico
    url(
        r'^cooperante/(?P<pk>\d+)/$',
        CooperanteDetalle.as_view(),
        name='cooperante_detail'
        ),
    # Modificacion de los datos del Cooperante
    url(
        r'^cooperante/(?P<pk>\d+)/editar/$',
        CooperanteUpdate.as_view(),
        name='cooperante_update'
        ),
    # Mapa de escuelas equipadas por un cooperante
    url(
        r'^cooperante/(?P<pk>\d+)/mapa/$',
        CooperanteMapaView.as_view(),
        name='cooperante_mapa'
        ),

    # Listado de todos los proyecto asignados
    url(
        r'^proyecto/list/$',
        ProyectoList.as_view(),
        name='proyecto_list'
        ),
    # Creacion de un nuevo proyecto
    url(
        r'^proyecto/add/$',
        ProyectoCrear.as_view(),
        name='proyecto_add'
        ),
    # Detalles de un proyecto en especifico
    url(
        r'^proyecto/(?P<pk>\d+)/$',
        ProyectoDetalle.as_view(),
        name='proyecto_detail'
        ),
    # Actualizacion de  Datos de un proyecto especifico
    url(
        r'^proyecto/(?P<pk>\d+)/editar/$',
        ProyectoUpdate.as_view(),
        name='proyecto_update'
        ),

    # Detalles de  una solicitud en especifico
    url(
        r'^solicitud/version/(?P<pk>\d+)/$',
        SolicitudVersionDetalle.as_view(),
        name='solicitud_version_detail'
        ),
    # Agregar nueva solitud
    url(
        r'^solicitud/version/add/$',
        SolicitudVersionCrear.as_view(),
        name='solicitud_version_add'
        ),
    # Agregar solitud mediante id de la escuela
    url(
        r'^solicitud/add/$',
        SolicitudCrearView.as_view(),
        name='solicitud_add'
    ),
    # Modificar los datos de una solicitud
    url(
        r'^solicitud/(?P<pk>\d+)/$',
        SolicitudUpdate.as_view(),
        name='solicitud_update'
        ),
    # listado de solicitudes
    url(
        r'^solicitud/list/$',
        cache_page(15)(SolicitudListView.as_view()),
        name='solicitud_list'
        ),
    # Creacion del Historia de Solicitud
    # punto de api
    url(
        r'^solicitud_comentarios/add/$',
        SolicitudComentarioCrear.as_view(),
        name='solicitud_comentario_add'
        ),

    # Creacion de Validacion
    url(
        r'^validacion/add/$',
        ValidacionCrearView.as_view(),
        name='validacion_add'
        ),
    # Actualizacion  de Validaciones
    url(
        r'^validacion/(?P<pk>\d+)/$',
        ValidacionUpdate.as_view(),
        name='validacion_update'
        ),
    # Agregar Comentarios
    #punto de api
    url(
        r'^validacion_comentario/add/$',
        ValidacionComentarioCrear.as_view(),
        name='validacion_comentario_add'
        ),
    # Mostrar lista de Validaciones
    url(
        r'^validacion/list/$',
        cache_page(15)(ValidacionListView.as_view()),
        name='validacion_list'
        ),

    # Api
    url(r'^api/', include(('apps.mye.api_urls', 'mye'), namespace='mye_api')),
]
