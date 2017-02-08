from datetime import date
from django import forms
from django.core.urlresolvers import reverse_lazy

from apps.escuela.models import Escuela, EscNivel, EscSector
from apps.main.models import Departamento, Municipio
from django.forms import ModelForm
from django.utils import timezone
from apps.mye.models import Cooperante, EscuelaCooperante, Proyecto, EscuelaProyecto, SolicitudVersion, Solicitud, Requisito, ValidacionVersion, Validacion


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
        instance = super(SolicitudNuevaForm, self).save(commit=False)
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


class ValidacionNuevaForm(forms.ModelForm):
    class Meta:
        model = Validacion
        fields = ('escuela', 'version', 'tipo')
        widgets = {
            'escuela': forms.HiddenInput(),
            'version': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(ValidacionNuevaForm, self).__init__(*args, **kwargs)
        self.fields['version'].label = 'Versión'

    def save(self, commit=True):
        instance = super(ValidacionNuevaForm, self).save(commit=False)
        instance.jornada = 1
        instance.edf = False
        instance.alumna = 0
        instance.alumno = 0
        instance.maestra = 0
        instance.maestro = 0
        if commit:
            instance.save()
        return instance


class ValidacionForm(forms.ModelForm):
    class Meta:
        model = Validacion
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
            'observacion': 'Observaciones',
            'requisito': 'Requerimientos',
        }

        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'version': forms.HiddenInput(),
            'fecha': forms.TextInput(attrs={'class': 'form-control datepicker'}),
            'jornada': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
            'requisito': forms.CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}),
        }

    def __init__(self, *args, **kwargs):
        super(ValidacionForm, self).__init__(*args, **kwargs)
        version = ValidacionVersion.objects.get(id=self.initial['version'])
        self.fields['requisito'].queryset = Requisito.objects.filter(id__in=version.requisito.all())


class InformeMyeForm(forms.ModelForm):
    CAMPO_CHOICES = (
        ("departamento","Departamento"),
        ("cooperante_mye","Cooperante en proceso"),
        ("proyecto_mye","Proyecto en proceso"),
        ("Direccion","Dirección"),
        ("municipio","Municipio"),
        ("nivel","Nivel"),
        ("sector","Sector"),
        ("poblacion_min","Población mínima"),
        ("poblacion_max","Población máxima"),
        ("solicitud","Solicitud"),
        ("solicitud_id","Número de solicitud"),
        ("equipamiento","Equipamiento"),
        ("equipamiento_id","Número de entrega"),
        ("cooperante_tpe","Cooperante de equipamiento"),
        ("proyecto_tpe","Poyecto de equipamiento"),)
    ESTADO_CHOICES = (
        (None, 'No importa'),
        (2, 'Sí'),
        (1, 'No'),)
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        required=False)
    cooperante_mye = forms.ModelMultipleChoiceField(
        label='Cooperante en proceso',
        queryset=Cooperante.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False)
    proyecto_mye = forms.ModelMultipleChoiceField(
        label='Proyecto en proceso',
        queryset=Proyecto.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False)
    codigo = forms.CharField(
        label='Código',
        required=False)
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'data-ajax--url': reverse_lazy('escuela_buscar_backend')}),
        required=False)
    direccion = forms.CharField(
        label='Dirección',
        widget=forms.TextInput(),
        required=False)
    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all(),
        required=False)
    nivel = forms.ModelChoiceField(
        queryset=EscNivel.objects.all(),
        required=False)
    sector = forms.ModelChoiceField(
        queryset=EscSector.objects.all(),
        required=False)
    poblacion_min = forms.IntegerField(
        label='Población mínima',
        required=False)
    poblacion_max = forms.IntegerField(
        label='Población máxima',
        required=False)
    solicitud = forms.ChoiceField(
        required=False,
        choices=ESTADO_CHOICES)
    solicitud_id = forms.IntegerField(
        label='Número de solicitud',
        min_value=1,
        required=False)
    equipamiento = forms.ChoiceField(
        required=False,
        choices=ESTADO_CHOICES)
    equipamiento_id = forms.IntegerField(
        label='Número de entrega',
        min_value=1,
        required=False)
    cooperante_tpe = forms.ModelMultipleChoiceField(
        label='Cooperante de equipamiento',
        queryset=Cooperante.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False)
    proyecto_tpe = forms.ModelMultipleChoiceField(
        label='Proyecto de equipamiento',
        queryset=Proyecto.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False)
    campos = forms.MultipleChoiceField(
        required=False,
        choices=ESTADO_CHOICES)

    class Meta:
        model = Escuela
        fields = ['codigo', 'nombre', 'municipio']
