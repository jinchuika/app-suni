from django.conf.urls import url
from apps.inventario import views as inventario_v

software_urls = [
    # Listado de software
    url(
        r'^software/list/$',
        inventario_v.SoftwareListView.as_view(),
        name='software_list'
        ),
    # Creacion de nuevo software
    url(
        r'^software/add/$',
        inventario_v.SoftwareCreateView.as_view(),
        name='software_add'
    ),
    # Detalles de software en especifico
    url(
        r'^software/(?P<pk>\d+)/detail/$',
        inventario_v.SoftwareDetailView.as_view(),
        name='software_detail'
    ),
    # Actualizacion de datos de software
    url(
        r'^software/(?P<pk>\d+)/edit/$',
        inventario_v.SoftwareUptadeView.as_view(),
        name='software_update'
    ),
    # Listado de las versioes de sistemas que exiten
    url(
        r'^software/versionsistema/list/$',
        inventario_v.VersionSistemaListView.as_view(),
        name='versionsistema_list'
    ),
    # Creacion de nuevas versiones de sistema
    url(
        r'^software/versionsistema/add/$',
        inventario_v.VersionSistemaCreateView.as_view(),
        name='versionsistema_add'
    ),
    # Detalles de version de sistema en especifico
    url(
        r'^software/versionsistema/(?P<pk>\d+)/detail/$',
        inventario_v.VersionSistemaDetailView.as_view(),
        name='versionsistema_detail'
    ),
    # Actualizacion de version de sistema
    url(
        r'^software/(?P<pk>\d+)/edit/$',
        inventario_v.VersionSistemaUpdateView.as_view(),
        name='software_update'
        )
    ]
