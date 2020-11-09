from django.conf.urls import url, include
from apps.controlNotas.views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
url(r'^notas/$', ControlExcelAddView.as_view(), name='excel_add'),
url(r'^notas/add/$', RegistrosAddView.as_view(), name='registro_add'),
url(
    r'^excel/$',
     RegistrosExcelAddView.as_view(),
    name="impacto_excel_add"
    ),

#api
url(r'^api/alumno/$', ResultadoNotasJson.as_view(), name='alumno_add'),
url(r'^api/visita/$', VisitasAddView.as_view(), name='visita_api_add'),
]
