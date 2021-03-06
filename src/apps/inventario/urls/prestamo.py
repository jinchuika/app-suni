from django.conf.urls import url, include
from apps.inventario import views as inventario_v


urlpatterns = [
    # url para la creacion de prestamos
    url(
        r'^prestamo/add/$',
        inventario_v.PrestamoCreateView.as_view(),
        name='prestamo_add'
        ),
    # url para el listado de prestamos
    url(
        r'^prestamo/list/$',
        inventario_v.PrestamoInformeView.as_view(),
        name='prestamo_list'
        ),
    # url para el detalle de prestamos
    url(
        r'^prestamo/(?P<pk>\d+)/detail/$',
        inventario_v.PrestamoDetailView.as_view(),
        name='prestamo_detail'
        ),
    # url para imprimir los detalles  de prestamos
    url(
        r'^prestamo/(?P<pk>\d+)/print/$',
        inventario_v.PrestamoPrintView.as_view(),
        name='prestamo_print'
        ),

]
