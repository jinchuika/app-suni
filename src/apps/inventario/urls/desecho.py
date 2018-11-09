from django.conf.urls import url, include
from apps.inventario import views as inventario_v


urlpatterns = [
    #  Creacion de Desechos
    url(
        r'^desechoempresa/add/$',
        inventario_v.DesechoEmpresaCreateView.as_view(),
        name='desechoempresa_add'
    ),
    # Ver los detalles de desecho
    url(
        r'^desechoempresa/(?P<pk>\d+)/$',
        inventario_v.DesechoEmpresaDetailView.as_view(),
        name='desechoempresa_detail'
    ),
    # Mostrar el listado de desecho
    url(
        r'^desechoempresa/$',
        inventario_v.DesechoEmpresaListView.as_view(),
        name='desechoempresa_list'
    ),
    # Creacion de salidas de desecho
    url(
        r'^desecho/add/$',
        inventario_v.DesechoSalidaCreateView.as_view(),
        name='desechosalida_add'
    ),
    # Edicion de la salida de desecho
    url(
        r'^desecho/(?P<pk>\d+)/edit/$',
        inventario_v.DesechoSalidaUpdateView.as_view(),
        name='desechosalida_update'
    ),
    # Detalles de la salida de desecho
    url(
        r'^desecho/(?P<pk>\d+)/detail/$',
        inventario_v.DesechoSalidaDetailView.as_view(),
        name='desechosalida_detail'
    ),
]
