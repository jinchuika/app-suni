from django.conf.urls import url, include
from apps.inventario import views as inventario_v


urlpatterns = [
    # url para la creacion de entradas
    url(
        r'^entrada/add/$',
        inventario_v.EntradaCreateView.as_view(),
        name='entrada_add'
        ),
    # url para la actualizacion de entradas
    url(
        r'^entrada/(?P<pk>\d+)/edit/$',
        inventario_v.EntradaUpdateView.as_view(),
        name='entrada_update'
        ),
    # url para detalles de entrada
    url(
        r'^entrada/(?P<pk>\d+)/$',
        inventario_v.EntradaDetailView.as_view(),
        name='entrada_detail'
    ),
    # ulr para los infomras de entrada
    url(
        r'^entrada/list/$',
        inventario_v.EntradaListView.as_view(),
        name='entrada_list'
    ),
    # url para actualziacion de  los detalles de entrada
    url(
        r'^entradadetalle/(?P<pk>\d+)/edit/$',
        inventario_v.EntradaDetalleUpdateView.as_view(),
        name='entradadetalle_update'
    ),
    # url de Carta de Agradecimiento
    url(
        r'^entradadetalle/reporte/carta/(?P<pk>\d+)/$',
        inventario_v.CartaAgradecimiento.as_view(),
        name='carta_agradecimiento'
    ),
    # url Constancia de lo Útil
    url(
        r'^entradadetalle/util/(?P<pk>\d+)/$',
        inventario_v.ConstanciaUtil.as_view(),
        name='reporte_sucio'
    ),
    # url Constancia de Entrada
    url(
        r'^entradadetalle/constancia/(?P<pk>\d+)/$',
        inventario_v.ConstanciaEntrada.as_view(),
        name='constancia_entrada'
    ),
    # url impresion de QR de dispositivos por detalle de entrada
    url(
        r'^entrada/(?P<pk>\d+)/reporteqr/(?P<detalle>\d+)/$',
        inventario_v.ImprimirQr.as_view(),
        name='imprimir_qr'
    ),
    # url impresion de QR de repuestos por detallle de entrada
    url(
        r'^entrada/(?P<pk>\d+)/reporterepuestosqr/(?P<detalle>\d+)/$',
        inventario_v.ReporteRepuestosQr.as_view(),
        name='imprimir_repuesto'
    ),
    # url para detalles de dispositivos de entradas
    url(
        r'^entrada/(?P<pk>\d+)/listadodispositivo/(?P<detalle>\d+)/$',
        inventario_v. EntradaDetalleDispositivos.as_view(),
        name='detalles_dispositivos'
    ),
    # url para detalles de repuesto de entradas
    url(
        r'^entrada/(?P<pk>\d+)/listadorepuesto/(?P<detalle>\d+)/$',
        inventario_v. EntradaDetalleRepuesto.as_view(),
        name='detalles_repuesto'
    ),
]
