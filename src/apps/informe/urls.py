from django.conf.urls import url
from apps.informe import views as informe_views
from django.views.decorators.cache import cache_page


urlpatterns = [
    #  acceso al informe
    url(
        r'^$',
        cache_page(4)(informe_views.InformeFinalView.as_view()),
        name="informe_nuevo"
        ),
    #informe viejo 
    url(
        r'^nuevo',
        informe_views.InformeView.as_view(),
        name="informe"
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
