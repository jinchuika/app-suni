from django.conf.urls import url
from apps.inventario import views as inventario_v

urlpatterns = [
    # Creacion de las salidas de inventario
    url(
        r'^salida/add/$',
        inventario_v.SalidaInventarioCreateView.as_view(),
        name='salidainventario_add'
    ),
    url(
    # Actualizacion  de las salidas de inventario
        r'^salida/(?P<pk>\d+)/edit/$',
        inventario_v.SalidaInventarioUpdateView.as_view(),
        name='salidainventario_edit'
    ),
    url(
    # Creacion de Paquetes
        r'^salida/(?P<pk>\d+)/crear_paquetes/$',
        inventario_v.SalidaPaqueteUpdateView.as_view(),
        name='paquete_update'
    )
]
