from django.conf.urls import url, include

from apps.naat import views as naat_v


urlpatterns = [
    url(r'^participante/actuales/$', naat_v.AsignacionesActualesListView.as_view(), name='participante_naat_add'),
    url(r'^participante/add/$', naat_v.ParticipanteNaatCreateView.as_view(), name='participante_naat_add'),

    url(r'^sesion/(?P<pk>\d+)/$', naat_v.SesionPresencialDetailView.as_view(), name='sesion_naat_detail'),
    url(r'^calendario/$', naat_v.SesionPresencialCalendarView.as_view(), name='sesion_naat_calendar'),
    url(
        r'^api/', include('apps.naat.api_urls', namespace='naat_api')),
]
