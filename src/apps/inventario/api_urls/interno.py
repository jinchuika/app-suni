from rest_framework import routers
from apps.inventario import api_views
from django.conf.urls import url

interno_router = routers.DefaultRouter()
# ruta de acceso al api de salidas
interno_router.register(
    r'inventariointerno',
    api_views.InventarioInternoViewSet,
    base_name='api_inventariointerno'
)
interno_router.register(
    r'asignacion',
    api_views.IInternoDispositivoViewSet,
    base_name='api_dispositivos_asignacion'
)
interno_router.register(
    r'usuarios',
    api_views.UsuarioListView,
    base_name='api_usuarios'
)
interno_urlpatterns = []
interno_urlpatterns += interno_router.urls