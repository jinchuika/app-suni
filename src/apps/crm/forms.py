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


class OfertaForm(forms.ModelForm):
    class Meta:
        model = crm_m.Oferta
        fields = '__all__'
        widgets = {
        }

    def __init__(self, *args, **kwargs):
        super(OfertaForm, self).__init__(*args, **kwargs)
        self.fields['recibido_por'].label_from_instance = lambda obj: "%s" % obj.get_full_name()


class OfertaInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de visitas de monitoreo
    """
    donante = forms.ModelChoiceField(
        queryset=crm_m.Donante.objects.all(),
        label='Donante',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False)
    tipo_oferta = forms.ModelChoiceField(
        queryset=crm_m.OfertaTipo.objects.all(),
        label='Tipo de Oferta',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))

    fecha_min = forms.CharField(
        label='Fecha (min)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max = forms.CharField(
        label='Fecha (max)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))


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
