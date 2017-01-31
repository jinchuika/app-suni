from django.conf.urls import url, include
from apps.users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'perfil/$', user_views.CurrentPerfilDetail.as_view(), name='perfil'),
    url(
        r'password_change/$',
        auth_views.password_change,
        {'template_name': 'users/password_change.html'},
        name='password_change',),
    url(
        r'password_change/done$',
        auth_views.password_change_done,
        {'template_name': 'users/password_change_done.html'},
        name='password_change_done',),
    url(r'password_change/done$', auth_views.password_change_done, name='password_change_done'),

    url(r'login', user_views.UserLogin.as_view(), name='login'),
    url(r'add$', user_views.PerfilCrear.as_view(), name='perfil_add'),
    url(r'all$', user_views.PerfilList.as_view(), name='perfil_list'),

    url(r'^(?P<pk>\d+)/$', user_views.PerfilUpdate.as_view(), name='perfil_detail'),
    url(r'^(?P<pk>\d+)/preferencias$', user_views.PerfilPreferenciasUpdate.as_view(), name='perfil_preferencias'),
    url(r'^preferences/', include('dynamic_preferences.urls')),
]
