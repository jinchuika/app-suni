from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User

from braces.views import LoginRequiredMixin, GroupRequiredMixin

from apps.cyd.forms import CursoForm, CrHitoFormSet, CrAsistenciaFormSet, SedeForm, GrupoForm
from apps.cyd.models import Curso, Sede, Grupo
from apps.main.models import Coordenada


class CursoCrear(LoginRequiredMixin, GroupRequiredMixin, CreateView):
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


class CursoDetalle(LoginRequiredMixin, DetailView):
    model = Curso
    template_name = 'cyd/curso_detail.html'


class CursoLista(LoginRequiredMixin, ListView):
    model = Curso
    template_name = 'cyd/curso_list.html'


class SedeCrear(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = [u"cyd_admin", u"cyd", u"cyd_capacitador", ]
    redirect_unauthenticated_users = True
    raise_exception = True

    model = Sede
    form_class = SedeForm
    template_name = 'cyd/sede_add.html'

    def form_valid(self, form):
        coordenada = Coordenada(
            lat=form.cleaned_data['lat'],
            lng=form.cleaned_data['lng'],
            descripcion='De la sede ' + form.instance.nombre)
        coordenada.save()
        form.instance.mapa = coordenada
        form.instance.mapa.save()
        return super(SedeCrear, self).form_valid(form)


class SedeDetalle(LoginRequiredMixin, DetailView):
    model = Sede
    template_name = 'cyd/sede_detail.html'


class SedeEditar(LoginRequiredMixin, UpdateView):
    model = Sede
    template_name = 'cyd/sede_add.html'
    form_class = SedeForm

    def get_initial(self):
        initial = super(SedeEditar, self).get_initial()
        initial['lat'] = self.object.mapa.lat
        initial['lng'] = self.object.mapa.lng
        return initial

    def form_valid(self, form):
        respuesta = form.save(commit=False)
        if self.object.mapa is None:
            print("no")
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
        return super(SedeEditar, self).form_valid(form)


class SedeLista(LoginRequiredMixin, ListView):
    model = Sede
    template_name = 'cyd/sede_list.html'

    def get_queryset(self):
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            return Sede.objects.filter(capacitador=self.request.user)
        else:
            return Sede.objects.all()

    def get_context_data(self, **kwargs):
        context = super(SedeLista, self).get_context_data(**kwargs)
        context['capacitador_list'] = User.objects.filter(groups__name='cyd_capacitador')
        return context


class GrupoCrear(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = [u"cyd", u"cyd_capacitador", u"cyd_admin", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = Grupo
    template_name = 'cyd/grupo_add.html'
    form_class = GrupoForm

    def get_form(self, form_class=None):
        form = super(GrupoCrear, self).get_form(form_class)
        if self.request.user.groups.filter(name="cyd_capacitador").exists():
            form.fields['sede'].queryset = Sede.objects.filter(capacitador=self.request.user)
        return form

