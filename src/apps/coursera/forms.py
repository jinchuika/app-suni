from django import forms
from datetime import date
from django.urls import reverse_lazy
from django.forms.models import inlineformset_factory
from django.forms.formsets import BaseFormSet, formset_factory

from apps.coursera import models as coursera_m

class FormMonitoreoCrear(forms.ModelForm):
	fecha = forms.DateField(initial=date.today(), widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
	invitaciones = forms.CharField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}))
	miembros = forms.CharField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}))
	aliado = forms.ModelChoiceField(queryset=coursera_m.Aliado.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control select2'}))

	class Meta:
		model = coursera_m.Monitoreo
		fields = '__all__'