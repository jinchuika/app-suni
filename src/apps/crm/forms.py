from django import forms
from django.urls import reverse_lazy
from django.forms import ModelForm
from django.contrib.auth.models import User

from apps.crm import models as crm_m


class DonanteForm(forms.ModelForm):
    class Meta:
        model = crm_m.Donante
        fields = '__all__'
        widgets = {
            'fax': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'})
        }


class ContactoForm(forms.ModelForm):
    class Meta:
        model = crm_m.DonanteContacto
        fields = '__all__'
        widgets = {
            'donante': forms.HiddenInput(attrs={'class': 'form-control'})
        }

    """def __init__(self, *args, **kwargs):
        super(ContactoForm, self).__init__(*args, **kwargs)
        self.fields['donante'].label = """""


class OfertaForm(forms.ModelForm):
    class Meta:
        model = crm_m.Oferta
        fields = '__all__'


class TelefonoForm(forms.ModelForm):
    class Meta:
        model = crm_m.TelefonoCrm
        fields = '__all__'
        widgets = {
            'donante': forms.HiddenInput()
        }


class CorreoForm(forms.ModelForm):
    class Meta:
        model = crm_m.MailCrm
        fields = '__all__'
        widgets = {
            'donante': forms.HiddenInput()
        }
