from rest_framework import routers
from apps.inventario import api_views

salida_router = routers.DefaultRouter()
# ruta de acceso al api de salidas
salida_router.register(
    r'inventariosalidas',
    api_views.SalidaInventarioViewSet,
    base_name='api_inventariosalidas'
)
salida_router.register(
    r'revisionsalidas',
    api_views.RevisionSalidaViewSet,
    base_name='api_revisionsalidas'
)
salida_urlpatterns = []
salida_urlpatterns += salida_router.urls
