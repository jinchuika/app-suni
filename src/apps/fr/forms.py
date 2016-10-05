from django import forms 
from django.forms import ModelForm, ModelChoiceField, formset_factory, modelformset_factory, widgets
from .models import *

class FormEmpresa(forms.ModelForm):
	class Meta:
		model = Empresa
		fields = '__all__'

class FormEvento(forms.ModelForm):
	class Meta:
		model = Evento
		fields = '__all__'
		widgets = {
		'fecha':forms.TextInput(attrs = {'class' : 'datepicker '}),
		}

class FormContacto(forms.ModelForm):
	class Meta:
		model = Contacto
		fields = ['nombre', 'apellido', 'direccion', 'etiquetas', 'evento', 'empresa', 'puesto', 'observacion']
		widgets = {
		'etiquetas': forms.SelectMultiple(attrs = {'class' : 'select2'}),
		'evento': forms.SelectMultiple(attrs = {'class' : 'select2'}),
		}