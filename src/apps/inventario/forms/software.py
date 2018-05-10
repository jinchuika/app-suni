
from django import forms
from django.forms import ModelForm
from apps.inventario import models as inv_m


class SoftwareCreateForm(forms.ModelForm):
    class Meta:
        model = inv_m.Software
        fields = '__all__'


class VersionSistemaForm(forms.ModelForm):
    class Meta:
        model = inv_m.VersionSistema
        fields = '__all__'
