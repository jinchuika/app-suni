
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
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render
from braces.views import (LoginRequiredMixin, GroupRequiredMixin, JsonRequestResponseMixin, CsrfExemptMixin)
from apps.cyd import forms as cyd_f
from apps.cyd import models as cyd_m
from apps.escuela.models import Escuela
from apps.main.models import Coordenada
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class CursoCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    """ Creacion de cursos desde una vista
    """
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
    """ Detalles de un Curso
    """
    model = cyd_m.Curso
    template_name = 'cyd/curso_detail.html'


class CursoListView(LoginRequiredMixin, ListView):
    """Listado de cursos"""
    model = cyd_m.Curso
    template_name = 'cyd/curso_list.html'


class SedeCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = [u"cyd_admin", u"cyd", u"cyd_capacitador", ]
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
            except ObjectDoesNotExist:
                form.add_error('udi', 'El UDI no es válido o no existe.')
                return self.form_invalid(form)

        return super(SedeCreateView, self).form_valid(form)

class SedeDetailView(LoginRequiredMixin, DetailView):
    """Detalles de una sede en especifico"""
    model = cyd_m.Sede
    template_name = 'cyd/sede_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SedeDetailView, self).get_context_data(**kwargs)
        context['asesoria_form'] = cyd_f.AsesoriaForm(initial={'sede': self.object})
        return context


class SedeUpdateView(LoginRequiredMixin, UpdateView):
    """Actualizacion de Una sede en especifico"""
    model = cyd_m.Sede
    template_name = 'cyd/sede_add.html'
    form_class = cyd_f.SedeForm

    def get_form(self, form_class=None):
        form = super(SedeUpdateView, self).get_form(form_class)
        form.fields['udi'].initial = self.object.escuela_beneficiada.codigo
        # if self.request.user.groups.filter(name="cyd_capacitador").exists():
            # form.fields['capacitador'].queryset = form.fields['capacitador'].queryset.filter(id=self.request.user.id)
        return form

    def get_initial(self):
        initial = super(SedeUpdateView, self).get_initial()
        return initial

    def form_valid(self, form):
        municipio = form.instance.municipio
        udi = form.cleaned_data['udi']
        if udi != "":
            try:
                escuela = Escuela.objects.get(codigo=udi)
                form.instance.nombre = str(municipio.departamento.nombre) + str(", ") + str(municipio.nombre) + str("("+ udi +")") + str("("+ str(form.instance.tipo_sede) + ")")
                form.instance.escuela_beneficiada = escuela
            except ObjectDoesNotExist:
                form.add_error('udi', 'El UDI no es válido o no existe.')
                return self.form_invalid(form)

        return super(SedeUpdateView, self).form_valid(form)

class SedeListView(LoginRequiredMixin, FormView):   
    """Muestra el listado de sedes que se han creado""" 
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
    """Creacion de grupos desde una vista"""    
    group_required = [u"cyd", u"cyd_capacitador", u"cyd_admin", ]   
    redirect_unauthenticated_users = True   
    raise_exception = True  
    model = cyd_m.Grupo 
    template_name = 'cyd/grupo_add.html'    
    form_class = cyd_f.GrupoForm

    def get_success_url(self):
        return reverse('grupo_detail', kwargs={'pk': self.object.id})

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
    """Detalles de un grupo en especifico"""
    model = cyd_m.Grupo
    template_name = 'cyd/grupo_detail.html'

    def get_context_data(self, **kwargs):
        ultimo_grupo= cyd_m.Grupo.objects.filter(sede=self.object.sede,curso=self.object.curso).last()
        context = super(GrupoDetailView, self).get_context_data(**kwargs)
        context['genero_list'] = cyd_m.ParGenero.objects.all()
        context['grupo_list_form'] = cyd_f.GrupoListForm()
        context['grupo_list_form'].fields['grupo'].queryset = cyd_m.Grupo.objects.filter(
            Q(sede=self.object.sede), ~Q(id=self.object.id))
        return context


class GrupoListView(LoginRequiredMixin, GroupRequiredMixin, FormView):
    """Listado de grupos que existen"""
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
    """Calendario donde se muestaran los recordatorios y asesorias"""
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
    """Punto de acceso que regresa un Json para el calendario"""
    def get(self, request, *args, **kwargs):
        print(self.request.GET.get)
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


