from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.forms import authenticate
from django.core.exceptions import ValidationError
from apps.escuela.models import Escuela, EscContacto, EscContactoTelefono, EscContactoMail
from django.forms.models import inlineformset_factory, BaseInlineFormSet

class FormEscuelaCrear(forms.ModelForm):
	class Meta:
		model = Escuela
		fields = '__all__'
		exclude = ['cooperante_asignado']
		widgets = {
			'municipio': forms.Select(attrs={'class': 'select2'})
		}

class ContactoForm(forms.ModelForm):
	class Meta:
		model = EscContacto
		fields = '__all__'
		widgets = {
			'escuela':forms.HiddenInput()
		}

class ContactoTelefonoForm(forms.ModelForm):
	class Meta:
		model = EscContactoTelefono
		fields = '__all__'

ContactoTelefonoFormSet = inlineformset_factory(EscContacto, EscContactoTelefono, fields='__all__',extra=1, can_delete=True)
ContactoMailFormSet = inlineformset_factory(EscContacto, EscContactoMail, fields='__all__', extra=1,can_delete=True)