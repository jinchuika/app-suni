from django.conf.urls import url
from apps.inventario import views as inv_v

urlpatterns = [
	# Creacion de asignación de inventario interno
    url(
        r'^interno/add/$',
        inv_v.InventarioInternoCreateView.as_view(),
        name='inventariointerno_add'
    ),
    # Asignación de dispositivos de inventario interno
    url(
        r'^interno/(?P<pk>\d+)/edit/$',
        inv_v.InventarioInternoUpdateView.as_view(),
        name='inventariointerno_edit'
    ),
    # Asignación de dispositivos a salida de inventario
    url(
        r'^interno/(?P<pk>\d+)/asignar_dispositivo/$',
        inv_v.InventarioInternoPaqueteUpdateView.as_view(),
        name='asignar_dispositivo'
    ),
    # Detalle de asignación
    url(
        r'^interno/(?P<pk>\d+)/$',
        inv_v.InventarioInternoDetailView.as_view(),
        name='inventariointerno_detail'
    ),
    # Informe de asignaciones
    url(
        r'^interno/list/$',
        inv_v.InventarioInternoListView.as_view(),
        name='inventariointerno_list'
    ),
    # Carta de Responsabilidad
    url(
        r'^interno/(?P<pk>\d+)/cartaprint/$',
        inv_v.CartaPrintView.as_view(),
        name='carta_responsabilidad_print'
    ),
]