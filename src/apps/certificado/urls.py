from django.conf.urls import url
from apps.certificado import views as certificado_views

urlpatterns = [
    #  acceso al formulario para ingresar el dpi del participante
    url(
        r'^$',
        certificado_views.CertificadoMaestroView.as_view(),
        name="certificado"
        ),
    # acceso a los listado de cursos del participante tiene asignados
    url(
        r'^maestros/$',
        certificado_views.ListadoMaestroView.as_view(),
        name="listado"
        ),  
    # generacion de pdf
    url(
        r'^diplomapdf/$',
        certificado_views.DiplomaPdfView.as_view(),
        name="diplomapdf"
        ),
    # constancia pdf
    url(
        r'^constanciapdf/$',
        certificado_views.ConstanciaPdfView.as_view(),
        name="constanciapdf"
        )
   
]


