from django.conf.urls import url
from apps.kardex.views import *

urlpatterns = [
	url(r'^$', Equipolog.as_view(), name='kardex_equipo'),
	url(r'^compras/', InformeCompras.as_view(), name='kardex_compras'),
	url(r'^informe/(?P<ini>[\w-]+)/(?P<out>[\w-]+)/$', informe_general, name='equipo_list'),
	url(r'^entrada/(?P<pk>\d+)/$', EquipoEntrada.as_view(), name='kardex_equipo_entrada'),
	url(r'^salida/(?P<pk>\d+)/$', EquipoSalida.as_view(), name='kardex_equipo_salida'),
	url(r'^out/', SalidaCreate.as_view(), name='kardex_salida'),
	url(r'^in/$', EntradaCreate.as_view(), name='kardex_entrada'),
	url(r'^in/(?P<tipo>\d+)/(?P<ini>[\w-]+)/(?P<out>[\w-]+)/$', get_informe_entradas, name='kardex_entrada_informe'),
	url(r'^proveedor/', ProveedorCreate.as_view(), name='kardex_proveedor')
]