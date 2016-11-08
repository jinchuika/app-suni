from django.conf.urls import url
from apps.tpe.views import *

urlpatterns = [
    url(r'^equipamiento/add/$', EquipamientoCrearView.as_view(), name='equipamiento_add'),
    url(r'^equipamiento/(?P<pk>\d+)/$', EquipamientoUpdateView.as_view(), name='equipamiento_update'),

]
