from django.conf.urls import url, include
from apps.inventario import views as inv_v

urlpatterns = [
    # Listado de Tarimas
    url(
        r'^tarima/list/$',
        inv_v.TarimaListView.as_view(),
        name='tarima_list'
        ),
    # Agregar Tarima
    url(
        r'^tarima/add/$',
        inv_v.TarimaCrearCreateView.as_view(),
        name='tarima_add'
        ),
    # Actualizar Tarima
    url(
        r'^tarima/update/(?P<pk>\d+)$',
        inv_v.TarimaActualizarUpdateView.as_view(),
        name='tarima_update'
        ),


    # Listado de Sectores
    url(
        r'^sector/list/$',
        inv_v.SectoreListarListView.as_view(),
        name='sector_list'
        ),
    # Agregar Sector
    url(
        r'^sector/add/$',
        inv_v.SectorCrearCreateView.as_view(),
        name='sector_add'
        ),
    # Actualizar Sector
    url(
        r'^sector/(?P<pk>\d+)/update/$',
        inv_v.SectorActualizarUpdateView.as_view(),
        name='sector_update'
        ),


    # Listado de Niveles
    url(
        r'^nivel/list/$',
        inv_v.NivelListarListView.as_view(),
        name='nivel_list'
        ),
    # Agregar Nivel
    url(
        r'^nivel/add/$',
        inv_v.NivelCrearCreateView.as_view(),
        name='nivel_add'
        ),
    # Actualizar Nivel
    url(
        r'^nivel/update/(?P<pk>\d+)$',
        inv_v.NivelActualizarUpdateView.as_view(),
        name='nivel_update'
        ),


    # Listado de Pasillos
    url(
        r'^pasillo/list/$',
        inv_v.PasilloListView.as_view(),
        name='pasillo_list'
        ),
    # Agregar Pasillo
    url(
        r'^pasillo/add/$',
        inv_v.PasilloCrearCreateView.as_view(),
        name='pasillo_add'
        ),
    # Actualizar Pasillo
    url(
        r'^pasillo/update/(?P<pk>\d+)$',
        inv_v.PasilloActualizarUpdateView.as_view(),
        name='pasillo_update'
        ),
    #  Detalles de Sector
    url(
        r'^sector/(?P<pk>\d+)/$',
        inv_v.SectorDetailView.as_view(),
        name='sector_detail'
        ),
    #  informe de bodega
    url(
        r'^informe/resumebodega/$',
        inv_v.BodegaResumenInformeListView.as_view(),
        name='bodega_informe_resumen'
        ),
    #  imprimi informe de bodega
    url(
        r'^informe/resumebodega/print/$',
        inv_v.BodegaResumenInformePrintView.as_view(),
        name='bodega_informe_resumen_print'
        ),
]
