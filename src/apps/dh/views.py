from datetime import datetime
from django.views.generic import View, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from braces.views import (
    LoginRequiredMixin, GroupRequiredMixin, CsrfExemptMixin,
    JsonRequestResponseMixin)

from apps.dh.forms import EventoDHForm
from apps.dh.models import EventoDH
from apps.mye.models import EscuelaCooperante, EscuelaProyecto


class EventoDHCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = [u"dejando_huella", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = EventoDH
    template_name = 'dh/evento_add.html'
    form_class = EventoDHForm

    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super(EventoDHCreateView, self).form_valid(form)


class EventoDHUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    group_required = [u"dejando_huella", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = EventoDH
    template_name = 'dh/evento_add.html'
    form_class = EventoDHForm


class EventoDHDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    group_required = [u"dejando_huella", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = EventoDH
    template_name = 'dh/evento_detail.html'


class CalendarioDHView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    group_required = [u"dejando_huella", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    template_name = 'dh/calendario.html'


class EventoDHCalendarHomeView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def get(self, request, *args, **kwargs):
        response = []
        inicio = datetime.strptime(self.request.GET.get('start'), '%Y-%m-%d')
        fin = datetime.strptime(self.request.GET.get('end'), '%Y-%m-%d')
        evento_list = EventoDH.objects.filter(
            fecha__gte=inicio,
            fecha__lte=fin)
        for evento in evento_list:
            response.append({
                'title': str(evento.titulo),
                'start': str(datetime.combine(evento.fecha, evento.hora_inicio)) if evento.hora_inicio else str(evento.fecha),
                'end': str(datetime.combine(evento.fecha, evento.hora_fin)) if evento.hora_fin else str(evento.fecha),
                'color': evento.tipo_evento.color,
                'url': evento.get_absolute_url()})
        return self.render_json_response(response)


class ReservacionListView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    group_required = [u"dejando_huella", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    template_name = 'dh/reservacion_list.html'

    def get_context_data(self, **kwargs):
        context = super(ReservacionListView, self).get_context_data(**kwargs)
        context['cooperante_list'] = EscuelaCooperante.objects.all()
        context['proyecto_list'] = EscuelaProyecto.objects.all()
        return context
