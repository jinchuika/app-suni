from django import forms
from django.forms import ModelForm
from  apps.Evaluacion import models as eva_models 
from apps.cyd import models as cyd_models
from braces.views import (
    LoginRequiredMixin, GroupRequiredMixin
)
from django.contrib.auth.models import User
from django.forms.widgets import TextInput


class FormularioAdd(forms.ModelForm):
    """ Formulario para el control de la creación de un formulario
    """

    udi = forms.CharField(
        label='Escuela Beneficiada',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '13', 'required': 'true', 'placeholder': '00-00-0000-00', 'tabindex': '4'}))

    class Meta:
        model = eva_models.formulario
        fields = ('usuario', 'escuela', 'evaluacion','fecha_inicio_formulario', 'fecha_fin_formulario')
        exclude = ('escuela',)
        widgets = {
                'usuario': forms.Select(attrs={'class': 'select2 form-control'}),
                'Evaluacion': forms.Select(attrs={'class': 'select2 form-control'}),
            }
        
    def __init__(self, *args, **kwargs):
        super(FormularioAdd, self).__init__(*args, **kwargs)
        
        self.fields['usuario'].queryset = User.objects.filter(groups__name="cyd_capacitador")
        self.fields['usuario'].label_from_instance = lambda usuario: usuario.get_full_name()



class FormularioForm(forms.ModelForm):
    """ Formulario para el control del listado de formulario, editar fomrulario
    """

    class Meta:
        model = eva_models.formulario
        fields = ('usuario', 'escuela', 'evaluacion','fecha_inicio_formulario', 'fecha_fin_formulario')
        widgets = {
                'usuario': forms.Select(attrs={'class': 'select2 form-control'}),
                'Evaluacion': forms.Select(attrs={'class': 'select2 form-control'}),

            }
        
    def __init__(self, *args, **kwargs):
        super(FormularioForm, self).__init__(*args, **kwargs)
        
        self.fields['usuario'].queryset = User.objects.filter(groups__name="cyd_capacitador")
        self.fields['usuario'].label_from_instance = lambda usuario: usuario.get_full_name()