class RecordatorioCalendarioListView(JsonRequestResponseMixin, View):
    def get(self, request, *args, **kwargs):
        response = []
        calendario_list = cyd_m.RecordatorioCalendario.objects.filter(
            fecha__gte=datetime.strptime(self.request.GET.get('start'), '%Y-%m-%d'),
            fecha__lte=datetime.strptime(self.request.GET.get('end'), '%Y-%m-%d'))
        capacitador = self.request.GET.get('capacitador', False)
        if capacitador:
            calendario_list = calendario_list.filter(capacitador=capacitador)
        for calendario in calendario_list:
            response.append({
                'title': 'Recordatorio  {}'.format(calendario.id),
                'start': '{}'.format(calendario.fecha),
                'end': '{}'.format(calendario.fecha),
                'color': '#ff0000',
                'tipo': 'c',
                'tip_title': '{}-{}'.format(calendario.capacitador.get_full_name(),calendario.fecha),
                'tip_text': calendario.observacion,
                })
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
        context['genero_list'] = cyd_m.ParGenero.objects.all()
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
            if self.request_json['genero'].isdigit():
                genero = cyd_m.ParGenero.objects.get(id=self.request_json['genero'])
            else:
                genero = cyd_m.ParGenero.objects.get(genero=self.request_json['genero'])

            if self.request_json['rol'].isdigit():
                rol = cyd_m.ParRol.objects.get(id=self.request_json['rol'])
            else:
                rol = cyd_m.ParRol.objects.get(nombre=self.request_json['rol'])

            escuela = Escuela.objects.get(codigo=self.request_json['udi'])
            grupo = cyd_m.Grupo.objects.get(id=self.request_json['grupo'])
            etnia = cyd_m.ParEtnia.objects.get(id=self.request_json['etnia'] if 'etnia' in self.request_json else 1)
            escolaridad = cyd_m.ParEscolaridad.objects.get(id=self.request_json['escolaridad'] if 'escolaridad' in self.request_json else 1)

            participante = cyd_m.Participante.objects.create(
                dpi=self.request_json['dpi'],
                nombre=self.request_json['nombre'],
                apellido=self.request_json['apellido'],
                genero=genero,
                rol=rol,
                mail=self.request_json['mail'] if 'mail' in self.request_json else "",
                tel_movil=self.request_json['tel_movil'] if 'tel_movil' in self.request_json else "",
                escuela=escuela,
                slug=self.request_json['dpi'],
                activo=True,
                etnia=etnia,
                escolaridad=escolaridad)
            participante.asignar(grupo)
        except IntegrityError:
            participante = cyd_m.Participante.objects.get(slug=self.request_json['dpi'])

            participante.nombre = self.request_json['nombre']
            participante.apellido = self.request_json['apellido']
            participante.genero = genero
            participante.rol = rol
            participante.mail = self.request_json['mail'] if 'mail' in self.request_json else ""
            participante.tel_movil = self.request_json['tel_movil'] if 'tel_movil' in self.request_json else ""
            participante.escuela = escuela
            participante.save()

            asignacion_existe = cyd_m.Asignacion.objects.filter(participante=participante, grupo=grupo)
            if len(asignacion_existe) == 0:
                asignar_grupo =  cyd_m.Asignacion(
                    participante=participante,
                    grupo=grupo
                )
                asignar_grupo.save()

            error_dict = {u"message": u"Asignado correctamente", u"status": u"ok"}
            #return self.render_bad_request_response(error_dict)
            return self.render_json_response(error_dict)
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

    def get_form(self, form_class=None, **kwargs):
        form = super(ParticipanteBuscarView, self).get_form(form_class)
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            form.fields['sede'].queryset = self.request.user.sedes.filter(activa=True)
        else:
            form.fields['sede'].queryset = cyd_m.Sede.objects.filter(activa=True)
        return form

    def get_context_data(self, **kwargs):
        context = super(ParticipanteBuscarView, self).get_context_data(**kwargs)
        context['asignar_form'] = cyd_f.ParticipanteAsignarForm()

        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            context['asignar_form'].fields['sede'].queryset = self.request.user.sedes.all()
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
        contador =0
        listado_participantes =[]
        listado_asistencia = []
        if self.request.POST['grupo']:
            print("si viene grupo")
            datos = cyd_m.Grupo.objects.filter(id=self.request.POST['grupo'])
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
                    control_academico['grupo'] = str(asignacion.grupo)
                    control_academico['sede'] = str(asignacion.grupo.sede)
                    control_academico['udi'] = asignacion.participante.escuela.codigo
                    control_academico['nombre'] = asignacion.participante.nombre
                    control_academico['apellido'] = asignacion.participante.apellido
                    control_academico['asistencia']= list(nota_asistencia.values('nota'))
                    control_academico['trabajos'] = list(nota_trabajos.values('cr_hito__nombre','nota'))
                    listado_participantes.append(control_academico)
        elif self.request.POST['escuela']:
            print("si viene escuela")
            asignaciones = cyd_m.Asignacion.objects.filter(participante__escuela=self.request.POST['escuela'])
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
                control_academico['grupo'] = str(asignacion.grupo)
                control_academico['sede'] = str(asignacion.grupo.sede)
                control_academico['udi'] = asignacion.participante.escuela.codigo
                control_academico['nombre'] = asignacion.participante.nombre
                control_academico['apellido'] = asignacion.participante.apellido
                control_academico['asistencia']= list(nota_asistencia.values('nota'))
                control_academico['trabajos'] = list(nota_trabajos.values('cr_hito__nombre','nota'))
                listado_participantes.append(control_academico)
        else:
            print("no viene grupo")
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
        try:
            sedes = cyd_m.Sede.objects.filter(capacitador=capacitador,fecha_creacion__date__gte=self.request.POST['fecha_min'],fecha_creacion__date__lte=self.request.POST['fecha_max'])
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
                ##
                escuela_invitada=cyd_m.Asignacion.objects.filter(grupo__sede=sede)
                escuela_invitada.values("participante__escuela").distinct()
                numero_escuelas_invitadas=escuela_invitada.values("participante__escuela").distinct().count()
                if numero_escuelas_invitadas == 0:
                    listado_datos['invitada']=0
                elif numero_escuelas_invitadas ==1:
                    listado_datos['invitada']=1
                else:
                    listado_datos['invitada']=numero_escuelas_invitadas -1
                ##
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
        except MultiValueDictKeyError as e:
            sedes = cyd_m.Sede.objects.filter(capacitador=capacitador)
            asignacion_capacitador= cyd_m.Asignacion.objects.filter(grupo__sede__capacitador=capacitador)
            #print(asignacion_capacitador.values("participante__escuela").distinct())
            for sede in sedes:
                listado_datos={}
                escuela_invitada=cyd_m.Asignacion.objects.filter(grupo__sede=sede)
                escuela_invitada.values("participante__escuela").distinct()
                numero_escuelas_invitadas=escuela_invitada.values("participante__escuela").distinct().count()
                if numero_escuelas_invitadas == 0:
                    listado_datos['invitada']=0
                elif numero_escuelas_invitadas ==1:
                    listado_datos['invitada']=1
                else:
                    listado_datos['invitada']=numero_escuelas_invitadas -1
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

