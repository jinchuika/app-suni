from django.conf.urls import url, include
from apps.conta import views as conta_v

app_name = 'conta'
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

 # Api
 url(r'^api/', include(('apps.conta.api_urls', 'conta'), namespace='conta_api'))
]
