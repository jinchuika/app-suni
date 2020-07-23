from django.conf.urls import url
from apps.coursera import views as coursera_views

urlpatterns = [
    #  acceso a formulario de ingreso de información
    url(
        r'^monitoreo/add/$',
        coursera_views.MonitoreoCreateView.as_view(),
        name='monitoreo_add'),
    # reporte de data
    url(
        r'^monitoreo/informe/$',
        coursera_views.MonitoreoInformeView.as_view(),
        name="informe"
        )
]
