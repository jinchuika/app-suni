from django import forms

from apps.kalite.models import Rubrica, Indicador


class RubricaForm(forms.ModelForm):
    class Meta:
        model = Rubrica
        fields = '__all__'


class IndicadorForm(forms.ModelForm):
    class Meta:
        model = Indicador
        fields = '__all__'
        widgets = {
            'rubrica': forms.HiddenInput()
        }
