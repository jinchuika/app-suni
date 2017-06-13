from django.conf.urls import url
from apps.dh.views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^evento/add/$', EventoDHCreateView.as_view(), name='evento_dh_add'),
    url(r'^evento/(?P<pk>\d+)/$', EventoDHDetailView.as_view(), name='evento_dh_detail'),
    url(r'^evento/(?P<pk>\d+)/edit$', EventoDHUpdateView.as_view(), name='evento_dh_update'),
    url(r'^evento/calendario/home$', cache_page(5)(EventoDHCalendarHomeView.as_view()), name='evento_dh_calendario_home'),

    url(r'^calendario/$', cache_page(5)(CalendarioDHView.as_view()), name='evento_dh_calendario'),
    url(r'^reservaciones/$', ReservacionListView.as_view(), name='dh_reservaciones'),
]
