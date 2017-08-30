from django import forms

from apps.kalite.models import Rubrica, Indicador, Visita, TipoVisita, Grado


class TipoVisitaForm(forms.ModelForm):
    class Meta:
        model = TipoVisita
        fields = '__all__'
        widgets = {
            'rubricas': forms.CheckboxSelectMultiple()
        }


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


class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ('numero', 'tipo_visita', 'escuela', 'fecha', 'hora_inicio', 'hora_fin')
        widgets = {
            'escuela': forms.HiddenInput(),
            'fecha': forms.TextInput(attrs={'class': 'datepicker'})
        }


class GradoForm(forms.ModelForm):
    class Meta:
        model = Grado
        fields = ('visita', 'grado', 'seccion')
        widgets = {
            'visita': forms.HiddenInput()
        }
