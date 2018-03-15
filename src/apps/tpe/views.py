import math
from django.shortcuts import reverse
from django.db.models import Count
from django.utils.timezone import datetime
from django.views.generic import DetailView, ListView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin, GroupRequiredMixin,
    CsrfExemptMixin, JsonRequestResponseMixin)

from apps.main.mixins import InformeMixin
from apps.escuela.views import EscuelaDetail
from apps.escuela.models import Escuela
from apps.tpe import models as tpe_m
from apps.tpe import forms as tpe_f


class EquipamientoCrearView(PermissionRequiredMixin, CreateView):
    model = tpe_m.Equipamiento
    form_class = tpe_f.EquipamientoNuevoForm
    permission_required = 'tpe.add_equipamiento'
    redirect_unauthenticated_users = True
    raise_exception = True

    def get_success_url(self):
        return reverse(
            'escuela_equipamiento_update',
            kwargs={'pk': self.object.escuela.id, 'id_equipamiento': self.object.id})


class EquipamientoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    """Vista para editar un :model:`tpe.Equipamiento`. Solo funciona para
    recibir un `EquipamientoForm` mediante POST y actualizar los datos,
    pero no muestra ningún template con el método GET.
    """

    model = tpe_m.Equipamiento
    form_class = tpe_f.EquipamientoForm
    permission_required = 'tpe.change_equipamiento'
    redirect_unauthenticated_users = False
    raise_exception = True


class EquipamientoDetailView(EscuelaDetail):

    def get_context_data(self, **kwargs):
        id_equipamiento = self.kwargs.pop('id_equipamiento')
        context = super(EquipamientoDetailView, self).get_context_data(**kwargs)
        context['equipamiento_detail'] = id_equipamiento
        return context


class EquipamientoListView(LoginRequiredMixin, FormView):
    """Vista para listado de :class:`Equipamiento`. Obtiene los datos usando DRF.
    """
    form_class = tpe_f.EquipamientoListForm
    template_name = 'tpe/equipamiento_list.html'


class EquipamientoInformeView(EquipamientoListView):
    """Informe extendido de :class:`Equipamiento`s. Contiene muchos más datos que la clase de la
    cual hereda sus atributos, pero reutiliza el mismo formulario para hacer los filtros.
    """
    template_name = 'tpe/equipamiento_informe.html'


class EquipamientoListHomeView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request, *args, **kwargs):
        today = datetime.now()
        equipamiento_list = {'equipamiento': [], 'renovacion': []}
        for i in range(1, 13):
            equipamiento_list['equipamiento'].append(
                tpe_m.Equipamiento.objects.filter(
                    fecha__year=today.year,
                    fecha__month=i,
                    renovacion=False)
                .count())
            equipamiento_list['renovacion'].append(
                tpe_m.Equipamiento.objects.filter(
                    fecha__year=today.year,
                    fecha__month=i,
                    renovacion=True)
                .count())
        return self.render_json_response(equipamiento_list)


class EquipamientoMapView(CsrfExemptMixin, JsonRequestResponseMixin, TemplateView):
    """Vista para mostrar el mapa de los :class:`Equipamiento`s realizados.

    Todo:
        Esta vista probablemente se cambiará en el futuro para utilizar las nuevas herramientas
        de dashboards e informes dinámicos. Parecido a `apps.ie.views.MapDashboardView`.
    """
    template_name = 'tpe/map.html'

    def get_context_data(self, **kwargs):
        context = super(EquipamientoMapView, self).get_context_data(**kwargs)
        context['equipamientos'] = tpe_m.Equipamiento.objects.count()
        context['escuelas'] = Escuela.objects.annotate(
            num_equipamiento=Count('equipamiento')).filter(num_equipamiento__gt=0).count()
        return context

    def post(self, request, *args, **kwargs):
        page = 30
        pages = int(math.floor(tpe_m.Equipamiento.objects.all().count() / page)) + 1
        current_page = int(self.request.POST.get('page', 1))
        desde = (current_page - 1) * page
        hasta = current_page * page
        equipamiento_list = tpe_m.Equipamiento.objects.all()[desde:hasta]
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
    """Listado de las :class:`Garantia`s de los :class:`Equipamiento`s."""
    model = tpe_m.Garantia
    template_name = 'tpe/garantia_list.html'
    group_required = [u"garantia", u"tpe_admin"]
    raise_exception = True


class GarantiaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = tpe_m.Garantia
    form_class = tpe_f.GarantiaForm
    template_name = 'tpe/garantia_add.html'
    permission_required = 'tpe.add_garantia'
    redirect_unauthenticated_users = False
    raise_exception = True

    def form_valid(self, form):
        form.instance.id = form.cleaned_data['equipamiento'].id
        return super(GarantiaCreateView, self).form_valid(form)


class GarantiaDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = tpe_m.Garantia
    template_name = 'tpe/garantia_detail.html'
    group_required = [u"garantia", u"tpe_admin"]
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(GarantiaDetailView, self).get_context_data(**kwargs)
        context['ticket_form'] = tpe_f.TicketSoporteForm(initial={'garantia': self.object})
        context['ticket_cerrado_form'] = tpe_f.TicketCierreForm(initial={'cerrado': True})
        context['ticket_registro_form'] = tpe_f.TicketRegistroForm()
        context['ticket_registro_update_form'] = tpe_f.TicketRegistroUpdateForm()
        context['ticket_reparacion_form'] = tpe_f.TicketReparacionForm()
        context['ticket_transporte_form'] = tpe_f.TicketTransporteForm()

        if 'ticket_id' in self.kwargs:
            context['ticket_detail'] = self.kwargs['ticket_id']
        return context


class GarantiaPrintDetalle(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request, *args, **kwargs):
        ticket = tpe_m.TicketSoporte.objects.get(id=self.request.POST.get('ticket_id'))
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
        ticket = tpe_m.TicketSoporte.objects.get(id=self.request.POST.get('ticket_id'))
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
    model = tpe_m.TicketSoporte
    form_class = tpe_f.TicketSoporteForm
    permission_required = 'tpe.add_ticketsoporte'
    raise_exception = True

    def form_valid(self, form):
        form.instance.abierto_por = self.request.user
        form.instance.fecha_abierto = datetime.today()
        return super(TicketCreateView, self).form_valid(form)


class TicketCierreView(LoginRequiredMixin, UpdateView):
    model = tpe_m.TicketSoporte
    form_class = tpe_f.TicketCierreForm

    def form_valid(self, form):
        form.instance.cerrado_por = self.request.user
        form.instance.fecha_cierre = datetime.today()
        return super(TicketCierreView, self).form_valid(form)


class TicketRegistroCreateView(LoginRequiredMixin, CreateView):
    model = tpe_m.TicketRegistro
    form_class = tpe_f.TicketRegistroForm

    def form_valid(self, form):
        form.instance.ticket = tpe_m.TicketSoporte.objects.get(id=self.kwargs['ticket_id'])
        form.instance.fecha = datetime.today()
        form.instance.creado_por = self.request.user
        return super(TicketRegistroCreateView, self).form_valid(form)


class TicketRegistroUpdateView(LoginRequiredMixin, UpdateView):
    model = tpe_m.TicketRegistro
    form_class = tpe_f.TicketRegistroUpdateForm


class TicketReparacionCreateView(LoginRequiredMixin, CreateView):
    model = tpe_m.TicketReparacion
    form_class = tpe_f.TicketReparacionForm

    def form_valid(self, form):
        form.instance.ticket = tpe_m.TicketSoporte.objects.get(id=self.kwargs['ticket_id'])
        form.instance.fecha_inicio = datetime.today()
        form.instance.estado = tpe_m.TicketReparacionEstado.objects.first()
        return super(TicketReparacionCreateView, self).form_valid(form)


class ReparacionListView(InformeMixin):
    form_class = tpe_f.TicketReparacionListForm
    template_name = 'tpe/reparacion_list.html'
    filter_list = {
        'estado': 'estado',
    }
    queryset = tpe_m.TicketReparacion.objects.all()

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
    model = tpe_m.TicketReparacion
    form_class = tpe_f.TicketReparacionUpdateForm
    template_name = 'tpe/reparacion_update.html'

    def get_context_data(self, **kwargs):
        context = super(ReparacionUpdateView, self).get_context_data(**kwargs)
        context['repuesto_form'] = tpe_f.TicketReparacionRepuestoForm(
            initial={'reparacion': self.object})
        if self.request.user.groups.filter(name='tpe_admin').exists():
            context['repuesto_auth_form'] = tpe_f.TicketReparacionRepuestoAuthForm(
                initial={'autorizado': True, 'rechazado': False})
            context['repuesto_reject_form'] = tpe_f.TicketReparacionRepuestoAuthForm(
                initial={'autorizado': False, 'rechazado': True})
        return context

    def form_valid(self, form):
        solucion_tipo = form.cleaned_data['solucion_tipo']
        if solucion_tipo is not None:
            form.instance.fecha_fin = datetime.today()
        if solucion_tipo is not None and solucion_tipo.id != 1:
            form.instance.estado = tpe_m.TicketReparacionEstado.objects.get(id=2)
        else:
            form.instance.estado = tpe_m.TicketReparacionEstado.objects.get(id=3)
        return super(ReparacionUpdateView, self).form_valid(form)


