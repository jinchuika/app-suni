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
 # Informe de existencia
 url(
    r'^informe/dispositivo/existencias/$',
    conta_v.ExistenciaDispositivosInformeView.as_view(),
    name='informe_existencias_dispositivo'
   ),
          # api para la existencia de dipositivos
 url(
    r'^informe/existencias/$',
    conta_v.InformeExistencias.as_view(),
    name='informe_existencias'
   ),
   # api para el rastreo de dispositivos
 url(
    r'^informe/desecho/rastreo/$',
    conta_v.InformeRastreoDesecho.as_view(),
    name='informe_rastreo_desecho'
   ),
 # Informe de rastreo de existencias
 url(
    r'^informe/rastreo/desecho/$',
    conta_v.DesechoRastreoInformeView.as_view(),
    name='informe_rastreo'
   ),
# api para el rastreo de dispositivos
 url(
    r'^informe/repuesto/rastreo/$',
    conta_v.InformeRastreoRepuesto.as_view(),
    name='informe_rastreo_repuesto'
   ),
# Informe de rastreo de repuestos
 url(
    r'^informe/rastreo/repuesto/$',
    conta_v.RepuestoRastreoInformeView.as_view(),
    name='informe_repuesto'
   ),
# Informe de rastreo de dipositivos
 url(
    r'^informe/rastreo/dispositivos/$',
    conta_v.RastreoDispositivoContabilidad.as_view(),
    name='informe_repuesto'
   ),
 # Urls para el modulo de BEQT 

  # Informe de Entradas
 url(
    r'^beqt/informentrada/$',
    conta_v.ContabilidadBEQTEntradaInformeListView.as_view(),
    name='contabilidad_entrada_beqt'
   ),

 url(
    r'^beqt/informentradapi/$',
    conta_v.InformeEntradaBeqtJson.as_view(),
    name='contabilidad_api_entrada_beqt'
    ),
     # Informe de Dispositivos x Entrada
 url(
    r'^beqt/informentradadispositivo/$',
    conta_v.ContabilidadEntradaDispBeqtInformeListView.as_view(),
    name='contabilidad_beqt_entrada_dispositivo'
   ),
    # Devolver Data de Informe de Dispositivos x Entrada
 url(
    r'^beqt/informentradadispositivoapi/$',
    conta_v.InformeEntradaDispositivoBeqtJson.as_view(),
    name='contabilidad_beqt_api_entrada_dispositivo'
    ),
  # Informe de Salidas por Donación
 url(
    r'^beqt/informesalidas/$',
    conta_v.ContabilidadBeqtSalidasInformeListView.as_view(),
    name='contabilidad_beqt_salidas'
   ),
 # Devolver Data de Informe de Entradas
 url(
    r'^beqt/informesalidasapi/$',
    conta_v.InformeSalidaBeqtJson.as_view(),
    name='contabilidad_beqt_api_salidas'
    ),
 
    # Informe de Resumen
 url(
    r'^beqt/informeresumen/$',
    conta_v.ContabilidadResumenBeqtInformeListView.as_view(),
    name='contabilidad_beqt_resumen'
   ),
 # Devolver Data de Resumen
 url(
    r'^beqt/informeresumenapi/$',
    conta_v.InformeResumenBeqtJson.as_view(),
    name='contabilidad_beqt_api_resumen'
    ),   
     

## Planilla Contabilidad
 url(
   r'^apiplanilla/$',
   conta_v.PlanillaApiConta.as_view(),
   name="api_planilla"
   ),
 url(
   r'^apidatosplanilla/$',
   conta_v.FiltrosPlanillaApiConta.as_view(),
   name="api_datosplanilla"
   ),
 url(
   r'^planilla/$',
   conta_v.PlanillaContaView.as_view(),
   name="planilla_conta"
   ),
      
        

 # Api
 url(r'^api/', include(('apps.conta.api_urls', 'conta'), namespace='conta_api'))
]
