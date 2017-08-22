from math import floor
from django.shortcuts import reverse
from django.db.models import Count, Q
from django.utils.timezone import datetime
from django.views.generic import DetailView, ListView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin, GroupRequiredMixin,
    CsrfExemptMixin, JsonRequestResponseMixin)

from apps.main.mixins import InformeMixin
from apps.escuela.views import EscuelaDetail
from apps.escuela.models import Escuela
from apps.tpe.models import (
    Equipamiento, Garantia, TicketSoporte, TicketRegistro,
    Monitoreo, TicketReparacionEstado, TicketReparacion, TicketReparacionRepuesto,
    TicketTransporte)
from apps.tpe.forms import (
    EquipamientoNuevoForm, EquipamientoForm, GarantiaForm, TicketSoporteForm,
    TicketCierreForm, TicketRegistroForm, EquipamientoListForm, MonitoreoListForm,
    TicketReparacionForm, TicketReparacionListForm, TicketReparacionUpdateForm,
    TicketReparacionRepuestoForm, TicketReparacionRepuestoAuthForm, TicketTransporteForm,
    TicketRegistroUpdateForm, TicketInformeForm, TicketReparacionInformeForm)


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
        'nombre': 'escuela__nombre__icontains',
        'direccion': 'escuela__direccion__icontains',
        'municipio': 'escuela__municipio',
        'departamento': 'escuela__municipio__departamento',
        'nivel': 'escuela__nivel',
        'equipamiento_id': 'id',
        'cooperante_tpe': 'cooperante',
        'proyecto_tpe': 'proyecto',
        'fecha_min': 'fecha__gte',
        'fecha_max': 'fecha__lte'
    }
    queryset = Equipamiento.objects.all()

    def create_response(self, queryset):
        var = [
            {
                'entrega': equipamiento.id,
                'entrega_url': equipamiento.get_absolute_url(),
                'escuela': equipamiento.escuela.nombre,
                'escuela_url': equipamiento.escuela.get_absolute_url(),
                'escuela_codigo': equipamiento.escuela.codigo,
                'fecha': str(equipamiento.fecha),
                'renovacion': 'Sí' if equipamiento.renovacion else 'No',
                'khan': 'Sí' if equipamiento.servidor_khan else 'No',
                'cantidad': equipamiento.cantidad_equipo,
                'tipo_red': str(equipamiento.tipo_red) if equipamiento.red else 'No',
                'cooperante': [{
                    'nombre': cooperante.nombre,
                    'url': cooperante.get_absolute_url()}
                    for cooperante in equipamiento.cooperante.all()],
                'proyecto': [{
                    'nombre': proyecto.nombre,
                    'url': proyecto.get_absolute_url()}
                    for proyecto in equipamiento.proyecto.all()],
            } for equipamiento in queryset
        ]
        return var


class EquipamientoInformeView(EquipamientoListView):
    template_name = 'tpe/equipamiento_informe.html'

    def create_response(self, queryset):
        return [
            {
                'entrega': equipamiento.id,
                'escuela': '<a href="{}">{} <br /></a>'.format(
                    equipamiento.escuela.get_absolute_url(),
                    equipamiento.escuela.nombre),
                'codigo': equipamiento.escuela.codigo,
                'departamento': str(equipamiento.escuela.municipio.departamento),
                'municipio': str(equipamiento.escuela.municipio),
                'direccion': str(equipamiento.escuela.direccion),
                'fecha': str(equipamiento.fecha),
                'renovacion': 'Sí' if equipamiento.renovacion else 'No',
                'khan': 'Sí' if equipamiento.servidor_khan else 'No',
                'cantidad': equipamiento.cantidad_equipo,
                'tipo_red': str(equipamiento.tipo_red) if equipamiento.red else 'No',
                'cooperante': [{
                    'cooperante': '<a href="{}">{}</a>'.format(
                        cooperante.get_absolute_url(),
                        cooperante.nombre)}
                    for cooperante in equipamiento.cooperante.all()],
                'proyecto': [{
                    'proyecto': '<a href="{}">{}</a>'.format(
                        proyecto.get_absolute_url(),
                        proyecto.nombre)}
                    for proyecto in equipamiento.proyecto.all()],
                'alumnas': equipamiento.poblacion.alumna if equipamiento.poblacion else "",
                'alumnos': equipamiento.poblacion.alumno if equipamiento.poblacion else "",
                'total_alumnos': equipamiento.poblacion.total_alumno if equipamiento.poblacion else "",
                'maestras': equipamiento.poblacion.maestra if equipamiento.poblacion else "",
                'maestros': equipamiento.poblacion.maestro if equipamiento.poblacion else "",
                'total_maestros': equipamiento.poblacion.total_maestro if equipamiento.poblacion else "",
            } for equipamiento in queryset
        ]


