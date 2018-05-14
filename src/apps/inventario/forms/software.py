
from django import forms
from django.forms import ModelForm
from apps.inventario import models as inv_m


class SoftwareCreateForm(forms.ModelForm):
    """Formulario para la  :class:`SoftwareCreateView` y :class:`SoftwareUpdateView`
    """
    class Meta:
        model = inv_m.Software
        fields = '__all__'


class VersionSistemaForm(forms.ModelForm):
    """Formulario para la  :class:`VersionSistemaCreateView` y :class:`VersionSistemaUpdateView`
    """
    class Meta:
        model = inv_m.VersionSistema
        fields = '__all__'
