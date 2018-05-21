from rest_framework import routers
from django.conf.urls import url
from apps.tpe import api_views

reparacion_api_list = api_views.TicketReparacionViewSet.as_view({
    'get': 'list'})

monitoreo_api = api_views.MonitoreoViewSet.as_view({
    'get': 'list',
    'post': 'create'})

monitoreo_api_detail = api_views.MonitoreoViewSet.as_view({
    'get': 'retrieve',
    'post': 'update',
    'patch': 'partial_update'})

evaluacionmonitoreo_api = api_views.EvaluacionMonitoreoViewSet.as_view({
    'get': 'list',
    'post': 'update'})
evaluacionmonitoreo_api_detail = api_views.EvaluacionMonitoreoViewSet.as_view({
    'get': 'retrieve',
    'post': 'update',
    'patch': 'partial_update'})

dispositivoreparacion_api = api_views.DispositivoReparacionViewSet.as_view({
    'get': 'list'})

router = routers.DefaultRouter()

# Acceso al api de equipamietno
router.register(r'equipamiento',
                api_views.EquipamientoViewSet,
                base_name='equipamiento')

# Listado de equipamientos
router.register(r'equipamiento-informe',
                api_views.EquipamientoFullViewSet,
                base_name='equipamiento-informe')

# Acceso al api de equipamiento para mostrar en el calendario las fechas
router.register(r'equipamiento-calendar',
                api_views.EquipamientoCalendarViewSet,
                base_name='equipamiento-calendar')

# Acceso al api de evaluacion de monitoreo
router.register(r'evaluacion-monitoreo',
                api_views.EvaluacionMonitoreoFullViewSet,
                base_name='evaluacion-monitoreo')

# Acceso al api de repacion de dispositivo nos muestra la lista de los Dispositivos
router.register(r'dispositivo-reparacion',
                api_views.DispositivoReparacionViewSet,
                base_name='dispositivo-reparacion')

# Acceso a las  visitas de monitoreo que se han hecho para el calendario
router.register(r'visita-monitoreo-calendar',
                api_views.VisitaMonitoreoCalendarViewset,
                base_name='visita-monitoreo-calendar')

# Acceso  para crear los reportes de las visitas de monitoreo
router.register(r'visita-monitoreo',
                api_views.VisitaMonitoreoViewset,
                base_name='visita-monitoreo')

# Acceso  para equipamientos con coordenadas
router.register(r'equipamiento-mapa',
                api_views.EquipamientoMapaViewSet,
                base_name='equipamiento-mapa')

urlpatterns = [
    url(r'^reparacion/list/$',
        reparacion_api_list,
        name='reparacion_api_list'),

    url(r'^monitoreo/$',
        monitoreo_api,
        name='monitoreo_api'),

    url(r'^monitoreo/(?P<pk>\d+)/$',
        monitoreo_api_detail,
        name='monitoreo_api_detail'),

    url(r'^evaluacionmonitoreo/$',
        evaluacionmonitoreo_api,
        name='evaluacionmonitoreo_api'),

    url(r'^evaluacionmonitoreo/(?P<pk>\d+)/$',
        evaluacionmonitoreo_api_detail,
        name='evaluacionmonitoreo_api_detail'),
]

urlpatterns += router.urls