class InformeEscuelaListView(LoginRequiredMixin, FormView):
    template_name = 'cyd/InformeEscuela.html'
    form_class = cyd_f.InformeEscuelaForm

class InformeGrupoListView(LoginRequiredMixin, FormView):
    template_name = 'cyd/InformeGrupo.html'
    form_class = cyd_f.InformeAsistenciaForm


class InformeGrupo(views.APIView):
    def post(self, request):
        listado_grupo=[]
        correlativo=0
        sede = cyd_m.Sede.objects.get(id=self.request.POST['sede'])
        curso = cyd_m.Curso.objects.get(id=self.request.POST['curso'])
        grupos = cyd_m.Grupo.objects.get(id=self.request.POST['grupo'])
        asignaciones=cyd_m.Asignacion.objects.filter(grupo=grupos, grupo__sede=sede, grupo__curso=curso)
        for asignacion in asignaciones:
            datos_grupo={}
            correlativo = correlativo +1
            datos_grupo['Numero']=correlativo
            datos_grupo['Nombre']=asignacion.participante.nombre
            datos_grupo['Apellido']=asignacion.participante.apellido
            datos_grupo['Id']=asignacion.participante.dpi
            datos_grupo['Genero']=asignacion.participante.genero.genero
            datos_grupo['Correo']=asignacion.participante.mail
            datos_grupo['Escuela']=asignacion.participante.escuela.nombre
            datos_grupo['Udi']=asignacion.participante.escuela.codigo
            try:
                datos_grupo['Etnia']=asignacion.participante.etnia.nombre
            except Exception as e:
                datos_grupo['Etnia']="No tiene asignado"

            datos_grupo['Curso']=asignacion.grupo.curso.nombre
            datos_grupo['Grupo']=asignacion.grupo.numero
            datos_grupo['Telefono']=asignacion.participante.tel_movil
            try:
                datos_grupo['Escolaridad']=asignacion.participante.escolaridad.nombre
            except Exception as e:
                datos_grupo['Escolaridad']="No tiene"

            datos_grupo['url']=asignacion.participante.get_absolute_url()
            listado_grupo.append(datos_grupo)
        return Response(
                listado_grupo,
            status=status.HTTP_200_OK
            )

