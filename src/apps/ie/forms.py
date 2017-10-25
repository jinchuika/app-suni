from django import forms

from apps.escuela.models import EscPoblacion
from apps.ie.models import (
    Laboratorio, Computadora, Serie, Validacion, ValidacionVersion, Requerimiento)


class LaboratorioCreateForm(forms.ModelForm):

    """Formulario para crear un :class:`Laboratorio`.
    """

    class Meta:
        model = Laboratorio
        fields = ('escuela',)
        widgets = {
            'escuela': forms.HiddenInput()
        }


class LaboratorioUpdateForm(forms.ModelForm):
    class Meta:
        model = Laboratorio
        fields = '__all__'
        exclude = ('escuela', 'organizacion')
        widgets = {
            'fecha': forms.TextInput(attrs={'class': 'datepicker form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
            'fotos_link': forms.URLInput(attrs={'class': 'form-control'}),
            'marca_equipo': forms.Select(attrs={'class': 'form-control'}),
            'tipo_equipo': forms.Select(attrs={'class': 'form-control'}),
            'poblacion': forms.Select(attrs={'class': 'form-control'}),
            'cantidad_computadoras': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(LaboratorioUpdateForm, self).__init__(*args, **kwargs)
        if 'poblacion' in self.initial:
            self.fields['poblacion'].queryset = EscPoblacion.objects.filter(escuela=self.instance.escuela)
            self.fields['poblacion'].label_from_instance = lambda obj: '{} ({})'.format(obj.total_alumno, obj.fecha)


class ComputadoraForm(forms.ModelForm):
    class Meta:
        model = Computadora
        fields = ('laboratorio',)
        widgets = {
            'laboratorio': forms.HiddenInput()
        }


class SerieForm(forms.ModelForm):
    class Meta:
        model = Serie
        fields = '__all__'
        widgets = {
            'computadora': forms.Select(attrs={'class': 'form-control'}),
            'item': forms.Select(attrs={'class': 'select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(SerieForm, self).__init__(*args, **kwargs)
        self.fields['item'].label_from_instance = lambda obj: "%s" % '{} - {}'.format(obj.tipo, obj)


class IEValidacionCreateForm(forms.ModelForm):

    """Formulario para crear una :class:`Validacion`.
    """

    class Meta:
        model = Validacion
        fields = ('escuela', 'version')
        widgets = {
            'escuela': forms.HiddenInput()
        }


class IEValidacionUpdateForm(forms.ModelForm):

    """Formulario para crear una :class:`Validacion`.
    """

    class Meta:
        model = Validacion
        fields = '__all__'
        exclude = ('escuela', 'version')
        widgets = {
            'fecha_inicio': forms.TextInput(attrs={'class': 'form-control datepicker'}),
            'fotos_link': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
            'requerimientos': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(IEValidacionUpdateForm, self).__init__(*args, **kwargs)
        version = ValidacionVersion.objects.get(id=self.instance.version.id)
        self.fields['requerimientos'].queryset = Requerimiento.objects.filter(id__in=version.requisitos.all())


class IEValidacionVersionForm(forms.ModelForm):
    class Meta:
        model = ValidacionVersion
        fields = '__all__'
        widgets = {
            'requisitos': forms.CheckboxSelectMultiple()
        }


class RequerimientoForm(forms.ModelForm):
    class Meta:
        model = Requerimiento
        fields = '__all__'
