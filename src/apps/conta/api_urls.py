from rest_framework import routers
from apps.conta import api_views


router = routers.DefaultRouter()

# Acceso al api de Periodo Fiscal
router.register(r'periodofiscal',
                api_views.PeriodoFiscalViewSet,
                base_name='periodofiscal')
# Accesi al api de precio estandar
router.register(r'precioestandar',
                api_views.PrecioEstandarViewSet,
                base_name='precioestandar')

# Accesi al api de periodo fiscal por existencia
router.register(r'periodofiscalinforme',
                api_views.PeriodoFiscalPorExistenciaViewSet,
                base_name='precioestandarexistencia')

urlpatterns = []
urlpatterns += router.urls
