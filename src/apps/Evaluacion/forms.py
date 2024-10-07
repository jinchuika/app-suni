from django import forms
from django.forms import ModelForm
from  apps.Evaluacion import models as eva_models 
from django.urls import reverse_lazy

from apps.cyd import models as cyd_models
from apps.main.models import Departamento, Municipio
from braces.views import (
    LoginRequiredMixin, GroupRequiredMixin
)
from django.contrib.auth.models import User
from django.forms.widgets import TextInput
from datetime import datetime

class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"

class DateTimeLocalField(forms.DateTimeField):
    input_formats = [
        "%Y-%m-%dT%H:%M:%S", 
        "%Y-%m-%dT%H:%M:%S.%f", 
        "%Y-%m-%dT%H:%M"
    ]
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")

class FormularioAdd(forms.ModelForm):
    """ Formulario para el control de la creación de un formulario
    """

    class Meta:
        model = eva_models.Formulario

        fields = ('usuario', 'escuela', 'evaluacion', 'fecha_inicio_formulario', 'fecha_fin_formulario', 'sede')
        exclude = ('escuela',)
        widgets = {
            'usuario': forms.Select(attrs={'class': 'select2 form-control'}),
            'sede': forms.Select(attrs={'class': 'select2 form-control'}),
            'evaluacion': forms.Select(attrs={'class': 'select2 form-control'}),
            'fecha_inicio_formulario': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'fecha_fin_formulario': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }

    fecha_inicio_formulario = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        required=False
    )
    fecha_fin_formulario = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        required=False
    )
    
        
    def __init__(self, *args, **kwargs):
        super(FormularioAdd, self).__init__(*args, **kwargs)

        fecha_inicio = datetime(2024, 1, 1)
        self.fields['sede'].queryset = cyd_models.Sede.objects.filter(finalizada=False, fecha_creacion__gte=fecha_inicio)

        self.fields['usuario'].queryset = User.objects.filter(groups__name="cyd_capacitador")
        self.fields['usuario'].label_from_instance = lambda usuario: usuario.get_full_name()


class FormularioForm(forms.ModelForm):
    """ Formulario para el control del listado de formulario, editar fomrulario
    """
    fecha_inicio_formulario = DateTimeLocalField(required=False)
    fecha_fin_formulario = DateTimeLocalField(required=False)


    class Meta:
        model = eva_models.Formulario

        fields = ('usuario', 'evaluacion','fecha_inicio_formulario', 'fecha_fin_formulario','sede')
        widgets = {
                'usuario': forms.Select(attrs={'class': 'select2 form-control'}),
                'sede': forms.Select(attrs={'class': 'select2 form-control'}),
                'Evaluacion': forms.Select(attrs={'class': 'select2 form-control'}),
                'fecha_inicio_formulario': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
                }),
                'fecha_fin_formulario': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
                }),
            }
        
        fecha_inicio_formulario = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            required=False
        )
        fecha_fin_formulario = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            required=False
        )
        

    def __init__(self, *args, **kwargs):
        super(FormularioForm, self).__init__(*args, **kwargs)
        
        fecha_inicio = datetime(2024, 1, 1)
        self.fields['sede'].queryset = cyd_models.Sede.objects.filter(finalizada=False, fecha_creacion__gte=fecha_inicio)

        self.fields['usuario'].queryset = User.objects.filter(groups__name="cyd_capacitador")
        self.fields['usuario'].label_from_instance = lambda usuario: usuario.get_full_name()



class InformeEstadisticasForm(forms.ModelForm):
    """ Formulario para el control de la creación de un formulario
    """
    class Meta:
        model = eva_models.Formulario
        fields = ('usuario', 'escuela','sede','evaluacion','fecha_inicio_formulario','fecha_fin_formulario')
        exclude = ('escuela',)
        widgets = {
            'sede': forms.Select(attrs={'class': 'select2 form-control'}),
            'evaluacion': forms.Select(attrs={'class': 'select2 form-control'}),
        }


    departamento = forms.ModelMultipleChoiceField(
        queryset= Departamento.objects.all(),
        required=False,
        label="Departamentos",
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )
    
    municipio = forms.ModelMultipleChoiceField(
        queryset= Municipio.objects.all(),  
        required=False,
        label="Municipios",
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )

    usuario = forms.ModelMultipleChoiceField(
        queryset= User.objects.filter(groups__name="cyd_capacitador"), 
        required=False,
        label="Capacitador",
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )

    fecha_inicio_formulario = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}),
        required=False)
    
    
    fecha_fin_formulario = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}),
        required=False)


        
    def __init__(self, *args, **kwargs):
        super(InformeEstadisticasForm, self).__init__(*args, **kwargs)

        fecha_inicio = datetime(2024, 1, 1)
        self.fields['sede'].queryset = cyd_models.Sede.objects.filter(fecha_creacion__gte=fecha_inicio)
        self.fields['usuario'].label_from_instance = lambda usuario: usuario.get_full_name()
        self.fields['evaluacion'].required = False

