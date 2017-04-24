from django import forms
from apps.main.models import Departamento, Municipio


class GeoForm(forms.Form):
    departamento = forms.ModelChoiceField(Departamento.objects.all())
    municipio = forms.ModelChoiceField(Municipio.objects.all())


class DateForm(forms.Form):
    fecha_min = forms.CharField(
        label='Fecha mínima',
        widget=forms.TextInput(attrs={'class': 'datepicker'}),
        required=False)
    fecha_max = forms.CharField(
        label='Fecha máxima',
        widget=forms.TextInput(attrs={'class': 'datepicker'}),
        required=False)


class GeoDateForm(GeoForm, DateForm):
    def __init__(self, *args, **kwargs):
        super(GeoDateForm, self).__init__(*args, **kwargs)
