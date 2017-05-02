from datetime import datetime, timedelta
from django.urls import reverse_lazy
from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.tpe.models import (
    Equipamiento, Garantia, TicketReparacion,
    TicketSoporte, TicketReparacionRepuesto)
from apps.tpe.forms import TicketReparacionRepuestoAuthForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'main/index.html'

    def get_widgets(self):
        widgets = []

        if self.request.user.groups.filter(name='tpe').exists():
            today = datetime.now()
            equipamiento_list = Equipamiento.objects.filter(fecha__year=today.year)
            widgets.append({
                'queryset': '',
                'template_name': 'widgets/tpe_equipamiento_chart.html',
                'media_js': {
                    'js/distributed/Chart.min.js'
                },
                'extra': {
                    'url': reverse_lazy('equipamiento_list_home'),
                    'equipamiento_total': equipamiento_list.count(),
                    'computadoras_total': sum(e.cantidad_equipo for e in equipamiento_list),
                    'alumnos_total': sum(e.poblacion.total_alumno for e in equipamiento_list if e.poblacion),
                    'maestros_total': sum(e.poblacion.total_maestro for e in equipamiento_list if e.poblacion)
                }
            })
            widgets.append({
                'queryset': '',
                'template_name': 'widgets/tpe_equipamiento_calendario.html',
                'media_css': [
                    'css/fullcalendar.min.css',
                ],
                'media_js': [
                    'js/distributed/moment.min.js',
                    'js/distributed/fullcalendar.min.js',
                    'js/distributed/fullcalendar.es.js',
                ],
                'extra': {
                    'url_validacion': reverse_lazy('validacion_list_home'),
                    'url_equipamiento': reverse_lazy('equipamiento_calendario_home'),
                }
            })

        if self.request.user.groups.filter(name='garantia').exists():
            widgets.append({
                'queryset': Garantia.objects.filter(
                    fecha_vencimiento__gte=datetime.now(),
                    fecha_vencimiento__lte=(datetime.now() + timedelta(days=21))),
                'template_name': 'widgets/tpe_garantia_pendiente.html'
            })
            widgets.append({
                'queryset': TicketSoporte.objects.filter(cerrado=False),
                'template_name': 'widgets/tpe_tickets_abiertos.html'
            })

        if self.request.user.groups.filter(name='tpe_tecnico').exists():
            widgets.append({
                'queryset': TicketReparacion.objects.filter(
                    tecnico_asignado=self.request.user,
                    ticket__cerrado=False,
                    solucion_tipo=None),
                'template_name': 'widgets/tpe_reparacion_list.html'
            })

        if self.request.user.groups.filter(name='tpe_admin').exists():
            widgets.append({
                'queryset': TicketReparacionRepuesto.objects.filter(
                    reparacion__ticket__cerrado=False,
                    autorizado=False,
                    rechazado=False,),
                'template_name': 'widgets/tpe_repuestos_pendientes.html',
                'extra': {
                    'repuesto_auth_form': TicketReparacionRepuestoAuthForm(initial={'autorizado': True, 'rechazado': False}),
                    'repuesto_reject_form': TicketReparacionRepuestoAuthForm(initial={'autorizado': False, 'rechazado': True})
                }
            })
        return widgets

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['widgets'] = self.get_widgets()
        return context
