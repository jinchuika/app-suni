from django.shortcuts import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, FormView

from django.http import JsonResponse
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from dal import autocomplete

from apps.mye.forms import InformeMyeForm, CooperanteForm, ProyectoForm, SolicitudVersionForm, SolicitudForm, SolicitudNuevaForm, ValidacionNuevaForm, ValidacionForm
from apps.mye.models import Cooperante, Proyecto, SolicitudVersion, Solicitud, Validacion
from apps.tpe.models import Equipamiento
from apps.main.models import Municipio


class CooperanteCrear(LoginRequiredMixin, CreateView):
    model = Cooperante
    template_name = 'mye/cooperante_form.html'
    form_class = CooperanteForm


class CooperanteDetalle(LoginRequiredMixin, DetailView):
    model = Cooperante
    template_name = 'mye/cooperante.html'


class CooperanteUpdate(LoginRequiredMixin, UpdateView):
    model = Cooperante
    template_name = 'mye/cooperante_form.html'
    form_class = CooperanteForm


class CooperanteList(LoginRequiredMixin, ListView):
    model = Cooperante
    template_name = 'mye/cooperante_list.html'


class ProyectoCrear(LoginRequiredMixin, CreateView):
    model = Proyecto
    template_name = 'mye/proyecto_form.html'
    form_class = ProyectoForm


class ProyectoDetalle(LoginRequiredMixin, DetailView):
    model = Proyecto
    template_name = 'mye/proyecto.html'


class ProyectoUpdate(LoginRequiredMixin, UpdateView):
    model = Proyecto
    template_name = 'mye/proyecto_form.html'
    form_class = ProyectoForm


class ProyectoList(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'mye/proyecto_list.html'


class SolicitudVersionCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SolicitudVersion
    template_name = 'mye/solicitud_version_form.html'
    form_class = SolicitudVersionForm
    permission_required = 'mye.add_solicitud_version'
    redirect_unauthenticated_users = True
    raise_exception = True


class SolicitudVersionDetalle(LoginRequiredMixin, DetailView):
    model = SolicitudVersion
    template_name = 'mye/solicitud_version.html'


class SolicitudCrearView(LoginRequiredMixin, CreateView):
    model = Solicitud
    form_class = SolicitudNuevaForm

    def form_valid(self, form):
        response = super(SolicitudCrearView, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super(SolicitudCrearView, self).form_valid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def get_success_url(self):
        return reverse('escuela_solicitud_update', kwargs={'pk': self.object.escuela.id, 'id_solicitud': self.object.id})


class SolicitudUpdate(LoginRequiredMixin, UpdateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'mye/solicitud_form.html'

    def get_success_url(self):
        return reverse('escuela_detail', kwargs={'pk': self.object.escuela.id})


class ValidacionCrearView(LoginRequiredMixin, CreateView):
    model = Validacion
    form_class = ValidacionNuevaForm

    def form_valid(self, form):
        response = super(ValidacionCrearView, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super(ValidacionCrearView, self).form_valid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def get_success_url(self):
        return reverse('escuela_validacion_update', kwargs={'pk': self.object.escuela.id, 'id_validacion': self.object.id})


class ValidacionUpdate(LoginRequiredMixin, UpdateView):
    model = Validacion
    form_class = ValidacionForm
    template_name = 'mye/solicitud_form.html'

    def get_success_url(self):
        return reverse('escuela_detail', kwargs={'pk': self.object.escuela.id})

class InformeMyeView(LoginRequiredMixin, FormView):
    form_class = InformeMyeForm
    template_name = 'mye/informe_form.html'

class InformeMyeBackend(autocomplete.Select2QuerySetView):
    def get_paginate_by(self, queryset):
        return None

    def has_more(self, context):
        return False

    def get_result_label(self, result):
        return {
            'url': result.get_absolute_url(),
            'codigo': result.codigo,
            'nombre': result.nombre,
            'direccion': result.direccion,
            'municipio': result.municipio.nombre,
            'departamento': result.municipio.departamento.nombre,
            'nivel': result.nivel.nivel,
            'poblacion': result.poblacion_actual,
        }

    def get_queryset(self):
        qs = Escuela.objects.all()

        nombre = self.forwarded.get('nombre', None)
        direccion = self.forwarded.get('direccion', None)
        municipio = self.forwarded.get('municipio', None)
        departamento = self.forwarded.get('departamento', None)
        cooperante_mye = self.forwarded.get('cooperante_mye', None)
        proyecto_mye = self.forwarded.get('proyecto_mye', None)
        nivel = self.forwarded.get('nivel', None)
        sector = self.forwarded.get('sector', None)
        poblacion_min = self.forwarded.get('poblacion_min', None)
        poblacion_max = self.forwarded.get('poblacion_max', None)
        solicitud = self.forwarded.get('solicitud', None)
        solicitud_id = self.forwarded.get('solicitud_id', None)
        equipamiento = self.forwarded.get('equipamiento', None)
        equipamiento_id = self.forwarded.get('equipamiento_id', None)
        cooperante_tpe = self.forwarded.get('cooperante_tpe', None)
        proyecto_tpe = self.forwarded.get('proyecto_tpe', None)

        if self.q:
            qs = qs.filter(codigo=self.q)
        if solicitud:
            solicitud_list = Solicitud.objects.all()
            if solicitud == "2":
                qs = qs.filter(solicitud__in=solicitud_list).distinct()
            if solicitud == "1":
                qs = qs.exclude(solicitud__in=solicitud_list).distinct()
        if solicitud_id:
            solicitud_list = Solicitud.objects.filter(id=solicitud_id)
            qs = qs.filter(solicitud__in=solicitud_list).distinct()
        if equipamiento_id:
            equipamiento_list = Equipamiento.objects.filter(id=equipamiento_id)
            qs = qs.filter(equipamiento__in=equipamiento_list).distinct()
        if equipamiento:
            equipamiento_list = Equipamiento.objects.all()
            if equipamiento == "2":
                qs = qs.filter(equipamiento__in=equipamiento_list).distinct()
            if equipamiento == "1":
                qs = qs.exclude(equipamiento__in=equipamiento_list).distinct()
        if departamento:
            qs = qs.filter(municipio__in=Municipio.objects.filter(departamento=departamento)).distinct()
        if municipio:
            qs = qs.filter(municipio=municipio)
        if cooperante_mye:
            qs = qs.filter(cooperante_asignado__in=cooperante_mye).distinct()
        if proyecto_mye:
            qs = qs.filter(proyecto_asignado__in=proyecto_mye).distinct()
        if nombre:
            qs = qs.filter(nombre__icontains=nombre)
        if direccion:
            qs = qs.filter(direccion__icontains=direccion)
        if nivel:
            qs = qs.filter(nivel=nivel)
        if sector:
            qs = qs.filter(sector=sector)
        if poblacion_min:
            solicitud_list = Solicitud.objects.filter(total_alumno__gte=poblacion_min)
            qs = qs.filter(solicitud__in=solicitud_list).distinct()
        if poblacion_max:
            solicitud_list = Solicitud.objects.filter(total_alumno__lte=poblacion_max)
            qs = qs.filter(solicitud__in=solicitud_list).distinct()
        if cooperante_tpe:
            equipamiento_list = Equipamiento.objects.filter(cooperante__in=cooperante_tpe)
            qs = qs.filter(equipamiento__in=equipamiento_list).distinct()
        if proyecto_tpe:
            equipamiento_list = Equipamiento.objects.filter(proyecto__in=proyecto_tpe)
            qs = qs.filter(equipamiento__in=equipamiento_list).distinct()
        return qs
