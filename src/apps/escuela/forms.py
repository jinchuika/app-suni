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
		widgets = {
			'municipio': forms.Select(attrs={'class': 'select2'})
		}

class ContactoForm(forms.ModelForm):
	class Meta:
		model = EscContacto
		fields = '__all__'

class ContactoTelefonoForm(forms.ModelForm):
	class Meta:
		model = EscContactoTelefono
		fields = '__all__'

def get_contacto_telefono_formset(form, formset=BaseInlineFormSet, **kwargs):
	return inlineformset_factory(EscContacto, EscContactoTelefono, form, formset, **kwargs)
		

ContactoTelefonoFormSet = inlineformset_factory(EscContacto, EscContactoTelefono, fields='__all__', extra=2)
ContactoMailFormSet = inlineformset_factory(EscContacto, EscContactoMail, fields='__all__', extra=1)