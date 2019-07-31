from rest_framework import routers
from apps.inventario import api_views

dispositivo_router = routers.DefaultRouter()
# ruta de acceso al api de Dispositivos
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
dispositivo_router.register(
    r'dispositivopaquete',
    api_views.DispositivosPaquetesViewSet,
    base_name='api_dispositivopaquete'
)
dispositivo_router.register(
    r'dispositivopaquetedit',
    api_views.DispositivoPaqueteViewset,
    base_name='api_dispositivopaquetedit'
)
dispositivo_router.register(
    r'solicitudmovimientolist',
    api_views.SolicitudMovimientoViewSet,
    base_name='api_solicitudmovimiento'

)
dispositivo_urlpatterns = []
dispositivo_urlpatterns += dispositivo_router.urls
