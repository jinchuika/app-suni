from django.conf.urls import url, include
from apps.Evaluacion import views as evaluacion_view

urlpatterns = [
    url(
        r'^api/',
        include(('apps.Evaluacion.api_urls', 'Evaluacion'), namespace='evaluacion_api')),
        
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
    
]