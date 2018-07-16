from rest_framework import routers
from apps.inventario import api_views

salida_router = routers.DefaultRouter()
salida_router.register(
    r'inventariosalidas',
    api_views.SalidaInventarioViewSet,
    base_name='api_inventariosalidas'
)
salida_urlpatterns = []
salida_urlpatterns += salida_router.urls
