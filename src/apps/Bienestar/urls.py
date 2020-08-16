from django.conf.urls import url, include
from apps.Bienestar import views as bienestar_views

urlpatterns = [
    #  acceso al formulario para ingresar el dpi del participante
    url(
        r'^$',
        bienestar_views.CuestionarioView.as_view(),
        name="cuestionario"
        ),
    url(
        r'^resultadobienestar/$',
        bienestar_views.ResultadoBienestarJson.as_view(),
        name="bienestar_json"
        ),
    url(
        r'^resultadobienestarinforme/$',
        bienestar_views.BienestarListView.as_view(),
        name="bienestar_informe"
        ),
    url(
        r'^excel/$',
        bienestar_views.BienestarExcelAddView.as_view(),
        name="bienestar_excel_add"
        ),
    url(
        r'^bienestarinformeapi/$',
        bienestar_views.InformeBienestarJson.as_view(),
        name="bienestar_informe_api"
        ),
    url(
        r'^graficainformeapi/$',
        bienestar_views.GraficasBienestarJson.as_view(),
        name="graficas_informe_api"
        ),
    url(
        r'^lineatiempotodosinformeapi/$',
        bienestar_views.InformeLineaTiempoTodosBienestarJson.as_view(),
        name="linea_tiempo_informe_api"
        ),
    url(
        r'^bienestarinformepieapi/$',
        bienestar_views.InformeBienestarPieJson.as_view(),
        name="api_informe_individual_pie"
        )
     # Api
     #url(r'^api/', include(('apps.Bienestar.api_urls', 'bienestar'), namespace='bienestar_api'))


]
