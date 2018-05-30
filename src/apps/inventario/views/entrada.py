from django.shortcuts import reverse
from django.views.generic import CreateView,  UpdateView, DetailView, FormView
from braces.views import (
    LoginRequiredMixin
)
from apps.inventario import models as inv_m
from apps.inventario import forms as inv_f


class EntradaCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos de Entrada mediante una :class:`entrada`
    Funciona  para recibir los datos de un  'EntradaForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """

    model = inv_m.Entrada
    form_class = inv_f.EntradaForm
    template_name = 'inventario/entrada/entrada_add.html'

    def form_valid(self, form):
        form.instance.creada_por = self.request.user
        return super(EntradaCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EntradaCreateView, self).get_context_data(**kwargs)
        context['listado'] = inv_m.Entrada.objects.filter(en_creacion='True')

        return context


class EntradaDetailView(LoginRequiredMixin, DetailView):
    """Para generar detalles de la :class:`entrada`   con sus respectivos campos.
    """
    model = inv_m.Entrada
    template_name = 'inventario/entrada/entrada_detail.html'


class EntradaListView(LoginRequiredMixin, FormView):
    """Vista Encargada para mostrar las Lista de la :class:'Entrada' con su respectivo
    formulario de busqueda de filtros
    """
    model = inv_m.Entrada
    template_name = 'inventario/entrada/entrada_list.html'
    form_class = inv_f.EntradaInformeForm


class EntradaUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para actualizar de :class:`Entrada`. con sus respectivos campos
    """
    model = inv_m.Entrada
    form_class = inv_f.EntradaUpdateForm
    template_name = 'inventario/entrada/entrada_add.html'

    def get_context_data(self, **kwargs):
        context = super(EntradaUpdateView, self).get_context_data(**kwargs)
        context['EntradaDetalleForm'] = inv_f.EntradaDetalleForm(initial={'entrada': self.object})
        return context


class EntradaDetalleView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos de los Detalles de Entrada mediante una :class:`EntradaDetalle`
    Funciona  para recibir los datos de un  'EntradaDetalleForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.EntradaDetalle
    form_class = inv_f.EntradaDetalleForm
    template_name = 'inventario/entrada/entradadetalle_add.html'


class EntradaDetalleUpdateView(LoginRequiredMixin, UpdateView):
    """Vista Encargada de actualizar los datos mediante la :class:`EntradaDetalle`.
    """
    model = inv_m.EntradaDetalle
    form_class = inv_f.EntradaDetalleUpdateForm
    template_name = 'inventario/entrada/entradadetalle_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EntradaDetalleUpdateView, self).get_context_data(**kwargs)
        context['datos'] = inv_m.EntradaDetalle.objects.get(id=self.object.id)
        print(inv_m.EntradaDetalle.objects.get(id=self.object.id))
        return context

    def get_success_url(self):
        return reverse('entrada_update', kwargs={'pk': self.object.entrada.id})
