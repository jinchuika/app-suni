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
    # Detalles de la Salida
    url(
        r'^salida/(?P<pk>\d+)/detail/$',
        inv_v.SalidaInventarioDetailView.as_view(),
        name='salidainventario_detail'
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
    # Listado de revision de salida
    url(
        r'^salida/revision/list/$',
        inv_v.RevisionSalidaListView.as_view(),
        name='revisionsalida_list'
    ),
    # Asignación de dispositivos a paquetes
    url(
        r'^salida/(?P<pk>\d+)/paquetes/$',
        inv_v.SalidaPaqueteView.as_view(),
        name='salida_paquete'
    ),
    # Detalles de Paquete
    url(
        r'^salida/paquetes/(?P<pk>\d+)/$',
        inv_v.SalidaPaqueteDetailView.as_view(),
        name='detalle_paquete'
    ),

    # Creación de Historicos de paquetes
    url(
        r'^salida/historico/add/$',
        inv_v.RevisionComentarioCreate.as_view(),
        name='historico_salida'
    ),
    # Control de Calidad
    url(
        r'^salida/controlcalidad/$',
        inv_v.ControlCalidadListView.as_view(),
        name='controlcalidad_list'
    ),

]
