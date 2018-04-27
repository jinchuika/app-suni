from django import forms
from django.urls import reverse_lazy
from django.forms import ModelForm
from django.contrib.auth.models import User

from apps.crm import models as crm_m


class DonanteForm(forms.ModelForm):
    """Formulario para la  :class:`DonanteCreateView` y :class:`DonanteUpdateView`
    """
    class Meta:
        model = crm_m.Donante
        fields = '__all__'
        widgets = {
            'fax': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'})
        }


class ContactoForm(forms.ModelForm):
    """Formulario para la  :class:`ContactoCreateView` y :class:`ContactoDetailView`
    """
    class Meta:
        model = crm_m.DonanteContacto
        fields = '__all__'
        widgets = {
             'donante': forms.HiddenInput(attrs={'class': 'form-control'})
        }


class OfertaForm(forms.ModelForm):
    """Formulario para la :class:`OfertaCreateView` y :class:`OfertaUpdateView`
    """
    class Meta:
        model = crm_m.Oferta
        fields = '__all__'
        widgets = {
            'fecha_inicio': forms.TextInput({'class': 'form-control datepicker'}),
            'fecha_bodega': forms.TextInput({'class': 'form-control datepicker'}),
            'fecha_carta': forms.TextInput({'class': 'form-control datepicker'})

        }

    def __init__(self, *args, **kwargs):
        super(OfertaForm, self).__init__(*args, **kwargs)
        self.fields['recibido_por'].label_from_instance = lambda obj: "%s" % obj.get_full_name()


class OfertaInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Ofertas
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
    """Formulario para la Creacion de Telefonos de la :class:`TelefonoCreateView`
    """
    class Meta:
        model = crm_m.TelefonoCrm
        fields = '__all__'
        widgets = {
            'donante': forms.HiddenInput()
        }


class CorreoForm(forms.ModelForm):
    """Formulario para la Creacion de Correos de la :class:`CorreoCreateView`
    """
    class Meta:
        model = crm_m.MailCrm
        fields = '__all__'
        widgets = {
            'donante': forms.HiddenInput()
        }
