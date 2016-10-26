from django.conf.urls import url
from apps.cyd.views import *

urlpatterns = [
    url(r'^curso/add$', CursoCrear.as_view(), name='curso_add'),
]
