from django.views.generic import DetailView, UpdateView, CreateView
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from apps.inventario import models as inv_m
from apps.inventario import forms as inv_f


class DispositivoDetailView(DetailView):
    """
    Esta clase sirve como base para todos los detalles de :class:`Dispositivo`.
    Agrega el formulario para creación de :class:`DipositivoFalla`
    """
    model = inv_m.Dispositivo

    def get_context_data(self, *args, **kwargs):
        context = super(DispositivoDetailView, self).get_context_data(*args, **kwargs)
        context['form_falla'] = inv_f.DispositivoFallaForm(initial={'dispositivo': self.object})
        return context


class DispositivoFallaCreateView(LoginRequiredMixin, CreateView):
    """Creación de :class:`DispositivoFalla`, no admite el método GET"""
    model = inv_m.DispositivoFalla
    form_class = inv_f.DispositivoFallaForm

    def form_valid(self, form):
        form.instance.reportada_por = self.request.user
        return super(DispositivoFallaCreateView, self).form_valid(form)


class TecladoUpdateView(LoginRequiredMixin, UpdateView):
    model = inv_m.Teclado
    form_class = inv_f.TecladoForm
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
    template_name = 'inventario/dispositivo/teclado/teclado_form.html'


class TecladoDetailView(LoginRequiredMixin, DispositivoDetailView):
    model = inv_m.Teclado
    template_name = 'inventario/dispositivo/teclado/teclado_detail.html'
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True


class MonitorDetailView(LoginRequiredMixin, DispositivoDetailView):
    """Esta clase sirve para ver los detalles de :class:`Monitor`
     mostrando los datos necesarios
    """
    model = inv_m.Monitor
    template_name = 'inventario/dispositivo/monitor/monitor_detail.html'
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
