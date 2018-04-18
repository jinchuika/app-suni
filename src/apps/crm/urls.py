from django.conf.urls import url, include
from apps.crm import views as crm_v

urlpatterns = [
    url(
        r'^Donantes/list/$',
        crm_v.DonanteListView.as_view(),
        name='donantes_list')
        ]
