from django.shortcuts import reverse
from django.views.generic import DetailView, ListView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin, GroupRequiredMixin, CsrfExemptMixin, JsonRequestResponseMixin
)
from apps.main.mixins import InformeMixin
from apps.inventario import models as inv_m
from apps.inventario import forms as inv_f


class SoftwareListView(PermissionRequiredMixin, ListView):
    model = inv_m.Software
    template_name = 'inventario/software/software_list.html'
    permission_required = ''


class SoftwareCreateView(LoginRequiredMixin, CreateView):
    form_class = inv_f.SoftwareCreateForm
    template_name = 'inventario/software/software_add.html'

    def get_success_url(self):
        return reverse('software_list')


class SoftwareDetailView(LoginRequiredMixin, DetailView):
    model = inv_m.Software
    template_name = 'inventario/software/software_detail.html'


class VersionSistemaListView(LoginRequiredMixin, ListView):
    model = inv_m.VersionSistema
    template_name = 'inventario/software/versionsistema_list.html'


class VersionSistemaCreateView(LoginRequiredMixin, CreateView):
    form_class = inv_f.VersionSistemaForm
    template_name = 'inventario/software/versionsistema_add.html'

    def get_success_url(self):
        return reverse('versionsistema_list')


class VersionSistemaDetailView(LoginRequiredMixin, DetailView):
        model = inv_m.VersionSistema
        template_name = 'inventario/software/versionsistema_detail.html'
