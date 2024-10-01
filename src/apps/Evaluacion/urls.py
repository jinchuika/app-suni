from django.conf.urls import url, include
from apps.Evaluacion import views as evaluacion_view

urlpatterns = [
    url(
        r'api/',
        include('apps.Evaluacion.api_urls')),
        
    url(r'^formulario/(?P<formulario_id>\d+)/$',
        evaluacion_view.asignacionPreguntaView.as_view(),
        name='preguntas'),

    url(r'^respuestas/$', 
        evaluacion_view.guardarPreguntas.as_view(),
        name='respuestas_add'),  

    url(r'acceso',
        evaluacion_view.ingresoDPIView.as_view(),
        name='acceso'),

    url(r'finalizado',
        evaluacion_view.FinalizadoView.as_view(),
        name='finalizado'),

    url(r'formulario/add/',
        evaluacion_view.FormularioAdd.as_view(),
        name='formulario_add'),

    url(r'formulario/list/',
        evaluacion_view.FormularioListView.as_view(),
        name='formulario_list'),

    url(r'^formulario/(?P<pk>\d+)/edit/$',
        evaluacion_view.FormularioUpdateView.as_view(),
        name='formulario_edit'),

    #Inicio de Api´s 
    url(
        r'^estadistica/detalle/$',
        evaluacion_view.EstadisticasJson.as_view(),
        name='estadistica_detail'
        ),

    url(
        r'^api/participantes/info/$',
        evaluacion_view.participantesApi.as_view(),
        name='participantes_info'
        ),
    #Fin de Api´s 


    url(r'formulario/(?P<pk>\d+)/detail',
        evaluacion_view.FormularioDetail.as_view(),
        name='formulario_ditail'
        ),

    url(r'informe/$',
        evaluacion_view.EstadisticasInformeApi.as_view(),
        name='api_evaluacion_informe'
        ),
    #Inicio de Informes 
    url(
        r'^informe/estadisticas/$',
        evaluacion_view.InformeEvalaucionesView.as_view(),
        name='informe_estadisticas'
        )
]