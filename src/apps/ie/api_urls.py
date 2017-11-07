from apps.ie import api_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'dash-organizacion', api_views.DashOrganizacionViewSet)
router.register(r'dash-laboratorio', api_views.DashLaboratorioViewSet)
router.register(r'dash-geo', api_views.DashGeografiaViewSet, base_name='geo')
router.register(r'dash-escuela', api_views.DashEscuelaViewSet, base_name='escuela')
router.register(r'laboratorio', api_views.LaboratorioViewSet, base_name='laboratorio')
router.register(r'validacion', api_views.IEValidacionViewSet, base_name='validacion')

urlpatterns = router.urls
