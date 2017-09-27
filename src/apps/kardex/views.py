from django.views.generic import DetailView, ListView, FormView
from django.views.generic.edit import CreateView, UpdateView

from braces.views import LoginRequiredMixin, GroupRequiredMixin

from apps.kardex.models import (
    Proveedor, Equipo, Entrada, EntradaDetalle,
    Salida, SalidaDetalle)
from apps.kardex.forms import (
    EquipoForm, EntradaForm, EntradaCerrarForm, ProveedorForm,
    SalidaForm, SalidaDetalleForm, SalidaCerrarForm,
    EntradaDetalleForm, KardexInformeForm)


class EquipoListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    group_required = [u"kardex", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    template_name = 'kardex/equipo_list.html'
    model = Equipo

    def get_context_data(self, **kwargs):
        context = super(EquipoListView, self).get_context_data(**kwargs)
        context['equipo_form'] = EquipoForm()
        return context


class ProveedorListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    group_required = [u"kardex", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    template_name = 'kardex/proveedor_list.html'
    model = Proveedor

    def get_context_data(self, **kwargs):
        context = super(ProveedorListView, self).get_context_data(**kwargs)
        context['proveedor_form'] = ProveedorForm()
        return context


class ProveedorCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = [u"kardex", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'kardex/proveedor_form.html'


class ProveedorUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    group_required = [u"kardex", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'kardex/proveedor_form.html'


class ProveedorDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    group_required = [u"kardex", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = Proveedor
    template_name = 'kardex/proveedor_detail.html'


class EquipoCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = [u"kardex", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    """Vista para crear un :model:`kardex.Equipo`.
    Esta vista no tiene acceso mediante GET.
    """

    model = Equipo
    form_class = EquipoForm


class EntradaCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = [u"kardex", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = Entrada
    form_class = EntradaForm
    template_name = 'kardex/entrada.html'

    def get_context_data(self, **kwargs):
        context = super(EntradaCreateView, self).get_context_data(**kwargs)
        context['pendientes_list'] = Entrada.objects.filter(terminada=False)
        context['filter_form'] = KardexInformeForm()
        return context


class EntradaDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    group_required = [u"kardex", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = Entrada
    template_name = 'kardex/entrada_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EntradaDetailView, self).get_context_data(**kwargs)
        if not self.object.terminada:
            equipo_queryset = Equipo.objects.exclude(
                id__in=self.object.detalles.values('equipo').values_list('equipo'))
            context['detalle_form'] = EntradaDetalleForm(initial={'entrada': self.object})
            context['detalle_form'].fields['equipo'].queryset = equipo_queryset
            context['cerrar_form'] = EntradaCerrarForm(instance=self.object, initial={'terminada': True})
        return context


class EntradaPrintView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    group_required = [u"kardex", ]
    redirect_unauthenticated_users = True
    raise_exception = True

    """Vista para imprimir la salida.
    """

    model = Entrada
    template_name = 'kardex/entrada_print.html'


class EntradaDetalleCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = [u"kardex", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = EntradaDetalle
    form_class = EntradaDetalleForm
    template_name = 'kardex/entrada.html'


class EntradaUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    group_required = [u"kardex", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = Entrada
    form_class = EntradaCerrarForm


class SalidaCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = [u"kardex", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = Salida
    template_name = 'kardex/salida.html'
    form_class = SalidaForm

    def get_context_data(self, **kwargs):
        context = super(SalidaCreateView, self).get_context_data(**kwargs)
        context['pendientes_list'] = Salida.objects.filter(terminada=False)
        context['filter_form'] = KardexInformeForm()
        return context


class SalidaUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    group_required = [u"kardex", ]
    redirect_unauthenticated_users = True
    raise_exception = True

    """Para recibir el formulario que cierra la :model:`kardex.Salida`.
    Redirecciona al detalle de la :model:`kardex.Salida`.
    """

    model = Salida
    form_class = SalidaCerrarForm


class SalidaDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    group_required = [u"kardex", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = Salida
    template_name = 'kardex/salida_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SalidaDetailView, self).get_context_data(**kwargs)
        if not self.object.terminada:
            context['detalle_form'] = SalidaDetalleForm(initial={'salida': self.object})
            context['cerrar_form'] = SalidaCerrarForm(
                instance=self.object,
                initial={'terminada': True})
        return context


class SalidaPrintView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    group_required = [u"kardex", ]
    redirect_unauthenticated_users = True
    raise_exception = True

    """Vista para imprimir la salida.
    """

    model = Salida
    template_name = 'kardex/salida_print.html'


class SalidaDetalleCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = [u"kardex", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = SalidaDetalle
    form_class = SalidaDetalleForm


class KardexInformeView(LoginRequiredMixin, GroupRequiredMixin, FormView):
    group_required = [u"kardex", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    template_name = "kardex/informe.html"
    form_class = KardexInformeForm
