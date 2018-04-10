from django.conf.urls import url
from apps.escuela.views import *
from apps.tpe.views import EquipamientoDetailView
from apps.mye.views import ValidacionDetailView

urlpatterns = [
    # url para la creacion de escuelas
    url(
        r'^$',
        EscuelaCrear.as_view(),
        name='escuela_crear'),

    # url para la creacion de escuelas
    url(
        r'^add/$',
        EscuelaCrear.as_view(),
        name='escuela_add'),

    # url para la busqueda de la escuela
    url(
        r'^buscar/$',
        EscuelaBuscar.as_view(),
        name='escuela_buscar'),

    # url para la solicitud de los detalles de una escuela
    url(
        r'^(?P<pk>\d+)/solicitud/(?P<id_solicitud>\d+)/$',
        EscuelaDetail.as_view(),
        name='escuela_solicitud_update'),

    # url para los detalles de una escuela
    url(
        r'^(?P<pk>\d+)/$',
        EscuelaDetail.as_view(),
        name='escuela_detail'),

    # url para editar los detalles de una escuela
    url(
        r'^(?P<pk>\d+)/editar/$',
        EscuelaEditar.as_view(),
        name='escuela_update'),

    # url para actualizar los detalles del equipamiento de la escuela
    url(
        r'^(?P<pk>\d+)/equipamiento/(?P<id_equipamiento>\d+)/edit$',
        EscuelaDetail.as_view(),
        name='escuela_equipamiento_update'),

    # url para mostrar los detalles de  los equipamientos
    url(
        r'^(?P<pk>\d+)/equipamiento/(?P<id_equipamiento>\d+)/$',
        EquipamientoDetailView.as_view(),
        name='escuela_equipamiento_detail'),

    # url para mostrar las validaciones
    url(
        r'^(?P<pk>\d+)/validacion/(?P<id_validacion>\d+)/edit$',
        EscuelaDetail.as_view(),
        name='escuela_validacion_update'),

    # url para los detalles de la validadcion
    url(
        r'^(?P<pk>\d+)/validacion/(?P<id_validacion>\d+)/$',
        ValidacionDetailView.as_view(),
        name='escuela_validacion_detail'),

    # url para edicion del contacto
    url(
        r'^(?P<id_escuela>\d+)/contacto/(?P<pk>\d+)/',
        EscContactoEditar.as_view(),
        name='escuela_contacto_edit'),

    # url para la creacion del contacto
    url(
        r'^(?P<id_escuela>\d+)/contacto/$',
        EscContactoCrear.as_view(),
        name='escuela_contacto_add'),

    # url para la creacion de la poblacion
    url(
        r'^poblacion/add/$',
        EscPoblacionCreateView.as_view(),
        name='poblacion_add'),

    # url para  los detalles de la matricula
    url(
        r'^(?P<id_escuela>\d+)/matricula/add/$',
        EscMatriculaCreateView.as_view(),
        name='matricula_add'),

    # url para  creacion del rendimiento academico
    url(
        r'^(?P<id_escuela>\d+)/rendimientoacademico/add/$',
        EscRendimientoAcademicoCreateView.as_view(),
        name='rendimientoacademico_add'),

]
