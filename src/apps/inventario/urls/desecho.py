from django.conf.urls import url, include
from apps.inventario import views as inventario_v


urlpatterns = [
    # url para la creacion de Desechos
    url(
        r'^desechoempresa/add/$',
        inventario_v.DesechoEmpresaCreateView.as_view(),
        name='desechoempresa_add'
    ),
    # url para detalles de desecho
    url(
        r'^desechoempresa/(?P<pk>\d+)/$',
        inventario_v.DesechoEmpresaDetailView.as_view(),
        name='desechoempresa_detail'
    ),
    # url para listado de desecho
    url(
        r'^desechoempresa/$',
        inventario_v.DesechoEmpresaListView.as_view(),
        name='desechoempresa_list'
    ),
    # url para agregar desechos
    url(
        r'^desecho/add/$',
        inventario_v.DesechoSalidaCreateView.as_view(),
        name='desechosalida_add'
    ),

]
