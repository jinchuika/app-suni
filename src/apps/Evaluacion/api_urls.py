from django.conf.urls import url
from apps.Evaluacion import api_views

sede_api_list = api_views.SedeViewSet.as_view({
    'get': 'list'})

urlpatterns = [
    url(r'sede/list/$', sede_api_list , name='api_sede_list'),
]
