from django.shortcuts import get_object_or_404, reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from dal import autocomplete

from apps.escuela.forms import FormEscuelaCrear, ContactoForm, BuscarEscuelaForm
from apps.escuela.models import Escuela, EscContacto
from apps.escuela.mixins import ContactoContextMixin
from apps.mye.forms import EscuelaCooperanteForm, EscuelaProyectoForm, SolicitudNuevaForm, SolicitudForm, ValidacionNuevaForm, ValidacionForm
from apps.tpe.forms import EquipamientoForm, EquipamientoNuevoForm
from apps.tpe.models import Equipamiento
from apps.mye.models import EscuelaCooperante, EscuelaProyecto, Solicitud, Validacion
from apps.main.models import Municipio


class EscuelaCrear(LoginRequiredMixin, CreateView):
    template_name = 'escuela/add.html'
    raise_exception = True
    redirect_unauthenticated_users = True
    form_class = FormEscuelaCrear


class EscuelaDetail(LoginRequiredMixin, DetailView):
    template_name = 'escuela/detail.html'
    model = Escuela

    def get_context_data(self, **kwargs):
        context = super(EscuelaDetail, self).get_context_data(**kwargs)
        context['solicitud_nueva_form'] = SolicitudNuevaForm(initial={'escuela': self.object.pk})
        context['equipamiento_nuevo_form'] = EquipamientoNuevoForm(initial={'escuela': self.object.pk})
        context['validacion_nueva_form'] = ValidacionNuevaForm(initial={'escuela': self.object.pk})

        # Crea un formulario de solicitud si encuentra la ID
        if 'id_solicitud' in self.kwargs:
            solicitud = Solicitud.objects.get(pk=self.kwargs['id_solicitud'])
            if solicitud in self.object.solicitud.all():
                context['solicitud_form'] = SolicitudForm(instance=solicitud)
                context['solicitud_id'] = self.kwargs['id_solicitud']

        if 'id_validacion' in self.kwargs:
            validacion = Validacion.objects.get(pk=self.kwargs['id_validacion'])
            if validacion in self.object.validacion.all():
                context['validacion_form'] = ValidacionForm(instance=validacion)
                context['validacion_id'] = self.kwargs['id_validacion']

        # Crea un formulario de equipamiento si encuentra la ID
        if 'id_equipamiento' in self.kwargs:
            equipamiento = Equipamiento.objects.get(pk=self.kwargs['id_equipamiento'])
            if equipamiento in self.object.equipamiento.all():
                context['equipamiento_form'] = EquipamientoForm(instance=equipamiento)
                context['equipamiento_id'] = self.kwargs['id_equipamiento']
        return context


class EscuelaCooperanteUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Escuela
    form_class = EscuelaCooperanteForm
    template_name = 'mye/cooperante_asignacion_escuela.html'
    permission_required = 'mye.change_escuela_cooperante'
    redirect_unauthenticated_users = True
    raise_exception = True

    def get_form(self, *args, **kwargs):
        eliminar = self.request.user.has_perm('mye.delete_escuela_cooperante')
        form = self.form_class(eliminar=eliminar, **self.get_form_kwargs())
        form.initial['cooperante_asignado'] = [c.cooperante for c in EscuelaCooperante.objects.filter(escuela=self.object, activa=True)]
        return form

    def get_success_url(self):
        return reverse('escuela_detail', kwargs={'pk': self.kwargs['pk']})


class EscuelaProyectoUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Escuela
    form_class = EscuelaProyectoForm
    template_name = 'mye/proyecto_asignacion_escuela.html'
    permission_required = 'mye.change_escuela_proyecto'
    redirect_unauthenticated_users = True
    raise_exception = True

    def get_form(self, *args, **kwargs):
        eliminar = self.request.user.has_perm('mye.delete_escuela_proyecto')
        form = self.form_class(eliminar=eliminar, **self.get_form_kwargs())
        form.initial['proyecto_asignado'] = [c.proyecto for c in EscuelaProyecto.objects.filter(escuela=self.object, activa=True)]
        return form

    def get_success_url(self):
        return reverse('escuela_detail', kwargs={'pk': self.kwargs['pk']})


class EscuelaEditar(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "escuela.change_escuela"
    model = Escuela
    template_name = 'escuela/add.html'
    form_class = FormEscuelaCrear
    raise_exception = True
    redirect_unauthenticated_users = True


class EscContactoCrear(LoginRequiredMixin, ContactoContextMixin, CreateView):
    template_name = 'escuela/contacto.html'
    model = EscContacto
    form_class = ContactoForm

    def get_initial(self):
        escuela = get_object_or_404(Escuela, id=self.kwargs.get('id_escuela'))
        return{'escuela': escuela}

    def get_success_url(self):
        return reverse('escuela_detail', kwargs={'pk': self.kwargs['id_escuela']})


class EscContactoEditar(LoginRequiredMixin, ContactoContextMixin, UpdateView):
    template_name = 'escuela/contacto.html'
    model = EscContacto
    form_class = ContactoForm

    def get_success_url(self):
        return reverse('escuela_detail', kwargs={'pk': self.kwargs['id_escuela']})


class EscuelaBuscar(LoginRequiredMixin, FormView):
    form_class = BuscarEscuelaForm
    template_name = 'escuela/buscar.html'


class EscuelaBuscarBackend(autocomplete.Select2QuerySetView):
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
