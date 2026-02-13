from django.conf.urls import url, include
from apps.cyd.views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^', include('apps.cyd.api_urls')),
    url(r'^curso/add/$', CursoCreateView.as_view(), name='curso_add'),
    url(r'^curso/list/$', CursoListView.as_view(), name='curso_list'),
    url(r'^curso/(?P<pk>\d+)/$', CursoDetailView.as_view(), name='curso_detail'),
    url(r'^curso/(?P<pk>\d+)/edit/$', CursoUpdateView.as_view(), name='curso_edit'),
    url(r'^curso/api/add/$', CreacionCursosApi.as_view(), name='curso_api_add'),
    url(r'^curso/api/informe/$',InformeCursos.as_view(), name='informe_api_cursos'), 

    url(r'^sede/add/$', SedeCreateView.as_view(), name='sede_add'),
    url(r'^sede/list/$', SedeListView.as_view(), name='sede_list'),
    url(r'^sede/(?P<pk>\d+)/$', SedeDetailView.as_view(), name='sede_detail'),
    url(r'^sede/(?P<pk>\d+)/editar$', SedeUpdateView.as_view(), name='sede_update'),

    url(r'^grupo/add/$', GrupoCreateView.as_view(), name='grupo_add'),
    url(r'^grupo/list/$', GrupoListView.as_view(), name='grupo_list'),
    url(r'^grupo/(?P<pk>\d+)/$', GrupoDetailView.as_view(), name='grupo_detail'),
    url(r'^grupo/asignacion/$', AsignacionWebView.as_view(), name='asignacion_web'),
    url(r'^grupo/grafica/pastel/$', GraficaPastelAprobadosReprobadosHombresMujeres.as_view(), name='grafica_pastel_grupo'),

    url(r'^calendario/$', CalendarioView.as_view(), name='cyd_calendario'),
    url(r'^calendario/list/$', CalendarioListView.as_view(), name='cyd_calendario_list'),
    url(r'^recordatorio/list/$', RecordatorioCalendarioListView.as_view(), name='cyd_recordatorio_list'),

    url(r'^participante/add/$', ParticipanteCreateView.as_view(), name='participante_add'),
    url(r'^participante/(?P<pk>\d+)/edit/$', ParticipanteUpdateView.as_view(), name='participante_add'),
    url(r'^participante/add/a/$', ParticipanteJsonCreateView.as_view(), name='participante_add_ajax'),
    url(r'^participante/(?P<pk>\d+)/$', ParticipanteDetailView.as_view(), name='participante_detail'),
    url(r'^participante/(?P<pk>\d+)/escuelaupdate/$', ParticipanteEscuelaUpdateView.as_view(), name='participante_escuela_update'),
    url(r'^participante/buscar/$', ParticipanteBuscarView.as_view(), name='participante_buscar'),
    url(r'^participante/importar/$', ParticipanteCreateListView.as_view(), name='participante_importar'),
    url(r'^participante/api/naat/$',InformeParticipantesNaat.as_view(), name='informe_participantes_naat'),
    url(r'^participante/api/capacitador/$',InformeParticipanteCapacitador.as_view(), name='participantes_api_capacitador'),
    url(r'^participante/importar/naat/$',ImportarParticipantesNaat.as_view(), name='participantes_importar_naat'),
    
    url(r'^controlacademico/grupo/$', CotrolAcademicoGruposFormView.as_view(), name='control_academico_grupo'),
    url(r'^controlacademico/api/grupo/$', InformeControlAcademicoGrupos.as_view(), name='control_academico_grupo_informe'),
    url(r'^controlacademico/api/asistencia/$', InformeAsistencia.as_view(), name='control_academico_asistencia_informe'),
    url(r'^controlacademico/api/finalizacionproyecto/$', InformeFinal.as_view(), name='informe_final'),
    url(r'^controlacademico/api/capacitadores/$', InformeCapacitadores.as_view(), name='informe_api_capacitador'),
    url(r'^controlacademico/api/grupos/$', InformeGrupo.as_view(), name='informe_api_grupos'),
    url(r'^controlacademico/api/asistencia/periodo/$', InformeAsistenciaPeriodo.as_view(), name='informe_api_asistencia_periodo'),
    url(r'^controlacademico/api/escuela/sede/$',InformeEscuelaSede.as_view(), name='informe_api_escuela_sede'),
    url(r'^controlacademico/api/escuela/lista/$',InformeListadoEscuela2.as_view(), name='informe_api_escuela_lista'),
    url(r'^controlacademico/api/asistencia/agregar/$',InformeListadoEscuela.as_view(), name='asistencia_api_agregar'),
    url(r'^controlacademico/api/sede/escuela/$',InformeListadoSedeEscuela.as_view(), name='informe_api_sede_escuela'),

    url(r'^informe/controlacademico/$', ControlAcademicoInformeListView.as_view() , name='informe_control_academico'),
    url(r'^informe/asistencia/$', AsistenciaInformeListView.as_view(), name='informe_asistencia'),
    url(r'^informe/finalizacionproyecto/$',FinalizacionProcesoInformeListView.as_view(), name='informe_finalizacion_proyecto'),
    url(r'^informe/capacitador/$',InformeCapacitadoresListView.as_view(), name='informe_capacitador'),
    url(r'^informe/escuela/$',InformeEscuelaListView.as_view(), name='informe_escuela'),
    url(r'^informe/escuela/lista/$',InformeEscuelasListadoListView.as_view(), name='informe_escuela_lista'),
    url(r'^informe/grupo/$',InformeGrupoListView.as_view(), name='informe_grupo'),
    url(r'^informe/asistencia/periodos/$',InformeAsistenciaPeriodosListView.as_view(), name='informe_asistencia_periodos'),
    url(r'^informe/escuela/sede/$',InformeEscuelaSedeView.as_view(), name='informe_escuela_sede'),
    url(r'^informe/escuela/capacitadas/$',InformeListadoEscuelasListView.as_view(), name='informe_escuela_capacitadas'),
    url(r'^informe/participante/naat/$',NaatInformeView.as_view(), name='informe_naat'),
    url(r'^informe/escuela/lista/sede/$',InformeEscuelasSedesView.as_view(), name='informe_escuela_sede_lista'), 
    url(r'^informe/cursos/$',InformeCursosView.as_view(), name='informe_cursos'), 
    url(r'^informe/capacitador/participantes/$',InformeCapacitadorParticipanteView.as_view(), name='informe_capacitador_participantes'),
    url(r'^informe/participantes/solo/$',InformeSoloParticipanteView.as_view(), name='informe_solo_participantes'), 
    
    url(r'^asistencia/$',InformeAsistenciaWebView.as_view(), name='asistencia_web'),
    url(r'^asistencia/asignar/$',AsignarAsistencia.as_view(), name='asistencia_web_asignar'),
    url(r'^chamilo/$', ChamiloAddView.as_view(), name='chamilo_add'),
    url(r'^capacitacion/list/home/$', cache_page(5)(CapacitacionListHomeView.as_view()), name='capacitacion_list_home'),

    #conexión con php Naat
    url(r'^naat/facilitador/list$',FacilitadoresList.as_view(), name='facilitadores_list_naat'),
    url(r'^naat/facilitador/add$', CrearFacilitadorView.as_view(), name='facilitador_add_naat'),
]
