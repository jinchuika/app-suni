from datetime import date
from django import forms
from django.core.urlresolvers import reverse_lazy

from apps.escuela.models import (
    Escuela, EscNivel, EscSector,
    EscPoblacion)
from apps.main.models import Departamento, Municipio
from apps.mye import models as mye_m


class CooperanteForm(forms.ModelForm):
    class Meta:
        """Datos del  modelo
        """
        model = mye_m.Cooperante
        fields = '__all__'
        widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control'})}


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = mye_m.Proyecto
        fields = '__all__'
        widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control'})}


class CPFilterForm(forms.Form):
    equipamientos_min = forms.IntegerField(
        label='Equipamientos (min)',
        required=False,
        widget=forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}))
    equipamientos_max = forms.IntegerField(
        label='Equipamientos (max)',
        required=False,
        widget=forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}))
    equipo_min = forms.IntegerField(
        label='Cantidad de computadoras (min)',
        required=False,
        widget=forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}))
    equipo_max = forms.IntegerField(
        label='Cantidad de computadoras (max)',
        required=False,
        widget=forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}))
    fecha_min = forms.CharField(
        label='Fecha (min)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max = forms.CharField(
        label='Fecha (max)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))

class PYFilterForm(forms.Form):
        cantidad_equipamientos = forms.IntegerField(
            label='Equipamientos (min)',
            required=False,
            widget=forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}))


class SolicitudVersionForm(forms.ModelForm):
    """Formulario para versiones de solicitudes
    """
    class Meta:
        model = mye_m.SolicitudVersion
        fields = '__all__'
        widgets = {
            'requisito': forms.CheckboxSelectMultiple()
        }


class SolicitudNuevaForm(forms.ModelForm):

    class Meta:
        model = mye_m.Solicitud
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
        if commit:
            poblacion = EscPoblacion(fecha=instance.fecha, escuela=instance.escuela)
            poblacion.save()
            instance.poblacion = poblacion
            instance.save()
        return instance


class SolicitudForm(forms.ModelForm):
    alumna = forms.IntegerField(
        label='Cantidad de niñas',
        widget=forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}))
    alumno = forms.IntegerField(
        label='Cantidad de niños',
        widget=forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}))
    total_alumno = forms.IntegerField(
        required=False, label='Total de estudiantes',
        widget=forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}))
    maestra = forms.IntegerField(
        label='Cantidad de maestras',
        widget=forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}))
    maestro = forms.IntegerField(
        label='Cantidad de maestros',
        widget=forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}))
    total_maestro = forms.IntegerField(
        required=False, label='Total de maestros',
        widget=forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}))

    class Meta:
        model = mye_m.Solicitud
        fields = [
            'fecha', 'formulario', 'version', 'jornada', 'edf', 'lab_actual',
            'alumna', 'alumno', 'total_alumno', 'maestra', 'maestro', 'total_maestro',
            'requisito', 'medio', 'observacion',
        ]
        exclude = ('escuela', ' poblacion')
        labels = {
            'formulario': 'Formulario físico',
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
        version = mye_m.SolicitudVersion.objects.get(id=self.initial['version'])
        self.fields['requisito'].queryset = mye_m.Requisito.objects.filter(id__in=version.requisito.all())
        if self.instance.poblacion:
            self.fields['alumna'].initial = self.instance.poblacion.alumna
            self.fields['alumno'].initial = self.instance.poblacion.alumno
            self.fields['total_alumno'].initial = self.instance.poblacion.total_alumno
            self.fields['maestra'].initial = self.instance.poblacion.maestra
            self.fields['maestro'].initial = self.instance.poblacion.maestro
            self.fields['total_maestro'].initial = self.instance.poblacion.total_maestro

    def save(self, commit=True):
        instance = super(SolicitudForm, self).save(commit=False)
        if commit:
            if not instance.poblacion:
                instance.poblacion = EscPoblacion(fecha=instance.fecha, escuela=instance.escuela)
            instance.poblacion.fecha = instance.fecha
            instance.poblacion.escuela = instance.escuela
            instance.poblacion.alumna = self.cleaned_data['alumna']
            instance.poblacion.alumno = self.cleaned_data['alumno']
            instance.poblacion.total_alumno = self.cleaned_data['total_alumno']
            instance.poblacion.maestra = self.cleaned_data['maestra']
            instance.poblacion.maestro = self.cleaned_data['maestro']
            instance.poblacion.total_maestro = self.cleaned_data['total_maestro']
            instance.poblacion.save()
            instance.save()
            self.save_m2m()
        return instance


class SolicitudListForm(forms.Form):
    EQUIPADA_CHOICES = (
        (1, 'No importa'),
        (2, 'Sí'),
        (3, 'No'),)
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        required=False)
    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all(),
        required=False)
    codigo = forms.CharField(
        label='Código',
        required=False)
    nombre = forms.CharField(
        required=False)
    direccion = forms.CharField(
        label='Dirección',
        widget=forms.TextInput(),
        required=False)
    fecha_min = forms.CharField(
        label='Fecha mínima',
        widget=forms.TextInput(attrs={'class': 'datepicker'}),
        required=False)
    fecha_max = forms.CharField(
        label='Fecha máxima',
        widget=forms.TextInput(attrs={'class': 'datepicker'}),
        required=False)
    alumnos_min = forms.CharField(
        label='Población mínima',
        widget=forms.NumberInput(attrs={'min': '0'}),
        required=False)
    alumnos_max = forms.CharField(
        label='Población máxima',
        widget=forms.NumberInput(attrs={'min': '1'}),
        required=False)
    equipada = forms.ChoiceField(
        label='Equipada',
        choices=EQUIPADA_CHOICES,
        required=False)


