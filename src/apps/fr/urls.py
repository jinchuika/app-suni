from django.conf.urls import url
from .models import *
from .views import *

urlpatterns = [
url(r'^empresa/$', CreateEmpresa.as_view(), name = 'contacto_empresa'),
url(r'^empresa/perfil/(?P<empresa_pk>\d)/$', EmpresaDetail.as_view(), name = 'empresa_detail'),
url(r'^empresa/editar/(?P<empresa_pk>\d)/$', EditEmpresa.as_view(), name = 'empresa_edit'),
url(r'^empresa/(?P<empresa_pk>\d)/contacto/$', CreateContactIntoEmpresa.as_view(), name = 'empresa_contacto'),
url(r'^empresa/(?P<empresa_pk>\d)/contacto/(?P<contact_pk>\d)/$', EditContacto.as_view(), name = 'empresa_contacto_edit'),
url(r'^empresa/(?P<empresa_pk>\d)/etiqueta/(?P<tag_pk>\d+)/$', ContactoEtiqueta.as_view(), name='empresa_tag'),
url(r'^empresa/(?P<empresa_pk>\d)/evento/(?P<tag_pk>\d+)/$', ContactoEvento.as_view(), name='empresa_evento'),
url(r'^evento/', CreateEvento.as_view(), name = 'contacto_evento'),
url(r'^$', CreateContacto.as_view(), name = 'contacto_contactos'),
url(r'^etiqueta/(?P<tag_pk>\d+)/$', ContactoEtiqueta.as_view(), name='contacto_etiqueta'),
url(r'^evento/(?P<tag_pk>\d+)/$', ContactoEvento.as_view(), name='contacto_evento'),

]