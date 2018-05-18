
from django import forms
from django.forms import ModelForm
from apps.inventario import models as inv_m


class SoftwareCreateForm(forms.ModelForm):
    """Formulario para la  :class:`SoftwareCreateView` y :class:`SoftwareUpdateView`
    """
    class Meta:
        model = inv_m.Software
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control select2'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'})
            }


class VersionSistemaForm(forms.ModelForm):
    """Formulario para la  :class:`VersionSistemaCreateView` y :class:`VersionSistemaUpdateView`
    """
    class Meta:
        model = inv_m.VersionSistema
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'so': forms.Select(attrs={'class': 'form-control select2'}),
            'software': forms.SelectMultiple(attrs={'class': 'form-control select2'})
            }
