from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views import static

urlpatterns = [
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', admin.site.urls),
    url(r'^ie/', include('apps.ie.urls')),
    url(r'^users/', include('apps.users.urls')),
    url(r'^escuela/', include('apps.escuela.urls')),
    url(r'^escuela/', include('apps.escuela.api_urls')),
    url(r'^cyd/', include('apps.cyd.urls')),
    url(r'^cyd/', include('apps.cyd.api_urls')),
    url(r'^kalite/', include('apps.kalite.urls')),
    url(r'^kalite/', include('apps.kalite.api_urls')),
    url(r'^mye/', include('apps.mye.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^contactos/', include('apps.fr.urls')),
    url(r'^kardex/', include('apps.kardex.urls')),
    url(r'^kardex/', include('apps.kardex.api_urls')),
    url(r'^tpe/', include('apps.tpe.urls')),
    url(r'^dh/', include('apps.dh.urls')),
    url(r'^naat/', include('apps.naat.urls')),
    url(r'^', include('apps.main.api_urls')),
    url(r'^$', include('apps.main.urls')),
]

if settings.DEBUG and settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
