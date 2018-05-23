from django.conf.urls import url
from apps.inventario import views as inventario_v

urlpatterns = [
    # Edicion de Teclados
    url(
        r'^teclado/(?P<triage>[\w\d-]+)/edit/$',
        inventario_v.TecladoUpdateView.as_view(),
        name='teclado_update'
        ),
    # Detalles de Teclados
    url(
        r'^teclado/(?P<triage>[\w\d-]+)/$',
        inventario_v.TecladoDetailView.as_view(),
        name='teclado_detail')

]
