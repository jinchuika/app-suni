from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.forms import authenticate
from django.core.exceptions import ValidationError
from apps.escuela.models import Escuela
from apps.main.models import Municipio

class FormEscuelaCrear(forms.ModelForm):
	class Meta:
		model = Escuela
		fields = '__all__'
		widgets = {
			'municipio': forms.Select(attrs={'class': 'select2'})
		}