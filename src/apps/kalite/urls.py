from django.conf.urls import url
from apps.kalite.views import *


urlpatterns = [
    url(r'^rubrica/list/$', RubricaListView.as_view(), name='rubrica_list'),
    url(r'^rubrica/add/$', RubricaCreateView.as_view(), name='rubrica_add'),
    url(r'^rubrica/(?P<pk>\d+)/$', RubricaDetailView.as_view(), name='rubrica_detail'),

    url(r'^indicador/add/$', IndicadorCreateView.as_view(), name='indicador_add'),
]
