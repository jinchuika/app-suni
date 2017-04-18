from datetime import date
from django import forms
from django.forms import ModelForm
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy

from apps.escuela.models import (
    Escuela, EscNivel, EscSector,
    EscPoblacion)
from apps.main.models import Departamento, Municipio
from apps.mye.models import (
    Cooperante, EscuelaCooperante, Proyecto,
    EscuelaProyecto, SolicitudVersion, Solicitud,
    Requisito, ValidacionVersion, Validacion)


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
        if commit:
            poblacion = EscPoblacion(fecha=instance.fecha, escuela=instance.escuela)
            poblacion.save()
            instance.poblacion = poblacion
            instance.save()
        return instance


class SolicitudForm(ModelForm):
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
        model = Solicitud
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
        version = SolicitudVersion.objects.get(id=self.initial['version'])
        self.fields['requisito'].queryset = Requisito.objects.filter(id__in=version.requisito.all())
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
    cooperante_mye = forms.ModelChoiceField(
        label='Cooperante en proceso',
        queryset=Cooperante.objects.all(),
        widget=forms.Select(attrs={'class': 'select2'}),
        required=False)
    proyecto_mye = forms.ModelChoiceField(
        label='Proyecto en proceso',
        queryset=Proyecto.objects.all(),
        widget=forms.Select(attrs={'class': 'select2'}),
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
        model = Validacion
        fields = [
            'version', 'tipo', 'jornada',
            'alumna', 'alumno', 'total_alumno', 'maestra', 'maestro', 'total_maestro',
            'requisito', 'observacion', 'completada'
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
            'jornada': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
            'requisito': forms.CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}),
        }

    def __init__(self, *args, **kwargs):
        super(ValidacionForm, self).__init__(*args, **kwargs)
        version = ValidacionVersion.objects.get(id=self.initial['version'])
        self.fields['requisito'].queryset = Requisito.objects.filter(id__in=version.requisito.all())
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
        ("cooperante_mye", "Cooperante en proceso"),
        ("proyecto_mye", "Proyecto en proceso"),
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
        choices=CAMPO_CHOICES,
        widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Escuela
        fields = ['codigo', 'nombre', 'municipio']


class ValidacionListForm(SolicitudListForm):
    ESTADO_CHOICES = (
        (None, 'No importa'),
        (True, 'Sí'),
        (False, 'No'),)
    estado = forms.ChoiceField(
        label='Completada',
        required=False,
        choices=ESTADO_CHOICES)
