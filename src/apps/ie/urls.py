from django.conf.urls import url, include
from apps.ie.views import *


urlpatterns = [
    url(r'^laboratorio/add/$', LaboratorioCreateView.as_view(), name='laboratorio_add'),
    url(r'^laboratorio/list/$', LaboratorioListView.as_view(), name='laboratorio_list'),
    url(r'^laboratorio/(?P<pk>\d+)/$', LaboratorioDetailView.as_view(), name='laboratorio_detail'),
    url(r'^laboratorio/(?P<pk>\d+)/update/$', LaboratorioUpdateView.as_view(), name='laboratorio_update'),

    url(r'^computadora/add/$', ComputadoraCreateView.as_view(), name='computadora_add'),
    url(r'^serie/add/$', SerieCreateView.as_view(), name='serie_add'),
]
