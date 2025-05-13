
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
from apps.main import creacion_filtros_informe as crear_dict
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models import Sum, Count
from django.utils import timezone
from django.db import connection
from openpyxl import load_workbook
from apps.Evaluacion.models import Formulario
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
                #form.instance.nombre = str(municipio.departamento.nombre) + str(", ") + str(municipio.nombre) + str("("+ udi +")") + str("("+ str(form.instance.tipo_sede) + ")")
                form.instance.nombre = str(municipio.departamento.nombre) + str(", ") + str(municipio.nombre) + str("("+ udi +")") + str("("+")")
                #form.instance.nombre = str(municipio.departamento.nombre) + str(", ") + str(municipio.nombre) + str("("+ udi +")") + str("("+escuela.nombre+")")
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
        total_chicos = 0
        total_chicas = 0        
        for data in self.object.get_participantes()['listado']:
            total_chicos = total_chicos + data['participante'].chicos
            total_chicas = total_chicas + data['participante'].chicas       
        context['total_chicos'] = total_chicos
        context['total_chicas'] = total_chicas

        formulario = Formulario.objects.filter(sede__id=self.object.id).last()
        context['formulario'] = formulario

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
            form.fields['sede'].queryset = cyd_m.Sede.objects.filter(capacitador=self.request.user, activa=True)
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
        context['grupo_list_form'].fields['grupo'].queryset = cyd_m.Grupo.objects.filter(Q(sede=self.object.sede),~Q(id=self.object.id), cyd_grupo_creado_por=self.request.user )
        """context['grupo_list_form'].fields['grupo'].queryset = cyd_m.Grupo.objects.filter(
            Q(sede=self.object.sede), ~Q(id=self.object.id),  cyd_grupo_creado_por=self.request.user)"""
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
        response = []
        calendario_list = cyd_m.Calendario.objects.filter(
            fecha__gte=datetime.strptime(self.request.GET.get('start'), '%Y-%m-%d'),
            fecha__lte=datetime.strptime(self.request.GET.get('end'), '%Y-%m-%d'))
        calendario_sedes = cyd_m.Sede.objects.filter(fecha_creacion__gte=datetime.strptime(self.request.GET.get('start'), '%Y-%m-%d'),
            fecha_creacion__lte=datetime.strptime(self.request.GET.get('end'), '%Y-%m-%d'))        
        capacitador = self.request.GET.get('capacitador', False)
        if capacitador:
            calendario_list = calendario_list.filter(grupo__sede__capacitador__id=capacitador)
        else:
            if "cyd_admin" in self.request.user.groups.values_list('name', flat=True):
                 calendario_list = calendario_sedes
            else:
                calendario_list = calendario_list.filter(grupo__sede__capacitador__id=self.request.user.id) 
        sede = self.request.GET.get('sede', False)
        if sede:
            calendario_list = calendario_list.filter(grupo__sede__id=sede)
        for calendario in calendario_list:
             if "cyd_admin" in self.request.user.groups.values_list('name', flat=True):                 
                 response.append({
                    'title': calendario.escuela_beneficiada.nombre,
                    'start': calendario.fecha_creacion.date(),
                    'end': calendario.fecha_creacion.date(),
                    'color': calendario.capacitador.perfil.color,
                    'tipo': 'c',
                    'tip_title': '{},{}'.format(calendario.nombre,calendario.capacitador.get_full_name()),
                    'tip_text': 'Escuela: {} \nDireccion:{} \nCodigo {}' .format(calendario.escuela_beneficiada.nombre,calendario.escuela_beneficiada.direccion,calendario.escuela_beneficiada.codigo),
                    '_id': '{}'.format(calendario.id),
                    '_url':calendario.get_absolute_url()})                
             else:
                 response.append({
                    'title': 'Grupo {}'.format(calendario.grupo),
                    'start': '{} {}'.format(calendario.fecha, calendario.hora_inicio),
                    'end': '{} {}'.format(calendario.fecha, calendario.hora_fin),
                    'color': calendario.grupo.sede.capacitador.perfil.color,
                    'tipo': 'c',
                    'tip_title': '{},{}'.format(calendario.grupo.curso,calendario.grupo.sede.capacitador.get_full_name()),
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
        else:
            if "cyd_admin" in self.request.user.groups.values_list('name', flat=True):
                 calendario_list = calendario_list
            else:
                calendario_list = calendario_list.filter(capacitador__id=self.request.user.id)
        for calendario in calendario_list:
            response.append({
                'id':calendario.id,
                'title': 'Recordatorio  {}'.format(calendario.id),
                'start': '{}'.format(calendario.fecha),
                'end': '{}'.format(calendario.fecha),
                'color': '#ff0000',
                'tipo': 'c',
                'tip_title': '{}-{}'.format(calendario.capacitador.get_full_name(),calendario.fecha),
                'tip_text': calendario.observacion,
                'evento':'r',
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
        context['escolaridad_list'] = cyd_m.ParEscolaridad.objects.all()
        context['etnia_list'] = cyd_m.ParEtnia.objects.all()
        context['profesion_list'] = cyd_m.Profesion.objects.all()
        context['grado_list'] = cyd_m.Grado.objects.all()        
        return context

    def get_form(self, form_class=None):
        form = super(ParticipanteCreateListView, self).get_form(form_class)
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            #form.fields['sede'].queryset = self.request.user.sedes.all()
            form.fields['sede'].queryset = self.request.user.sedes.filter(activa=True,finalizada=False)
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
            try:
                etnia = cyd_m.ParEtnia.objects.get(nombre=self.request_json['etnia'] if 'etnia' in self.request_json else "Ladino")
            except Exception as e:
                etnia = cyd_m.ParEtnia.objects.get(id=int(self.request_json['etnia']) if 'etnia' in self.request_json else 1)
            try:
                escolaridad = cyd_m.ParEscolaridad.objects.get(nombre=self.request_json['escolaridad'] if 'escolaridad' in self.request_json else "Basico")
            except Exception as e:
                escolaridad = cyd_m.ParEscolaridad.objects.get(id=self.request_json['escolaridad'] if 'escolaridad' in self.request_json else 1)
            try:
                profesion = cyd_m.Profesion.objects.get(nombre=self.request_json['profesion'] if 'profesion' in self.request_json else "Otros")
            except:
                profesion = cyd_m.Profesion.objects.get(id=self.request_json['profesion'] if 'profesion' in self.request_json else 1)
            try:
                grado_imparte =cyd_m.Grado.objects.get(grado_asignado =self.request_json['grado_impartido'] if 'grado_impartido' in self.request_json else "Preprimaria")
            except:
                 grado_imparte =cyd_m.Grado.objects.get(id=self.request_json['grado_impartido'] if 'grado_impartido' in self.request_json else 1)

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
                profesion=profesion,
                grado_impartido=grado_imparte,
                chicos=self.request_json['chicos'],
                chicas=self.request_json['chicas'],
                escolaridad=escolaridad,                
                cyd_participante_creado_por = self.request.user)            
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
            participante.activo=True
            participante.etnia=etnia,
            participante.profesion=profesion
            participante.grado_impartido=grado_imparte
            participante.chicos=self.request_json['chicos']
            participante.chicas=self.request_json['chicas']
            participante.escolaridad=escolaridad
            participante.cyd_participante_creado_por = self.request.user
            participante.save()

            asignacion_existe = cyd_m.Asignacion.objects.filter(participante=participante, grupo=grupo)
            if len(asignacion_existe) == 0:
                asignar_grupo =  cyd_m.Asignacion(
                    participante=participante,
                    grupo=grupo,
                    cyd_asignacion_creado_por = self.request.user
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
            form.fields['sede'].queryset = self.request.user.sedes.filter(activa=True,finalizada=False)            
        else:
            form.fields['sede'].queryset = cyd_m.Sede.objects.filter(activa=True,finalizada=False)           
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

    def get_form_kwargs(self, **kwargs):
        kwargs = super(CotrolAcademicoGruposFormView, self).get_form_kwargs()
        kwargs.update({'user':self.request.user}) 
        return kwargs
  
    

class InformeControlAcademicoGrupos(views.APIView):
    def post(self, request):
        contador =0
        listado_participantes =[]
        listado_asistencia = []
        try:
            if self.request.POST['grupo']:
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
                        control_academico['finalizada'] = asignacion.grupo.sede.finalizada
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
        except KeyError:
            print("Trae mas")
            asignaciones = cyd_m.Asignacion.objects.filter(participante__escuela__codigo=self.request.POST['udi'])
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
            escuela = self.request.POST['udi']
        except MultiValueDictKeyError:
            escuela =None       
        try:
            sede = cyd_m.Sede.objects.filter(id=self.request.POST['sede'],activa=True)
            curso = cyd_m.Curso.objects.filter(id=self.request.POST['curso'])
            grupos = cyd_m.Grupo.objects.filter(sede=sede, curso=curso)
            asistencia = cyd_m.CrAsistencia.objects.filter(curso=curso)
        except Exception:
           
            if escuela:
                grupos=cyd_m.Grupo.objects.filter(sede__escuela_beneficiada__codigo=escuela)
            else:
                 grupos=cyd_m.Grupo.objects.filter(id=self.request.POST['grupo'])        
        for grupo in grupos:
            listado_grupos ={}
            listado_grupos['grupo'] = grupo.sede.nombre
            listado_grupos['grupo_url'] = grupo.get_absolute_url()
            listado_grupos['curso']= grupo.curso.nombre
            participantes = cyd_m.Asignacion.objects.filter(grupo=grupo)
            for participante in participantes:
                notas = cyd_m.NotaAsistencia.objects.filter(asignacion=participante)            
            for x in range(1, notas.count()+1):
                data = cyd_m.NotaAsistencia.objects.filter(gr_calendario__cr_asistencia__modulo_num=x, asignacion__grupo=grupo, nota__gte=1)
                data2 = cyd_m.NotaAsistencia.objects.filter(gr_calendario__cr_asistencia__modulo_num=x, asignacion__grupo=grupo, nota=0)
                fecha =  cyd_m.Calendario.objects.filter(cr_asistencia__modulo_num=x,grupo=grupo)
                fecha_mostrar = fecha.values('fecha','hora_inicio','hora_fin')
                try:                
                    listado_grupos['asistencia'+str(x)] = data.count()
                    listado_grupos['inacistencia'+str(x)]= data2.count()
                    listado_grupos['fecha_asistencia'+str(x)]= fecha_mostrar[0]['fecha']
                    listado_grupos['hora_inicio_asistencia'+str(x)]=fecha_mostrar[0]['hora_inicio']
                    listado_grupos['hora_fin_asistencia'+str(x)]=fecha_mostrar[0]['hora_fin']                    
                except:
                    listado_grupos['asistencia'+str(x)] = data.count()
                    listado_grupos['inacistencia'+str(x)]= data2.count()
                    listado_grupos['fecha_asistencia'+str(x)]= "No tiene"
                    listado_grupos['hora_inicio_asistencia'+str(x)]="No tiene"
                    listado_grupos['hora_fin_asistencia'+str(x)]="No tiene"                    

            listado_grupos['cantidad_asistencia']=notas.count()
            listado_datos.append(listado_grupos)
        return Response(
                listado_datos,
            status=status.HTTP_200_OK
            )

class ControlAcademicoInformeListView(LoginRequiredMixin, FormView):
    template_name = 'cyd/ControlAcademicoInforme.html'
    form_class = cyd_f.ControlAcademicoGrupoForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ControlAcademicoInformeListView, self).get_form_kwargs()
        kwargs.update({'user':self.request.user})  
        return kwargs

class AsistenciaInformeListView(LoginRequiredMixin, FormView):
    template_name = 'cyd/AsistenciaInforme.html'
    form_class = cyd_f.InformeAsistenciaForm

class FinalizacionProcesoInformeListView(LoginRequiredMixin, FormView):
    template_name = 'cyd/FinalizacionProyectoInforme.html'
    form_class = cyd_f.InformeAsistenciaFinalForm

class InformeFinal(views.APIView):
    """informe final de proyectos 
    """
    def post(self, request):
        listado_datos=[]
        listado_datos2={}
        try:
            escuela = self.request.POST['udi']
        except MultiValueDictKeyError:
            escuela =None
        if escuela:
            sede= cyd_m.Sede.objects.filter(escuela_beneficiada__codigo=escuela).first()
            curso = cyd_m.Curso.objects.get(id=self.request.POST['curso'])
            #print("Aca esta  para la nueva funcion de escuela")
        else:
            sede = cyd_m.Sede.objects.get(id=self.request.POST['sede'],activa=True)
            curso = cyd_m.Curso.objects.get(id=self.request.POST['curso'])
        grupos = cyd_m.Grupo.objects.filter(sede=sede, curso=curso)
        asistencia = cyd_m.CrAsistencia.objects.filter(curso=curso)        
        #total_maestros=cyd_m.Asignacion.objects.filter(grupo__sede=sede,participante__rol=4).count()
        #total_directores=cyd_m.Asignacion.objects.filter(grupo__sede=sede,participante__rol=5).count()
        #total_hombre=cyd_m.Asignacion.objects.filter(grupo__sede=sede,participante__genero__id=1).count()
        #total_mujeres=cyd_m.Asignacion.objects.filter(grupo__sede=sede,participante__genero__id=2).count()
        #maestros_aprobados= grupos.first().count_aprobados()
        #maestros_reprobados= total_maestros - grupos.first().count_aprobados()
        total_maestros = 0
        total_hombres  = 0
        total_mujeres = 0
        maestros_aprobados = 0
        maestros_reprobados = 0
        for data_grupos in grupos:
            total_maestros = total_maestros + data_grupos.get_hombres() + data_grupos.get_mujeres()
            total_hombres = total_hombres + data_grupos.get_hombres()
            total_mujeres = total_mujeres + data_grupos.get_mujeres()
            maestros_aprobados = maestros_aprobados + data_grupos.count_aprobados()
            maestros_reprobados = maestros_reprobados +  data_grupos.count_reprobados()            
        maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede=sede,abandono=True).count() 
        listado_datos2['capacitador']= grupos.first().sede.capacitador.get_full_name()
        listado_datos2['sede']= sede.nombre
        listado_datos2['sede_url']= sede.get_absolute_url()
        listado_datos2['curso']= curso.nombre
        listado_datos2['grupo_url']= grupos.first().get_absolute_url()       
        listado_datos2['total_maestro']=total_maestros        
        listado_datos2['total_hombre']=total_hombres
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
        #capacitador = User.objects.get(id=self.request.POST['capacitador'])
        si_es_naat =False
        try:
            capacitador = self.request.POST['capacitador']
        except MultiValueDictKeyError:
            capacitador =0
        try:
            fecha_min = self.request.POST['fecha_min']
        except MultiValueDictKeyError:
            fecha_min =0
        try:
            fecha_max = self.request.POST['fecha_max']
        except MultiValueDictKeyError:
            fecha_max = 0
        sort_params = {}
        crear_dic(sort_params,'capacitador',capacitador)
        crear_dic(sort_params,'fecha_creacion__gte',fecha_min)
        crear_dic(sort_params,'fecha_creacion__lte',fecha_max)
        crear_dic(sort_params,'activa',True)
        try:
            print("Sin errores")
            #sedes = cyd_m.Sede.objects.filter(capacitador=capacitador,fecha_creacion__gte=self.request.POST['fecha_min'],fecha_creacion__lte=self.request.POST['fecha_max'],activa=True)
            sedes = cyd_m.Sede.objects.filter(**sort_params)
            asignacion_capacitador= cyd_m.Asignacion.objects.filter(grupo__sede__capacitador=capacitador)
            for sede in sedes:
                total_chicos = 0
                total_chicas = 0
                contador_participantes_invitados=0    
                total_participantes = sede.get_participantes()["resumen"]['genero'].aggregate(Sum('cantidad'))
                for data_participante in sede.get_participantes()['listado']:                   
                    if data_participante['invitado'] =="Si":
                        contador_participantes_invitados = contador_participantes_invitados + 1
                    total_chicos = total_chicos + data_participante["participante"].chicos
                    total_chicas = total_chicas + data_participante["participante"].chicas
                
                listado_datos={}
                contador_sede = contador_sede +1
                listado_datos['numero']=contador_sede
                listado_datos['sede']=sede.nombre
                listado_datos['sede_url']=sede.get_absolute_url()
                listado_datos["chicos"]=total_chicos
                listado_datos["chicas"]=total_chicas
                contado_participantes=0
                contador_curso=0
                contado_asignacion =0
                grupos=cyd_m.Grupo.objects.filter(sede=sede)
                listado_datos['grupos']=grupos.count()
                ##
                escuela_invitada=cyd_m.Asignacion.objects.filter(grupo__sede=sede)                
                escuela_invitada.values("participante__escuela").distinct()
                es_naat = escuela_invitada.values("grupo__curso__nombre").distinct()
                for data_naat in es_naat:
                    if "NAAT" in data_naat["grupo__curso__nombre"]:                        
                        si_es_naat = True
                    else:
                        si_es_naat = False
                numero_escuelas_invitadas=escuela_invitada.values("participante__escuela").distinct().count()                          
                if not si_es_naat:
                    #print(sede.get_escuelas_invitadas())
                    if sede.get_escuelas_invitadas().count()==1:
                        listado_datos['invitada'] = sede.get_escuelas_invitadas().count()
                    else:
                        listado_datos['invitada'] = 0

                    """if numero_escuelas_invitadas == 0:
                        listado_datos['invitada']=0
                    elif numero_escuelas_invitadas ==1:                                          
                            listado_datos['invitada']=1
                    else:
                        listado_datos['invitada']=numero_escuelas_invitadas -1"""
                else:
                     listado_datos['invitada']=0
                ##                
                for asignacion in grupos:                                      
                    listado_curso.append(asignacion.curso)                  
                    contado_participantes = contado_participantes + cyd_m.Asignacion.objects.filter(grupo=asignacion).distinct().count()
                    contado_asignacion = contado_asignacion + cyd_m.Asignacion.objects.filter(grupo=asignacion).count()
                listado_curso=list(dict.fromkeys(listado_curso))
                for cantida in listado_curso:
                    contador_curso=contador_curso+1
                listado_curso=[]
                listado_datos['participantes'] = total_participantes['cantidad__sum']
                listado_datos['asignaciones']=contado_asignacion
                listado_datos['curso']=contador_curso
                listado_datos['fecha'] = sede.fecha_creacion.year
                listado_datos["participantes_invitados"]=contador_participantes_invitados
                listado_sede.append(listado_datos)
        except MultiValueDictKeyError as e:
            print("Trae errores")           
            sedes = cyd_m.Sede.objects.filter(capacitador=capacitador,activa=True)
            asignacion_capacitador= cyd_m.Asignacion.objects.filter(grupo__sede__capacitador=capacitador)           
            for sede in sedes:
                total_chicos = 0
                total_chicas = 0
                contador_participantes_invitados =0                
                for data_participante in sede.get_participantes()['listado']:
                    if data_participante['invitado'] =="Si":
                        contador_participantes_invitados = contador_participantes_invitados + 1
                    total_chicos = total_chicos + data_participante["participante"].chicos
                    total_chicas = total_chicas + data_participante["participante"].chicas                
                total_participantes = sede.get_participantes()["resumen"]['genero'].aggregate(Sum('cantidad'))
                listado_datos={}
                escuela_invitada=cyd_m.Asignacion.objects.filter(grupo__sede=sede)
                escuela_invitada.values("participante__escuela").distinct()
                es_naat = escuela_invitada.values("grupo__curso__nombre").distinct()
                for data_naat in es_naat:
                    if "NAAT" in data_naat["grupo__curso__nombre"]:                        
                        si_es_naat = True
                    else:
                        si_es_naat = False
                numero_escuelas_invitadas=escuela_invitada.values("participante__escuela").distinct().count()
                if not si_es_naat:
                    listado_datos['invitada'] = sede.get_escuelas_invitadas()
                    contador_invitadas = contador_invitadas = sede.get_escuelas_invitadas()
                    """if numero_escuelas_invitadas == 0:
                        listado_datos['invitada']=0
                    elif numero_escuelas_invitadas ==1:
                        listado_datos['invitada']=1
                    else:
                        listado_datos['invitada']=numero_escuelas_invitadas -1"""
                else:
                     listado_datos['invitada']=0
                contador_sede = contador_sede +1
                listado_datos["chicos"]=total_chicos
                listado_datos["chicas"]=total_chicas
                listado_datos["participantes_invitados"]=contador_participantes_invitados
                listado_datos['numero']=contador_sede
                listado_datos['sede']=sede.nombre
                listado_datos['sede_url']=sede.get_absolute_url()
                contado_participantes=0
                contador_curso=0
                contado_asignacion =0
                grupos=cyd_m.Grupo.objects.filter(sede=sede)
                listado_datos['grupos']=grupos.count()
                for asignacion in grupos:
                    listado_curso.append(asignacion.curso)
                    contado_participantes = contado_participantes + cyd_m.Asignacion.objects.filter(grupo=asignacion).distinct().count()
                    contado_asignacion = contado_asignacion + cyd_m.Asignacion.objects.filter(grupo=asignacion).count()
                listado_curso=list(dict.fromkeys(listado_curso))
                for cantida in listado_curso:
                    contador_curso=contador_curso+1
                listado_curso=[]
                listado_datos['participantes']=total_participantes['cantidad__sum']
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
        capacitacion_list = {'escuelas': [], 'sedes': [],'invitadas': []}        
        contador_sedes= 0
        contador_escuelas = 0
        contador_escuelas_invitadas=0        
        for i in range(1,(today.month)+1):
            if self.request.user.groups.filter(name="cyd_capacitador").exists():
                 sedes_sql = "SELECT id FROM  cyd_sede WHERE(YEAR(fecha_creacion)={year} AND MONTH(fecha_creacion)={mes}) AND activa=1 AND capacitador_id={capacitador}".format(year=today.year,mes=i,capacitador=self.request.user.id)
            else:
                sedes_sql = "SELECT id FROM  cyd_sede WHERE(YEAR(fecha_creacion)={year} AND MONTH(fecha_creacion)={mes}) AND activa=1".format(year=today.year,mes=i)                
            with connection.cursor() as cursor:
                    cursor.execute(sedes_sql)
                    result =cursor.fetchall()                
            for data in result:
                contador_sedes = contador_sedes + 1
                sede_list = cyd_m.Sede.objects.get(id=data[0])
                contador_escuelas = contador_escuelas + sede_list.get_escuelas().count()
                contador_escuelas_invitadas = contador_escuelas_invitadas + sede_list.get_escuelas_invitadas().count()                
            capacitacion_list['sedes'].append(contador_sedes)
            capacitacion_list['escuelas'].append(contador_escuelas)
            capacitacion_list['invitadas'].append(contador_escuelas_invitadas)
            contador_sedes = 0
            contador_escuelas = 0
            contador_escuelas_invitadas =0
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
        sede = cyd_m.Sede.objects.get(id=self.request.POST['sede'],activa=True)
        curso = cyd_m.Curso.objects.get(id=self.request.POST['curso'])
        grupos = cyd_m.Grupo.objects.get(id=self.request.POST['grupo'])        
        #asignaciones=cyd_m.Asignacion.objects.filter(grupo=grupos,grupo__sede=sede,grupo__curso=curso)
        asignaciones=cyd_m.Asignacion.objects.filter(grupo__id=grupos.id,grupo__curso__id=curso.id)
        #asignaciones=cyd_m.Asignacion.objects.filter(grupo__sede__id=sede.id, grupo__curso__id=curso.id)        
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
        listado_grupo=[]
        correlativo=0
        
        try:
            sede = cyd_m.Sede.objects.get(id=self.request.POST['sede'],activa=True)
            grupos = cyd_m.Grupo.objects.get(id=self.request.POST['grupo'])
            calendario=cyd_m.Calendario.objects.get(id=self.request.POST['asistencia'],grupo=grupos,grupo__sede=sede)
           
        except Exception:
            calendario=cyd_m.Calendario.objects.get(id=self.request.POST['asistencia'],grupo__sede__escuela_beneficiada__codigo=self.request.POST['udi'])
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
        sede = cyd_m.Sede.objects.get(id=self.request.POST['sede'],activa=True)
        udi_beneficiada =  sede.escuela_beneficiada.codigo
        grupo= cyd_m.Grupo.objects.filter(sede=sede).first()
        asignaciones=cyd_m.Asignacion.objects.filter(grupo__sede=sede)
        escuelas=cyd_m.Asignacion.objects.filter(grupo__sede=sede).values('participante__escuela__nombre','participante__escuela__codigo').distinct()      
        for escuela in escuelas:            
            datos_grupo={}
            correlativo = correlativo +1
            if udi_beneficiada == escuela['participante__escuela__codigo']:
                datos_grupo['Beneficiada']=True
            else:
                datos_grupo['Beneficiada']=False
            datos_grupo['Numero']=correlativo
            datos_grupo['Escuela']=escuela['participante__escuela__nombre']
            datos_grupo['Udi']=escuela['participante__escuela__codigo']
            datos_grupo['Url']=Escuela.objects.get(codigo=escuela['participante__escuela__codigo']).get_absolute_url()
            if grupo.sede.escuela_beneficiada.codigo == escuela['participante__escuela__codigo']:
                numero_hombres = grupo.get_hombres()
                numero_mujeres = grupo.get_mujeres()
            else:  
                datos=cyd_m.Asignacion.objects.filter(grupo__sede=sede,participante__escuela__codigo=escuela['participante__escuela__codigo'])
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

def crear_dic(mapping, key, value):
        if value !=0:
            mapping[key] = value

class InformeListadoEscuela2(views.APIView):   
    def post(self, request):
        acumulador_aprobados=0
        listado_escuelas=[]
        contador_aprobados = 0
        contador_reprobados = 0
        contador_maestros = 0
        contador_maestras =0
        contador_sedes = 0
        #kwargs = dict(self.request.POST)        
        #print(self.request.POST['departamento'])
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

        sort_params = {}
        crear_dic(sort_params,'municipio__departamento',departamento)
        crear_dic(sort_params,'municipio',municipio)
        crear_dic(sort_params,'capacitador',capacitador)
        crear_dic(sort_params,'fecha_creacion__gte',fecha_min)
        crear_dic(sort_params,'fecha_creacion__lte',fecha_max)
        crear_dic(sort_params,'activa',True)
        sedes_encontradas = cyd_m.Sede.objects.filter(**sort_params).order_by('-fecha_creacion')     
        for data_participantes in sedes_encontradas:
                contador_sedes = contador_sedes +1                                                
                data = data_participantes.get_participantes()["resumen"]
                total_maestros = data['genero'].aggregate(Sum('cantidad'))
                total_hombre = data['genero'].filter(nombre_genero="Hombre")
                total_mujeres = data['genero'].filter(nombre_genero="Mujer")

                for total_maestros_hombres in total_hombre:
                    contador_maestros = total_maestros_hombres["cantidad"]                

                for total_maestros_mujeres in total_mujeres:
                    contador_maestras = total_maestros_mujeres["cantidad"]                   
                datos_escuela ={}
                datos_escuela["Numero"] = contador_sedes
                datos_escuela["Url"] = data_participantes.get_absolute_url()
                datos_escuela["escuela"]=data_participantes.escuela_beneficiada.nombre
                datos_escuela["escuela_url"]=data_participantes.escuela_beneficiada.get_absolute_url()
                datos_escuela["maestros"]=total_maestros['cantidad__sum']
                datos_escuela["hombres"]=contador_maestros
                datos_escuela["mujeres"]=contador_maestras
                datos_escuela["aprobados"]=data['estado']['aprobado']['cantidad']
                datos_escuela["reprobados"]=data['estado']['reprobado']['cantidad']
                datos_escuela["nivelar"]=data['estado']['nivelar']['cantidad']
                datos_escuela["capacitador"]=data_participantes.capacitador.get_full_name()
                datos_escuela["sede"]=data_participantes.nombre
                datos_escuela["fecha"]=data_participantes.fecha_creacion.date()
                datos_escuela["departamento"]=data_participantes.municipio.departamento.nombre
                datos_escuela["municipio"]=data_participantes.municipio.nombre
                datos_escuela["udi"]=data_participantes.escuela_beneficiada.codigo
                listado_escuelas.append(datos_escuela)
                contador_maestras = 0
                contador_maestros = 0   
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
            sede = cyd_m.Sede.objects.filter(id=self.request.POST['sede'],activa=True)
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
        porcentaje=self.request.POST["datos[porcentaje]"],
        cyd_curso_creado_por = self.request.user
        )
        nuevo_curso.save()
        try:
            for x in range(int(self.request.POST["cantidad_asistencia"])):
                nueva_asistencia=cyd_m.CrAsistencia(
                    curso=cyd_m.Curso.objects.last(),
                    modulo_num=str(x+1),
                    punteo_max=self.request.POST["datos[asistencias-"+str(x)+"-punteo_max]"],
                    cyd_cr_asistencia_creado_por= self.request.user
                )
                nueva_asistencia.save()
                #print("modulo:"+str(x+1)+" punteo:"+self.request.POST["datos[asistencias-"+str(x)+"-punteo_max]"])
        except:
            print("Solo llego 1")
        try:
            for x in range(int(self.request.POST["cantidad_hitos"])):
                nuevo_hito=cyd_m.CrHito(
                    curso=cyd_m.Curso.objects.last(),
                    nombre=self.request.POST["datos[hitos-"+str(x)+"-nombre]"],
                    punteo_max=self.request.POST["datos[hitos-"+str(x)+"-punteo_max]"],
                    cyd_cr_hito_creado_por =self.request.user
                )
                nuevo_hito.save()
                #print("Nombre:"+self.request.POST["datos[hitos-"+str(x)+"-nombre]"]+" punteo:"+self.request.POST["datos[hitos-"+str(x)+"-punteo_max]"])
        except:
            print("solo lleva 1 tarea")


        return Response(
                "Curso creado exitosamente",
            status=status.HTTP_200_OK
            )
class GraficaPastelAprobadosReprobadosHombresMujeres(views.APIView):

    def get(self, request):
        grupo = cyd_m.Grupo.objects.get(id=self.request.GET["grupo"])        
        porcentaje = (grupo.get_porcentaje_aprobados())       
        porcentaje_resultado_hombre = round((grupo.get_hombres() *100) / (grupo.get_hombres() + grupo.get_mujeres()))
        porcentaje_resultado_mujer = round((grupo.get_mujeres() *100) / (grupo.get_hombres() + grupo.get_mujeres()))        
        valores = {'genero': [],'resultado': [],'porcentaje_genero':[],'porcentaje_resultado':[]}        
        valores["genero"].append(grupo.get_hombres())
        valores["genero"].append(grupo.get_mujeres()) 
        valores["resultado"].append(grupo.count_aprobados())      
        valores["resultado"].append(grupo.count_reprobados())   
        valores["porcentaje_resultado"].append(int(porcentaje))      
        valores["porcentaje_resultado"].append(int(100-porcentaje))
        valores["porcentaje_genero"].append(int(porcentaje_resultado_hombre))   
        valores["porcentaje_genero"].append(int(porcentaje_resultado_mujer))  
        return Response(
            valores,
            status=status.HTTP_200_OK
            ) 

class InformeListadoSedeEscuela(views.APIView):   
    def post(self, request):
        listado_escuelas=[]
        numero =0
        try:
            departamento = [x for x in self.request.POST.getlist('departamento[]')]
            list_departamento = [] 
            if len(departamento) ==0:
                departamento = self.request.POST['departamento'] 
                list_departamento.append(departamento)  
        except MultiValueDictKeyError:
            departamento=0
        try:
            municipio = [int(x) for x in self.request.POST.getlist('municipio[]')]
            list_municipio = [] 
            if len(municipio) ==0:
                municipio = self.request.POST['municipio'] 
                list_municipio.append(municipio)  
        except MultiValueDictKeyError:
            municipio=0
        try:
            capacitador = [int(x) for x in self.request.POST.getlist('capacitador[]')]
            list_capacitador = [] 
            if len(capacitador) ==0:
                capacitador = self.request.POST['capacitador'] 
                list_capacitador.append(capacitador)  
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

        sort_params = {}
        if len(list_departamento)==1:
            crear_dic(sort_params,'municipio__departamento__id__in',list_departamento)
        else:
            crear_dic(sort_params,'municipio__departamento__id__in',departamento)
        if len(list_municipio)==1:
            crear_dic(sort_params,'municipio__id__in',list_municipio)
        else:
            crear_dic(sort_params,'municipio__id__in',municipio)
        if len(list_capacitador)==1:
            crear_dic(sort_params,'capacitador__id__in',list_capacitador)
        else:
            crear_dic(sort_params,'capacitador__id__in',capacitador)
        crear_dic(sort_params,'fecha_creacion__gte',fecha_min)
        crear_dic(sort_params,'fecha_creacion__lte',fecha_max)
        crear_dic(sort_params,'activa',True)
        sedes_encontradas = cyd_m.Sede.objects.filter(**sort_params).order_by('-fecha_creacion')                   
        for data_participantes in sedes_encontradas:              
                es_naat = data_participantes.get_es_naat()
                for info_sede in data_participantes.get_escuelas():
                    numero = numero +1
                    escuela_sede = {}
                    escuela_sede["escuela_url"] = info_sede.get_absolute_url() 
                    escuela_sede["url_sede"] = data_participantes.get_absolute_url()  
                    escuela_sede["numero"] = numero       
                    escuela_sede["escuela"] =info_sede.nombre
                    escuela_sede["direccion"] = info_sede.direccion
                    escuela_sede["codigo"]= info_sede.codigo
                    escuela_sede["cantidad_participantes"]= info_sede.cantidad_participantes
                    escuela_sede["sede"]= data_participantes.nombre                    
                    if data_participantes.fecha_creacion.year <=2023:
                        escuela_sede["estado_sede"]= True
                    else:
                        escuela_sede["estado_sede"] =data_participantes.finalizada

                    escuela_sede["capacitador"]= data_participantes.capacitador.get_full_name()
                    escuela_sede["departamento"]= data_participantes.municipio.departamento.nombre
                    escuela_sede["municipio"]= data_participantes.municipio.nombre
                    escuela_sede["fecha"]= data_participantes.fecha_creacion.date()
                    escuela_sede["control_academico"]= info_sede.get_escuelas_sedes(capacitador, info_sede.codigo,data_participantes.id)                    
                    if data_participantes.escuela_beneficiada.codigo == info_sede.codigo:
                        escuela_sede["beneficiada"] = "Beneficiada"
                    else:
                        if es_naat:
                            escuela_sede["beneficiada"] = "Beneficiada"
                        else:
                            escuela_sede["beneficiada"] = "No beneficiada"
                    listado_escuelas.append(escuela_sede)              
        return Response(
                listado_escuelas,
            status=status.HTTP_200_OK
            )
    
class InformeEscuelasSedesView(LoginRequiredMixin, FormView):
    """ Vista para obtener la informacion de los dispositivos para crear el informe de existencia mediante un
    api mediante el metodo GET  y lo muestra en el tempalte
    """
    template_name = 'cyd/InformeEscuelaSedeV2.html'
    form_class = cyd_f.InformeEscuelaSedeslistadoForm


def get_obtener_curso(curso,numero,fecha_max,fecha_min,departamento,municipio):    
    numero_nuevo=0
    datos_varios_cursos = []
    sort_params = {}
    sort_params_genero_hombre ={}
    sort_params_genero_mujer ={}
    crear_dic(sort_params,'grupo__sede__fecha_creacion__lte',fecha_max)
    crear_dic(sort_params,'grupo__sede__fecha_creacion__gte',fecha_min)
    crear_dic(sort_params,'grupo__curso__id',curso)
    crear_dic(sort_params,'grupo__sede__municipio__id',municipio)
    crear_dic(sort_params,'grupo__sede__municipio__departamento__id',departamento)

    crear_dic(sort_params_genero_hombre,'grupo__sede__fecha_creacion__lte',fecha_max)
    crear_dic(sort_params_genero_hombre,'grupo__sede__fecha_creacion__gte',fecha_min)
    crear_dic(sort_params_genero_hombre,'grupo__curso__id',curso)
    crear_dic(sort_params_genero_hombre,'participante__genero__id',2)
    crear_dic(sort_params_genero_hombre,'grupo__sede__municipio__id',municipio)
    crear_dic(sort_params_genero_hombre,'grupo__sede__municipio__departamento__id',departamento)
    
    crear_dic(sort_params_genero_mujer,'grupo__curso__id',curso)
    crear_dic(sort_params_genero_mujer,'grupo__sede__fecha_creacion__lte',fecha_max)
    crear_dic(sort_params_genero_mujer,'grupo__sede__fecha_creacion__gte',fecha_min)
    crear_dic(sort_params_genero_mujer,'participante__genero__id',1)
    crear_dic(sort_params_genero_mujer,'grupo__sede__municipio__id',municipio)
    crear_dic(sort_params_genero_mujer,'grupo__sede__municipio__departamento__id',departamento)       
    aprobados =0
    reprobados = 0    
    asignaciones = cyd_m.Asignacion.objects.filter(**sort_params)    
    if curso != 0:
        data_curso = cyd_m.Curso.objects.get(id=curso)  
        asignaciones_mujeres = cyd_m.Asignacion.objects.filter(**sort_params_genero_mujer)
        asignaciones_hombres = cyd_m.Asignacion.objects.filter(**sort_params_genero_hombre)        
        for data in asignaciones:            
            if data.get_aprobado():
                aprobados = aprobados +1
            else:
                reprobados = reprobados +1       
        datos_curso = {}
        datos_curso["numero"] = numero
        if curso !=0:
            datos_curso["nombre"] = data_curso.nombre
        else:
            datos_curso["nombre"] = "pueva"

        datos_curso["total_participantes"] = asignaciones.count()  
        datos_curso["total_hombres"] = asignaciones_hombres.count()       
        datos_curso["total_mujeres"] =asignaciones_mujeres.count()
        datos_curso["total_aprobados"] = aprobados
        datos_curso["total_reprobados"]= reprobados
        datos_curso["total_sedes"]= asignaciones.values_list('grupo__sede').distinct().count()
        datos_curso["total_municipios"]= asignaciones.values_list('grupo__sede__municipio').distinct().count()
        datos_curso["total_departamentos"]= asignaciones.values_list('grupo__sede__municipio__departamento').distinct().count()    
        return datos_curso
    else:
        for data_asig in asignaciones.values_list('grupo__curso__id','grupo__curso__nombre').distinct().order_by('-grupo__curso__id'):
            numero_nuevo = numero_nuevo +1
            datos_curso = {}           
            aprobados = sum(b.get_aprobado() for b in asignaciones.filter(grupo__curso__id=data_asig[0]) )
            reprobados = sum(c.get_reprobado() for c in asignaciones.filter(grupo__curso__id=data_asig[0]) )            
            datos_curso["numero"] = numero_nuevo
            datos_curso["nombre"] = data_asig[1]
            datos_curso["total_participantes"] = asignaciones.filter(grupo__curso__id=data_asig[0]).count()
            datos_curso["total_hombres"] = asignaciones.filter(grupo__curso__id=data_asig[0],participante__genero__id=1).count()     
            datos_curso["total_mujeres"] = asignaciones.filter(grupo__curso__id=data_asig[0],participante__genero__id=2).count()
            datos_curso["total_aprobados"] = aprobados
            datos_curso["total_reprobados"]= reprobados
            datos_curso["total_sedes"]= asignaciones.filter(grupo__curso__id=data_asig[0]).values_list("grupo__sede__id").distinct().count()
            datos_curso["total_municipios"]= asignaciones.values_list('grupo__sede__municipio').distinct().count()
            datos_curso["total_departamentos"]= asignaciones.values_list('grupo__sede__municipio__departamento').distinct().count()   
            datos_varios_cursos.append(datos_curso)
        return datos_varios_cursos 
class InformeCursos(views.APIView):   
    def post(self, request):
        listado_cursos = []
        numero = 0
        try:
            cursos = [x for x in self.request.POST.getlist('curso[]')]
            cursos_buscar = [] 
            if len(cursos) ==0:
                curso = self.request.POST['curso'] 
                cursos_buscar.append(curso)
            else:
                cursos_buscar=cursos  
        except MultiValueDictKeyError:
            cursos_buscar=[]        
        try:
            departamento = self.request.POST['departamento'] 
        except MultiValueDictKeyError:
            departamento=0
        try:
           municipio = self.request.POST['municipio']
        except MultiValueDictKeyError:
            municipio=0 
        try:
            fecha_min=self.request.POST['fecha_min']
        except MultiValueDictKeyError:
            fecha_min=0
        try:
            fecha_max=self.request.POST['fecha_max']
        except MultiValueDictKeyError:
            fecha_max=0
                 
        if len(cursos_buscar) > 1:
            print(1)           
            for data_curso in cursos_buscar:                
                numero = numero  + 1 
                listado_cursos.append(get_obtener_curso(data_curso,numero,fecha_max,fecha_min,departamento,municipio))
                
        elif len(cursos_buscar)==1:
            print(2)            
            listado_cursos.append(get_obtener_curso(cursos_buscar.pop(),1,fecha_max,fecha_min,departamento,municipio))
            
        elif len(cursos_buscar)==0:
            print(3)           
            for data in get_obtener_curso(0,0,fecha_max,fecha_min,departamento,municipio):
                listado_cursos.append(data)
            #listado_cursos.append(get_obtener_curso(0,0,fecha_max,fecha_min,departamento,municipio))           

        return Response(
                listado_cursos,
            status=status.HTTP_200_OK
            )
class InformeCursosView(LoginRequiredMixin, FormView):
    """ Vista para obtener la informacion de los dispositivos para crear el informe de existencia mediante un
    api mediante el metodo GET  y lo muestra en el tempalte
    """
    template_name = 'cyd/Informe_cursos.html'
    form_class = cyd_f.InformeCursoslistadoForm

class InformeParticipanteCapacitador(views.APIView):
    """ Punto de acceso para obtener la informacion de los participantes  filtrandolo por capacitador y un rango de fecha
        url de acceso: '/cyd/informe/capacitador/participantes/' obtiene la informacion mediante un medoto post ejecutado desde un boton 
        del formulario 
    """   
    def post(self, request):
        listado_participantes = []
        numero = 0
        conteo_participantes = 0
        restante_cascada = 0
        participantes = 0
        otros_participantes = 0
        lista_capacitador = []
        try:
            capacitador = [x for x in self.request.POST.getlist('capacitador[]')]         
            if len(capacitador)==0:
                lista_capacitador.append(self.request.POST['capacitador'])                

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
        if capacitador == 0:           
            sede = cyd_m.Sede.objects.filter(fecha_creacion__lte=fecha_max, fecha_creacion__gte=fecha_min)
        else:            
             if len(lista_capacitador)==1:
                 sede = cyd_m.Sede.objects.filter(capacitador__id__in=lista_capacitador,fecha_creacion__lte=fecha_max, fecha_creacion__gte=fecha_min)
             else:
                 sede = cyd_m.Sede.objects.filter(capacitador__id__in=capacitador,fecha_creacion__lte=fecha_max, fecha_creacion__gte=fecha_min)
        for data_participantes in sede:
            for participante in data_participantes.get_participantes()['listado']:
                conteo_participantes = conteo_participantes + 1
                if participante['year']==2010:
                    numero = numero +1
                    if numero <=16142:
                            participantes = participantes +1
                            info_participante = {}
                            info_participante["numero"]=conteo_participantes
                            info_participante["url"]=participante['participante'].get_absolute_url()
                            info_participante["nombre"]=participante['participante'].nombre
                            info_participante["apellido"]=participante['participante'].apellido
                            info_participante["escuela"]=participante['participante'].escuela.codigo
                            info_participante["dpi"]=participante['participante'].dpi
                            info_participante["genero"]=participante['participante'].genero.genero
                            
                            if participante['participante'].mail is not None:                     
                                info_participante["mail"]=participante['participante'].mail
                            else:
                                info_participante["mail"]="No tiene"

                            if participante['participante'].tel_casa is not None: 
                                info_participante["tel_casa"]=participante['participante'].tel_casa
                            else:
                                info_participante["tel_casa"]="No tiene"

                            if participante['participante'].tel_movil is not None: 
                                info_participante["tel_movil"]=participante['participante'].tel_movil
                            else:
                                info_participante["tel_movil"]="No tiene"
                            
                            try:
                                info_participante["escolaridad"]=participante['participante'].escolaridad.nombre
                            except:
                                info_participante["escolaridad"]="No tiene"
                            
                            try:
                                info_participante["etnia"]=participante['participante'].etnia.nombre
                            except:
                                info_participante["etnia"]="No tiene" 
                            try:
                                info_participante["profesion"]=participante['participante'].profesion.nombre
                            except:
                                info_participante["profesion"]="No tiene"
                            try:    
                                info_participante["grado_impartido"]=participante['participante'].grado_impartido.grado_asignado
                            except:
                                info_participante["grado_impartido"]="No tiene"
                            info_participante["chicos"]=participante['participante'].chicos
                            info_participante["chicas"]=participante['participante'].chicas
                            info_participante["nota"]=round(participante['nota'],0)
                            info_participante["capacitador"]=data_participantes.capacitador.get_full_name()
                            listado_participantes.append(info_participante)
                    else:
                        restante_cascada = restante_cascada + 1 
                else:
                     otros_participantes = otros_participantes + 1
                     info_participante = {}
                     info_participante["numero"]=conteo_participantes
                     info_participante["url"]=participante['participante'].get_absolute_url()
                     info_participante["nombre"]=participante['participante'].nombre
                     info_participante["apellido"]=participante['participante'].apellido
                     info_participante["escuela"]=participante['participante'].escuela.codigo
                     info_participante["dpi"]=participante['participante'].dpi
                     info_participante["genero"]=participante['participante'].genero.genero                    
                     if participante['participante'].mail is not None:                     
                        info_participante["mail"]=participante['participante'].mail
                     else:
                        info_participante["mail"]="No tiene"

                     if participante['participante'].tel_casa is not None: 
                        info_participante["tel_casa"]=participante['participante'].tel_casa
                     else:
                        info_participante["tel_casa"]="No tiene"

                     if participante['participante'].tel_movil is not None: 
                        info_participante["tel_movil"]=participante['participante'].tel_movil
                     else:
                        info_participante["tel_movil"]="No tiene"
                    
                     try:
                        info_participante["escolaridad"]=participante['participante'].escolaridad.nombre
                     except:
                        info_participante["escolaridad"]="No tiene"
                    
                     try:
                        info_participante["etnia"]=participante['participante'].etnia.nombre
                     except:
                        info_participante["etnia"]="No tiene"                      
                    
                     try:
                        info_participante["profesion"]=participante['participante'].profesion.nombre
                     except:
                        info_participante["profesion"]="No tiene"
                     try:    
                        info_participante["grado_impartido"]=participante['participante'].grado_impartido.grado_asignado
                     except:
                        info_participante["grado_impartido"]="No tiene"
                     info_participante["chicos"]=participante['participante'].chicos
                     info_participante["chicas"]=participante['participante'].chicas
                     info_participante["nota"]=round(participante['nota'],0)
                     info_participante["capacitador"]=data_participantes.capacitador.get_full_name()
                     listado_participantes.append(info_participante)        
        return Response({"data":listado_participantes,"cascada":restante_cascada},
            status=status.HTTP_200_OK
            )        
    
class InformeCapacitadorParticipanteView(LoginRequiredMixin, FormView):
    """ Vista para obtener la informacion de los dispositivos para crear el informe de existencia mediante un
    api mediante el metodo GET  y lo muestra en el tempalte
    """
    template_name = 'cyd/InformeParticipanteCapacitador.html'
    form_class = cyd_f.InformeParticipanteCapacitadorForm


class InformeParticipantesNaat(views.APIView):
    def get(self, request):
        #partipantes = cyd_m.Asignacion.objects.filter(grupo__curso__nombre__contains="NAAT").values(grupo__sede)[:10]
        #print(partipantes)
        listado_participante=[]
        sedes = cyd_m.Grupo.objects.filter(curso__nombre__icontains="NAAT").values('sede_id').distinct()
        grupo = cyd_m.Grupo.objects.filter(curso__nombre__icontains="NAAT").values('id').distinct()
        sedes_buscar = cyd_m.Sede.objects.filter(id__in=sedes)
        for data in sedes_buscar:
            data_dict ={}
            for data1 in data.get_participantes()['listado']:
                data_dict["participante"] = str(data1["participante"])
                listado_participante.append(data_dict)
            
            print("************")
            
        
        return Response(
            listado_participante,
            status=status.HTTP_200_OK
            )
    
class NaatInformeView(LoginRequiredMixin, TemplateView):
    """ Vista para obtener la informacion de los dispositivos para crear el informe de existencia mediante un
    api mediante el metodo GET  y lo muestra en el tempalte
    """
    redirect_unauthenticated_users = True
    raise_exception = True
    template_name = "cyd/informe_naat.html"
    #form_class = conta_f.RastreoDesechoInformeForm 

class SubirControlAcademicoExcel(views.APIView):
    def get(self, request):
        #partipantes = cyd_m.Asignacion.objects.filter(grupo__curso__nombre__contains="NAAT").values(grupo__sede)[:10]
        #print(partipantes)
        listado_participante=[]
        sedes = cyd_m.Grupo.objects.filter(curso__nombre__icontains="NAAT").values('sede_id').distinct()
        grupo = cyd_m.Grupo.objects.filter(curso__nombre__icontains="NAAT").values('id').distinct()
        sedes_buscar = cyd_m.Sede.objects.filter(id__in=sedes)
        for data in sedes_buscar:
            data_dict ={}
            for data1 in data.get_participantes()['listado']:
                data_dict["participante"] = str(data1["participante"])
                listado_participante.append(data_dict)
            
            print("************")
            
        
        return Response(
            "Ingresados exitosamente",
            status=status.HTTP_200_OK
            )