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

]
