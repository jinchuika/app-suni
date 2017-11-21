from datetime import datetime
from django.shortcuts import reverse
from django.db import models

from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, UpdateView, FormView

from django.http import JsonResponse
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, CsrfExemptMixin, JsonRequestResponseMixin

from apps.main.mixins import InformeMixin
from apps.mye.forms import (
    InformeMyeForm, CooperanteForm, ProyectoForm,
    SolicitudVersionForm, SolicitudForm, SolicitudNuevaForm,
    ValidacionNuevaForm, ValidacionForm, ValidacionListForm,
    SolicitudListForm)
from apps.mye.models import (
    Cooperante, Proyecto, SolicitudVersion,
    Solicitud, Validacion, ValidacionComentario)
from apps.tpe.models import Equipamiento
from apps.main.models import Municipio
from apps.escuela.models import Escuela
from apps.escuela.views import EscuelaDetail


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


class ValidacionComentarioCrear(CsrfExemptMixin, JsonRequestResponseMixin, View):
    require_json = True

    def post(self, request, *args, **kwargs):
        try:
            id_validacion = self.request_json["id_validacion"]
            validacion = Validacion.objects.filter(id=id_validacion)
            comentario = self.request_json["comentario"]
            if not len(comentario) or len(validacion) == 0:
                raise KeyError
        except KeyError:
            error_dict = {u"message": u"Sin comentario"}
            return self.render_bad_request_response(error_dict)
        comentario_validacion = ValidacionComentario(validacion=validacion[0], usuario=self.request.user, comentario=comentario)
        comentario_validacion.save()
        return self.render_json_response({
            "comentario": comentario_validacion.comentario,
            "fecha": str(comentario_validacion.fecha),
            "usuario": str(comentario_validacion.usuario.perfil)
        })


class ValidacionDetailView(EscuelaDetail):

    def get_context_data(self, **kwargs):
        id_validacion = self.kwargs.pop('id_validacion')
        context = super(ValidacionDetailView, self).get_context_data(**kwargs)
        context['validacion_detail'] = id_validacion
        return context


class SolicitudListView(InformeMixin):
    form_class = SolicitudListForm
    template_name = 'mye/solicitud_list.html'
    queryset = Solicitud.objects.all()
    filter_list = {
        'codigo': 'escuela__codigo',
        'nombre': 'escuela__nombre__contains',
        'direccion': 'escuela__direccion__contains',
        'municipio': 'escuela__municipio',
        'departamento': 'escuela__municipio__departamento',
        'fecha_min': 'fecha__gte',
        'fecha_max': 'fecha__lte',
        'alumnos_min': 'poblacion__total_alumno__gte',
        'alumnos_max': 'poblacion__total_alumno__lte'
    }

    def create_response(self, queryset):
        return [
            {
                'departamento': str(solicitud.escuela.municipio.departamento),
                'municipio': solicitud.escuela.municipio.nombre,
                'escuela': '<a href="{}">{} <br />({})</a>'.format(
                    solicitud.escuela.get_absolute_url(),
                    solicitud.escuela.nombre,
                    solicitud.escuela.codigo),
                'requisitos': str(solicitud.porcentaje_requisitos())[:4] + "%",
                'alumnos': solicitud.poblacion.total_alumno,
                'maestros': solicitud.poblacion.total_maestro,
                'fecha': solicitud.fecha
            } for solicitud in queryset
        ]


class ValidacionListView(SolicitudListView):
    form_class = ValidacionListForm
    template_name = 'mye/validacion_list.html'
    queryset = Validacion.objects.all()

    def create_response(self, queryset):
        return [
            {
                'departamento': str(validacion.escuela.municipio.departamento),
                'municipio': validacion.escuela.municipio.nombre,
                'escuela': '<a href="{}">{} <br />({})</a>'.format(
                    validacion.escuela.get_absolute_url(),
                    validacion.escuela.nombre,
                    validacion.escuela.codigo),
                'estado': {
                    'estado': 'Completa' if validacion.completada is True else 'Pendiente',
                    'url': validacion.get_absolute_url()},
                'fecha': '{}'.format(validacion.fecha_inicio),
                'fecha_equipamiento': '{}'.format(validacion.fecha_equipamiento),
                'requisitos': str(validacion.porcentaje_requisitos())[:4] + "%",
                'comentarios': [{
                    'comentario': '- ' + com.comentario
                } for com in validacion.comentarios.all().order_by('fecha')]
            } for validacion in queryset
        ]

    def __init__(self, *args, **kwargs):
        super(ValidacionListView, self).__init__(*args, **kwargs)
        self.filter_list['fecha_min'] = 'fecha_inicio__gte'
        self.filter_list['fecha_max'] = 'fecha_inicio__lte'
        self.filter_list['fecha_tpe_min'] = 'fecha_equipamiento__gte'
        self.filter_list['fecha_tpe_max'] = 'fecha_equipamiento__lte'
        self.filter_list['estado'] = 'completada'
        self.filter_list['version'] = 'version'
