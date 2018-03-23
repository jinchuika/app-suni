from rest_framework import routers
# from django.conf.urls import url
from apps.mye import api_views


router = routers.DefaultRouter()
router.register(r'solicitud', api_views.SolicitudViewSet)
router.register(r'validacion', api_views.ValidacionViewSet)
router.register(r'validacion-calendar', api_views.ValidacionCalendarViewSet, base_name='validacion-calendar')
router.register(r'cooperante', api_views.CooperanteViewSet, base_name='cooperante')
router.register(r'proyectos',api_views.ProyectoViewSet, base_name='proyectos')


urlpatterns = []
urlpatterns += router.urls
