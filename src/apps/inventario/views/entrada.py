from django.shortcuts import reverse
from django.views.generic import CreateView,  UpdateView
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
        print(self.request.user)
        return super(EntradaCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EntradaCreateView, self).get_context_data(**kwargs)
        context['listado'] = inv_m.Entrada.objects.filter(en_creacion='True')
        return context


class EntradaUpdateView(LoginRequiredMixin, UpdateView):
    model = inv_m.Entrada
    form_class = inv_f.EntradaUpdateForm
    template_name = 'inventario/entrada/entrada_add.html'
