from django import forms
from datetime import datetime
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.messages.views import SuccessMessageMixin
from rest_framework import views,status
from rest_framework.response import Response

from braces.views import (LoginRequiredMixin, GroupRequiredMixin, JsonRequestResponseMixin, CsrfExemptMixin)

from apps.cyd import forms as cyd_f
from apps.cyd import models as cyd_m
from apps.escuela.models import Escuela
from apps.main.models import Coordenada
from django.contrib.auth.models import User


class CursoCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = [u"cyd_admin", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = cyd_m.Curso
    template_name = 'cyd/curso_add.html'
    form_class = cyd_f.CursoForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        hito_formset = cyd_f.CrHitoFormSet()
        asistencia_formset = cyd_f.CrAsistenciaFormSet()
        return self.render_to_response(
            self.get_context_data(
                forrm=form,
                hito_formset=hito_formset,
                asistencia_formset=asistencia_formset))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        hito_formset = cyd_f.CrHitoFormSet(self.request.POST)
        asistencia_formset = cyd_f.CrAsistenciaFormSet(self.request.POST)
        if form.is_valid() and hito_formset.is_valid() and asistencia_formset.is_valid():
            return self.form_valid(form, formset_list=(hito_formset, asistencia_formset))
        else:
            return self.form_invalid(form, formset_list=(hito_formset, asistencia_formset))

    def form_valid(self, form, **kwargs):
        self.object = form.save()
        for formset in kwargs['formset_list']:
            formset.instance = self.object
            formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, **kwargs):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                hito_formset=kwargs['formset_list'][0],
                asistencia_formset=kwargs['formset_list'][1]))

class CursoDetailView(LoginRequiredMixin, DetailView):
    model = cyd_m.Curso
    template_name = 'cyd/curso_detail.html'


class CursoListView(LoginRequiredMixin, ListView):
    model = cyd_m.Curso
    template_name = 'cyd/curso_list.html'


class SedeCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = [u"cyd_admin", u"cyd", u"cyd_capacitador"]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = cyd_m.Sede
    form_class = cyd_f.SedeForm
    template_name = 'cyd/sede_add.html'

    def form_valid(self, form):
        form.instance.capacitador = self.request.user 
        form.instance.fecha_creacion = datetime.now()

        municipio = form.instance.municipio
        udi = form.cleaned_data['udi']
        if udi != "":
            try:
                escuela = Escuela.objects.get(codigo=udi)
                form.instance.nombre = str(municipio.departamento.nombre) + str(", ") + str(municipio.nombre) + str("("+ udi +")") + str("("+ str(form.instance.tipo_sede) + ")")
                form.instance.escuela_beneficiada = escuela
                form.instance.mapa = escuela.mapa
            except ObjectDoesNotExist:
                form.add_error('udi', 'El UDI no es válido o no existe.')
                return self.form_invalid(form)

        return super(SedeCreateView, self).form_valid(form)

class SedeDetailView(LoginRequiredMixin, DetailView):
    model = cyd_m.Sede
    template_name = 'cyd/sede_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SedeDetailView, self).get_context_data(**kwargs)
        context['asesoria_form'] = cyd_f.AsesoriaForm(initial={'sede': self.object})
        return context


class SedeUpdateView(LoginRequiredMixin, UpdateView):
    model = cyd_m.Sede
    template_name = 'cyd/sede_add.html'
    form_class = cyd_f.SedeForm

    def get_form(self, form_class=None):
        form = super(SedeUpdateView, self).get_form(form_class)
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            form.fields['capacitador'].queryset = form.fields['capacitador'].queryset.filter(id=self.request.user.id)
        return form

    def get_initial(self):
        initial = super(SedeUpdateView, self).get_initial()
        initial['lat'] = self.object.mapa.lat
        initial['lng'] = self.object.mapa.lng
        return initial

    def form_valid(self, form):
        respuesta = form.save(commit=False)
        if self.object.mapa is None:
            coordenada = Coordenada(
                lat=form.cleaned_data['lat'],
                lng=form.cleaned_data['lng'],
                descripcion='De la sede ' + respuesta.nombre)
            coordenada.save()
            self.object.mapa = coordenada
        else:
            self.object.mapa.lat = form.cleaned_data['lat']
            self.object.mapa.lng = form.cleaned_data['lng']
            self.object.mapa.save()
        return super(SedeUpdateView, self).form_valid(form) 


