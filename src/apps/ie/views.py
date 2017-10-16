from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from apps.ie.models import Laboratorio, Computadora, Serie
from apps.ie.forms import (
    LaboratorioCreateForm, LaboratorioUpdateForm,
    ComputadoraForm, SerieForm)


class LaboratorioCreateView(CreateView):
    model = Laboratorio
    form_class = LaboratorioCreateForm

    def form_valid(self, form):
        form.instance.poblacion = form.instance.escuela.poblaciones.last()
        form.instance.organizacion = self.request.user.perfil.organizacion
        return super(LaboratorioCreateView, self).form_valid(form)


class LaboratorioDetailView(DetailView):
    model = Laboratorio
    template_name = "ie/laboratorio_detail.html"

    def get_context_data(self, **kwargs):
        context = super(LaboratorioDetailView, self).get_context_data(**kwargs)
        context['computadora_form'] = ComputadoraForm(initial={
            'laboratorio': self.object})

        # filtrar las computadoras de este laboratorio
        context['serie_form'] = SerieForm()
        computadora_queryset = context['serie_form'].fields['computadora'].queryset
        computadora_queryset = computadora_queryset.filter(laboratorio=self.object)
        context['serie_form'].fields['computadora'].queryset = computadora_queryset
        return context


class LaboratorioListView(ListView):
    model = Laboratorio
    template_name = "asd"


class LaboratorioUpdateView(UpdateView):
    model = Laboratorio
    template_name = "ie/laboratorio_detail.html"
    form_class = LaboratorioUpdateForm

    def get_context_data(self, **kwargs):
        context = super(LaboratorioUpdateView, self).get_context_data(**kwargs)
        context['computadora_form'] = ComputadoraForm(initial={
            'laboratorio': self.object})
        context['serie_form'] = SerieForm()
        return context


class ComputadoraCreateView(CreateView):
    model = Computadora
    form_class = ComputadoraForm


class SerieCreateView(CreateView):
    model = Serie
    form_class = SerieForm
