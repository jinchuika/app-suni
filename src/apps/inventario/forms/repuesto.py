from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from apps.inventario import models as inv_m


class RepuestoForm(forms.Form):
    """ Este Formulario se encarga de enviar los filtros para las respectivas busquedas
    """
    tipo = forms.ModelChoiceField(
        queryset=inv_m.DispositivoTipo.objects.all(),
        label='Tipo de dispositivo',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tarima = forms.CharField(
        label='Tarima',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))


class RepuestosUpdateForm(forms.ModelForm):
    """Formulario para la edicion de los repuestos de la :class:`Repuesto`
    """
    class Meta:
        model = inv_m.Repuesto
        fields = '__all__'
        exclude = ['tipo', 'estado', 'tarima', 'codigo_qr', 'entrada']
