from django.conf.urls import url
from apps.inventario import views as inv_v

urlpatterns = [
    # Listado de Repuestos
    url(
        r'^repuesto/list/$',
        inv_v.RepuestosAsignacionCreateView.as_view(),
        name='repuesto_list'
    ),
    # Detalles de Repuestos
    url(
        r'^repuesto/(?P<pk>\d+)/$',
        inv_v.RepuestosDetailView.as_view(),
        name='repuesto_detail'
    ),
    # Edicion de Repuestos
    url(
        r'^repuesto/(?P<pk>\d+)/edit/$',
        inv_v.RepuestosUpdateView.as_view(),
        name='repuesto_edit'
    ),
    # Imprimir Qr de RepuestosList
    url(
        r'^repuesto/reporteqr/(?P<pk>\d+)/$',
        inv_v.RepuestosQRprint.as_view(),
        name='repuestoqr_print'
    )
]
