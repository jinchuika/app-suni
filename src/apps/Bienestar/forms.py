from django import forms
from apps.Bienestar.models import Colaborador

class CuestionarioForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = '__all__'

class BienestarInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Bienestar
    """
    colaborador = forms.ModelChoiceField(
        queryset=Colaborador.objects.values_list('usuario',flat=True).distinct(),
        label='Colaborador',
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        )

    fecha_min = forms.CharField(
        label='Fecha (min)',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max = forms.CharField(
        label='Fecha (max)',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
