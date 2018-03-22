from django.conf.urls import url, include

from apps.naat import views as naat_v


urlpatterns = [
    # Creación de un :class:`ProcesoNaat`
    url(
        r'^proceso/add/$',
        naat_v.ProcesoNaatCreateView.as_view(),
        name='proceso_naat_add'),

    # Detalle de un :class:`ProcesoNaat`
    url(
        r'^proceso/(?P<pk>\d+)/$',
        naat_v.ProcesoNaatDetailView.as_view(),
        name='proceso_naat_detail'),

    # Listado de :class:`ProcesoNaat`
    url(
        r'^proceso/list/$',
        naat_v.ProcesoNaatListView.as_view(),
        name='proceso_naat_list'),

    url(
        r'^participante/actuales/$',
        naat_v.AsignacionesActualesListView.as_view(),
        name='participante_naat_add'),

    # Creación individual de un nuevo :class:`Participante` para asignarlo a un :class:`Proceso`
    url(
        r'^participante/add/$',
        naat_v.ParticipanteNaatCreateView.as_view(),
        name='participante_naat_add'),
    # Creación de una nueva :class:`SesionPresencial`
    url(
        r'^sesion/add/$',
        naat_v.SesionPresencialCreateView.as_view(),
        name='sesion_naat_add'),
    # Detalle de una :class:`SesionPresencial`
    url(
        r'^sesion/(?P<pk>\d+)/$',
        naat_v.SesionPresencialDetailView.as_view(),
        name='sesion_naat_detail'),
    # Edición de una :class:`SesionPresencial`
    url(
        r'^sesion/(?P<pk>\d+)/editar/$',
        naat_v.SesionPresencialUpdateView.as_view(),
        name='sesion_naat_update'),

    # Calendario de sesiones de Naat
    url(
        r'^calendario/$',
        naat_v.SesionPresencialCalendarView.as_view(),
        name='sesion_naat_calendar'),
    url(
        r'^api/',
        include('apps.naat.api_urls', namespace='naat_api')),
]
