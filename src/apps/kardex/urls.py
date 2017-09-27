from django.conf.urls import url
from apps.kardex.views import *

urlpatterns = [
    url(r'^equipo/$', EquipoListView.as_view(), name='kardex_equipo_list'),
    url(r'^equipo/add/$', EquipoCreateView.as_view(), name='kardex_equipo_add'),

    url(r'^proveedor/$', ProveedorListView.as_view(), name='kardex_proveedor_list'),
    url(r'^proveedor/add/$', ProveedorCreateView.as_view(), name='kardex_proveedor_add'),
    url(r'^proveedor/(?P<pk>\d+)/$', ProveedorDetailView.as_view(), name='kardex_proveedor_detail'),
    url(r'^proveedor/(?P<pk>\d+)/update/$', ProveedorUpdateView.as_view(), name='kardex_proveedor_update'),

    url(r'^entrada/$', EntradaCreateView.as_view(), name='kardex_entrada'),
    url(r'^entrada/(?P<pk>\d+)/$', EntradaDetailView.as_view(), name='kardex_entrada_detail'),
    url(r'^entrada/(?P<pk>\d+)/print/$', EntradaPrintView.as_view(), name='kardex_entrada_print'),
    url(r'^entrada/(?P<pk>\d+)/update/$', EntradaUpdateView.as_view(), name='kardex_entrada_update'),
    url(r'^entradadetalle/add/$', EntradaDetalleCreateView.as_view(), name='kardex_entradadetalle_add'),

    url(r'^salida/$', SalidaCreateView.as_view(), name='kardex_salida'),
    url(r'^salida/add/$', SalidaCreateView.as_view(), name='kardex_salida_add'),
    url(r'^salida/(?P<pk>\d+)/$', SalidaDetailView.as_view(), name='kardex_salida_detail'),
    url(r'^salida/(?P<pk>\d+)/print/$', SalidaPrintView.as_view(), name='kardex_salida_print'),
    url(r'^salida/(?P<pk>\d+)/update/$', SalidaUpdateView.as_view(), name='kardex_salida_update'),
    url(r'^salidadetalle/add/$', SalidaDetalleCreateView.as_view(), name='kardex_salidadetalle_add'),

    url(r'^informe/$', KardexInformeView.as_view(), name='kardex_informe'),
]
