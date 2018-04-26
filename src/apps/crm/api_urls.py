from rest_framework import routers
from apps.crm import api_views

router = routers.DefaultRouter()

# Acceso al api de Ofertas
router.register(r'ofertas',
                api_views.OfertaViewSet,
                base_name='ofertas')
urlpatterns = []
urlpatterns += router.urls
