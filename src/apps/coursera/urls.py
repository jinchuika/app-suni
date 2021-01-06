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
        ),
    # carga de excel
    url(
        r'^excel/$',
        coursera_views.CourseraExcelAddView.as_view(),
        name="coursera_excel_add"
        ),
    # informe excel
    url(
        r'^informe/excel/$',
        coursera_views.CourseraListView.as_view(),
        name="coursera_excel_informe"
        ),
  # api
  url(
      r'^informe/$',
      coursera_views.ResultadoCourseraJson.as_view(),
      name="coursera_json_informe"
      ),
   url(
    r'^informe/monitoreo/$',
    coursera_views.ResultadoCourseraMonitoreoJson.as_view(),
    name="coursera_json_informe_monitoreo"
    ),
]
