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


class InformeMyeView(LoginRequiredMixin, FormView):
    form_class = InformeMyeForm
    template_name = 'mye/informe_form.html'


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


class InformeMyeBk(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def armar_query(self, filtros):
        qs = Escuela.objects.all()

        codigo = filtros.get('codigo', None)
        nombre = filtros.get('nombre', None)
        direccion = filtros.get('direccion', None)
        municipio = filtros.get('municipio', None)
        departamento = filtros.get('departamento', None)
        cooperante_mye = filtros.get('cooperante_mye', None)
        proyecto_mye = filtros.get('proyecto_mye', None)
        nivel = filtros.get('nivel', None)
        sector = filtros.get('sector', None)
        poblacion_min = filtros.get('poblacion_min', None)
        poblacion_max = filtros.get('poblacion_max', None)
        solicitud = filtros.get('solicitud', None)
        solicitud_id = filtros.get('solicitud_id', None)
        validada = filtros.get('validada', None)
        validacion_id = filtros.get('validacion_id', None)
        equipamiento = filtros.get('equipamiento', None)
        equipamiento_id = filtros.get('equipamiento_id', None)
        cooperante_tpe = filtros.get('cooperante_tpe', None)
        proyecto_tpe = filtros.get('proyecto_tpe', None)

        if codigo:
            qs = qs.filter(codigo=codigo)
        if solicitud:
            solicitud_list = Solicitud.objects.all()
            # sí
            if solicitud == "2":
                qs = qs.filter(solicitud__in=solicitud_list).distinct()
            # no
            if solicitud == "1":
                qs = qs.exclude(solicitud__in=solicitud_list).distinct()
        if solicitud_id:
            solicitud_list = Solicitud.objects.filter(id=solicitud_id)
            qs = qs.filter(solicitud__in=solicitud_list).distinct()
        # Con validación
        if validada == "2":
            qs = qs.annotate(num_validacion=models.Count("validacion")).filter(num_validacion__gte=1)
        # Sin validación
        if validada == "1":
            qs = qs.annotate(num_validacion=models.Count("validacion")).filter(num_validacion=0)
        if validacion_id:
            validacion_list = Validacion.objects.filter(id=validacion_id)
            qs = qs.filter(validacion__in=validacion_list).distinct()
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

    def crear_item(self, item, extras=None):
        campo_basic = {
            'url': item.get_absolute_url(),
            'codigo': item.codigo,
            'nombre': item.nombre,
            'municipio': item.municipio.nombre,
            'departamento': item.municipio.departamento.nombre,
            'nivel': item.nivel.nivel,
            'poblacion': item.poblacion_actual,
            'extras': {}
        }
        if 'direccion' in extras:
            campo_basic['extras']['direccion'] = item.direccion
        if 'cooperante_mye' in extras:
            cooperante_list = item.cooperante_asignado.all().values('nombre')
            campo_basic['extras']['cooperante_mye'] = ', '.join(i['nombre'] for i in cooperante_list)
        if 'proyecto_mye' in extras:
            proyecto_list = item.proyecto_asignado.all().values('nombre')
            campo_basic['extras']['proyecto_mye'] = ', '.join(i['nombre'] for i in proyecto_list)
        if 'sector' in extras:
            campo_basic['extras']['sector'] = item.sector.sector
        if 'solicitud' in extras:
            campo_basic['extras']['solicitud'] = "Sí" if item.solicitud.count() > 0 else "No"
        if 'validada' in extras:
            validacion_list = Validacion.objects.filter(escuela=item, completada=True)
            campo_basic['extras']['validada'] = "Sí" if validacion_list.count() > 0 else "No"
        if 'equipada' in extras:
            campo_basic['extras']['equipada'] = "Sí" if item.equipamiento.count() > 0 else "No"
        if 'equipamiento_id' in extras:
            equipamiento_list = item.equipamiento.all().values('id')
            campo_basic['extras']['equipamiento_id'] = '<br /> '.join(str(i['id']) for i in equipamiento_list)
        if 'equipamiento_fecha' in extras:
            equipamiento_list = item.equipamiento.all().values('fecha')
            campo_basic['extras']['equipamiento_fecha'] = '<br /> '.join(str(i['fecha']) for i in equipamiento_list)
        if 'hist_validacion' in extras:
            campo_basic['extras']['hist_validacion'] = ''
            for validacion in item.validacion.all():
                comentario_list = validacion.comentarios.all().values('comentario')
                campo_basic['extras']['hist_validacion'] += ', '.join(i['comentario'] for i in comentario_list)
                campo_basic['extras']['hist_validacion'] += '<br />'
        return campo_basic

    def armar_lista(self, lista_objeto, extras=None):
        return [
            self.crear_item(item, extras) for item in lista_objeto
        ]

    def post(self, request, *args, **kwargs):
        print(self.request_json)
        qs = self.armar_query(self.request_json)
        return self.render_json_response(self.armar_lista(qs, self.request_json['extras']))


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
        'cooperante_mye': 'escuela__asignacion_cooperante__in',
        'proyecto_mye': 'escuela__asignacion_proyecto__in',
        'fecha_min': 'fecha__gte',
        'fecha_max': 'fecha__lte',
        'alumnos_min': 'total_alumno__gte',
        'alumnos_max': 'total_alumno__lte',
    }

    def create_response(self, queryset):
        return [
            {
                'departamento': str(solicitud.escuela.municipio.departamento),
                'municipio': solicitud.escuela.municipio.nombre,
                'escuela': str(solicitud.escuela),
                'escuela_url': solicitud.escuela.get_absolute_url(),
                'requisitos': [
                    {
                        'req': str(r['requisito'])[:10],
                        'cumple': r['cumple']
                    } for r in solicitud.listar_requisito()
                ],
                'alumnos': solicitud.total_alumno,
                'maestros': solicitud.total_maestro
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
                'escuela': str(validacion.escuela),
                'escuela_url': validacion.escuela.get_absolute_url(),
                'estado': 'Completa' if validacion.completada is True else 'Pendiente',
                'validacion_url': validacion.get_absolute_url(),
                'requisitos': [
                    {
                        'req': str(r['requisito'])[:10],
                        'cumple': r['cumple']
                    } for r in validacion.listar_requisito()
                ],
                'historial': [{
                    'fecha': com.fecha,
                    'comentario': com.comentario
                } for com in validacion.comentarios.all().order_by('fecha')]
            } for validacion in queryset
        ]

    def __init__(self, *args, **kwargs):
        super(ValidacionListView, self).__init__(*args, **kwargs)
        self.filter_list['estado'] = 'completada'
