from django import forms
from datetime import date
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from apps.recaudacionFondos import models as rf_m


class ProveedoresUpdateForm(forms.ModelForm):
    """Formulario para la  :class:`ProveedorUpdateView`
    """
    class Meta:
        model = rf_m.Proveedor
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control'})
            }

class EntradaForm(forms.ModelForm):
    field_order = ['proveedor','fecha','observaciones']
    class Meta:
        model = rf_m.Entrada
        fields = '__all__'
        exclude = ['terminada']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'select2'}),
            'fecha': forms.TextInput(attrs={'class': 'datepicker'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'})
        }

class EntradaDetalleForm(forms.ModelForm):

    """Para agregar un :model:`kardex.EntradaDetalle` a una
    :model:`recolecionFondos.Entrada`.
    """
    field_order = ['articulo','cantidad','caja']
    class Meta:
        model = rf_m.DetalleEntrada
        fields = '__all__'
        widgets = {
            'articulo': forms.Select(attrs={'class': 'select2'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control'}),
            'caja': forms.TextInput(attrs={'class': 'form-control'}),
            'tarima': forms.Select(attrs={'class': 'select2'}),
            'entrada': forms.HiddenInput()
        }

class RecaudacionInformeForm(forms.Form):

    """Formulario de filtros para el informe de inventario en recaudacionFondos.
    """

    articulo = forms.ModelChoiceField(
        required=False,
        queryset=rf_m.Articulo.objects.all(),
        widget=forms.Select(attrs={'class': 'select2 form-control', 'id': 'articulo_informe'}))
    fecha_inicio = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'datepicker form-control'}))
    fecha_fin = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'datepicker form-control'}))

class ArticuloForm(forms.ModelForm):

    """Para agregar un :model:`kardex.EntradaDetalle` a una
    :model:`recolecionFondos.Entrada`.
    """
    field_order = ['nombre','articulo','precio']
    class Meta:
        model = rf_m.Articulo
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'select2'}),

        }

class SalidaForm(forms.ModelForm):
    field_order = ['tipo','fecha','url','observaciones']
    class Meta:
        model = rf_m.Salida
        fields = '__all__'
        exclude = ['terminada']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'select2'}),
            'fecha': forms.TextInput(attrs={'class': 'datepicker'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'})
        }

class SalidaDetalleForm(forms.ModelForm):

    """Para agregar un :model:`kardex.EntradaDetalle` a una
    :model:`recolecionFondos.Entrada`.
    """
    field_order = ['articulo','cantidad','precio']
    class Meta:
        model = rf_m.DetalleSalida
        fields = '__all__'
        widgets = {
            'articulo': forms.Select(attrs={'class': 'select2'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.TextInput(attrs={'class': 'form-control'}),
            'salida': forms.HiddenInput()
        }
