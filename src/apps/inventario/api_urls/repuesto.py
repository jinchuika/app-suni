from rest_framework import routers
from apps.inventario import api_views

repuestos_router = routers.DefaultRouter()
# ruta de acceso al api de repuesto
repuestos_router.register(
    r'repuesto',
    api_views.RepuestoInventarioViewSet,
    base_name='api_repuesto'
)
repuesto_urlpatterns = []
repuesto_urlpatterns += repuestos_router.urls
