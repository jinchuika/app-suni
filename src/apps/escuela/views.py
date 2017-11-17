"""Vistas para la gestión de escuelas
"""
from django.shortcuts import get_object_or_404, reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from apps.main.models import Coordenada
from apps.mye.models import (
    Solicitud, Validacion)
from apps.mye.forms import (
    SolicitudNuevaForm, SolicitudForm,
    ValidacionNuevaForm, ValidacionForm)
from apps.tpe.models import Equipamiento
from apps.tpe.forms import EquipamientoForm, EquipamientoNuevoForm
from apps.kalite.forms import VisitaForm

from apps.ie.forms import LaboratorioCreateForm, IEValidacionCreateForm

from apps.escuela.forms import (
    FormEscuelaCrear, ContactoForm, EscuelaBuscarForm, EscPoblacionForm,
    EscMatriculaForm, EscRendimientoAcademicoForm)
from apps.escuela.models import (
    Escuela, EscContacto, EscContactoTelefono, EscContactoMail, EscPoblacion,
    EscMatricula, EscRendimientoAcademico)
from apps.main.mixins import InformeMixin


class EscuelaCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Vista para crear una escuela
    """
    permission_required = "escuela.add_escuela"
    template_name = 'escuela/add.html'
    raise_exception = True
    redirect_unauthenticated_users = True
    form_class = FormEscuelaCrear

    def form_valid(self, form):
        response = super(EscuelaCrear, self).form_valid(form)
        if form.cleaned_data['lat'] and form.cleaned_data['lng']:
            mapa = Coordenada(lat=form.cleaned_data['lat'], lng=form.cleaned_data['lng'])
            mapa.save()
            self.object.mapa = mapa
            self.object.save()
        return response


class EscuelaDetail(LoginRequiredMixin, DetailView):
    """Vista para el perfil de :model:`escuela.Escuela`."""
    template_name = 'escuela/detail.html'
    model = Escuela

    def get_template_names(self):
        if (self.request.user.groups.filter(name='nacion_digital').exists()
            or not self.request.user.is_superuser):
            return ['ie/escuela_detail.html']
        else:
            return ['escuela/detail.html']

    def get_context_data(self, **kwargs):
        """Obtiene las variables de contexto para enviar al template

        Args:
            **kwargs: Puede contener el id para solicitud, validacion o equipamiento

        Returns:
            list: Variables de contexto para el template
        """
        context = super(EscuelaDetail, self).get_context_data(**kwargs)
        context['poblacion_form'] = EscPoblacionForm(initial={'escuela': self.object.pk})
        context['matricula_form'] = EscMatriculaForm(initial={'escuela': self.object.pk})
        context['rendimiento_form'] = EscRendimientoAcademicoForm(initial={'escuela': self.object.pk})
        context['solicitud_nueva_form'] = SolicitudNuevaForm(initial={'escuela': self.object.pk})
        context['equipamiento_nuevo_form'] = EquipamientoNuevoForm(initial={'escuela': self.object.pk})
        context['validacion_nueva_form'] = ValidacionNuevaForm(initial={'escuela': self.object.pk})
        context['visita_kalite_nueva_form'] = VisitaForm(initial={'escuela': self.object.pk})

        if self.object.poblaciones.count() > 0:
            context['laboratorio_form'] = LaboratorioCreateForm(initial={'escuela': self.object.pk})
            context['ie_validacion_form'] = IEValidacionCreateForm(initial={'escuela': self.object.pk})

        if 'id_solicitud' in self.kwargs:
            # Crea un formulario para editar la solicitud si encuentra que se envió una ID
            solicitud = Solicitud.objects.get(pk=self.kwargs['id_solicitud'])
            if solicitud in self.object.solicitud.all():
                context['solicitud_form'] = SolicitudForm(instance=solicitud)
                context['solicitud_id'] = self.kwargs['id_solicitud']

        if 'id_validacion' in self.kwargs:
            validacion = Validacion.objects.get(pk=self.kwargs['id_validacion'])
            if validacion in self.object.validacion.all():
                context['validacion_form'] = ValidacionForm(instance=validacion)
                context['validacion_id'] = self.kwargs['id_validacion']

        if 'id_equipamiento' in self.kwargs:
            # Crea un formulario de equipamiento si encuentra la ID
            equipamiento = Equipamiento.objects.get(pk=self.kwargs['id_equipamiento'])
            if equipamiento in self.object.equipamiento.all():
                context['equipamiento_form'] = EquipamientoForm(instance=equipamiento)
                context['equipamiento_id'] = self.kwargs['id_equipamiento']

        return context


class EscuelaEditar(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Edita una objeto de escuela.
    Requiere el permiso `escuela.change_escuela`
    """
    permission_required = "escuela.change_escuela"
    model = Escuela
    template_name = 'escuela/add.html'
    form_class = FormEscuelaCrear
    raise_exception = True
    redirect_unauthenticated_users = True

    def get_initial(self):
        initial = super(EscuelaEditar, self).get_initial()
        if self.object.mapa:
            initial['lat'] = self.object.mapa.lat
            initial['lng'] = self.object.mapa.lng
        return initial

    def form_valid(self, form):
        response = super(EscuelaEditar, self).form_valid(form)
        if form.cleaned_data['lat'] and form.cleaned_data['lng']:
            if self.object.mapa:
                self.object.mapa.lat = form.cleaned_data['lat']
                self.object.mapa.lng = form.cleaned_data['lng']
                self.object.mapa.save()
            else:
                mapa = Coordenada(lat=form.cleaned_data['lat'], lng=form.cleaned_data['lng'])
                mapa.save()
                self.object.mapa = mapa
                self.object.save()
        return response


