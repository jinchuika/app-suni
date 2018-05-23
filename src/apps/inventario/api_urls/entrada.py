from rest_framework import routers
from apps.inventario import api_views

router = routers.DefaultRouter()
# ruta de acceso al api de detalles
router.register(
    r'detalles',
    api_views.EntradaDetalleViewSet,
    base_name='api_detalles'
    )
urlpatterns = []
urlpatterns += router.urls
