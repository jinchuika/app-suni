from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from apps.inventario import models as inv_m


class RepuestoForm(forms.Form):
    """ Este Formulario se encarga de enviar los filtros para las respectivas busquedas
    """

    id = forms.IntegerField(
        label='No. Repuesto',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    tipo = forms.ModelChoiceField(
        queryset=inv_m.DispositivoTipo.objects.all(),
        label='Tipo de dispositivo',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    marca = forms.ModelChoiceField(
        queryset=inv_m.DispositivoMarca.objects.all(),
        label='Marca',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'}))

    modelo = forms.CharField(
        label='Modelo',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    tarima = forms.ModelChoiceField(
        queryset=inv_m.Tarima.objects.all(),
        label='Tarima',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'}))


class RepuestosUpdateForm(forms.ModelForm):
    """Formulario para la edicion de los repuestos de la :class:`Repuesto`
    """
    class Meta:
        model = inv_m.Repuesto
        fields = '__all__'
        exclude = ['tipo', 'estado', 'codigo_qr', 'entrada', 'entrada_detalle', 'impreso', 'disponible', 'valido']
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 80, 'rows': 5, 'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control select2'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2'})
        }
