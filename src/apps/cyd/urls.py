from django.conf.urls import url
from apps.cyd.views import *

urlpatterns = [
    url(r'^curso/add/$', CursoCrear.as_view(), name='curso_add'),
    url(r'^curso/list/$', CursoLista.as_view(), name='curso_list'),
    url(r'^curso/(?P<pk>\d+)/$', CursoDetalle.as_view(), name='curso_detail'),

    url(r'^sede/add/$', SedeCrear.as_view(), name='sede_add'),
    url(r'^sede/list/$', SedeLista.as_view(), name='sede_list'),
    url(r'^sede/(?P<pk>\d+)/$', SedeDetalle.as_view(), name='sede_detail'),
    url(r'^sede/(?P<pk>\d+)/editar$', SedeEditar.as_view(), name='sede_update'),

    url(r'^grupo/add/$', GrupoCrear.as_view(), name='grupo_add'),
]
