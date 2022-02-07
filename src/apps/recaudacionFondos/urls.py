from django.conf.urls import url, include
from apps.recaudacionFondos import views as rf_v

urlpatterns = [
    # Editar Proveedor
    url(
        r'^proveedores/(?P<pk>\d+)/$',
        rf_v.ProveedorUptadeView.as_view(),
        name='recaudacion_proveedor_edit'
        ),
    # Listado de proveedores
    url(
        r'^proveedores/$',
        rf_v.ProveedorDetailView.as_view(),
        name='recaudacion_proveedor_detail'
        ),
    # Creacion de entrada
    url(
        r'^entrada/$',
        rf_v.EntradaCreateView.as_view(),
        name='recaudacion_entrada_add'
        ),
    # Edicion  de entrada
    url(
        r'^entrada/edit/(?P<pk>\d+)/$',
        rf_v.EntradaDetailView.as_view(),
        name='recaudacion_entrada_edit'
        ),
    # detalle de entrada
    url(
        r'^detallentrada/add/$',
        rf_v.EntradaDetalleCreateView.as_view(),
        name='recaudacion_entradadetalle_add'
        ),
    # creacion de articulos
    url(
        r'^articulo/add/$',
        rf_v.ArticuloCreateView.as_view(),
        name='recaudacion_articulo_add'
        ),
    # Creacion de salida
    url(
        r'^salida/$',
        rf_v.SalidaCreateView.as_view(),
        name='recaudacion_salida_add'
        ),
    # Edicion  de salida
    url(
        r'^salida/edit/(?P<pk>\d+)/$',
        rf_v.SalidaDetailView.as_view(),
        name='recaudacion_salida_edit'
        ),
    # Edicion  de salida
    url(
        r'^salida/update/(?P<pk>\d+)/$',
        rf_v.SalidaUpdateView.as_view(),
        name='recaudacion_salida_update'
        ),
    # detalle de entrada
    url(
        r'^detallesalida/add/$',
        rf_v.SalidaDetalleCreateView.as_view(),
        name='recaudacion_salidadetalle_add'
        ),
    # Api
    url(r'^api/', include(('apps.recaudacionFondos.api_urls', 'recaudacionFondos'), namespace='recaudacionFondos_api')),

        ]
