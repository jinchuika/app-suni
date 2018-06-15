from rest_framework import routers
from apps.inventario import api_views

bodega_routers = routers.DefaultRouter()
# ruta de acceso al api de bodega

bodega_routers.register(
    r'tarima',
    api_views.TarimaViewSet,
    base_name='api_bodega'
)
bodega_routers.register(
    r'sector', api_views.SectorViewSet,
    base_name='api_sector'

)
bodega_urlpatterns = []
bodega_urlpatterns += bodega_routers.urls
