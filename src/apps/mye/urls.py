from django.conf.urls import url
from .views import CooperanteCrear, CooperanteDetalle, CooperanteUpdate

urlpatterns = [
	url(r'^cooperante/add/$', CooperanteCrear.as_view(), name='cooperante_add'),
	url(r'^cooperante/(?P<pk>\d+)/$', CooperanteDetalle.as_view(), name='cooperante_detail'),
	url(r'^cooperante/(?P<pk>\d+)/editar/$', CooperanteUpdate.as_view(), name='cooperante_update'),
]