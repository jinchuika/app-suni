
from django import forms
from django.forms import ModelForm
from apps.inventario import models as inv_m


class TarimaForm(forms.ModelForm):
    class Meta:
        model = inv_m.Tarima
        fields = '__all__'
        exclude = ('creada_por',)


class SectorForm(forms.ModelForm):
    class Meta:
        model = inv_m.Sector
        fields = '__all__'
        exclude = ('creada_por',)

class NivelForm(forms.ModelForm):
    class Meta:
        model = inv_m.Nivel
        fields = '__all__'
        exclude = ('creada_por',)

class PasilloForm(forms.ModelForm):
    class Meta:
        model = inv_m.Pasillo
        fields = '__all__'
