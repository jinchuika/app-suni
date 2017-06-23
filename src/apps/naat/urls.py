from django.conf.urls import url, include
from apps.naat import api_views

from rest_framework.routers import DefaultRouter

naat_router = DefaultRouter()
# naat_router.register(r'api/asignacion', api_views.AsignacionNaatViewSet)
# naat_router.register(r'api/participante', api_views.ParticipanteNaatViewSet)
# naat_router.register(r'api/facilitador', api_views.FacilitadorNaatViewSet)

urlpatterns = [
    url(
        r'api/facilitador/$',
        api_views.FacilitadorListView.as_view(),
        name='facilitador_list'),
    url(
        r'api/facilitador/(?P<username>\w+)/$',
        api_views.FacilitadorRetrieveView.as_view(),
        name='facilitador_detail'),
    url(
        r'api/participante/$',
        api_views.ParticipanteListView.as_view(),
        name='participante_list'),
    url(
        r'api/participante/(?P<dpi>\w+)/$',
        api_views.ParticipanteRetrieveView.as_view(),
        name='participante_detail'),
    url(
        r'api/participante/(?P<dpi>\w+)/update/$',
        api_views.ParticipanteUpdateView.as_view(),
        name='participante_update'),
    url(
        r'api/asignacion/$',
        api_views.AsignacionNaatListView.as_view(),
        name='asignacion_list'),
    url(
        r'', include(naat_router.urls)),
]
