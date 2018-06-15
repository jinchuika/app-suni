from django.shortcuts import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from braces.views import (
    LoginRequiredMixin
)

from apps.escuela import models as escuela_m
from apps.inventario import models as inv_m
from apps.inventario import forms as inv_f


class SalidaInventarioCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos de Salida mediante una :class:`SalidaInventario`
    Funciona  para recibir los datos de un  'SalidaInventarioForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.SalidaInventario
    form_class = inv_f.SalidaInventarioForm
    template_name = 'inventario/salida/salida_add.html'

    def get_context_data(self, **kwargs):
        context = super(SalidaInventarioCreateView, self).get_context_data(**kwargs)
        context['salidainventario'] = inv_m.SalidaInventario.objects.filter(en_creacion='True')
        return context

    def form_valid(self, form):
        print(form.cleaned_data['codigo'])
        form.instance.escuela = escuela_m.Escuela.objects.get(codigo=form.cleaned_data['codigo'])
        form.instance.creada_por = self.request.user
        super(SalidaInventarioCreateView, self).form_valid(form)