class EquipamientoListHomeView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request, *args, **kwargs):
        today = datetime.now()
        equipamiento_list = []
        for i in range(1, 13):
            equipamiento_list.append(Equipamiento.objects.filter(fecha__year=today.year, fecha__month=i).count())
        return self.render_json_response(equipamiento_list)


class EquipamientoCalendarHomeView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def get(self, request, *args, **kwargs):
        response = []
        inicio = datetime.strptime(self.request.GET.get('start'), '%Y-%m-%d')
        fin = datetime.strptime(self.request.GET.get('end'), '%Y-%m-%d')
        equipamiento_list = Equipamiento.objects.filter(
            fecha__gte=inicio,
            fecha__lte=fin)
        for equipamiento in equipamiento_list:
            response.append({
                'title': str(equipamiento.escuela),
                'start': str(equipamiento.fecha),
                'url': equipamiento.get_absolute_url(),
                'tip_title': str(equipamiento.escuela.municipio),
                'tip_text': equipamiento.escuela.direccion})
        return self.render_json_response(response)


class EquipamientoMapView(CsrfExemptMixin, JsonRequestResponseMixin, TemplateView):
    template_name = 'tpe/map.html'

    def get_context_data(self, **kwargs):
        context = super(EquipamientoMapView, self).get_context_data(**kwargs)
        context['equipamientos'] = Equipamiento.objects.count()
        context['escuelas'] = Escuela.objects.annotate(num_equipamiento=Count('equipamiento')).filter(num_equipamiento__gt=0).count()
        return context

    def post(self, request, *args, **kwargs):
        page = 30
        pages = int(floor(Equipamiento.objects.all().count() / page)) + 1
        current_page = int(self.request.POST.get('page', 1))
        desde = (current_page - 1) * page
        hasta = current_page * page
        equipamiento_list = Equipamiento.objects.all()[desde:hasta]
        response_list = [{
            'info': '{}<br>{}<br>{}'.format(
                str(equipamiento.escuela),
                str(equipamiento.escuela.municipio),
                str(equipamiento.fecha)),
            'lat': equipamiento.escuela.mapa.lat,
            'lng': equipamiento.escuela.mapa.lng}
            for equipamiento in equipamiento_list
            if equipamiento.escuela.mapa]
        return self.render_json_response({
            'next': current_page != pages,
            'page': current_page + 1,
            'data': response_list})


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

    def form_valid(self, form):
        form.instance.id = form.cleaned_data['equipamiento'].id
        return super(GarantiaCreateView, self).form_valid(form)


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
        context['ticket_registro_update_form'] = TicketRegistroUpdateForm()
        context['ticket_reparacion_form'] = TicketReparacionForm()
        context['ticket_transporte_form'] = TicketTransporteForm()

        if 'ticket_id' in self.kwargs:
            context['ticket_detail'] = self.kwargs['ticket_id']
        return context


class GarantiaPrintDetalle(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request, *args, **kwargs):
        ticket = TicketSoporte.objects.get(id=self.request.POST.get('ticket_id'))
        return self.render_json_response({
            'escuela': "{}, {}, ({})".format(
                ticket.garantia.equipamiento.escuela,
                ticket.garantia.equipamiento.escuela.direccion,
                ticket.garantia.equipamiento.escuela.codigo),
            'garantia': ticket.garantia.id,
            'ticket': ticket.id,
            'registros': [{
                'tipo': str(registro.tipo),
                'fecha': registro.fecha,
                'usuario': registro.creado_por.get_full_name()
            } for registro in ticket.registros.all()],
            'reparaciones': [{
                'triage': reparacion.triage,
                'dispositivo': str(reparacion.tipo_dispositivo),
                'falla_reportada': reparacion.falla_reportada,
                'falla_encontrada': reparacion.falla_encontrada if reparacion.falla_encontrada else ""
            } for reparacion in ticket.reparaciones.all()],
            'descripcion': ticket.descripcion
        })


class TicketVisitaPrintDetalle(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request, *args, **kwargs):
        ticket = TicketSoporte.objects.get(id=self.request.POST.get('ticket_id'))
        return self.render_json_response({
            'escuela': "{}, {}, ({})".format(
                ticket.garantia.equipamiento.escuela,
                ticket.garantia.equipamiento.escuela.direccion,
                ticket.garantia.equipamiento.escuela.codigo),
            'garantia': ticket.garantia.id,
            'ticket': ticket.id,
            'descripcion': ticket.descripcion
        })


class TicketCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = TicketSoporte
    form_class = TicketSoporteForm
    permission_required = 'tpe.add_ticketsoporte'
    raise_exception = True

    def form_valid(self, form):
        form.instance.abierto_por = self.request.user
        form.instance.fecha_abierto = datetime.today()
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
        form.instance.creado_por = self.request.user
        return super(TicketRegistroCreateView, self).form_valid(form)


