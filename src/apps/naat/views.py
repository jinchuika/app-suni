from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, FormView

from braces.views import GroupRequiredMixin

from apps.naat import models as naat_m
from apps.naat import forms as naat_f
from apps.cyd import models as cyd_m
from apps.escuela import models as escuela_m


class BaseNaatPermission(GroupRequiredMixin):
    """Vista base para asignar los proteger las vistas de Naat y que solo puedan ser accedidas por usuarios
    de los grupos correspondientes.

    Todo:
        Definir si hay vistas que puedan ser informes generales para usuarios de `consulta`
    """
    group_required = ["naat", "naat_facilitador"]
    redirect_unauthenticated_users = False
    raise_exception = True


class ParticipanteNaatCreateView(BaseNaatPermission, CreateView):
    """Vista para crear un nuevo :class:`Participante` y una :class:`AsignacionNaat` asociada al mismo.
    La validación de que no exista un dato duplicado se realiza a nivel de base de datos.
    """
    model = cyd_m.Participante
    form_class = naat_f.AsignacionNaatForm
    template_name = 'naat/participante_add.html'

    def get_form(self, form_class=None):
        """
        Para filtra las opciones disponibles para elegir a `capacitador` en el formulario
        """
        form = super(ParticipanteNaatCreateView, self).get_form(form_class)
        if self.request.user.groups.filter(name="naat_facilitador").exists():
            form.fields['capacitador'].queryset = form.fields['capacitador'].queryset.filter(id=self.request.user.id)
        return form

    def form_valid(self, form):
        """Se debe validar que el UDI de la :class:`Escuela` exista para asignarla al :class:`Participante`
        que se está creando.
        """
        try:
            form.instance.escuela = escuela_m.Escuela.objects.get(codigo=form.cleaned_data['udi'])
        except ObjectDoesNotExist:
            form.add_error('udi', 'El UDI no es válido o no existe.')
            return self.form_invalid(form)
        return_value = super(ParticipanteNaatCreateView, self).form_valid(form)

        # Es necesario confirmar que el :class:`Participante` se creó correctamente en la base de datos
        if form.instance.pk:
            try:
                form.instance.asignaciones_naat.create(
                    capacitador=form.cleaned_data['capacitador'])
            except IntegrityError:
                # Valida en caso de que la :class:`AsignacionNaat` no pueda ser creada
                form.instance.delete()
                form.add_error('dpi', 'Error al asignar participante.')
                return self.form_invalid(form)
        return return_value


class AsignacionesActualesListView(BaseNaatPermission, ListView):
    """Esta vista es un acceso rápido a los :class:`Participante`s asignados actualmente al facilitador.
    """
    template_name = 'naat/asignaciones_actuales.html'

    def get_queryset(self):
        return naat_m.AsignacionNaat.objects.filter(
            capacitador=self.request.user,
            activa=True)


class SesionPresencialDetailView(BaseNaatPermission, DetailView):
    template_name = 'naat/sesionpresencial_detail.html'
    model = naat_m.SesionPresencial


class SesionPresencialCalendarView(BaseNaatPermission, FormView):
    template_name = 'naat/calendario.html'
    form_class = naat_f.CalendarFilterForm

    def get_form(self, form_class=None):
        """
        Para filtrar el formulario si el usuario pertenece al grupo 'naat_facilitador`
        """
        form = super(SesionPresencialCalendarView, self).get_form(form_class)
        if self.request.user.groups.filter(name="naat_facilitador").exists():
            form.fields['capacitador'].queryset = form.fields['capacitador'].queryset.filter(id=self.request.user.id)
            form.fields['capacitador'].empty_label = None
        return form
