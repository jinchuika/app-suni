from django import forms 
from django.forms import ModelForm, ModelChoiceField, formset_factory, modelformset_factory
from .models import *


#class EquipoForm(forms.Form):
#	equipo = forms.CharField(max_length=100)

class FormularioEquipo(ModelForm):
	class Meta:
		model = Equipo
		fields = ['nombre_equipo']


class FormularioEntrada(forms.ModelForm):
	fecha = forms.CharField(widget=forms.TextInput(attrs={'class':'datepicker'}))
	class Meta:
		model = Entrada
		fields = '__all__'

class FormularioSalida(forms.ModelForm):
	fecha = forms.CharField(widget=forms.TextInput(attrs={'class':'datepicker'}))
	class Meta:
		model = Salida
		fields = '__all__'

class FormularioProveedor(forms.ModelForm):
	class Meta:
		model = Proveedor
		fields = '__all__'
