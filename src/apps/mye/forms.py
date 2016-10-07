from django import forms
from django.forms import ModelForm
from .models import Cooperante, EscuelaCooperante
from apps.escuela.models import Escuela

class CooperanteForm(ModelForm):
	class Meta:
		model = Cooperante
		fields = '__all__'
		widgets = { 'nombre': forms.TextInput(attrs={'class': 'form-control'})}

class EscuelaCooperanteForm(ModelForm):
	class Meta:
		model = Escuela
		fields = ['cooperante_asignado']
		widgets = {
			'cooperante_asignado': forms.SelectMultiple(attrs={'class': 'select2'})
		}