class EscContactoCrear(LoginRequiredMixin, CreateView):
    """Crea un nuevo contacto para escuelas
    """
    template_name = 'escuela/contacto.html'
    model = EscContacto
    form_class = ContactoForm

    def form_valid(self, form):
        response = super(EscContactoCrear, self).form_valid(form)
        if form.cleaned_data['telefono']:
            telefono = EscContactoTelefono(contacto=self.object, telefono=form.cleaned_data['telefono'])
            telefono.save()
        if form.cleaned_data['mail']:
            mail = EscContactoMail(contacto=self.object, mail=form.cleaned_data['mail'])
            mail.save()
        return response

    def get_initial(self):
        """Obtiene los datos iniciales del contacto

        Returns:
            dict: La escuela para llenar en el campo `escuela` del formulario
        """
        escuela = get_object_or_404(Escuela, id=self.kwargs.get('id_escuela'))
        return {'escuela': escuela}

    def get_success_url(self):
        """Obtiene la url de la escuela después de crear el contacto

        Returns:
            string: url de la escuela
        """
        return reverse('escuela_detail', kwargs={'pk': self.kwargs['id_escuela']})


class EscContactoEditar(LoginRequiredMixin, UpdateView):
    """Edición de contacto de escuela
    """
    template_name = 'escuela/contacto.html'
    model = EscContacto
    form_class = ContactoForm

    def get_initial(self):
        """Obtiene los datos para el formulario

        Returns:
            dict: Lista de valores para los campos
        """
        initial = super(EscContactoEditar, self).get_initial()
        initial['telefono'] = self.object.telefono.first()
        initial['mail'] = self.object.mail.first()
        return initial

    def form_valid(self, form):
        response = super(EscContactoEditar, self).form_valid(form)
        if form.cleaned_data['telefono']:
            if self.object.telefono.count() == 0:
                telefono = EscContactoTelefono(contacto=self.object, telefono=form.cleaned_data['telefono'])
                telefono.save()
            else:
                telefono = self.object.telefono.all().first()
                telefono.telefono = form.cleaned_data['telefono']
                telefono.save()
        if form.cleaned_data['mail']:
            if self.object.mail.count() == 0:
                mail = EscContactoMail(contacto=self.object, mail=form.cleaned_data['mail'])
                mail.save()
            else:
                mail = self.object.mail.all().first()
                mail.mail = form.cleaned_data['mail']
                mail.save()
        return response

    def get_success_url(self):
        """Obitne la url de la escuela del contacto

        Returns:
            string: url de la escuela del contacto
        """
        return reverse('escuela_detail', kwargs={'pk': self.kwargs['id_escuela']})


class EscuelaBuscar(InformeMixin):
    """Buscador de escuelas
    """
    form_class = EscuelaBuscarForm
    template_name = 'escuela/escuela_buscar.html'
    queryset = Escuela.objects.distinct()
    filter_list = {
        'codigo': 'codigo',
        'nombre': 'nombre__icontains',
        'direccion': 'direccion__icontains',
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
        """Arma el filtro de escuelas.
        Se modifica en base a `InformeMixin` para parsear los valores `True`/`False`.

        Args:
            filtros (dict): Filtros para aplicar al queryset

        Returns:
            QuerySet: Queryset de escuelas filtradas
        """
        queryset = super(EscuelaBuscar, self).get_queryset(filtros)
        if filtros.get('solicitud', None):
            queryset = queryset.filter(solicitud__isnull=eval(filtros.get('solicitud')))
        if filtros.get('validacion', None):
            queryset = queryset.filter(validacion__isnull=eval(filtros.get('validacion')))
        if filtros.get('equipamiento', None):
            queryset = queryset.filter(equipamiento__isnull=eval(filtros.get('equipamiento')))
        return queryset

    def create_response(self, queryset):
        """Summary

        Args:
            queryset (QuerySet): Queryset de escuelas encontradas por los filtros

        Returns:
            list: Lista de escuelas para formatear con JSON
        """
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


class EscPoblacionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = EscPoblacion
    form_class = EscPoblacionForm

    permission_required = "escuela.add_escpoblacion"
    raise_exception = True
    redirect_unauthenticated_users = True


class EscMatriculaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    """Vista para crear una `:class:EscMatricula`.
    """

    model = EscMatricula
    form_class = EscMatriculaForm
    template_name = 'escuela/escmatricula_form.html'

    permission_required = "escuela.add_escmatricula"
    raise_exception = True
    redirect_unauthenticated_users = True

    def get_initial(self):
        """Obtiene los datos iniciales de la escuela
        """
        escuela = get_object_or_404(Escuela, id=self.kwargs.get('id_escuela'))
        return {'escuela': escuela}


class EscRendimientoAcademicoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    """Vista para crear una `:class:EscRendimientoAcademico`.
    """

    model = EscRendimientoAcademico
    form_class = EscRendimientoAcademicoForm
    template_name = 'escuela/escrendimientoacademico_form.html'

    permission_required = "escuela.add_escrendimientoacademico"
    raise_exception = True
    redirect_unauthenticated_users = True

    def get_initial(self):
        """Obtiene los datos iniciales de la escuela
        """
        escuela = get_object_or_404(Escuela, id=self.kwargs.get('id_escuela'))
        return {'escuela': escuela}
