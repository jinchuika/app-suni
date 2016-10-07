from django.conf.urls import url
from .models import *
from .views import *

urlpatterns = [
url(r'^empresa/$', CreateEmpresa.as_view(), name = 'contacto_empresa'),
url(r'^empresa/(?P<pk>\d)/$', EmpresaDetail.as_view(), name = 'empresa_detail'),
url(r'^empresa/(?P<pk>\d)/etiqueta/(?P<id>[0-9]+)/$', ContactoEtiqueta.as_view(), name='empresa_tag'),
url(r'^evento/', CreateEvento.as_view(), name = 'contacto_evento'),
url(r'^contactos/$', CreateContacto.as_view(), name = 'contacto_contactos'),
url(r'^contactos/etiqueta/(?P<pk>\d+)/$', ContactoEtiqueta.as_view(), name='contacto_etiqueta'),
url(r'^contactos/evento/(?P<pk>\d+)/$', ContactoEvento.as_view(), name='contacto_evento'),

]