class ValidacionNuevaForm(forms.ModelForm):
    class Meta:
        model = mye_m.Validacion
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
        if commit:
            poblacion = EscPoblacion(fecha=instance.fecha_inicio, escuela=instance.escuela)
            poblacion.save()
            instance.poblacion = poblacion
            instance.save()
        return instance


class ValidacionForm(forms.ModelForm):
    alumna = forms.IntegerField(
        label='Cantidad de niñas',
        widget=forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}))
    alumno = forms.IntegerField(
        label='Cantidad de niños',
        widget=forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}))
    total_alumno = forms.IntegerField(
        required=False, label='Total de estudiantes',
        widget=forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}))
    maestra = forms.IntegerField(
        label='Cantidad de maestras',
        widget=forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}))
    maestro = forms.IntegerField(
        label='Cantidad de maestros',
        widget=forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}))
    total_maestro = forms.IntegerField(
        required=False, label='Total de maestros',
        widget=forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}))

    class Meta:
        model = mye_m.Validacion
        fields = [
            'version', 'tipo', 'jornada', 'fecha_equipamiento',
            'alumna', 'alumno', 'total_alumno', 'maestra', 'maestro', 'total_maestro',
            'requisito', 'observacion', 'fotos_link', 'completada'
        ]
        exclude = ('escuela',)
        labels = {
            'jornada': 'Cantidad de jornadas en la escuela',
            'edf': 'La escuela fue EDF',
            'observacion': 'Observaciones',
            'requisito': 'Requerimientos',
        }
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'version': forms.HiddenInput(),
            'fecha_equipamiento': forms.TextInput(attrs={'class': 'form-control datepicker'}),
            'jornada': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
            'requisito': forms.CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}),
        }

    def __init__(self, *args, **kwargs):
        super(ValidacionForm, self).__init__(*args, **kwargs)
        version = mye_m.ValidacionVersion.objects.get(id=self.initial['version'])
        self.fields['requisito'].queryset = mye_m.Requisito.objects.filter(id__in=version.requisito.all())
        if self.instance.poblacion:
            self.fields['alumna'].initial = self.instance.poblacion.alumna
            self.fields['alumno'].initial = self.instance.poblacion.alumno
            self.fields['total_alumno'].initial = self.instance.poblacion.total_alumno
            self.fields['maestra'].initial = self.instance.poblacion.maestra
            self.fields['maestro'].initial = self.instance.poblacion.maestro
            self.fields['total_maestro'].initial = self.instance.poblacion.total_maestro

    def save(self, commit=True):
        instance = super(ValidacionForm, self).save(commit=False)
        if commit:
            if not instance.poblacion:
                instance.poblacion = EscPoblacion(fecha=instance.fecha_inicio, escuela=instance.escuela)
            instance.poblacion.fecha = instance.fecha_inicio
            instance.poblacion.escuela = instance.escuela
            instance.poblacion.alumna = self.cleaned_data['alumna']
            instance.poblacion.alumno = self.cleaned_data['alumno']
            instance.poblacion.total_alumno = self.cleaned_data['total_alumno']
            instance.poblacion.maestra = self.cleaned_data['maestra']
            instance.poblacion.maestro = self.cleaned_data['maestro']
            instance.poblacion.total_maestro = self.cleaned_data['total_maestro']
            instance.poblacion.save()
            if self.cleaned_data['completada']:
                instance.fecha_final = date.today()
            instance.save()
            self.save_m2m()
        return instance


class InformeMyeForm(forms.ModelForm):
    CAMPO_CHOICES = (
        ("direccion", "Dirección"),
        ("sector", "Sector"),
        ("solicitud", "Solicitud"),
        ("validada", "Validada"),
        ("equipada", "Equipada"),
        ("equipamiento_id", "Número de entrega"),
        ("equipamiento_fecha", "Fecha de equipamiento"),
        ("cooperante_tpe", "Cooperante de equipamiento"),
        ("proyecto_tpe", "Poyecto de equipamiento"),
        ("hist_validacion", "Historial de validación"),)
    ESTADO_CHOICES = (
        (None, 'No importa'),
        (2, 'Sí'),
        (1, 'No'),)
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        required=False)
    codigo = forms.CharField(
        label='Código',
        required=False)
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'data-ajax--url': reverse_lazy('informe_mye_backend')}),
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
    validada = forms.ChoiceField(
        required=False,
        choices=ESTADO_CHOICES)
    validacion_id = forms.IntegerField(
        label='Número de validación',
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
        queryset=mye_m.Cooperante.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False)
    proyecto_tpe = forms.ModelMultipleChoiceField(
        label='Proyecto de equipamiento',
        queryset=mye_m.Proyecto.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False)
    campos = forms.MultipleChoiceField(
        required=False,
        choices=CAMPO_CHOICES,
        widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Escuela
        fields = ['codigo', 'nombre', 'municipio']


class ValidacionListForm(SolicitudListForm):
    ESTADO_CHOICES = (
        (1, 'No importa'),
        (2, 'Sí'),
        (3, 'No'),)
    completada = forms.ChoiceField(
        label='Completada',
        required=False,
        choices=ESTADO_CHOICES)
    fecha_tpe_min = forms.CharField(
        label='Fecha de equipamiento (mín)',
        widget=forms.TextInput(attrs={'class': 'datepicker'}),
        required=False)
    fecha_tpe_max = forms.CharField(
        label='Fecha de equipamiento (máx)',
        widget=forms.TextInput(attrs={'class': 'datepicker'}),
        required=False)
