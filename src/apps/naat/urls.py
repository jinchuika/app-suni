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

    url(r'^participante/actuales/$', naat_v.AsignacionesActualesListView.as_view(), name='participante_naat_add'),
    url(r'^participante/add/$', naat_v.ParticipanteNaatCreateView.as_view(), name='participante_naat_add'),

    url(r'^sesion/add/$', naat_v.SesionPresencialCreateView.as_view(), name='sesion_naat_add'),
    url(r'^sesion/(?P<pk>\d+)/$', naat_v.SesionPresencialDetailView.as_view(), name='sesion_naat_detail'),
    url(r'^sesion/(?P<pk>\d+)/editar/$', naat_v.SesionPresencialUpdateView.as_view(), name='sesion_naat_update'),

    url(r'^calendario/$', naat_v.SesionPresencialCalendarView.as_view(), name='sesion_naat_calendar'),
    url(
        r'^api/', include('apps.naat.api_urls', namespace='naat_api')),
]
