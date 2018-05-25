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
    # Api
    url(r'^api/', include(('apps.inventario.api_urls', 'inventario'), namespace='inventario_api')),

]
