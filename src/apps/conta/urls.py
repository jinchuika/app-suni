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
 url(
     r'^precioestandar/informecantidad/$',
     conta_v.InformeCantidadJson.as_view(),
     name='prueba'
    ),
 url(
    r'^precioestandar/informentrada/$',
    conta_v.ContabilidadEntradaInformeListView.as_view(),
    name='contabilidad_entrada'
   ),
 url(
  r'^precioestandar/informentradapi/$',
  conta_v.InformeEntradaJson.as_view(),
  name='contabilidad_api_entrada'
 ),


 # Api
 url(r'^api/', include(('apps.conta.api_urls', 'conta'), namespace='conta_api'))
]