class InformeAsistenciaPeriodosListView(LoginRequiredMixin, FormView):
    template_name = 'cyd/InformeAsistenciaPeriodos.html'
    form_class = cyd_f.InformeAsistenciaPeriodoForm

class InformeAsistenciaPeriodo(views.APIView):
    def post(self, request):
        print("Ingreso aca");
        listado_grupo=[]
        correlativo=0
        sede = cyd_m.Sede.objects.get(id=self.request.POST['sede'])
        grupos = cyd_m.Grupo.objects.get(id=self.request.POST['grupo'])
        try:
            calendario=cyd_m.Calendario.objects.get(id=self.request.POST['asistencia'],grupo=grupos,grupo__sede=sede)
            print(calendario)
        except Exception:
            print("No existen la consulta revise los parametros de busqueda")

        asignaciones=cyd_m.Asignacion.objects.filter(grupo=calendario.grupo)
        for asignacion in asignaciones:
            validacion_asistencia = cyd_m.NotaAsistencia.objects.filter(asignacion=asignacion,gr_calendario=calendario)
            for validar in validacion_asistencia:
                if validar.nota !=0:
                    datos_grupo={}
                    correlativo = correlativo +1
                    datos_grupo['Numero']=correlativo
                    datos_grupo['Nombre']=asignacion.participante.nombre
                    datos_grupo['Apellido']=asignacion.participante.apellido
                    datos_grupo['Escuela']=asignacion.participante.escuela.nombre
                    datos_grupo['url']=asignacion.participante.get_absolute_url()
                    listado_grupo.append(datos_grupo)
        return Response(
                listado_grupo,
            status=status.HTTP_200_OK
            )

class InformeListadoEscuelasListView(LoginRequiredMixin, FormView):
    template_name = 'cyd/InformeListadoEscuelas.html'
    form_class = cyd_f.InformeAsistenciaPeriodoForm

class InformeEscuelasListadoListView(LoginRequiredMixin, FormView):
    template_name = 'cyd/InformeEscuelaListado.html'
    form_class = cyd_f.InformeEscuelalistadoForm

class InformeEscuelaSedeView(LoginRequiredMixin, FormView):
    template_name = 'cyd/InformeEscuelaSede.html'
    form_class = cyd_f.InformeSedeForm



class InformeEscuelaSede(views.APIView):
    def post(self, request):
        listado_grupo=[]
        correlativo=0
        numero_hombres=0
        numero_mujeres=0
        sede = cyd_m.Sede.objects.get(id=self.request.POST['sede'])
        grupo= cyd_m.Grupo.objects.filter(sede=sede)
        asignaciones=cyd_m.Asignacion.objects.filter(grupo__sede=sede)
        escuelas=cyd_m.Asignacion.objects.filter(grupo__sede=sede).values('participante__escuela__nombre','participante__escuela__codigo').distinct()
        for escuela in escuelas:
            datos_grupo={}
            correlativo = correlativo +1
            datos_grupo['Numero']=correlativo
            datos_grupo['Escuela']=escuela['participante__escuela__nombre']
            datos_grupo['Udi']=escuela['participante__escuela__codigo']
            datos_grupo['Url']=Escuela.objects.get(codigo=escuela['participante__escuela__codigo']).get_absolute_url()
            datos=cyd_m.Asignacion.objects.filter(grupo__sede=sede,participante__escuela__nombre=escuela['participante__escuela__nombre'])
            for dato in datos:
                if dato.participante.genero.genero=="Hombre":
                    numero_hombres=numero_hombres+1
                else:
                    numero_mujeres=numero_mujeres+1
            datos_grupo['Hombres']=numero_hombres
            datos_grupo['Mujeres']=numero_mujeres
            datos_grupo['Total']=numero_mujeres+numero_hombres
            numero_hombres=0
            numero_mujeres=0
            listado_grupo.append(datos_grupo)
        return Response(
                listado_grupo,
            status=status.HTTP_200_OK
            )

