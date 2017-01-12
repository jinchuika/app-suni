from django.conf.urls import url
from apps.cyd.views import *

urlpatterns = [
    url(r'^curso/add/$', CursoCrear.as_view(), name='curso_add'),
    url(r'^curso/list/$', CursoLista.as_view(), name='curso_list'),
    url(r'^curso/(?P<pk>\d+)/$', CursoDetalle.as_view(), name='curso_detail'),
]
