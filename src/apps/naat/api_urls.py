from django.conf.urls import url
from apps.naat import api_views

calendario_api_list = api_views.SesionPresencialCalendarViewSet.as_view({'get': 'list'})

urlpatterns = [
    url(
        r'facilitador/$',
        api_views.FacilitadorListView.as_view(),
        name='facilitador_list'),
    url(
        r'facilitador/(?P<username>\w+)/$',
        api_views.FacilitadorRetrieveView.as_view(),
        name='facilitador_detail'),
    url(
        r'participante/$',
        api_views.ParticipanteListView.as_view(),
        name='participante_list'),
    url(
        r'participante/(?P<dpi>\w+)/$',
        api_views.ParticipanteRetrieveView.as_view(),
        name='participante_detail'),
    url(
        r'participante/(?P<dpi>\w+)/update/$',
        api_views.ParticipanteUpdateView.as_view(),
        name='participante_update'),
    url(
        r'asignacion/$',
        api_views.AsignacionNaatListView.as_view(),
        name='asignacion_list'),
    url(
        r'calendario/$',
        calendario_api_list,
        name='calendario_api_list'),
]
