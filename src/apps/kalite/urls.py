from django.conf.urls import url
from apps.kalite import views as kalite_views


urlpatterns = [
    url(r'^rubrica/list/$', kalite_views.RubricaListView.as_view(), name='rubrica_list'),
    url(r'^rubrica/add/$', kalite_views.RubricaCreateView.as_view(), name='rubrica_add'),
    url(r'^rubrica/(?P<pk>\d+)/$', kalite_views.RubricaDetailView.as_view(), name='rubrica_detail'),
    url(r'^indicador/add/$', kalite_views.IndicadorCreateView.as_view(), name='indicador_add'),

    url(r'^tipovisita/add/$', kalite_views.TipoVisitaCreateView.as_view(), name='tipovisita_add'),
    url(r'^tipovisita/list/$', kalite_views.TipoVisitaListView.as_view(), name='tipovisita_list'),
    url(r'^visita/(?P<pk>\d+)/$', kalite_views.VisitaDetailView.as_view(), name='visita_detail'),
    url(r'^visita/add/$', kalite_views.VisitaCreateView.as_view(), name='visita_kalite_add'),
    url(r'^visita/informe/$', kalite_views.VisitaInformeView.as_view(), name='visita_kalite_informe'),

    url(r'^calendario/$', kalite_views.VisitaCalendarView.as_view(), name='kalite_calendario'),
]
