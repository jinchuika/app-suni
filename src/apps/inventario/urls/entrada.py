from django.conf.urls import url
from apps.inventario import views as inventario_v

urlpatterns = [
    url(
        r'^entrada/add/$',
        inventario_v.EntradaCreateView.as_view(),
        name='entrada_add'
        ),
    url(
        r'^entrada/(?P<pk>\d+)/edit/$',
        inventario_v.EntradaUpdateView.as_view(),
        name='entrada_update'
        )

]
