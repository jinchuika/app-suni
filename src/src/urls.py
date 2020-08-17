from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views import static

urlpatterns = [
    # Acceso a los archivos de media
    url(
        r'^media/(?P<path>.*)$',
        static.serve,
        {'document_root': settings.MEDIA_ROOT}),

    # Contiene las  direcciiones de acceso del los administradores
    url(
        r'^admin/',
        admin.site.urls),

    # Contiene las direcciones de acceso  de ie
    url(
        r'^ie/',
        include('apps.ie.urls')),

    # Contiene las direcciones de acceso a los users
    url(
        r'^users/',
        include('apps.users.urls')),

    # Contiene  las direcciones de acceso  de las escuelas
    url(
        r'^escuela/',
        include('apps.escuela.urls')),

    # Contiene  el acceso al api de la escuela
    url(
        r'^escuela/',
        include('apps.escuela.api_urls')),

    # Contiene las direcciones de acceso del cyd
    url(
        r'^cyd/',
        include('apps.cyd.urls')),

    # Contiene el acceso al api del cyd
    url(
        r'^cyd/',
        include('apps.cyd.api_urls')),

    # Contiene  las direcciones de acceso del crm
    url(
        r'^crm/',
        include('apps.crm.urls')),

    # Contiene las direcciones de acceso  de  kalite
    url(
        r'^kalite/',
        include('apps.kalite.urls')),

    # Contiene el acceso del api de kalite
    url(
        r'^kalite/',
        include('apps.kalite.api_urls')),

    # Contiene las direcciones de acceso a mye
    url(
        r'^mye/',
        include('apps.mye.urls')),

    # Contiene las direcciones de acceso a las cuentas
    url(
        r'^accounts/',
        include('allauth.urls')),

    # Contiene las direcciones  de acceso a contactos
    url(
        r'^contactos/',
        include('apps.fr.urls')),

    # Contiene las direccioes de acceso al  kardez
    url(
        r'^kardex/',
        include('apps.kardex.urls')),

    # Contiene los accesos hacia el api de kardex
    url(
        r'^kardex/',
        include('apps.kardex.api_urls')),

    # Contiene las direcciones de aceso a tpe
    url(
        r'^tpe/',
        include('apps.tpe.urls')),

    # Contiene las direcciones de acceso a dh
    url(
        r'^dh/',
        include('apps.dh.urls')),

    # Contiene las direcciones de acceso a naat
    url(
        r'^naat/',
        include('apps.naat.urls')),

    # Contine las direcciones de aceso al inventario
    url(
        r'^i/',
        include('apps.inventario.urls')),
    # Contiene el acceso  al api del main
    url(
        r'^',
        include('apps.main.api_urls')),

    # Contiene las direcciones de aceso al main
    url(
        r'^$',
        include('apps.main.urls')),

    # Contiene las direcciones de aceso al main
    url(
        r'^conta/',
        include('apps.conta.urls')),
    # Contiene las direcciones de certificado
    url(
        r'^certificado/',
        include('apps.certificado.urls')),
    # Contiene las direcciones de coursera
    url(
        r'^coursera/',
        include('apps.coursera.urls')),
   # Contiene las direcciones de Bienestar
   url(
       r'^bienestar/',
       include('apps.Bienestar.urls')),
]

if settings.DEBUG and settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
