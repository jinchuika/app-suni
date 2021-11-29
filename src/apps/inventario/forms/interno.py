#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import forms
from apps.inventario import models as inv_m
from apps.crm import models as crm_m
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import Q

class InventarioInternoForm(forms.ModelForm):
	""" Formulario para la asignación de dispositivos a inventario interno """

	colaborador_asignado = forms.ModelChoiceField(
        queryset= User.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'})
    )
	
	class Meta:
		model = inv_m.InventarioInterno
		fields = '__all__'
		exclude = ['no_asignacion', 'creada_por', 'fecha_devolucion', 'estado', 'fecha_asignacion', 'borrador']

	def __init__(self, *args, **kwargs):
		super(InventarioInternoForm, self).__init__(*args, **kwargs)
		self.fields['colaborador_asignado'].label_from_instance = lambda obj: "%s" % obj.get_full_name()

class InventarioInternoDispositivosForm(forms.ModelForm):
	""" Formulario para la asignación de dispositivos de inventario """

	tipo_dispositivo = forms.ModelChoiceField(
		queryset=inv_m.DispositivoTipo.objects.filter(usa_triage=True),
		widget=forms.Select(attrs={'class': 'form-control select2'})
	)

	dispositivo = forms.ModelChoiceField(
		queryset=inv_m.Dispositivo.objects.none(),
		widget=forms.Select(attrs={'class': 'form-control select2'})
	)

	class Meta:
		model = inv_m.IInternoDispositivo
		fields = ('no_asignacion', 'tipo_dispositivo', 'dispositivo',)
		widgets = {
			'no_asignacion': forms.HiddenInput(),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['dispositivo'].queryset = inv_m.Dispositivo.objects.none()
		if 'tipo_dispositivo' in self.data:
			try:
				tipo = int(self.data.get('tipo_dispositivo'))
				self.fields['dispositivo'].queryset = inv_m.Dispositivo.objects.filter(
					tipo=tipo).order_by()
			except (ValueError, TypeError):
				pass

class InventarioInternoInformeForm(forms.Form):
	""" Formulario con parámetros de búsqueda para el informe de asignaciones de inventario interno"""

	estado = forms.ModelChoiceField(
		queryset=inv_m.IInternoEstado.objects.filter(~Q(id=inv_m.IInternoEstado.BR)),
		label='Estado',
		widget=forms.Select(attrs={'class': 'form-control select2'}),
		required=False)

	colaborador = forms.ModelChoiceField(
		queryset=User.objects.all(),
		label='Colaborador',
		widget=forms.Select(attrs={'class': 'form-control select2'}),
		required=False)

	tipo_dispositivo = forms.ModelChoiceField(
		queryset=inv_m.DispositivoTipo.objects.filter(usa_triage=True),
		label='Tipo Dispositivo',
		widget=forms.Select(attrs={'class': 'form-control select2'}),
		required=False)

	fecha_min = forms.CharField(
		label='Fecha (min)',
		required=False,
		widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))

	fecha_max = forms.CharField(
		label='Fecha (max)',
		required=False,
		widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))

	def __init__(self, *args, **kwargs):
		super(InventarioInternoInformeForm, self).__init__(*args, **kwargs)
		self.fields['colaborador'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())