class InformeListadoEscuela2(views.APIView):
    def post(self, request):
        acumulador_aprobados=0
        listado_escuelas=[]
        contador_fecha=0
        try:
            departamento=self.request.POST['departamento']
        except MultiValueDictKeyError:
            departamento=0
        try:
            municipio=self.request.POST['municipio']
        except MultiValueDictKeyError:
            municipio=0
        try:
            capacitador=self.request.POST['capacitador']
        except MultiValueDictKeyError:
            capacitador=0
        try:
            fecha_min=self.request.POST['fecha_min']
        except MultiValueDictKeyError:
            fecha_min=0
        try:
            fecha_max=self.request.POST['fecha_max']
        except MultiValueDictKeyError:
            fecha_max=0
        if departamento!=0:
            if departamento !=0 and municipio!=0:
                if departamento !=0 and municipio !=0 and capacitador !=0:
                    if departamento !=0 and municipio !=0 and capacitador !=0 and fecha_max!=0 and fecha_min!=0:
                        print("Trae departamento, municipio, capacitador y fechas")
                    else:
                        print("Trae departamento  , municipio y capacitador")
                else:
                    print("Trae departamento y municipio")
            else:
                print("Solo trae departamento")
                escuelas=cyd_m.Participante.objects.filter(escuela__municipio__departamento=departamento).values('escuela__nombre').distinct()
                capacitados=cyd_m.Participante.objects.filter(escuela__municipio__departamento=departamento)
                asignacion=cyd_m.Asignacion.objects.filter(grupo__sede__municipio__departamento=departamento)
                grupos=cyd_m.Grupo.objects.filter(sede__municipio__departamento=departamento)
                for asignados in capacitados:
                    nuevos=cyd_m.Asignacion.objects.filter(participante=asignados, grupo__sede__municipio__departamento=departamento)
                    for grupos in nuevos:
                        datos_escuela={}
                        datos_escuela[str(grupos.participante.escuela.nombre)]=str(grupos.grupo.count_aprobados())
                        listado_escuelas.append(datos_escuela)
                for data in listado_escuelas:
                    for nueva_escuela in escuelas:
                        if nueva_escuela['escuela__nombre'] in data:
                            acumulador_aprobados=acumulador_aprobados + int(list(data.values())[0])

        else:
            if municipio !=0:
                print("Solo trae municipio")
            if capacitador !=0:
                print("Solo trae capacitador")
            #Rango de fechas
            if fecha_min !=0:
                print("Solo trae fecha de inicio")
                contador_fecha=contador_fecha+1
            if fecha_max !=0:
                contador_fecha=contador_fecha+1
                print("Solo trae fecha de final")
            if(contador_fecha==2):
                print("Si trae el rango de fechas")
        return Response(
                listado_escuelas,
            status=status.HTTP_200_OK
            )
class InformeAsistenciaWebView(LoginRequiredMixin, FormView):
    template_name = 'cyd/Asistencia.html'
    form_class = cyd_f.InformeAsistenciaWebForm

