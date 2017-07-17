from datetime import datetime
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView

from django.core.urlresolvers import reverse

from braces.views import LoginRequiredMixin, GroupRequiredMixin, JsonRequestResponseMixin

from apps.cyd.forms import (
    CursoForm, CrHitoFormSet, CrAsistenciaFormSet,
    SedeForm, GrupoForm, CalendarioFilterForm,
    SedeFilterForm, ParticipanteForm, ParticipanteBaseForm)
from apps.cyd.models import Curso, Sede, Grupo, Calendario, Participante, ParRol, ParEtnia
from apps.escuela.models import Escuela
from apps.main.models import Coordenada


class CursoCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = [u"cyd_admin", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = Curso
    template_name = 'cyd/curso_add.html'
    form_class = CursoForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        hito_formset = CrHitoFormSet()
        asistencia_formset = CrAsistenciaFormSet()
        return self.render_to_response(
            self.get_context_data(
                forrm=form,
                hito_formset=hito_formset,
                asistencia_formset=asistencia_formset))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        hito_formset = CrHitoFormSet(self.request.POST)
        asistencia_formset = CrAsistenciaFormSet(self.request.POST)
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
    model = Curso
    template_name = 'cyd/curso_detail.html'


class CursoListView(LoginRequiredMixin, ListView):
    model = Curso
    template_name = 'cyd/curso_list.html'


class SedeCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = [u"cyd_admin", u"cyd", u"cyd_capacitador", ]
    redirect_unauthenticated_users = True
    raise_exception = True

    model = Sede
    form_class = SedeForm
    template_name = 'cyd/sede_add.html'

    def get_form(self, form_class=None):
        form = super(SedeCreateView, self).get_form(form_class)
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            form.fields['capacitador'].queryset = form.fields['capacitador'].queryset.filter(id=self.request.user.id)
        return form

    def form_valid(self, form):
        coordenada = Coordenada(
            lat=form.cleaned_data['lat'],
            lng=form.cleaned_data['lng'],
            descripcion='De la sede ' + form.instance.nombre)
        coordenada.save()
        form.instance.mapa = coordenada
        form.instance.mapa.save()
        return super(SedeCreateView, self).form_valid(form)


class SedeDetailView(LoginRequiredMixin, DetailView):
    model = Sede
    template_name = 'cyd/sede_detail.html'


class SedeUpdateView(LoginRequiredMixin, UpdateView):
    model = Sede
    template_name = 'cyd/sede_add.html'
    form_class = SedeForm

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


class SedeListView(LoginRequiredMixin, ListView):
    model = Sede
    template_name = 'cyd/sede_list.html'

    def get_queryset(self):
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            return Sede.objects.filter(capacitador=self.request.user)
        else:
            return Sede.objects.all()


class GrupoCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = [u"cyd", u"cyd_capacitador", u"cyd_admin", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = Grupo
    template_name = 'cyd/grupo_add.html'
    form_class = GrupoForm

    def get_form(self, form_class=None):
        form = super(GrupoCreateView, self).get_form(form_class)
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            form.fields['sede'].queryset = Sede.objects.filter(capacitador=self.request.user)
        return form

    def form_valid(self, form):
        grupo = form.save()
        for asistencia in grupo.curso.asistencias.all():
            grupo.asistencias.create(cr_asistencia=asistencia)
        return super(GrupoCreateView, self).form_valid(form)


class GrupoDetailView(LoginRequiredMixin, DetailView):
    model = Grupo
    template_name = 'cyd/grupo_detail.html'


class GrupoListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    group_required = [u"cyd", u"cyd_capacitador", u"cyd_admin", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = Grupo
    template_name = 'cyd/grupo_list.html'

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
        context['sede_form'] = SedeFilterForm()
        context['nueva_form'] = CalendarioFilterForm()
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            context['nueva_form'].fields['sede'].queryset = self.request.user.sedes.all()
            context['sede_form'].fields['capacitador'].empty_label = None
            context['sede_form'].fields['capacitador'].queryset = context['sede_form'].fields['capacitador'].queryset.filter(id=self.request.user.id)
            context['sede_form'].fields['sede'].queryset = self.request.user.sedes.all()
        return context


class CalendarioListView(JsonRequestResponseMixin, View):
    def get(self, request, *args, **kwargs):
        response = []
        calendario_list = Calendario.objects.filter(
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
                'curso': '{}'.format(calendario.grupo.curso),
                'description': 'Grupo {}, asistencia {} en la sede {}'.format(
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
    model = Participante
    template_name = 'cyd/participante_add.html'
    form_class = ParticipanteForm

    def get_form(self, form_class=None):
        form = super(ParticipanteCreateView, self).get_form(form_class)
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            form.fields['sede'].queryset = self.request.user.sedes.all()
        return form


class ParticipanteCreateListView(LoginRequiredMixin, GroupRequiredMixin, FormView):
    group_required = [u"cyd", u"cyd_capacitador", u"cyd_admin", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = Participante
    template_name = 'cyd/participante_importar.html'
    form_class = ParticipanteBaseForm

    def get_context_data(self, **kwargs):
        context = super(ParticipanteCreateListView, self).get_context_data(**kwargs)
        context['rol_list'] = ParRol.objects.all()
        return context

    def get_form(self, form_class=None):
        form = super(ParticipanteCreateListView, self).get_form(form_class)
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            form.fields['sede'].queryset = self.request.user.sedes.all()
        return form


class ParticipanteJsonCreateView(LoginRequiredMixin, JsonRequestResponseMixin, CreateView):
    require_json = True
    model = Participante
    form_class = ParticipanteForm

    def post(self, request, *args, **kwargs):
        try:
            escuela = Escuela.objects.get(codigo=self.request_json['udi'])
            grupo = Grupo.objects.get(id=self.request_json['grupo'])
            rol = ParRol.objects.get(id=self.request_json['rol'])
            participante = Participante.objects.create(
                dpi=self.request_json['dpi'],
                nombre=self.request_json['nombre'],
                apellido=self.request_json['apellido'],
                genero=self.request_json['genero'],
                rol=rol,
                mail=self.request_json['mail'],
                tel_movil=self.request_json['tel_movil'],
                escuela=escuela,
                slug=self.request_json['dpi'])
            participante.asignar(grupo)
        except IntegrityError:
            error_dict = {u"message": u"Dato duplicado"}
            return self.render_bad_request_response(error_dict)
        return self.render_json_response({'status': 'ok'})


class ParticipanteDetailView(LoginRequiredMixin, DetailView):
    model = Participante
    template_name = 'cyd/participante_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ParticipanteDetailView, self).get_context_data(**kwargs)
        context['rol_list'] = ParRol.objects.all()
        context['etnia_list'] = ParEtnia.objects.all()
        return context
