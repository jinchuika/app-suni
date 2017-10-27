from django.conf.urls import url, include
from apps.ie.views import *


urlpatterns = [
    url(r'^laboratorio/add/$', LaboratorioCreateView.as_view(), name='laboratorio_add'),
    url(r'^laboratorio/list/$', LaboratorioListView.as_view(), name='laboratorio_list'),
    url(r'^laboratorio/(?P<pk>\d+)/$', LaboratorioDetailView.as_view(), name='laboratorio_detail'),
    url(r'^laboratorio/(?P<pk>\d+)/update/$', LaboratorioUpdateView.as_view(), name='laboratorio_update'),

    url(r'^computadora/add/$', ComputadoraCreateView.as_view(), name='computadora_add'),
    url(r'^serie/add/$', SerieCreateView.as_view(), name='serie_add'),

    url(r'^requerimiento/add/$', RequerimientoCreateView.as_view(), name='ie_requerimiento_add'),
    url(r'^versionvalidacion/add/$', ValidacionVersionCreateView.as_view(), name='ie_versionvalidacion_add'),
    url(r'^validacion/add/$', ValidacionCreateView.as_view(), name='ie_validacion_add'),
    url(r'^validacion/(?P<pk>\d+)/$', IEValidacionDetailView.as_view(), name='ie_validacion_detail'),
    url(r'^validacion/(?P<pk>\d+)/update/$', IEValidacionUpdateView.as_view(), name='ie_validacion_update'),

    url(r'^dashboard/$', DashboardView.as_view(), name='ie_dashboard'),
    url(r'^dashboard/mapa/$', MapDashboardView.as_view(), name='ie_dashboard_mapa'),
    url(r'^dashboard/geo/$', GeoDashboardView.as_view(), name='ie_dashboard_geo'),

    url(r'^api/', include('apps.ie.api_urls'))
]