class SedeListView(LoginRequiredMixin, FormView):
    model = cyd_m.Sede
    template_name = 'cyd/sede_list.html'
    form_class = cyd_f.SedeFilterFormInforme
    group_required = [u"cyd_capacitador", u"cyd_admin"]

    def get_form(self, form_class=None):
        form = super(SedeListView, self).get_form(form_class)
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            form.fields['capacitador'].widget = forms.HiddenInput()
        return form

    def get_queryset(self):
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            return cyd_m.Sede.objects.filter(capacitador=self.request.user)
        else:
            return cyd_m.Sede.objects.all()


class GrupoCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = [u"cyd", u"cyd_capacitador", u"cyd_admin", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = cyd_m.Grupo
    template_name = 'cyd/grupo_add.html'
    form_class = cyd_f.GrupoForm

    def get_form(self, form_class=None):
        form = super(GrupoCreateView, self).get_form(form_class)
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            form.fields['sede'].queryset = cyd_m.Sede.objects.filter(capacitador=self.request.user)
        return form

    def form_valid(self, form):
        grupo = form.save()
        for asistencia in grupo.curso.asistencias.all():
            grupo.asistencias.create(cr_asistencia=asistencia)
        return super(GrupoCreateView, self).form_valid(form)


class GrupoDetailView(LoginRequiredMixin, DetailView):
    model = cyd_m.Grupo
    template_name = 'cyd/grupo_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GrupoDetailView, self).get_context_data(**kwargs)
        context['genero_list'] = cyd_m.ParGenero.objects.all()
        context['grupo_list_form'] = cyd_f.GrupoListForm()
        context['grupo_list_form'].fields['grupo'].queryset = cyd_m.Grupo.objects.filter(
            Q(sede=self.object.sede), ~Q(id=self.object.id))
        return context


class GrupoListView(LoginRequiredMixin, GroupRequiredMixin, FormView):
    group_required = [u"cyd", u"cyd_capacitador", u"cyd_admin", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = cyd_m.Grupo
    template_name = 'cyd/grupo_list.html'
    ordering = ['-sede', '-id']
    form_class = cyd_f.GrupoFilterFormInforme

    def get_form(self, form_class=None):
        form = super(GrupoListView, self).get_form(form_class)
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            form.fields['capacitador'].widget = forms.HiddenInput()
            form.fields['capacitador'].label = ''
            form.fields['sede'].queryset = self.request.user.sedes.filter(activa=True)
        return form

    def get_queryset(self):
        queryset = super(GrupoListView, self).get_queryset()
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            queryset = queryset.filter(sede__capacitador=self.request.user)
        return queryset


class CalendarioView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    group_required = [u"cyd", u"cyd_capacitador", u"cyd_admin", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    template_name = 'cyd/calendario.html'

    def get_context_data(self, **kwargs):
        context = super(CalendarioView, self).get_context_data(**kwargs)
        context['sede_form'] = cyd_f.SedeFilterForm()
        context['nueva_form'] = cyd_f.CalendarioFilterForm()
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            capacitador_qs = context['sede_form'].fields['capacitador'].queryset
            context['nueva_form'].fields['sede'].queryset = self.request.user.sedes.all()
            context['sede_form'].fields['capacitador'].queryset = capacitador_qs.filter(id=self.request.user.id)
            context['sede_form'].fields['sede'].queryset = self.request.user.sedes.all()
        return context


class CalendarioListView(JsonRequestResponseMixin, View):
    def get(self, request, *args, **kwargs):
        response = []
        calendario_list = cyd_m.Calendario.objects.filter(
            fecha__gte=datetime.strptime(self.request.GET.get('start'), '%Y-%m-%d'),
            fecha__lte=datetime.strptime(self.request.GET.get('end'), '%Y-%m-%d'))
        capacitador = self.request.GET.get('capacitador', False)
        if capacitador:
            calendario_list = calendario_list.filter(grupo__sede__capacitador__id=capacitador)
        sede = self.request.GET.get('sede', False)
        if sede:
            calendario_list = calendario_list.filter(grupo__sede__id=sede)
        for calendario in calendario_list:
            response.append({
                'title': 'Grupo {}'.format(calendario.grupo.numero),
                'start': '{} {}'.format(calendario.fecha, calendario.hora_inicio),
                'end': '{} {}'.format(calendario.fecha, calendario.hora_fin),
                'color': calendario.grupo.sede.capacitador.perfil.color,
                'tipo': 'c',
                'tip_title': '{}'.format(calendario.grupo.curso),
                'tip_text': 'Grupo {}, asistencia {} en la sede {}'.format(
                    calendario.grupo.numero,
                    calendario.cr_asistencia.modulo_num,
                    calendario.grupo.sede),
                '_id': '{}'.format(calendario.id),
                '_url': reverse('calendario_api_detail', kwargs={'pk': calendario.id})})
        return self.render_json_response(response)


class ParticipanteCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = [u"cyd", u"cyd_capacitador", u"cyd_admin", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = cyd_m.Participante
    template_name = 'cyd/participante_add.html'
    form_class = cyd_f.ParticipanteForm

    def get_form(self, form_class=None):
        form = super(ParticipanteCreateView, self).get_form(form_class)
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            form.fields['sede'].queryset = self.request.user.sedes.all()
        return form


class ParticipanteCreateListView(LoginRequiredMixin, GroupRequiredMixin, FormView):
    group_required = [u"cyd", u"cyd_capacitador", u"cyd_admin", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = cyd_m.Participante
    template_name = 'cyd/participante_importar.html'
    #form_class = cyd_f.ParticipanteBaseForm
    form_class = cyd_f.ParticipanteFormList

    def get_context_data(self, **kwargs):
        context = super(ParticipanteCreateListView, self).get_context_data(**kwargs)
        context['rol_list'] = cyd_m.ParRol.objects.all()
        return context

    def get_form(self, form_class=None):
        form = super(ParticipanteCreateListView, self).get_form(form_class)
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            form.fields['sede'].queryset = self.request.user.sedes.all()
        return form


class ParticipanteJsonCreateView(LoginRequiredMixin, JsonRequestResponseMixin, CreateView):
    require_json = True
    model = cyd_m.Participante
    form_class = cyd_f.ParticipanteForm

    def post(self, request, *args, **kwargs):
        try:
            if self.request_json['genero'] == 'M':
                id_genero = 1
            else:
                id_genero = 2
            escuela = Escuela.objects.get(codigo=self.request_json['udi'])
            grupo = cyd_m.Grupo.objects.get(id=self.request_json['grupo'])
            rol = cyd_m.ParRol.objects.get(id=self.request_json['rol'])
            genero = cyd_m.ParGenero.objects.get(id=id_genero)
            participante = cyd_m.Participante.objects.create(
                dpi=self.request_json['dpi'],
                nombre=self.request_json['nombre'],
                apellido=self.request_json['apellido'],
                genero=genero,
                rol=rol,
                mail=self.request_json['mail'],
                tel_movil=self.request_json['tel_movil'],
                escuela=escuela,
                slug=self.request_json['dpi'])
            participante.asignar(grupo)
        except IntegrityError:
            error_dict = {u"message": u"El dpi ya existe "}
            return self.render_bad_request_response(error_dict)
        return self.render_json_response({'status': 'ok'})


class ParticipanteDetailView(LoginRequiredMixin, DetailView):
    model = cyd_m.Participante
    template_name = 'cyd/participante_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ParticipanteDetailView, self).get_context_data(**kwargs)
        context['rol_list'] = cyd_m.ParRol.objects.all()
        context['etnia_list'] = cyd_m.ParEtnia.objects.all()
        context['escolaridad_list'] = cyd_m.ParEscolaridad.objects.all()
        context['genero_list'] = cyd_m.ParGenero.objects.all()
        return context


class ParticipanteEscuelaUpdateView(LoginRequiredMixin, JsonRequestResponseMixin, View):
    """Para modificar la escuela a la que pertenece un participante.
    Recibe el código UDI de la escuela y actualiza el ID en el registro del participante.
    El único método admitido por esta vista es PATCH, para realizar una actualización parcial.
    """
    def patch(self, request, *args, **kwargs):
        try:
            escuela = Escuela.objects.get(codigo=self.request_json['udi'])
            participante = cyd_m.Participante.objects.get(id=self.kwargs['pk'])
            participante.escuela = escuela
            participante.save()
        except Exception:
            error_dict = {u"message": u"Error. Verifique que el UDI sea correcto."}
            return self.render_bad_request_response(error_dict)
        return self.render_json_response({'status': 'ok'})


class ParticipanteBuscarView(LoginRequiredMixin, JsonRequestResponseMixin, FormView):
    form_class = cyd_f.ParticipanteBuscarForm
    template_name = 'cyd/participante_buscar.html'

    def get_form(self, form_class=None):
        form = super(ParticipanteBuscarView, self).get_form(form_class)
        form.fields['sede'].queryset = cyd_m.Sede.objects.all()
        return form

    def get_context_data(self, **kwargs):
        context = super(ParticipanteBuscarView, self).get_context_data(**kwargs)
        context['asignar_form'] = cyd_f.ParticipanteAsignarForm()

        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            #context['asignar_form'].fields['sede'].queryset = self.request.user.sedes.all()
            context['asignar_form'].fields['sede'].queryset = cyd_m.Sede.objects.all()
        return context

class ParticipanteUpdateView(LoginRequiredMixin, UpdateView):
    model = cyd_m.Participante
    template_name = 'cyd/participante_edit.html'
    form_class = cyd_f.ParticipanteForm


class CursoUpdateView(LoginRequiredMixin, UpdateView):
    model = cyd_m.Curso
    template_name = 'cyd/curso_edit.html'
    form_class = cyd_f.CursoForm


class CotrolAcademicoGruposFormView(LoginRequiredMixin, FormView):
    template_name = 'cyd/control_academico_grupo.html'
    form_class = cyd_f.ControlAcademicoGrupoForm

class InformeControlAcademicoGrupos(views.APIView):
    def post(self, request):
        datos = cyd_m.Grupo.objects.filter(id=self.request.POST['grupo'])
        contador =0
        listado_participantes =[]
        listado_asistencia = []
        for  data in datos:
            asignaciones = cyd_m.Asignacion.objects.filter(grupo=data.id)
            for asignacion in asignaciones:
                contador=contador+1
                nota_asistencia = cyd_m.NotaAsistencia.objects.filter(asignacion=asignacion)
                nota_trabajos  =  cyd_m.NotaHito.objects.filter(asignacion=asignacion)
                control_academico ={}
                control_academico['numero'] = contador
                control_academico['asignacion'] = asignacion.id
                control_academico['dpi'] = asignacion.participante.dpi
                control_academico['genero'] = asignacion.participante.genero.genero
                control_academico['curso'] = asignacion.grupo.curso.nombre
                control_academico['grupo'] = asignacion.grupo.id
                control_academico['udi'] = asignacion.participante.escuela.codigo
                control_academico['nombre'] = asignacion.participante.nombre
                control_academico['apellido'] = asignacion.participante.apellido
                control_academico['asistencia']= list(nota_asistencia.values('nota'))
                control_academico['trabajos'] = list(nota_trabajos.values('cr_hito__nombre','nota'))
                listado_participantes.append(control_academico)
        return Response(listado_participantes

            )

class InformeAsistencia(views.APIView):
    def post(self, request):
        listado_asistencia = []
        contador = 0
        contador_asistencia = 0
        total_asistencia = 0
        contador_inasistencia = 0
        listado_datos=[]
        try:
            sede = cyd_m.Sede.objects.filter(id=self.request.POST['sede'])
            curso = cyd_m.Curso.objects.filter(id=self.request.POST['curso'])
            grupos = cyd_m.Grupo.objects.filter(sede=sede, curso=curso)
            asistencia = cyd_m.CrAsistencia.objects.filter(curso=curso)
        except Exception:
            grupos=cyd_m.Grupo.objects.filter(id=self.request.POST['grupo'])
        for grupo in grupos:
            listado_grupos ={}
            listado_grupos['grupo'] = grupo.sede.nombre
            participantes = cyd_m.Asignacion.objects.filter(grupo=grupo)
            for participante in participantes:
                notas = cyd_m.NotaAsistencia.objects.filter(asignacion=participante)
            for x in range(1, notas.count()+1):
                data = cyd_m.NotaAsistencia.objects.filter(gr_calendario__cr_asistencia__modulo_num=x, asignacion__grupo=grupo, nota__gte=1)
                data2 = cyd_m.NotaAsistencia.objects.filter(gr_calendario__cr_asistencia__modulo_num=x, asignacion__grupo=grupo, nota=0)
                fecha =  cyd_m.Calendario.objects.filter(cr_asistencia__modulo_num=x,grupo=grupo)
                fecha_mostrar = fecha.values('fecha','hora_inicio','hora_fin')
                listado_grupos['asistencia'+str(x)] = data.count()
                listado_grupos['inacistencia'+str(x)]= data2.count()
                listado_grupos['fecha_asistencia'+str(x)]= fecha_mostrar[0]['fecha']
                listado_grupos['hora_inicio_asistencia'+str(x)]=fecha_mostrar[0]['hora_inicio']
                listado_grupos['hora_fin_asistencia'+str(x)]=fecha_mostrar[0]['hora_fin']
            listado_grupos['cantidad_asistencia']=notas.count()
            listado_datos.append(listado_grupos)
        return Response(
                listado_datos,
            status=status.HTTP_200_OK
            )

class ControlAcademicoInformeListView(LoginRequiredMixin, FormView):
    template_name = 'cyd/ControlAcademicoInforme.html'
    form_class = cyd_f.ControlAcademicoGrupoForm

class AsistenciaInformeListView(LoginRequiredMixin, FormView):
    template_name = 'cyd/AsistenciaInforme.html'
    form_class = cyd_f.InformeAsistenciaForm

class FinalizacionProcesoInformeListView(LoginRequiredMixin, FormView):
    template_name = 'cyd/FinalizacionProyectoInforme.html'
    form_class = cyd_f.InformeAsistenciaFinalForm

class InformeFinal(views.APIView):
    def post(self, request):
        listado_datos=[]
        listado_datos2={}
        sede = cyd_m.Sede.objects.get(id=self.request.POST['sede'])
        curso = cyd_m.Curso.objects.get(id=self.request.POST['curso'])
        grupos = cyd_m.Grupo.objects.filter(sede=sede, curso=curso)
        asistencia = cyd_m.CrAsistencia.objects.filter(curso=curso)
        total_maestros=cyd_m.Asignacion.objects.filter(grupo__sede=sede,participante__rol=1).count()
        total_hombre=cyd_m.Asignacion.objects.filter(grupo__sede=sede,participante__genero__id=1).count()
        total_mujeres=cyd_m.Asignacion.objects.filter(grupo__sede=sede,participante__genero__id=2).count()
        maestros_aprobados= grupos.first().count_aprobados()
        maestros_reprobados= total_maestros - grupos.first().count_aprobados()
        maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede=sede,abandono=True).count()    
        listado_datos2['capacitador']= grupos.first().sede.capacitador.get_full_name()
        listado_datos2['sede']= sede.nombre
        listado_datos2['curso']= curso.nombre
        listado_datos2['total_maestro']=total_maestros
        listado_datos2['total_hombre']=total_hombre
        listado_datos2['total_mujeres']=total_mujeres
        listado_datos2['maestros_aprobados']=maestros_aprobados
        listado_datos2['maestros_reprobados']=maestros_reprobados
        listado_datos2['maestros_desertores']=maestros_desertores
        listado_datos.append(listado_datos2)
        return Response(
                listado_datos,
            status=status.HTTP_200_OK
            )
class InformeCapacitadoresListView(LoginRequiredMixin, FormView):
    template_name = 'cyd/InformeCapacitadores.html'
    form_class = cyd_f.InformeCapacitadorForm


class InformeCapacitadores(views.APIView):
    def post(self, request):
        listado_sede=[]
        listado_curso=[]
        contador_sede=0
        capacitador = User.objects.get(id=self.request.POST['capacitador'])
        sedes = cyd_m.Sede.objects.filter(capacitador=capacitador)
        asignacion_capacitador= cyd_m.Asignacion.objects.filter(grupo__sede__capacitador=capacitador)
        for sede in sedes:
            listado_datos={}
            contador_sede = contador_sede +1
            listado_datos['numero']=contador_sede
            listado_datos['sede']=sede.nombre
            contado_participantes=0
            contador_curso=0
            grupos=cyd_m.Grupo.objects.filter(sede=sede)
            listado_datos['grupos']=grupos.count()
            for asignacion in grupos:
                listado_curso.append(asignacion.curso)
                contado_participantes = contado_participantes + cyd_m.Asignacion.objects.filter(grupo=asignacion).distinct().count()
                contado_asignacion = contado_participantes + cyd_m.Asignacion.objects.filter(grupo=asignacion).count()
            listado_curso=list(dict.fromkeys(listado_curso))
            for cantida in listado_curso:
                contador_curso=contador_curso+1
            listado_curso=[]
            listado_datos['participantes']=contado_participantes
            listado_datos['asignaciones']=contado_asignacion
            listado_datos['curso']=contador_curso
            listado_sede.append(listado_datos)
        return Response(
                listado_sede,
            status=status.HTTP_200_OK
            )

class CapacitacionListHomeView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request, *args, **kwargs):
        today = datetime.now()
        capacitacion_list = {'escuelas': [], 'sedes': []}
        for i in range(1, 13):
            if self.request.user.groups.filter(name="cyd_capacitador").exists():
                sedes_list = self.request.user.sedes.filter(
                    grupos__asistencias__fecha__year=today.year,
                    grupos__asistencias__fecha__month=i)
            else:
                sedes_list = cyd_m.Sede.objects.filter(
                    grupos__asistencias__fecha__year=today.year,
                    grupos__asistencias__fecha__month=i)

            capacitacion_list['sedes'].append(sedes_list.count())
            capacitacion_list['escuelas'].append(sum(e.get_escuelas().count() for e in sedes_list))

        return self.render_json_response(capacitacion_list)