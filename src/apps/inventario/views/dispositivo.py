from django.shortcuts import reverse
from django.views.generic import DetailView, UpdateView, CreateView
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from apps.inventario import models as inv_m
from apps.inventario import forms as inv_f


class TecladoUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para actualizar la :class:`Teclado` con sus respectivos campos
    """
    model = inv_m.Teclado
    form_class = inv_f.TecladoForm
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
    template_name = 'inventario/Dispositivos/Teclados/teclado_form.html'


class TecladoDetailView(LoginRequiredMixin, DetailView):
    """Vista para detalle de :class:`Teclado`,  con sus respectivos filtros
    """
    model = inv_m.Teclado
    template_name = 'inventario/Dispositivos/Teclados/teclado_detail.html'
    slug_field = "triage"
    slug_url_kwarg = "triage"
    query_pk_and_slug = True
