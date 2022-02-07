from rest_framework import routers
from apps.recaudacionFondos import api_views

recaudacion_routers = routers.DefaultRouter()

recaudacion_routers.register(
    r'proveedor',
    api_views.ProveedorViewSet,
    base_name='api_proveedor'
),
recaudacion_routers.register(
    r'entradas',
    api_views.EntradaViewSet,
    base_name='api_entradas'
),
recaudacion_routers.register(
    r'articulos',
    api_views.ArticuloViewSet,
    base_name='api_articulo'
),
recaudacion_routers.register(
    r'detallentrada',
    api_views.DetalleEntradaViewSet,
    base_name='api_detalle_entrada'
),
recaudacion_routers.register(
    r'salidas',
    api_views.SalidaViewSet,
    base_name='api_salidas'
),
recaudacion_routers.register(
    r'detallesalida',
    api_views.DetalleSalidaViewSet,
    base_name='api_detalle_salidas'
)
urlpatterns = []
urlpatterns += recaudacion_routers.urls
