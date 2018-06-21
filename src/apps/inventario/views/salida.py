from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView
from braces.views import (
    LoginRequiredMixin,PermissionRequiredMixin
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
        context['salidainventario_list'] = inv_m.SalidaInventario.objects.filter(en_creacion=True)
        return context

    def form_valid(self, form):
        form.instance.escuela = escuela_m.Escuela.objects.get(codigo=form.cleaned_data['udi'])
        form.instance.creada_por = self.request.user
        super(SalidaInventarioCreateView, self).form_valid(form)


class SalidaInventarioUpdateView(LoginRequiredMixin, UpdateView):
    """ Vista   para obtener los datos de Salida mediante una :class:`SalidaInventario`
    Funciona  para recibir los datos de un  'SalidaInventarioForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.SalidaInventario
    form_class = inv_f.SalidaInventarioUpdateForm
    template_name = 'inventario/salida/salida_edit.html'
    permission_required = 'inventario.salidainventario_change'

    def get_context_data(self, *args, **kwargs):
        context = super(SalidaInventarioUpdateView, self).get_context_data(*args, **kwargs)
        if self.request.user.has_perm("inventario.salidainventario_change"):
            context['cantidad_paquetes'] = inv_f.PaqueteCantidadForm()
        return context


class SalidaPaqueteUpdateView(LoginRequiredMixin, UpdateView):
    """ Vista   para obtener los datos de Paquete mediante una :class:`SalidaInventario`
    Funciona  para recibir los datos de un  'PaqueteCantidadForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.SalidaInventario
    form_class = inv_f.PaqueteCantidadForm
    template_name = 'inventario/salida/paquetes_add.html'

    def get_success_url(self):
        return reverse_lazy('salidainventario_edit', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.crear_paquetes(form.cleaned_data['cantidad'], self.request.user)
        return super(SalidaPaqueteUpdateView, self).form_valid(form)


