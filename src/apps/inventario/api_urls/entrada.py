from rest_framework import routers
from apps.inventario import api_views

entrada_router = routers.DefaultRouter()
# ruta de acceso al api de detalles
entrada_router.register(
    r'detalles',
    api_views.EntradaDetalleViewSet,
    base_name='api_detalles'
    ),
entrada_router.register(
    r'entrada-detalles',
    api_views.EntradaViewSet,
    base_name='api_entrada'
    ),
entrada_urlpatterns = []
entrada_urlpatterns += entrada_router.urls
