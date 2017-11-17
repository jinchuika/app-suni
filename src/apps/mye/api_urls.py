from rest_framework import routers
from django.conf.urls import url
from apps.mye import api_views


router = routers.DefaultRouter()
router.register(
    r'validacion-calendar',
    api_views.ValidacionCalendarViewSet,
    base_name='validacion-calendar')

urlpatterns = []
urlpatterns += router.urls
