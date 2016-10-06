from django.conf.urls import url
from .models import Escuela
from .views import *

urlpatterns = [
    url(r'^add/', EscuelaCrear.as_view(), name='escuela_add'),
    url(r'^(?P<pk>\d+)/$', EscuelaDetail.as_view(), name='escuela_detail'),
    url(r'^(?P<pk>\d+)/editar$', EscuelaEditar.as_view(), name='escuela_update'),
    url(r'^(?P<id_escuela>\d+)/contacto/(?P<pk>\d+)/', EscContactoEditar.as_view(), name='escuela_contacto_edit'),
    url(r'^(?P<id_escuela>\d+)/contacto/$', EscContactoCrear.as_view(), name='escuela_contacto_add'),
]
