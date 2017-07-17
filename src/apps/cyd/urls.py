from django.conf.urls import url, include
from apps.cyd.views import *


urlpatterns = [
    url(r'^', include('apps.cyd.api_urls')),
    url(r'^curso/add/$', CursoCreateView.as_view(), name='curso_add'),
    url(r'^curso/list/$', CursoListView.as_view(), name='curso_list'),
    url(r'^curso/(?P<pk>\d+)/$', CursoDetailView.as_view(), name='curso_detail'),

    url(r'^sede/add/$', SedeCreateView.as_view(), name='sede_add'),
    url(r'^sede/list/$', SedeListView.as_view(), name='sede_list'),
    url(r'^sede/(?P<pk>\d+)/$', SedeDetailView.as_view(), name='sede_detail'),
    url(r'^sede/(?P<pk>\d+)/editar$', SedeUpdateView.as_view(), name='sede_update'),

    url(r'^grupo/add/$', GrupoCreateView.as_view(), name='grupo_add'),
    url(r'^grupo/list/$', GrupoListView.as_view(), name='grupo_list'),
    url(r'^grupo/(?P<pk>\d+)/$', GrupoDetailView.as_view(), name='grupo_detail'),

    url(r'^calendario/$', CalendarioView.as_view(), name='cyd_calendario'),
    url(r'^calendario/list/$', CalendarioListView.as_view(), name='cyd_calendario_list'),

    url(r'^participante/add/$', ParticipanteCreateView.as_view(), name='participante_add'),
    url(r'^participante/add/a/$', ParticipanteJsonCreateView.as_view(), name='participante_add_ajax'),
    url(r'^participante/(?P<pk>\d+)/$', ParticipanteDetailView.as_view(), name='participante_detail'),

    url(r'^participante/importar/$', ParticipanteCreateListView.as_view(), name='participante_importar'),
]
