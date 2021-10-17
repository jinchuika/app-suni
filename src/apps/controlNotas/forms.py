from django import forms
from django.forms import ModelForm
from apps.controlNotas import models as control_m

class EvaluacionForm(forms.ModelForm):
    """ Formulario para el control de los periodos fiscales
    """
    class Meta:
        model = control_m.Evaluacion
        exclude = ('visita','cn_evaluacion_creado_por')
        fields = '__all__'
        widgets = {
            'materia': forms.Select(attrs={'class': 'form-control select2'}),
            'grado': forms.Select(attrs={'class': 'form-control select2'}),
            'observacion':forms.Textarea(attrs={'class': 'form-control'})
        }
