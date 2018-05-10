from django.conf.urls import url
from apps.inventario import views as inventario_v

software_urls = [
    url(
        r'^software/list/$',
        inventario_v.SoftwareListView.as_view(),
        name='software_list'
        ),
    url(
        r'^software/add/$',
        inventario_v.SoftwareCreateView.as_view(),
        name='software_add'
    ),
    url(
        r'^software/(?P<pk>\d+)/detail/$',
        inventario_v.SoftwareDetailView.as_view(),
        name='software_detail'
    ),
    url(
        r'^software/versionsistema/list/$',
        inventario_v.VersionSistemaListView.as_view(),
        name='versionsistema_list'
    ),
    url(
        r'^software/versionsistema/add/$',
        inventario_v.VersionSistemaCreateView.as_view(),
        name='versionsistema_add'
    ),
    url(
        r'^software/versionsistema/(?P<pk>\d+)/detail/$',
        inventario_v.VersionSistemaDetailView.as_view(),
        name='versionsistema_detail'
    )

]
