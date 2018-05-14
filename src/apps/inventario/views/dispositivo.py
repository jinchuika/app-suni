from django.shortcuts import reverse
from django.views.generic import DetailView
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from apps.inventario import models as inv_m
from apps.inventario import forms as inv_f


class TecladoDetailView(LoginRequiredMixin, DetailView):
    model = inv_m.Teclado
    template_name = 'inventario/Dispositivo/Teclados/teclado_detail.html'
