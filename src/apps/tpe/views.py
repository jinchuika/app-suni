from django.utils.timezone import datetime
from django.shortcuts import reverse
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, UpdateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, GroupRequiredMixin, CsrfExemptMixin, JsonRequestResponseMixin

from apps.main.mixins import InformeMixin
from apps.escuela.views import EscuelaDetail
from apps.tpe.models import Equipamiento, Garantia, TicketSoporte, TicketRegistro, Monitoreo
from apps.tpe.forms import EquipamientoNuevoForm, EquipamientoForm, GarantiaForm, TicketSoporteForm, TicketCierreForm, TicketRegistroForm, EquipamientoListForm, MonitoreoListForm


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


class EquipamientoListView(InformeMixin):
    form_class = EquipamientoListForm
    template_name = 'tpe/equipamiento_list.html'
    filter_list = {
        'codigo': 'escuela__codigo',
        'nombre': 'escuela__nombre__contains',
        'direccion': 'escuela__direccion__contains',
        'municipio': 'escuela__municipio',
        'departamento': 'escuela__municipio__departamento',
        'nivel': 'escuela__nivel',
        'equipamiento_id': 'id',
        'cooperante_tpe': 'cooperante__in',
        'fecha_min': 'fecha__gte',
        'fecha_max': 'fecha__lte'
    }
    queryset = Equipamiento.objects.all()

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
                'tipo_red': str(equipamiento.tipo_red) if equipamiento.red else 'No',
                'cooperante': [
                    {'nombre': cooperante.nombre, 'url': cooperante.get_absolute_url()}
                    for cooperante in equipamiento.cooperante.all()],
                'proyecto': [
                    {'nombre': proyecto.nombre, 'url': proyecto.get_absolute_url()}
                    for proyecto in equipamiento.proyecto.all()]
            } for equipamiento in queryset
        ]
        return var


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


class MonitoreoCreateView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    require_json = True

    def post(self, request, *args, **kwargs):
        try:
            equipamiento_id = self.kwargs["equipamiento_id"]
            equipamiento = Equipamiento.objects.filter(id=equipamiento_id)
            comentario = self.request_json["comentario"]
            if not len(comentario) or len(equipamiento) == 0:
                raise KeyError
        except KeyError:
            error_dict = {u"message": u"Sin comentario"}
            return self.render_bad_request_response(error_dict)
        monitoreo = Monitoreo(equipamiento=equipamiento[0], creado_por=self.request.user, comentario=comentario)
        monitoreo.save()
        return self.render_json_response({
            "equipamiento_id": monitoreo.equipamiento.id,
            "comentario": monitoreo.comentario,
            "fecha": str(monitoreo.fecha),
            "usuario": str(monitoreo.creado_por.perfil)
        })


class MonitoreoListView(InformeMixin):
    form_class = MonitoreoListForm
    template_name = 'tpe/monitoreo_list.html'
    queryset = Monitoreo.objects.all().order_by('equipamiento', 'fecha')
    filter_list = {
        'fecha_min': 'fecha__gte',
        'fecha_max': 'fecha__lte',
        'usuario': 'creado_por__perfil__id'
    }

    def create_response(self, queryset):
        var = [
            {
                'entrega': monitoreo.equipamiento.id,
                'entrega_url': monitoreo.equipamiento.get_absolute_url(),
                'escuela': str(monitoreo.equipamiento.escuela),
                'escuela_url': monitoreo.equipamiento.escuela.get_absolute_url(),
                'departamento': str(monitoreo.equipamiento.escuela.departamento),
                'municipio': str(monitoreo.equipamiento.escuela.municipio.nombre),
                'comentario': monitoreo.comentario,
                'fecha': monitoreo.fecha,
                'usuario': str(monitoreo.creado_por.perfil),
            } for monitoreo in queryset
        ]
        return var
