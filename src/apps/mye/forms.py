from datetime import date
from django import forms
from django.forms import ModelForm
from django.utils import timezone
from apps.mye.models import Cooperante, EscuelaCooperante, Proyecto, EscuelaProyecto, SolicitudVersion, Solicitud, Requisito
from apps.escuela.models import Escuela


class CooperanteForm(ModelForm):
    class Meta:
        """Datos del  modelo
        """
        model = Cooperante
        fields = '__all__'
        widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control'})}


class EscuelaCooperanteForm(ModelForm):
    """Formulario para asignaciones de cooperantes a escuelas
    """
    eliminar = False

    class Meta:
        model = Escuela
        fields = ['id', 'cooperante_asignado']
        widgets = {
            'id': forms.HiddenInput(),
            'cooperante_asignado': forms.SelectMultiple(attrs={'class': 'select2'})
        }

    def __init__(self, eliminar, *args, **kwargs):
        super(EscuelaCooperanteForm, self).__init__(*args, **kwargs)
        self.eliminar = eliminar

    def save(self, commit=True):
        instance = super(EscuelaCooperanteForm, self).save(commit=False)
        instance.asignacion_cooperante = instance.asignacion_cooperante.filter(activa=True)
        # Revisa que el usuario tenga permiso para eliminar
        if self.eliminar:
            # Revisa si un cooperante fue eliminado
            for asignacion in instance.asignacion_cooperante.all():
                if asignacion.cooperante not in self.cleaned_data['cooperante_asignado']:
                    asignacion.activa = False
                    asignacion.fecha_anulacion = timezone.now()
                    asignacion.save()
        for cooperante in self.cleaned_data['cooperante_asignado']:
            if EscuelaCooperante.objects.filter(escuela=instance, cooperante=cooperante, activa=True).count() == 0:
                esc_coo = EscuelaCooperante(escuela=instance, cooperante=cooperante)
                esc_coo.save()


class ProyectoForm(ModelForm):
    class Meta:
        model = Proyecto
        fields = '__all__'
        widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control'})}


class EscuelaProyectoForm(ModelForm):
    eliminar = False

    class Meta:
        model = Escuela
        fields = ['id', 'proyecto_asignado']
        widgets = {
            'id': forms.HiddenInput(),
            'proyecto_asignado': forms.SelectMultiple(attrs={'class': 'select2'})
        }

    def __init__(self, eliminar, *args, **kwargs):
        super(EscuelaProyectoForm, self).__init__(*args, **kwargs)
        self.eliminar = eliminar

    def save(self, commit=True):
        instance = super(EscuelaProyectoForm, self).save(commit=False)
        instance.asignacion_proyecto = instance.asignacion_proyecto.filter(activa=True)
        # Revisa que el usuario tenga permiso para eliminar
        if self.eliminar:
            # Revisa si un proyecto fue eliminado
            for asignacion in instance.asignacion_proyecto.all():
                if asignacion.proyecto not in self.cleaned_data['proyecto_asignado']:
                    asignacion.activa = False
                    asignacion.fecha_anulacion = timezone.now()
                    asignacion.save()
        for proyecto in self.cleaned_data['proyecto_asignado']:
            if EscuelaProyecto.objects.filter(escuela=instance, proyecto=proyecto, activa=True).count() == 0:
                esc_pro = EscuelaProyecto(escuela=instance, proyecto=proyecto)
                esc_pro.save()


class SolicitudVersionForm(ModelForm):
    """Formulario para versiones de solicitudes
    """
    class Meta:
        model = SolicitudVersion
        fields = '__all__'
        widgets = {
            'requisito': forms.CheckboxSelectMultiple()
        }


class SolicitudNuevaForm(forms.ModelForm):

    class Meta:
        model = Solicitud
        fields = ('escuela', 'version')
        widgets = {
            'escuela': forms.HiddenInput(),
            'version': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(SolicitudNuevaForm, self).__init__(*args, **kwargs)
        self.fields['version'].empty_label = None
        self.fields['version'].label = 'Versión'

    def save(self, commit=True):
        print("asd")
        instance = super(SolicitudNuevaForm, self).save(commit=False)
        print("dsa")
        instance.fecha = date.today()
        instance.jornada = 1
        instance.edf = False
        instance.lab_actual = False
        instance.alumna = 0
        instance.alumno = 0
        instance.maestra = 0
        instance.maestro = 0
        if commit:
            instance.save()
        return instance


class SolicitudForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = '__all__'
        exclude = ('escuela',)
        labels = {
            'alumna': 'Cantidad de alumnas',
            'alumno': 'Cantidad de alumnos',
            'maestra': 'Cantidad de maestras',
            'maestro': 'Cantidad de maestros',
            'total_alumno': 'Cantidad total de estudiantes',
            'total_maestro': 'Cantidad total de docentes',
            'jornada': 'Cantidad de jornadas en la escuela',
            'edf': 'La escuela fue EDF',
            'lab_actual': 'Tiene laboratorio actualmente',
            'observacion': 'Observaciones',
            'requisito': 'Requerimientos',
            'medio': 'Medios por los que escuchó de nosotros'
        }
        widgets = {
            'version': forms.HiddenInput(),
            'fecha': forms.TextInput(attrs={'class': 'form-control datepicker'}),
            'jornada': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
            'requisito': forms.CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}),
            'medio': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(SolicitudForm, self).__init__(*args, **kwargs)
        version = SolicitudVersion.objects.get(id=self.initial['version'])
        self.fields['requisito'].queryset = Requisito.objects.filter(id__in=version.requisito.all())
