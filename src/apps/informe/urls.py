from django.conf.urls import url
from apps.informe import views as informe_views


urlpatterns = [
    #  acceso al informe
    url(
        r'^$',
        informe_views.InformeView.as_view(),
        name="informe"
        ),
    #  api escuela
    url(
        r'^api/escuela',
        informe_views.ConsultaEscuelaApi.as_view(),
        name="consulta_escuela"
        )
]
