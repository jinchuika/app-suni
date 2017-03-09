from django.http import JsonResponse
from django.utils.timezone import datetime
from django.utils.dateparse import parse_date
from django.shortcuts import reverse
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, UpdateView, FormView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, GroupRequiredMixin, CsrfExemptMixin, JsonRequestResponseMixin

from apps.escuela.views import EscuelaDetail
from apps.tpe.models import Equipamiento, Garantia, TicketSoporte, TicketRegistro
from apps.tpe.forms import EquipamientoNuevoForm, EquipamientoForm, GarantiaForm, TicketSoporteForm, TicketCierreForm, TicketRegistroForm, EquipamientoListForm


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


class EquipamientoDetailView(EscuelaDetail):

    def get_context_data(self, **kwargs):
        id_equipamiento = self.kwargs.pop('id_equipamiento')
        context = super(EquipamientoDetailView, self).get_context_data(**kwargs)
        context['equipamiento_detail'] = id_equipamiento
        return context


class EquipamientoListView(CsrfExemptMixin, LoginRequiredMixin, FormView):
    form_class = EquipamientoListForm
    template_name = 'tpe/equipamiento_list.html'

    def get_queryset(self, filtros):
        queryset = Equipamiento.objects.all()
        if filtros.get('codigo', False):
            queryset = queryset.filter(escuela__codigo=filtros.get('codigo'))
        if filtros.get('nombre', False):
            queryset = queryset.filter(escuela__nombre__contains=filtros.get('nombre'))
        if filtros.get('direccion', False):
            queryset = queryset.filter(escuela__direccion__contains=filtros.get('direccion'))
        if filtros.get('municipio', False):
            queryset = queryset.filter(escuela__municipio=filtros.get('municipio'))
        if filtros.get('departamento', False):
            queryset = queryset.filter(escuela__municipio__departamento=filtros.get('departamento'))
        if filtros.get('nivel', False):
            queryset = queryset.filter(escuela__nivel=filtros.get('nivel'))
        if filtros.get('equipamiento_id', False):
            queryset = queryset.filter(id=filtros.get('equipamiento_id'))
        if filtros.get('cooperante_tpe', False):
            queryset = queryset.filter(cooperante__in=filtros.get('cooperante_tpe'))
        if filtros.get('fecha_min', False):
            print('fecha_min')
            queryset = queryset.filter(fecha__gte=parse_date(filtros.get('fecha_min')))
        if filtros.get('fecha_max', False):
            print('fecha_max')
            queryset = queryset.filter(fecha__lte=parse_date(filtros.get('fecha_max')))
        return queryset

    def create_response(self, queryset):
        var = [
            {
                'entrega': equipamiento.id,
                'entrega_url': equipamiento.get_absolute_url(),
                'escuela': str(equipamiento.escuela),
                'escuela_url': equipamiento.escuela.get_absolute_url(),
                'fecha': str(equipamiento.fecha),
                'renovacion': 'Sí' if equipamiento.renovacion else 'No',
                'khan': 'Sí' if equipamiento.servidor_khan else 'No',
                'cantidad_equipo': equipamiento.cantidad_equipo,
                'tipo_red': str(equipamiento.tipo_red) if equipamiento.red else 'No'
            } for equipamiento in queryset
        ]
        return var

    def post(self, request, *args, **kwargs):
        equipamiento_list = self.get_queryset(self.request.POST)
        return JsonResponse(self.create_response(equipamiento_list), safe=False)


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
