from django.conf.urls import url
from apps.inventario import views as inventario_v

urlpatterns = [
    # Salidas de inventario
    url(
        r'^salida/add/$',
        inventario_v.SalidaInventarioCreateView.as_view(),
        name='salidainventario_add'
    )
]
