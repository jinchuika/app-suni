from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from braces.views import LoginRequiredMixin, GroupRequiredMixin

from apps.cyd.forms import CursoForm, CrHitoFormSet, CrAsistenciaFormSet
from apps.cyd.models import Curso


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
