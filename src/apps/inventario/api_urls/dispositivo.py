from rest_framework import routers
from apps.inventario import api_views

dispositivo_router = routers.DefaultRouter()
# ruta de acceso al api de Desecho
dispositivo_router.register(
    r'dispositivo',
    api_views.DispositivoViewSet,
    base_name='api_dispositivo'
)
dispositivo_router.register(
    r'paquete',
    api_views.PaquetesViewSet,
    base_name='api_paquete'
)
dispositivo_urlpatterns = []
dispositivo_urlpatterns += dispositivo_router.urls
