from django import forms
from django.urls import reverse_lazy
from django.forms import ModelForm
from django.contrib.auth.models import User

from apps.conta import models as conta_m
from apps.inventario import models as inventario_m


class PeriodoFiscalForm(forms.ModelForm):
    """ Formulario para el control de los periodos fiscales
    """
    class Meta:
        model = conta_m.PeriodoFiscal
        fields = '__all__'
        widgets = {
            'fecha_inicio': forms.TextInput({'class': 'form-control datepicker'}),
            'fecha_fin': forms.TextInput({'class': 'form-control datepicker'})
        }


class PeriodoFiscalUpdateForm(forms.ModelForm):
    """ Formulario para la actualizacion de los periodos fiscales
    """
    class Meta:
        model = conta_m.PeriodoFiscal
        fields = '__all__'
        exclude = ['fecha_fin', 'fecha_inicio']


class PrecioEstandarForm(forms.ModelForm):
    """ Formulario para la crecion de :class:`PrecioEstandar`
    """
    class Meta:
        model = conta_m.PrecioEstandar
        fields = '__all__'
        exclude = ['periodo', 'creado_por']
        widgets = {
            'tipo_dispositivo': forms.Select(attrs={'class': 'form-control select2'}),
            'activo': forms.HiddenInput(),
            'precio': forms.TextInput(attrs={'class': 'form-control'}),
            'inventario': forms.Select(attrs={'class': 'form-control select2'})
        }


class PrecioEstandarInformeForm(forms.Form):
    """ Formulario para la aplicacion de filtros de busqueda de precio estandar
    """
    periodo = forms.ModelChoiceField(
        queryset=conta_m.PeriodoFiscal.objects.all(),
        label="Periodo Fiscal",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    tipo_dispositivo = forms.ModelChoiceField(
        queryset=inventario_m.DispositivoTipo.objects.all(),
        label="Tipo de Dispositivo",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
