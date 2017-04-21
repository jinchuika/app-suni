from datetime import datetime, timedelta
from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin
from apps.tpe.models import Garantia, TicketReparacion, TicketSoporte


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'main/index.html'

    def get_widgets(self):
        widgets = []
        if self.request.user.groups.filter(name='garantia').exists():
            widgets.append({
                'queryset': Garantia.objects.filter(
                    fecha_vencimiento__gte=datetime.now(),
                    fecha_vencimiento__lte=(datetime.now() + timedelta(days=15))),
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
                    solucion_tipo=None),
                'template_name': 'widgets/tpe_reparacion_list.html'
            })
        return widgets

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['widgets'] = self.get_widgets()
        return context
