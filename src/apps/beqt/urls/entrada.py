from django.conf.urls import url, include
from apps.beqt import views as beqt_v


urlpatterns = [
    # url para la creacion de entradas
    url(
        r'^entrada/add/$',
        beqt_v.EntradaCreateView.as_view(),
        name='entrada_beqt_add'
        ),
     # url para la actualizacion de entradas
    url(
        r'^entrada/(?P<pk>\d+)/edit/$',
        beqt_v.EntradaUpdateView.as_view(),
        name='entrada_beqt_update'
        ),
    # url para detalles de entrada
    url(
        r'^entrada/(?P<pk>\d+)/$',
        beqt_v.EntradaDetailView.as_view(),
        name='entrada_beqt_detail'
    ),
    # ulr para los infomras de entrada
    url(
        r'^entrada/list/$',
        beqt_v.EntradaListView.as_view(),
        name='entrada_beqt_list'
    ),
     # url para actualziacion de  los detalles de entrada
    url(
        r'^entradadetalle/(?P<pk>\d+)/edit/$',
        beqt_v.EntradaDetalleUpdateView.as_view(),
        name='entradadetalle_beqt_update'
    ),
     # url de Carta de Agradecimiento
    url(
        r'^entradadetalle/reporte/carta/(?P<pk>\d+)/$',
        beqt_v.CartaAgradecimiento.as_view(),
        name='carta_agradecimiento_beqt'
    ),
    # url Constancia de lo Útil
    url(
        r'^entradadetalle/util/(?P<pk>\d+)/$',
        beqt_v.ConstanciaUtil.as_view(),
        name='reporte_sucio_beqt'
    ),
    # url Constancia de Entrada
    url(
        r'^entradadetalle/constancia/(?P<pk>\d+)/$',
        beqt_v.ConstanciaEntrada.as_view(),
        name='constancia_entrada_beqt'
    ),
    # url impresion de QR de dispositivos por detalle de entrada
    url(
        r'^entrada/(?P<pk>\d+)/reporteqr/(?P<detalle>\d+)/$',
        beqt_v.ImprimirQr.as_view(),
        name='imprimir_qr_beqt'
    ),
    # url para detalles de dispositivos de entradas
    url(
        r'^entrada/(?P<pk>\d+)/listadodispositivo/(?P<detalle>\d+)/$',
        beqt_v. EntradaDetalleDispositivos.as_view(),
        name='detalles_dispositivos_beqt'
    ),
  
]
