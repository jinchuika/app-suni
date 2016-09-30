from django.conf.urls import url
from apps.kardex import views

urlpatterns = [
	url(r'^equipo/entrada/(?P<id_equipo>[0-9]+)/$', views.equipo_entrada, name='kardex_equipo_entrada'),
	url(r'^equipo/salida/(?P<id_equipo>[0-9]+)/$', views.equipo_salida, name='kardex_equipo_salida'),
	url(r'^equipo/$', views.index, name='kardex_equipo'),
	url(r'^out/', views.SalidaCreate.as_view(), name='kardex_salida'),
	url(r'^in/', views.EntradaCreate.as_view(), name='kardex_entrada'),
	url(r'^proveedor/', views.ProveedorCreate.as_view(), name='kardex_proveedor')
]