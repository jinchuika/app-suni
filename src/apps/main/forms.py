from django import forms
from django.core.urlresolvers import reverse_lazy

from apps.main.models import Departamento, Municipio


class GeoForm(forms.Form):
    """Formulario para mostrar listados de :model:`main.Departamento`
    y :model:`main.Municipio`. El departamento incluye la URL para generar
    un listado de municipios usando AJAX.
    """
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        widget=forms.Select(attrs={'data-url': reverse_lazy('municipio_api_list')}))
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


class DateRangeWidget(forms.TextInput):
    class Media:
        css = ('css/daterangepicker.css',)
        js = (
            'js/distributed/moment.min.js',
            'js/distributed/daterangepicker.js')
