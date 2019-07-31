from rest_framework import routers
from apps.inventario import api_views

desecho_router = routers.DefaultRouter()
# ruta de acceso al api de Desecho
desecho_router.register(
    r'desechodetalle',
    api_views.DesechoDetalleViewSet,
    base_name='api_desechodetalle'
),
desecho_router.register(
    r'desechodispositivo',
    api_views.DesechoDispositivoViewSet,
    base_name='api_desechodispositivo'
),
desecho_router.register(
    r'desecholist',
    api_views.DesechoSalidaViewSet,
    base_name='api_desecholist'
),
desecho_urlpatterns = []
desecho_urlpatterns += desecho_router.urls
