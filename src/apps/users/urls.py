from django.conf.urls import url, include
from apps.users import views as user_views

urlpatterns = [
    url(r'perfil/$', user_views.CurrentPerfilDetail.as_view(), name='perfil'),
    url(r'login', user_views.UserLogin.as_view(), name='login'),
    url(r'all$', user_views.PerfilList.as_view(), name='perfil_list'),
    url(r'profile/edit/$', user_views.PerfilUpdate.as_view(), name='profile_edit'),

    url(r'^(?P<pk>\d+)/$', user_views.PerfilUpdate.as_view(), name='perfil_detail'),
    url(r'^(?P<pk>\d+)/preferencias$', user_views.PerfilPreferenciasUpdate.as_view(), name='perfil_preferencias'),

    url(r'^(?P<pk>\d+)/update$', user_views.PerfilUpdate.as_view(), name='perfil_update'),
    url(r'^preferences/', include('dynamic_preferences.urls')),
]
