from rest_framework import routers
from apps.inventario import api_views

router = routers.DefaultRouter()
# ruta de acceso al api de detalles
router.register(
    r'detalles',
    api_views.EntradaDetalleViewSet,
    base_name='api_detalles'
    ),
router.register(
    r'entrada-detalles',
    api_views.EntradaViewSet,
    base_name='api_entrada'
    )
urlpatterns = []
urlpatterns += router.urls
