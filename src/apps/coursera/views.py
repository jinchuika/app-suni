# from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin, GroupRequiredMixin,
    CsrfExemptMixin, JsonRequestResponseMixin)
from django.views.generic import DetailView, ListView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from apps.coursera import models as coursera_m
from apps.coursera import forms as coursera_f

class MonitoreoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Vista para crear una escuela
    """
    model = coursera_m.Monitoreo
    permission_required = "coursera.add_monitoreo"
    template_name = 'coursera/monitoreo_add.html'
    raise_exception = True
    redirect_unauthenticated_users = True
    form_class = coursera_f.FormMonitoreoCrear

    def get_context_data(self, *args, **kwargs):
        context = super(MonitoreoCreateView, self).get_context_data(*args, **kwargs)
        context['registros'] = coursera_m.Monitoreo.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy('monitoreo_add')

class MonitoreoInformeView(FormView):
    template_name = 'coursera/monitoreo_informe.html'