class TicketRegistroUpdateView(LoginRequiredMixin, UpdateView):
    model = TicketRegistro
    form_class = TicketRegistroUpdateForm


class TicketReparacionCreateView(LoginRequiredMixin, CreateView):
    model = TicketReparacion
    form_class = TicketReparacionForm

    def form_valid(self, form):
        form.instance.ticket = TicketSoporte.objects.get(id=self.kwargs['ticket_id'])
        form.instance.fecha_inicio = datetime.today()
        form.instance.estado = TicketReparacionEstado.objects.first()
        return super(TicketReparacionCreateView, self).form_valid(form)


class ReparacionListView(InformeMixin):
    form_class = TicketReparacionListForm
    template_name = 'tpe/reparacion_list.html'
    filter_list = {
        'estado': 'estado',
    }
    queryset = TicketReparacion.objects.all()

    def create_response(self, queryset):
        var = [
            {
                'ticket': '<a href="{}">{}</a>'.format(
                    reparacion.ticket.get_absolute_url(),
                    reparacion.ticket),
                'triage': reparacion.triage,
                'dispositivo': str(reparacion.tipo_dispositivo),
                'fecha_inicio': str(reparacion.fecha_inicio),
                'falla_reportada': reparacion.falla_reportada,
                'escuela': '<a href="{}">{}</a>'.format(
                    reparacion.ticket.garantia.equipamiento.escuela.get_absolute_url(),
                    reparacion.ticket.garantia.equipamiento.escuela)
            } for reparacion in queryset
        ]
        return var


class ReparacionUpdateView(LoginRequiredMixin, UpdateView):
    model = TicketReparacion
    form_class = TicketReparacionUpdateForm
    template_name = 'tpe/reparacion_update.html'

    def get_context_data(self, **kwargs):
        context = super(ReparacionUpdateView, self).get_context_data(**kwargs)
        context['repuesto_form'] = TicketReparacionRepuestoForm(initial={'reparacion': self.object})
        if self.request.user.groups.filter(name='tpe_admin').exists():
            context['repuesto_auth_form'] = TicketReparacionRepuestoAuthForm(initial={'autorizado': True, 'rechazado': False})
            context['repuesto_reject_form'] = TicketReparacionRepuestoAuthForm(initial={'autorizado': False, 'rechazado': True})
        return context

    def form_valid(self, form):
        solucion_tipo = form.cleaned_data['solucion_tipo']
        if solucion_tipo is not None:
            form.instance.fecha_fin = datetime.today()
        if solucion_tipo is not None and solucion_tipo.id != 1:
            form.instance.estado = TicketReparacionEstado.objects.get(id=2)
        else:
            form.instance.estado = TicketReparacionEstado.objects.get(id=3)
        return super(ReparacionUpdateView, self).form_valid(form)


class ReparacionRepuestoCreateView(CreateView):
    model = TicketReparacionRepuesto
    form_class = TicketReparacionRepuestoForm

    def get_success_url(self):
        return reverse('reparacion_update', kwargs={'pk': self.object.reparacion.id})


