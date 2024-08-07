from django.conf.urls import url
from apps.beqt import views as beqt_v

urlpatterns = [
    # Creacion de las salidas de inventario
    url(
        r'^salida/add/$',
        beqt_v.SalidaInventarioCreateView.as_view(),
        name='salidainventario_beqt_add'
    ),
    # Actualizacion  de las salidas de inventario
    url(
        r'^salida/(?P<pk>\d+)/edit/$',
        beqt_v.SalidaInventarioUpdateView.as_view(),
        name='salidainventario_beqt_edit'
    ),
    # Detalles de la Salida
    url(
        r'^salida/(?P<pk>\d+)/detail/$',
        beqt_v.SalidaInventarioDetailView.as_view(),
        name='salidainventario_beqt_detail'
    ),
     # Listado de la Salida
    url(
        r'^salida/list/$',
        beqt_v.SalidaInventarioListView.as_view(),
        name='salidainventario_beqt_list'
    ),
    # Creacion de Paquetes
    url(
        r'^salida/(?P<pk>\d+)/crear_paquetes/$',
        beqt_v.SalidaPaqueteUpdateView.as_view(),
        name='paquete_beqt_update'
    ),
    # Creación de revisión de salida
    url(
        r'^salida/revision/add/$',
        beqt_v.RevisionSalidaCreateView.as_view(),
        name='revisionsalida_beqt_add'
    ),
    # Edición de revisión de salida
    url(
        r'^salida/revision/(?P<pk>\d+)/edit/$',
        beqt_v.RevisionSalidaUpdateView.as_view(),
        name='revisionsalida_beqt_update'
    ),
    # Listado de revision de salida
    url(
        r'^salida/revision/list/$',
        beqt_v.RevisionSalidaListView.as_view(),
        name='revisionsalida_beqt_list'
    ),
    # Asignación de dispositivos a paquetes
    url(
        r'^salida/(?P<pk>\d+)/paquetes/$',
        beqt_v.SalidaPaqueteView.as_view(),
        name='salida_paquete_beqt'
    ),
    # Detalles de Paquete
    url(
        r'^salida/paquetes/(?P<pk>\d+)/$',
        beqt_v.SalidaPaqueteDetailView.as_view(),
        name='detalle_paquete_beqt'
    ),

    # Creación de Historicos de paquetes
    url(
        r'^salida/historico/add/$',
        beqt_v.RevisionComentarioCreate.as_view(),
        name='historico_salida_beqt'
    ),
    # Creación de Historicos de Control de Calidad
    url(
        r'^salida/historicocontrol/add/$',
        beqt_v.RevisionComentarioSalidaCreate.as_view(),
        name='historico_control_beqt'
    ),
    # Control de Calidad
    url(
        r'^salida/controlcalidad/$',
        beqt_v.ControlCalidadListView.as_view(),
        name='controlcalidad_beqt_list'
    ),
    # Dispositivos Asignados
    url(
        r'^salida/dispositivoasignados/(?P<pk>\d+)/$',
        beqt_v.DispositivoAsignados.as_view(),
        name='dispositivo_beqt_asignados'
    ),
    # Imprimir Garantia
    url(
        r'^salida/(?P<pk>\d+)/garantia/$',
        beqt_v.GarantiaPrintView.as_view(),
        name='garantia_beqt_print'
    ),
    # Imprimir informe de laptops
    url(
        r'^salida/(?P<pk>\d+)/laptop/$',
        beqt_v.LaptopPrintView.as_view(),
        name='laptop_beqt_print'
    ),
    # Imprimir informe de Tablets
    url(
        r'^salida/(?P<pk>\d+)/tablets/$',
        beqt_v.TabletPrintView.as_view(),
        name='tablet_beqt_print'
    ),
    # Imprimir informe de TPE
    url(
        r'^salida/(?P<pk>\d+)/tpe/$',
        beqt_v.TpePrintView.as_view(),
        name='tpe_beqt_print'
    ),
    # Imprimir informe de mineduc
    url(
        r'^salida/(?P<pk>\d+)/mineduc/$',
        beqt_v.MineducPrintView.as_view(),
        name='mineduc_beqt_print'
    ),
    # Imprimir carta e prestamo
    url(
        r'^salida/(?P<pk>\d+)/prestamo/$',
        beqt_v.PrestamoCartaPrintView.as_view(),
        name='prestamo_carta_beqt_print'
    ),
    # Grid de dispsotivos en paquetes
    url(
        r'^salida/(?P<pk>\d+)/paquetesgrid/$',
        beqt_v.PaquetesDetalleGrid.as_view(),
        name='paquetes_beqt_grid'
    ),


]