class InformeListadoEscuela(views.APIView):
    def post(self, request):
        listado_grupo=[]
        correlativo=0
        try:
            sede = cyd_m.Sede.objects.filter(id=self.request.POST['sede'])
            curso = cyd_m.Curso.objects.filter(id=self.request.POST['curso'])
            grupos = cyd_m.Grupo.objects.filter(id=self.request.POST['grupo'])
            asistencia = cyd_m.Calendario.objects.get(id=self.request.POST['asistencia'],grupo=grupos,grupo__sede=sede,grupo__curso=curso)
        except Exception:
            print("No existen la consulta revise los parametros de busqueda")
        asignaciones=cyd_m.Asignacion.objects.filter(grupo=asistencia.grupo)
        for asignacion in asignaciones:
            validacion_asistencia = cyd_m.NotaAsistencia.objects.filter(asignacion=asignacion,gr_calendario=asistencia)
            for validar in validacion_asistencia:
                datos_grupo={}
                correlativo = correlativo +1
                datos_grupo['Numero']=correlativo
                datos_grupo['Maestro']= str(asignacion.participante.nombre)+str(" ") + str(asignacion.participante.apellido)
                datos_grupo['Asistencia']= validar.nota
                datos_grupo['Id_Asistencia']=validar.id
                datos_grupo['Id_Maestro']=asignacion.participante.id
                if validar.nota !=0:
                    datos_grupo['check']=1
                else:
                    datos_grupo['check']=2
                listado_grupo.append(datos_grupo)
        print(asistencia.grupo)
        return Response(
                listado_grupo,
            status=status.HTTP_200_OK
            )

class AsignarAsistencia(views.APIView):
    def post(self, request):
        if self.request.POST['datos[check]'] == str(1):
            asistencia = cyd_m.NotaAsistencia.objects.get(id=self.request.POST['datos[Id_Asistencia]'])
            asistencia.nota=0
            asistencia.save()
        else:
            asistencia = cyd_m.NotaAsistencia.objects.get(id=self.request.POST['datos[Id_Asistencia]'])
            asistencia.nota=asistencia.gr_calendario.cr_asistencia.punteo_max
            asistencia.save()
        return Response(
                "ingreso",
            status=status.HTTP_200_OK
            )

class AsignacionWebView(LoginRequiredMixin, FormView):
    template_name = 'cyd/asignacion_web.html'
    form_class = cyd_f.AsignacionWebForm

class ChamiloAddView(LoginRequiredMixin, TemplateView):
    template_name = 'cyd/cargar_chamilo.html'
    def post(self,request):
        if request.method == 'POST' and request.FILES['myfile']:
            myfile=request.FILES['myfile']
            fs=FileSystemStorage(location=settings.MEDIA_ROOT_EXCEL)
            filename=fs.save(myfile.name, myfile)
            uploaded_file_url=fs.url(filename)
            return render(request, 'cyd/cargar_chamilo.html',{
                'uploaded_file_url':uploaded_file_url
        })
        return render(request,'cyd/cargar_chamilo.html')

class CreacionCursosApi(views.APIView):
    """Apir para la creacion de cursos"""
    def post(self, request):
        nuevo_curso=cyd_m.Curso(
        nombre=self.request.POST["datos[nombre]"],
        nota_aprobacion=self.request.POST["datos[nota_aprobacion]"],
        porcentaje=self.request.POST["datos[porcentaje]"]
        )
        nuevo_curso.save()
        print(cyd_m.Curso.objects.last())
        try:
            for x in range(int(self.request.POST["cantidad_asistencia"])):
                nueva_asistencia=cyd_m.CrAsistencia(
                    curso=cyd_m.Curso.objects.last(),
                    modulo_num=str(x+1),
                    punteo_max=self.request.POST["datos[asistencias-"+str(x)+"-punteo_max]"]
                )
                nueva_asistencia.save()
                print("modulo:"+str(x+1)+" punteo:"+self.request.POST["datos[asistencias-"+str(x)+"-punteo_max]"])
        except:
            print("Solo llego 1")
        try:
            for x in range(int(self.request.POST["cantidad_hitos"])):
                nuevo_hito=cyd_m.CrHito(
                    curso=cyd_m.Curso.objects.last(),
                    nombre=self.request.POST["datos[hitos-"+str(x)+"-nombre]"],
                    punteo_max=self.request.POST["datos[hitos-"+str(x)+"-punteo_max]"]
                )
                nuevo_hito.save()
                print("Nombre:"+self.request.POST["datos[hitos-"+str(x)+"-nombre]"]+" punteo:"+self.request.POST["datos[hitos-"+str(x)+"-punteo_max]"])
        except:
            print("solo lleva 1 tarea")


        return Response(
                "Curso creado exitosamente",
            status=status.HTTP_200_OK
            )
