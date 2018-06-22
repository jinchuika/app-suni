from django.conf.urls import url
from apps.inventario import views as inv_v

urlpatterns = [
    # Creacion de las salidas de inventario
    url(
        r'^salida/add/$',
        inv_v.SalidaInventarioCreateView.as_view(),
        name='salidainventario_add'
    ),
    # Actualizacion  de las salidas de inventario
    url(
        r'^salida/(?P<pk>\d+)/edit/$',
        inv_v.SalidaInventarioUpdateView.as_view(),
        name='salidainventario_edit'
    ),
    # Creacion de Paquetes
    url(
        r'^salida/(?P<pk>\d+)/crear_paquetes/$',
        inv_v.SalidaPaqueteUpdateView.as_view(),
        name='paquete_update'
    ),
    # Creación de revisión de salida
    url(
        r'^salida/revision/add/$',
        inv_v.RevisionSalidaCreateView.as_view(),
        name='revisionsalida_add'
    ),
    # Edición de revisión de salida
    url(
        r'^salida/revision/(?P<pk>\d+)/edit/$',
        inv_v.RevisionSalidaUpdateView.as_view(),
        name='revisionsalida_update'
    ),
]