class ReparacionRepuestoUpdateView(GroupRequiredMixin, UpdateView):
    model = TicketReparacionRepuesto
    form_class = TicketReparacionRepuestoAuthForm
    group_required = [u"tpe_admin", ]
    raise_exception = True

    def form_valid(self, form):
        form.instance.autorizado_por = self.request.user
        form.instance.fecha_autorizado = datetime.today()
        return super(ReparacionRepuestoUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('reparacion_update', kwargs={'pk': self.object.reparacion.id})


class TicketTransporteCreateView(LoginRequiredMixin, CreateView):
    model = TicketTransporte
    form_class = TicketTransporteForm

    def form_valid(self, form):
        form.instance.ticket = TicketSoporte.objects.get(id=self.kwargs['ticket_id'])
        return super(TicketTransporteCreateView, self).form_valid(form)


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
        return [
            {
                'entrega': monitoreo.equipamiento.id,
                'entrega_url': monitoreo.equipamiento.get_absolute_url(),
                'escuela': str(monitoreo.equipamiento.escuela),
                'escuela_url': monitoreo.equipamiento.escuela.get_absolute_url(),
                'escuela_codigo': monitoreo.equipamiento.escuela.codigo,
                'departamento': str(monitoreo.equipamiento.escuela.municipio.departamento),
                'municipio': str(monitoreo.equipamiento.escuela.municipio.nombre),
                'comentario': monitoreo.comentario,
                'fecha': monitoreo.fecha,
                'usuario': str(monitoreo.creado_por.perfil),
            } for monitoreo in queryset
        ]


class TicketInformeView(InformeMixin):
    form_class = TicketInformeForm
    template_name = 'tpe/ticket_informe.html'
    filter_list = {
        'estado': 'cerrado',
        'fecha_abierto_min': 'fecha_abierto__gte',
        'fecha_abierto_max': 'fecha_abierto__lte',
        'fecha_cierre_min': 'fecha_cierre__gte',
        'fecha_cierre_max': 'fecha_cierre__lte'
    }
    queryset = TicketSoporte.objects.all()

    def create_response(self, queryset):
        var = [
            {
                'entrega': ticket.garantia.equipamiento.id,
                'escuela': {
                    'nombre': ticket.garantia.equipamiento.escuela.nombre,
                    'codigo': ticket.garantia.equipamiento.escuela.codigo,
                    'url': ticket.garantia.equipamiento.escuela.get_absolute_url()
                },
                'no_ticket': '<a href="{}">{}<a/>'.format(
                    ticket.get_absolute_url(),
                    ticket.id),
                'fecha_inicio': str(ticket.fecha_abierto),
                'fecha_fin': str(ticket.fecha_cierre) if ticket.fecha_cierre else "",
                'estado': 'Cerrado' if ticket.cerrado else 'Abierto',
                'costo_reparacion': ticket.get_costo_reparacion(),
                'costo_transporte': ticket.get_costo_transporte(),
                'costo_total': ticket.get_costo_total(),
            } for ticket in queryset
        ]
        return var


class TicketReparacionInformeView(InformeMixin):
    form_class = TicketReparacionInformeForm
    template_name = 'tpe/ticket_reparacion_informe.html'
    filter_list = {
        'estado': 'estado',
        'ticket': 'ticket',
        'tipo_dispositivo': 'tipo_dispositivo',
        'triage': 'triage',
        'tecnico_asignado': 'tecnico_asignado'
    }
    queryset = TicketReparacion.objects.all()

    def create_response(self, queryset):
        var = [
            {
                'entrega': reparacion.ticket.garantia.equipamiento.id,
                'escuela': {
                    'nombre': reparacion.ticket.garantia.equipamiento.escuela.nombre,
                    'codigo': reparacion.ticket.garantia.equipamiento.escuela.codigo,
                    'url': reparacion.ticket.garantia.equipamiento.escuela.get_absolute_url()
                },
                'no_ticket': '<a href="{}">{}<a/>'.format(
                    reparacion.ticket.get_absolute_url(),
                    reparacion.ticket.id),
                'triage': {
                    'triage': '{}-{}'.format(reparacion.tipo_dispositivo, reparacion.triage),
                    'url': reparacion.get_absolute_url()},
                'fecha_inicio': str(reparacion.fecha_inicio),
                'fecha_fin': str(reparacion.fecha_fin) if reparacion.fecha_fin else "",
                'falla_reportada': reparacion.falla_reportada,
                'falla_encontrada': reparacion.falla_encontrada,
                'solucion_detalle': reparacion.solucion_detalle,
                'estado': str(reparacion.estado),
                'tecnico_asignado': reparacion.tecnico_asignado.get_full_name(),
                'cooperante': [{
                    'nombre': cooperante.nombre,
                    'url': cooperante.get_absolute_url()}
                    for cooperante in reparacion.ticket.garantia.equipamiento.cooperante.all()],
            } for reparacion in queryset
        ]
        return var


class TicketCalendarView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def get(self, request, *args, **kwargs):
        response = []
        inicio_filtro = self.request.GET.get('start')
        fin_filtro = self.request.GET.get('end')
        ticket_abierto_list = TicketSoporte.objects.filter(
            fecha_abierto__range=[inicio_filtro, fin_filtro])
        ticket_cerrado_list = TicketSoporte.objects.filter(
            fecha_cierre__range=[inicio_filtro, fin_filtro], cerrado=True)
        for ticket in ticket_abierto_list:
            response.append({
                'title': 'Ticket {} (inicio)'.format(ticket.id),
                'start': str(ticket.fecha_abierto),
                'url': ticket.get_absolute_url(),
                'tip_title': 'Actual: Cerrado' if ticket.cerrado else 'Actual: Abierto',
                'tip_text': str(ticket.garantia.equipamiento.escuela)})
        for ticket in ticket_cerrado_list:
            response.append({
                'title': 'Ticket {} (fin)'.format(ticket.id),
                'start': str(ticket.fecha_abierto),
                'url': ticket.get_absolute_url(),
                'tip_title': 'Actual: Cerrado',
                'tip_text': str(ticket.garantia.equipamiento.escuela)})
        return self.render_json_response(response)


class CalendarioTPEView(LoginRequiredMixin, TemplateView):
    """Vista para el calendario de TPE."""

    template_name = 'tpe/calendario.html'
