from django.conf.urls import url
from apps.informe import views as informe_views


urlpatterns = [
    #  acceso al informe
    url(
        r'^$',
        informe_views.InformeView.as_view(),
        name="informe"
        ),
    url(
        r'^nuevo',
        informe_views.InformeFinalView.as_view(),
        name="informe_nuevo"
        ),
    #  api escuela
    url(
        r'^api/escuela/',
        informe_views.ConsultaEscuelaApi.as_view(),
        name="consulta_escuela"
        ),
    url(
        r'^api/nueva/',
        informe_views.ConsultaEscuelaApiDos.as_view(),
        name="consulta_escuela_2"
        ),

]
