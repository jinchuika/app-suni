from django.shortcuts import get_object_or_404, reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from apps.escuela.forms import (
    FormEscuelaCrear, ContactoForm, BuscarEscuelaForm,
    EscuelaBuscarForm)
from apps.escuela.models import Escuela, EscContacto
from apps.escuela.mixins import ContactoContextMixin
from apps.main.mixins import InformeMixin
from apps.mye.forms import EscuelaCooperanteForm, EscuelaProyectoForm, SolicitudNuevaForm, SolicitudForm, ValidacionNuevaForm, ValidacionForm
from apps.tpe.forms import EquipamientoForm, EquipamientoNuevoForm
from apps.tpe.models import Equipamiento
from apps.mye.models import EscuelaCooperante, EscuelaProyecto, Solicitud, Validacion, ValidacionTipo
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
        if self.request.user.groups.filter(name='mye_validacion_nula').count() > 0:
            context['validacion_nueva_form'].fields['tipo'].queryset = ValidacionTipo.objects.all()
        else:
            context['validacion_nueva_form'].fields['tipo'].queryset = ValidacionTipo.objects.exclude(id=3)

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


class EscuelaBuscar(InformeMixin):
    form_class = EscuelaBuscarForm
    template_name = 'escuela/escuela_buscar.html'
    queryset = Escuela.objects.distinct()
    filter_list = {
        'codigo': 'codigo',
        'nombre': 'nombre__contains',
        'direccion': 'direccion__contains',
        'municipio': 'municipio',
        'departamento': 'municipio__departamento',
        'nivel': 'nivel',
        'sector': 'sector',
        'cooperante_mye': 'asignacion_cooperante__in',
        'proyecto_mye': 'asignacion_proyecto__in',
        'fecha_min': 'fecha__gte',
        'fecha_max': 'fecha__lte',
        'poblacion_min': 'poblaciones__total_alumno__gte',
        'poblacion_max': 'poblaciones__total_alumno__lte',
        'solicitud_id': 'solicitud__id',
        'validacion_id': 'validacion__id',
        'equipamiento_id': 'equipamiento__id',
        'cooperante_tpe': 'equipamiento__cooperante',
        'proyecto_tpe': 'equipamiento__proyecto',
    }

    def get_queryset(self, filtros):
        queryset = super(EscuelaBuscar2, self).get_queryset(filtros)
        if filtros.get('solicitud', None):
            queryset = queryset.filter(solicitud__isnull=eval(filtros.get('solicitud')))
        if filtros.get('validacion', None):
            queryset = queryset.filter(validacion__isnull=eval(filtros.get('validacion')))
        if filtros.get('equipamiento', None):
            queryset = queryset.filter(equipamiento__isnull=eval(filtros.get('equipamiento')))
        return queryset

    def create_response(self, queryset):
        return [
            {
                'codigo': escuela.codigo,
                'direccion': escuela.direccion,
                'departamento': escuela.municipio.departamento.nombre,
                'municipio': escuela.municipio.nombre,
                'nombre': escuela.nombre,
                'escuela_url': escuela.get_absolute_url(),
                'sector': str(escuela.sector),
                'nivel': str(escuela.nivel),
                'poblacion': escuela.poblacion,
                'equipada': escuela.equipada
            } for escuela in queryset
        ]
