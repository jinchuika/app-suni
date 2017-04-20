from django import forms
from django.forms.models import inlineformset_factory
from django.forms.formsets import BaseFormSet, formset_factory

from apps.escuela.models import (
    Escuela, EscContacto, EscContactoTelefono,
    EscContactoMail, EscNivel, EscSector)
from apps.main.models import Departamento, Municipio
from apps.mye.models import Cooperante, Proyecto


class FormEscuelaCrear(forms.ModelForm):
    lat = forms.CharField(
        required=False,
        label='Latitud',
        widget=forms.NumberInput(attrs={'step': 'any'}))
    lng = forms.CharField(
        required=False,
        label='Longitud',
        widget=forms.NumberInput(attrs={'step': 'any'}))

    class Meta:
        model = Escuela
        fields = '__all__'
        exclude = ['cooperante_asignado', 'proyecto_asignado', 'mapa']
        widgets = {
            'municipio': forms.Select(attrs={'class': 'select2'})
        }


class EscuelaBuscarForm(forms.Form):
    ESTADO_CHOICES = (
        (None, 'No importa'),
        (False, 'Sí'),
        (True, 'No'),)
    cooperante_mye = forms.ModelChoiceField(
        label='Cooperante en proceso',
        queryset=Cooperante.objects.all(),
        required=False)
    proyecto_mye = forms.ModelChoiceField(
        label='Proyecto en proceso',
        queryset=Proyecto.objects.all(),
        required=False)
    codigo = forms.CharField(
        label='Código',
        required=False)
    nombre = forms.CharField(
        required=False)
    direccion = forms.CharField(
        label='Dirección',
        widget=forms.TextInput(),
        required=False)
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        required=False)
    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all(),
        required=False)
    nivel = forms.ModelChoiceField(
        queryset=EscNivel.objects.all(),
        required=False)
    sector = forms.ModelChoiceField(
        queryset=EscSector.objects.all(),
        required=False)
    poblacion_min = forms.IntegerField(
        label='Población mínima',
        required=False)
    poblacion_max = forms.IntegerField(
        label='Población máxima',
        required=False)
    solicitud = forms.ChoiceField(
        required=False,
        choices=ESTADO_CHOICES)
    solicitud_id = forms.IntegerField(
        label='Número de solicitud',
        min_value=1,
        required=False)
    validacion = forms.ChoiceField(
        label='Validación',
        required=False,
        choices=ESTADO_CHOICES)
    validacion_id = forms.IntegerField(
        label='Número de validación',
        min_value=1,
        required=False)
    equipamiento = forms.ChoiceField(
        required=False,
        choices=ESTADO_CHOICES)
    equipamiento_id = forms.IntegerField(
        label='Número de entrega',
        min_value=1,
        required=False)
    cooperante_tpe = forms.ModelChoiceField(
        label='Cooperante de equipamiento',
        queryset=Cooperante.objects.all(),
        required=False)
    proyecto_tpe = forms.ModelChoiceField(
        label='Proyecto de equipamiento',
        queryset=Proyecto.objects.all(),
        required=False)


class ContactoForm(forms.ModelForm):
    telefono = forms.CharField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}))
    mail = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = EscContacto
        fields = '__all__'
        widgets = {
            'escuela': forms.HiddenInput()
        }


class EscContactoTelefonoForm(forms.ModelForm):
    class Meta:
        model = EscContactoTelefono
        fields = '__all__'
        exclude = ['contacto']


class EscContactoTelefonoFormset(BaseFormSet):
    def clean(self):
        telefonos = []
        if any(self.errors):
            return

        for form in self.forms:
            if form.cleaned_data:
                telefono = form.cleaned_data['telefono']
                if telefono in telefonos:
                    raise forms.ValidationError('Los números no pueden repetirse')
                telefonos.append(telefono)


ContactoTelefonoFormSet = inlineformset_factory(
    EscContacto,
    EscContactoTelefono,
    fields='__all__',
    extra=1,
    can_delete=True)
ContactoMailFormSet = inlineformset_factory(
    EscContacto,
    EscContactoMail,
    fields='__all__',
    extra=1,
    can_delete=True)

MailFormSet = formset_factory(EscContactoTelefonoFormset, formset=EscContactoTelefonoFormset)
