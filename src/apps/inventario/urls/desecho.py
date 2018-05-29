from django.conf.urls import url, include
from apps.inventario import views as inventario_v


urlpatterns = [
    # url para la creacion de Desechos
    url(
        r'^desecho/add/$',
        inventario_v.DesechoEmpresaCreateView.as_view(),
        name='desechoempresa_add'
    ),
    # url para detalles de desecho
    url(
        r'^desecho/(?P<pk>\d+)/$',
        inventario_v.DesechoEmpresaDetailView.as_view(),
        name='desechoempresa_detail'
    ),
    # url para listado de desecho
    url(
        r'^desecho/$',
        inventario_v.DesechoEmpresaListView.as_view(),
        name='desechoempresa_list'
    ),

]