class ReparacionRepuestoCreateView(CreateView):
    model = tpe_m.TicketReparacionRepuesto
    form_class = tpe_f.TicketReparacionRepuestoForm

    def get_success_url(self):
        return reverse('reparacion_update', kwargs={'pk': self.object.reparacion.id})


class ReparacionRepuestoUpdateView(GroupRequiredMixin, UpdateView):
    model = tpe_m.TicketReparacionRepuesto
    form_class = tpe_f.TicketReparacionRepuestoAuthForm
    group_required = [u"tpe_admin", ]
    raise_exception = True

    def form_valid(self, form):
        form.instance.autorizado_por = self.request.user
        form.instance.fecha_autorizado = datetime.today()
        return super(ReparacionRepuestoUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('reparacion_update', kwargs={'pk': self.object.reparacion.id})


class TicketTransporteCreateView(LoginRequiredMixin, CreateView):
    model = tpe_m.TicketTransporte
    form_class = tpe_f.TicketTransporteForm

    def form_valid(self, form):
        form.instance.ticket = tpe_m.TicketSoporte.objects.get(id=self.kwargs['ticket_id'])
        return super(TicketTransporteCreateView, self).form_valid(form)


class MonitoreoCreateView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    require_json = True

    def post(self, request, *args, **kwargs):
        try:
            equipamiento_id = self.kwargs["equipamiento_id"]
            equipamiento = tpe_m.Equipamiento.objects.filter(id=equipamiento_id)
            comentario = self.request_json["comentario"]
            if not len(comentario) or len(equipamiento) == 0:
                raise KeyError
        except KeyError:
            error_dict = {u"message": u"Sin comentario"}
            return self.render_bad_request_response(error_dict)
        monitoreo = tpe_m.Monitoreo(
            equipamiento=equipamiento[0],
            creado_por=self.request.user,
            comentario=comentario)
        monitoreo.save()
        return self.render_json_response({
            "equipamiento_id": monitoreo.equipamiento.id,
            "comentario": monitoreo.comentario,
            "fecha": str(monitoreo.fecha),
            "usuario": str(monitoreo.creado_por.perfil)
        })


class MonitoreoListView(InformeMixin):
    form_class = tpe_f.MonitoreoListForm
    template_name = 'tpe/monitoreo_list.html'
    queryset = tpe_m.Monitoreo.objects.all().order_by('equipamiento', 'fecha')
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
    form_class = tpe_f.TicketInformeForm
    template_name = 'tpe/ticket_informe.html'
    filter_list = {
        'estado': 'cerrado',
        'fecha_abierto_min': 'fecha_abierto__gte',
        'fecha_abierto_max': 'fecha_abierto__lte',
        'fecha_cierre_min': 'fecha_cierre__gte',
        'fecha_cierre_max': 'fecha_cierre__lte'
    }
    queryset = tpe_m.TicketSoporte.objects.all()

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
    form_class = tpe_f.TicketReparacionInformeForm
    template_name = 'tpe/ticket_reparacion_informe.html'
    filter_list = {
        'estado': 'estado',
        'ticket': 'ticket',
        'tipo_dispositivo': 'tipo_dispositivo',
        'triage': 'triage',
        'tecnico_asignado': 'tecnico_asignado'
    }
    queryset = tpe_m.TicketReparacion.objects.all()

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
        ticket_abierto_list = tpe_m.TicketSoporte.objects.filter(
            fecha_abierto__range=[inicio_filtro, fin_filtro])
        ticket_cerrado_list = tpe_m.TicketSoporte.objects.filter(
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


class TicketRecepcionPrintView(LoginRequiredMixin, DetailView):

    """Para generar un formulario de recepción de garantía en base
    a un :model:`tpe.TicketSoporte`.
    """

    model = tpe_m.TicketSoporte
    template_name = 'tpe/ticket_recepcion_print.html'

    def get_context_data(self, **kwargs):
        """Elige la recepción del equipo del listado de :model:`tpe.TicketRegistro`
        relacionados al :model:`tpe.TicketSoporte`.
        """
        context = super(TicketRecepcionPrintView, self).get_context_data(**kwargs)
        context['recepcion'] = self.object.registros.filter(tipo__id=3).first()
        return context


class TicketEntregaPrintView(LoginRequiredMixin, DetailView):

    """Para generar un formulario de entrega de garantía en base
    a un :model:`tpe.TicketSoporte`.
    """

    model = tpe_m.TicketSoporte
    template_name = 'tpe/ticket_entrega_print.html'

    def get_context_data(self, **kwargs):
        """Elige la entrega del equipo del listado de :model:`tpe.TicketRegistro`
        relacionados al :model:`tpe.TicketSoporte`.
        """
        context = super(TicketEntregaPrintView, self).get_context_data(**kwargs)
        context['entrega'] = self.object.registros.filter(tipo__id=4).first()
        return context


class MonitoreoDetailView(LoginRequiredMixin, DetailView):

    """Vista para detalle de :model:`tpe.Monitoreo`. Se encarga de
    administrar los :model:`tpe.EvaluacionMonitoreo`.
    """

    model = tpe_m.Monitoreo
    template_name = 'tpe/monitoreo_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MonitoreoDetailView, self).get_context_data(**kwargs)
        if self.object.evaluaciones.count() == 0:
            context['evaluacion_form'] = tpe_f.EvaluacionMonitoreoCreateForm(
                instance=self.object,
                initial={'evaluacion': True})
        return context


class MonitoreoUpdateView(LoginRequiredMixin, UpdateView):
    form_class = tpe_f.EvaluacionMonitoreoCreateForm
    model = tpe_m.Monitoreo

    def form_valid(self, form):
        if form.cleaned_data['evaluacion'] is True:
            form.instance.crear_evaluaciones()
        return super(MonitoreoUpdateView, self).form_valid(form)


class EvaluacionMonitoreoInformeView(LoginRequiredMixin, FormView):

    """
    Vista para generar informes de class:`EvaluacionMonitoreo`.
    Realiza una conexión a DRF para funcionar.
    """

    form_class = tpe_f.MonitoreoListForm
    template_name = 'tpe/evaluacionmonitoreo_informe.html'


class DispositivoReparacionListView(LoginRequiredMixin, FormView):
    form_class = tpe_f.DispositivoReparacionListForm
    template_name = 'tpe/dispositivo_reparacion_list.html'

class VisitaInformeView( LoginRequiredMixin, CreateView ):
    """Vista   para obtener los datos de la Visitas mediante una :class:`VisitaMonitoreo`
    Funciona  para recibir los datos de un  'VisitaMonitoreoForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    form_class = tpe_f.VisitaMonitoreoCreateForm
    template_name = 'tpe/visita_add.html'

    def get_success_url(self):
        return reverse('visita_monitoreo_update', kwargs={'pk': self.object.id})


    def form_valid(self, form):
        form.instance.encargado = self.request.user
        form.instance.fecha_visita = datetime.today()
        form.instance.hora_inicio = datetime.now().time()
        form.instance.hora_final = datetime.now().time()
        return super(VisitaInformeView, self).form_valid(form)

class VisitaUpdateView(LoginRequiredMixin, UpdateView):
    model = tpe_m.VisitaMonitoreo
    form_class = tpe_f.VisitaMonitoreoForm
    template_name = 'tpe/visita_add.html'


class VisitaListView(LoginRequiredMixin, ListView):
    model = tpe_m.VisitaMonitoreo
    template_name = 'tpe/visita_list.html'
    raise_exception = True
    #form_class = tpe_f.VisitaMonitoreoForm

class VisitaDetailView(LoginRequiredMixin, DetailView):
    model = tpe_m.VisitaMonitoreo
    template_name = 'tpe/visita_detail.html'
    #form_class = tpe_f.VisitaMonitoreoForm
