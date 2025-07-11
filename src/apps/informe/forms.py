from django import forms
from datetime import date
from django.urls import reverse_lazy
from django.forms.models import inlineformset_factory
from django.forms.formsets import BaseFormSet, formset_factory
from apps.escuela.models import (
    Escuela, EscContacto, EscContactoTelefono,
    EscContactoMail, EscNivel, EscSector, EscPoblacion,
    EscMatricula, EscRendimientoAcademico)
from apps.main.models import Departamento, Municipio
from apps.mye.models import Cooperante, Proyecto
from django.contrib.auth.models import User

class informeForm(forms.Form):
    ESTADO_CHOICES = (
        (None, 'No importa'),
        (True, 'Sí'),
        (False, 'No'),)
    codigo = forms.CharField(
        label='Udi',
        required=False)
    nombre = forms.CharField(
        required=False)
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        widget=forms.Select(attrs={'data-url': reverse_lazy('municipio_api_list')}),
        required=False)
    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all(),
        required=False)
    fecha_min = forms.CharField(
        label='Fecha (min)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max = forms.CharField(
        label='Fecha (max)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))

    equipada = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=ESTADO_CHOICES,
        required=False,
        )
    cooperante_tpe = forms.ModelChoiceField(
        label='Cooperante de equipamiento',
        queryset=Cooperante.objects.all(),
        required=False)
    proyecto_tpe = forms.ModelChoiceField(
        label='Proyecto de equipamiento',
        queryset=Proyecto.objects.all(),
        required=False)
    capacitador = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='cyd_capacitador'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'}))
    capacitada = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=ESTADO_CHOICES,
        required=False,
        )
    fecha_min_capacitacion = forms.CharField(
        label='Fecha (min)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max_capacitacion = forms.CharField(
        label='Fecha (max)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    def __init__(self, *args, **kwargs):
        super(informeForm, self).__init__(*args, **kwargs)
        self.fields['capacitador'].label_from_instance = lambda obj: "%s" % obj.get_full_name()

class informeEscuelaForm(forms.Form):
    codigo = forms.CharField(
        label='Udi',
        required=False)
    nombre = forms.CharField(
        required=False)
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        widget=forms.Select(attrs={'data-url': reverse_lazy('municipio_api_list')}),
        required=False)
    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all(),
        required=False)

class informeEquipamientoForm(forms.Form):
    ESTADO_CHOICES = (
        (None, 'No importa'),
        (True, 'Sí'),
        (False, 'No'),)
    fecha_min = forms.CharField(
        label='Fecha (min)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max = forms.CharField(
        label='Fecha (max)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))

    equipada = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=ESTADO_CHOICES,
        required=False,
        )
    cooperante_tpe = forms.ModelChoiceField(
        label='Cooperante de equipamiento',
        queryset=Cooperante.objects.all(),
        required=False)
    proyecto_tpe = forms.ModelChoiceField(
        label='Proyecto de equipamiento',
        queryset=Proyecto.objects.all(),
        required=False)

class informeCapacitadaForm(forms.Form):
    ESTADO_CHOICES = (
        (0, 'No importa'),
        (1, 'Sí'),
        (2, 'No'),)
    capacitador = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='cyd_capacitador'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'}))
    capacitada = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=ESTADO_CHOICES,
        required=False,
        )
    fecha_min_capacitacion = forms.CharField(
        label='Fecha (min)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max_capacitacion = forms.CharField(
        label='Fecha (max)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    def __init__(self, *args, **kwargs):
        super(informeCapacitadaForm, self).__init__(*args, **kwargs)
        self.fields['capacitador'].label_from_instance = lambda obj: "%s" % obj.get_full_name()
