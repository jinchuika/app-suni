from django import forms
from django.forms import ModelForm, ModelChoiceField, formset_factory, modelformset_factory, widgets
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from apps.fr.models import *

class FormEmpresa(forms.ModelForm):
	class Meta:
		model = Empresa
		fields = '__all__'
		exclude = ('fr_empresa_creada_por',)

class FormEvento(forms.ModelForm):
	class Meta:
		model = Evento
		fields = '__all__'
		widgets = {
		'fecha':forms.TextInput(attrs = {'class' : 'datepicker '}),
		}
		exclude = ('fr_evento_creada_por',)
class FormContacto(forms.ModelForm):
	class Meta:
		model = Contacto
		fields = '__all__'
		widgets = {
		'etiquetas': forms.SelectMultiple(attrs = {'class' : 'select2'}),
		'evento': forms.SelectMultiple(attrs = {'class' : 'select2'}),
		}
		exclude = ('fr_contacto_creada_por',)
class FormContactoEmpresa(forms.ModelForm):
	class Meta:
		model = Contacto
		fields = '__all__'
		widgets = {
		'empresa' : forms.HiddenInput(),
		'nombre': forms.TextInput(attrs = {'class' : 'form-control'}),
		'apellido': forms.TextInput(attrs = {'class' : 'form-control'}),
		'direccion': forms.TextInput(attrs = {'class' : 'form-control'}),
		'etiquetas': forms.SelectMultiple(attrs = {'class' : 'select2'}),
		'evento': forms.SelectMultiple(attrs = {'class' : 'select2'}),
		'observacion': forms.Textarea(attrs = {'class' : 'form-control'}),
		'puesto': forms.TextInput(attrs = {'class' : 'form-control'}),
		}
		exclude = ('fr_contacto_creada_por',)

ContactoTelefonoFormSet = inlineformset_factory(Contacto, ContactoTelefono, fields='__all__',extra=1, can_delete=True)
ContactoMailFormSet = inlineformset_factory(Contacto, ContactoMail, fields='__all__', extra=1,can_delete=True)
