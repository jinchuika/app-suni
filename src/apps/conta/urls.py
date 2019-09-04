from django.conf.urls import url, include
from apps.conta import views as conta_v

urlpatterns = [
 # Creacion de periodos fiscales
 url(
    r'^periodo/add/$',
    conta_v.PeriodoFiscalCreateView.as_view(),
    name='periodo_add'
 ),
 # Listado de Periodos fiscales
 url(
    r'^periodo/list/$',
    conta_v.PeriodoFiscalListView.as_view(),
    name='periodo_list'
 ),
 # Detalles de  periodos fiscales
 url(
    r'^periodo/(?P<pk>\d+)/$',
    conta_v.PeriodoFiscalDetailView.as_view(),
    name='periodo_detail'
 ),
 # Actualizacion de  periodos fiscales
 url(
    r'^periodo/(?P<pk>\d+)/edit/$',
    conta_v.PeriodoFiscalUpdateView.as_view(),
    name='periodo_edit'
 ),
 # Creacion de precio Estandar
 url(
     r'^precioestandar/add/$',
     conta_v.PrecioEstandarCreateView.as_view(),
     name='precioestandar_add'
  ),
 # Listado de  precioes estandar
 url(
     r'^precioestandar/list/$',
     conta_v.PrecioEstandarListView.as_view(),
     name='precioestandar_list'
   ),
 # Informe de  precio estandar
 url(
     r'^precioestandar/informe/$',
     conta_v.PrecioEstandarInformeListView.as_view(),
     name='precioestandar_informe'
   ),
 # Devolver Data de Informe de Precio Estandar
 url(
     r'^precioestandar/informecantidad/$',
     conta_v.InformeCantidadJson.as_view(),
     name='prueba'
    ),
 # Informe de Entradas
 url(
    r'^precioestandar/informentrada/$',
    conta_v.ContabilidadEntradaInformeListView.as_view(),
    name='contabilidad_entrada'
   ),
 # Devolver Data de Informe de Entradas
 url(
    r'^precioestandar/informentradapi/$',
    conta_v.InformeEntradaJson.as_view(),
    name='contabilidad_api_entrada'
    ),
 # Informe de Dispositivos x Entrada
 url(
    r'^precioestandar/informentradadispositivo/$',
    conta_v.ContabilidadEntradaDispInformeListView.as_view(),
    name='contabilidad_entrada_dispositivo'
   ),
  # Devolver Data de Informe de Dispositivos x Entrada
 url(
    r'^precioestandar/informentradadispositivoapi/$',
    conta_v.InformeEntradaDispositivoJson.as_view(),
    name='contabilidad_api_entrada_dispositivo'
    ),
  # Informe de Salidas por Donación
 url(
    r'^precioestandar/informesalidas/$',
    conta_v.ContabilidadSalidasInformeListView.as_view(),
    name='contabilidad_salidas'
   ),
 # Devolver Data de Informe de Entradas
 url(
    r'^precioestandar/informesalidasapi/$',
    conta_v.InformeSalidaJson.as_view(),
    name='contabilidad_api_salidas'
    ),

   # Informe de Salidas por Desecho
 url(
    r'^precioestandar/informedesecho/$',
    conta_v.ContabilidadDesechoInformeListView.as_view(),
    name='contabilidad_desecho'
   ),
 # Devolver Data de Informe de Entradas
 url(
    r'^precioestandar/informedesechoapi/$',
    conta_v.InformeDesechoJson.as_view(),
    name='contabilidad_api_desecho'
    ),

    # Informe de Resumen
 url(
    r'^precioestandar/informeresumen/$',
    conta_v.ContabilidadResumenInformeListView.as_view(),
    name='contabilidad_resumen'
   ),
 # Devolver Data de Resumen
 url(
    r'^precioestandar/informeresumenapi/$',
    conta_v.InformeResumenJson.as_view(),
    name='contabilidad_api_resumen'
    ),

 # Api
 url(r'^api/', include(('apps.conta.api_urls', 'conta'), namespace='conta_api'))
]
