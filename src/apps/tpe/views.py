from django.utils.timezone import datetime
from django.shortcuts import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, GroupRequiredMixin

from apps.tpe.models import Equipamiento, Garantia, TicketSoporte, TicketRegistro
from apps.tpe.forms import EquipamientoNuevoForm, EquipamientoForm, GarantiaForm, TicketSoporteForm, TicketCierreForm, TicketRegistroForm


class EquipamientoCrearView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Equipamiento
    form_class = EquipamientoNuevoForm
    permission_required = 'tpe.add_equipamiento'
    redirect_unauthenticated_users = True
    raise_exception = True

    def get_success_url(self):
        return reverse('escuela_equipamiento_update', kwargs={'pk': self.object.escuela.id, 'id_equipamiento': self.object.id})


class EquipamientoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Equipamiento
    form_class = EquipamientoForm
    permission_required = 'tpe.change_equipamiento'
    redirect_unauthenticated_users = False
    raise_exception = True

    def get_success_url(self):
        return reverse('escuela_detail', kwargs={'pk': self.object.escuela.id})


class EquipamientoListView(LoginRequiredMixin, ListView):
    model = Equipamiento
    template_name = 'tpe/equipamiento_list.html'


class GarantiaListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Garantia
    template_name = 'tpe/garantia_list.html'
    group_required = [u"garantia", u"tpe_admin"]
    raise_exception = True


class GarantiaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Garantia
    form_class = GarantiaForm
    template_name = 'tpe/garantia_add.html'
    permission_required = 'tpe.add_garantia'
    redirect_unauthenticated_users = False
    raise_exception = True


class GarantiaDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = Garantia
    template_name = 'tpe/garantia_detail.html'
    group_required = [u"garantia", u"tpe_admin"]
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(GarantiaDetailView, self).get_context_data(**kwargs)
        context['ticket_form'] = TicketSoporteForm(initial={'garantia': self.object})
        context['ticket_cerrado_form'] = TicketCierreForm(initial={'cerrado': True})
        context['ticket_registro_form'] = TicketRegistroForm()

        if 'ticket_id' in self.kwargs:
            context['ticket_detail'] = TicketRegistro.objects.get(id=self.kwargs['ticket_id'])
        return context


class TicketCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = TicketSoporte
    form_class = TicketSoporteForm
    permission_required = 'tpe.add_ticketsoporte'
    raise_exception = True

    def form_valid(self, form):
        form.instance.abierto_por = self.request.user
        return super(TicketCreateView, self).form_valid(form)


class TicketCierreView(LoginRequiredMixin, UpdateView):
    model = TicketSoporte
    form_class = TicketCierreForm

    def form_valid(self, form):
        form.instance.cerrado_por = self.request.user
        form.instance.fecha_cierre = datetime.today()
        return super(TicketCierreView, self).form_valid(form)


class TicketRegistroCreateView(LoginRequiredMixin, CreateView):
    model = TicketRegistro
    form_class = TicketRegistroForm

    def form_valid(self, form):
        form.instance.ticket = TicketSoporte.objects.get(id=self.kwargs['ticket_id'])
        form.instance.fecha = datetime.today()
        form.instance.usuario = self.request.user
        return super(TicketRegistroCreateView, self).form_valid(form)
