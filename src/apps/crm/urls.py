from django.conf.urls import url, include
from apps.crm import views as crm_v

urlpatterns = [
    # Creacion de Donante
    url(
        r'^donante_add/$',
        crm_v.DonanteCreateView.as_view(),
        name='donantes_add'),
    # Detalles de Donante
    url(
        r'^donante_detail/(?P<pk>\d+)/$',
        crm_v.DonanteDetailView.as_view(),
        name='donante_detail'),
    # Actualizacion de los datos del Donantes
    url(
        r'^donante_update/(?P<pk>\d+)/$',
        crm_v.DonanteUpdateView.as_view(),
        name='donante_update'
    ),
    # Creacion de Oferta de los Donantes
    url(
        r'^oferta_add/$',
        crm_v.OfertaCreateView.as_view(),
        name='oferta_add'
    ),
    # Creacion de Contacto para Donantes
    url(
        r'^contacto_add/$',
        crm_v.ContactoCreateView.as_view(),
        name='contacto_add'),
    # Detalle de Contactos
    url(
        r'^contacto_detail/(?P<pk>\d+)/$',
        crm_v.ContactoDetailView.as_view(),
        name='contacto_detail'
    ),
    # Creacion de Telefono
    url(
        r'^telefono_add/$',
        crm_v.TelefonoCreateView.as_view(),
        name='telefono_add'
    ),
    # Creacion de Correo
    url(
        r'^correo_add/$',
        crm_v.CorreoCreateView.as_view(),
        name='correo_add'
    ),
    # Creacion de Historicos
    url(
        r'^historico/add/$',
        crm_v.HistoricoOfertaCrear.as_view(),
        name='historico_add'
    ),
    # Api
    url(r'^api/', include(('apps.crm.api_urls', 'crm'), namespace='crm_api')),
        ]
