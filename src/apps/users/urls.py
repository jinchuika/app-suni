from django.conf.urls import url, include
from django.contrib import admin
from apps.users import views as user_views
from django.views import(
	static
	)
urlpatterns = [
    url(r'login', user_views.UserLogin.as_view(), name='login'),
    url(r'all$', user_views.PerfilList.as_view(), name='perfil_list'),
    url(r'profile/edit/$', user_views.PerfilUpdate.as_view(), name='profile_edit'),
    url(r'profile/$', user_views.current_profile_redirect, name='profile'),
    
    url(r'^(?P<pk>\d+)/$', user_views.PerfilUpdate.as_view(), name='perfil_detail'),
    url(r'^(?P<pk>\d+)/preferencias$', user_views.PerfilPreferenciasUpdate.as_view(), name='perfil_preferencias'),
    
    url(r'^(?P<pk>\d+)/update$', user_views.PerfilUpdate.as_view(), name='perfil_update'),
    url(r'^$', user_views.index, name='index_user'),
    url(r'^preferences/', include('dynamic_preferences.urls')),
]