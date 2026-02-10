from django.conf.urls import url, include
from apps.crm import views as crm_v

urlpatterns = [
    # Creacion de Donante
    url(
        r'^donante/add/$',
        crm_v.DonanteCreateView.as_view(),
        name='donantes_add'),
    # Detalles de Donante
    url(
        r'^donante/(?P<pk>\d+)/$',
        crm_v.DonanteDetailView.as_view(),
        name='donante_detail'),
    # Actualizacion de los datos del Donantes
    url(
        r'^donante/(?P<pk>\d+)/edit/$',
        crm_v.DonanteUpdateView.as_view(),
        name='donante_edit'
    ),
    # Listado de donantes
    url(
        r'^donante/list/$',
        crm_v.DonanteListView.as_view(),
        name='donante_list'
    ),
    # Creacion de Oferta de los Donantes
    url(
        r'^oferta/add/$',
        crm_v.OfertaCreateView.as_view(),
        name='oferta_add'
    ),
    # Edicion de Donantes
    url(
        r'^oferta/(?P<pk>\d+)/edit/$',
        crm_v.OfertaUpdateView.as_view(),
        name='oferta_edit'
    ),
    # Detalles de  oferta
    url(
        r'^oferta/(?P<pk>\d+)/detail/$',
        crm_v.OfertaDetailView.as_view(),
        name='oferta_detail'
    ),
    # Informe de ofertas
    url(
        r'^oferta/list/$',
        crm_v.OfertaInformeView.as_view(),
        name='oferta_list'
    ),
    # Creacion de Contacto para Donantes
    url(
        r'^contacto/add/$',
        crm_v.ContactoCreateView.as_view(),
        name='contacto_add'),
    # Detalle de Contactos
    url(
        r'^contacto/(?P<pk>\d+)/detail/$',
        crm_v.ContactoDetailView.as_view(),
        name='contacto_detail'
    ),
    # Creacion de Telefono
    url(
        r'^telefono/add/$',
        crm_v.TelefonoCreateView.as_view(),
        name='telefono_add'
    ),
    # Creacion de Correo
    url(
        r'^correo/add/$',
        crm_v.CorreoCreateView.as_view(),
        name='correo_add'
    ),
    # Creacion de Historicos
    url(
        r'^historico/add/$',
        crm_v.HistoricoOfertaCrear.as_view(),
        name='historico_add'
    ),
    url(
        r'^informe/proveedores/$',
        crm_v.InformeDonanteView.as_view(),
        name='informe_gastos'
    ),
    url(
        r'^api/proveedor/gastos$',
        crm_v.DonantesGastosInformeApi.as_view(),
        name='api_gastos_proveedor'
    ),
    # Api
    url(r'^api/', include(('apps.crm.api_urls', 'crm'), namespace='crm_api')),
        ]
