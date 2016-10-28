from django.conf.urls import url
from apps.kardex.views import *

urlpatterns = [
	url(r'^equipo/$', Equipolog.as_view(), name='kardex_equipo'),
	url(r'^equipo/informe/(?P<ini>[\w-]+)/(?P<out>[\w-]+)/$', informe_general, name='equipo_list'),
	url(r'^equipo/entrada/(?P<pk>\d+)/$', EquipoEntrada.as_view(), name='kardex_equipo_entrada'),
	url(r'^equipo/salida/(?P<pk>\d+)/$', EquipoSalida.as_view(), name='kardex_equipo_salida'),
	url(r'^out/', SalidaCreate.as_view(), name='kardex_salida'),
	url(r'^in/', EntradaCreate.as_view(), name='kardex_entrada'),
	url(r'^proveedor/', ProveedorCreate.as_view(), name='kardex_proveedor')
]