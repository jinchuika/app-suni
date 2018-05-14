from django.conf.urls import url
from apps.inventario import views as inventario_v

urlpatterns = [
    # Listado de Teclados
    url(
        r'^teclados/list/$',
        inventario_v.SoftwareListView.as_view(),
        name='teclado_detail'
        ),

]
