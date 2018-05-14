from django import forms
from django.forms import ModelForm
from apps.inventario import models as inv_m

class TecladoForm(forms.ModelForm):
    class Meta:
        model = inv_m.Teclado
        
