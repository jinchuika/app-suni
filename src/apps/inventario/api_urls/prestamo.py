from rest_framework import routers
from apps.inventario import api_views

prestamo_router = routers.DefaultRouter()
# ruta de acceso al api de salidas
prestamo_router.register(
    r'prestamo',
    api_views.PrestamoViewSet,
    base_name='api_prestamo'
)
prestamo_urlpatterns = []
prestamo_urlpatterns += prestamo_router.urls
