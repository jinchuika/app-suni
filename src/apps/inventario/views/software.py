from django.shortcuts import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from apps.inventario import models as inv_m
from apps.inventario import forms as inv_f


class SoftwareListView(PermissionRequiredMixin, ListView):
    """Listado del :Model:`Software` con sus respectivos datos
    """

    model = inv_m.Software
    template_name = 'inventario/software/software_list.html'
    permission_required = ''


class SoftwareCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos de Software mediante una :class:`software`
    Funciona  para recibir los datos de un  'SoftwareCreateForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    form_class = inv_f.SoftwareCreateForm
    template_name = 'inventario/software/software_add.html'

    def get_success_url(self):
        return reverse('software_list')


class SoftwareDetailView(LoginRequiredMixin, DetailView):
    """Vista Encargada de Mostrar Los Detalles de un software seleccionado
    """
    model = inv_m.Software
    template_name = 'inventario/software/software_detail.html'


class VersionSistemaListView(LoginRequiredMixin, ListView):
    """Listado del :Model:`Version` con sus respectivos datos.
    """
    model = inv_m.VersionSistema
    template_name = 'inventario/software/versionsistema_list.html'


class VersionSistemaCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos de Version de Sistema mediante una :class:`VersionSistema`
    Funciona  para recibir los datos de un  'VersionSistemaForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    form_class = inv_f.VersionSistemaForm
    template_name = 'inventario/software/versionsistema_add.html'

    def get_success_url(self):
        return reverse('versionsistema_list')


class VersionSistemaDetailView(LoginRequiredMixin, DetailView):
    """Vista Encargada de Mostrar Los Detalles de una version del sistema seleccionado
    """
    model = inv_m.VersionSistema
    template_name = 'inventario/software/versionsistema_detail.html'
