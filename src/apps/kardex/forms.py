from django import forms 
from django.forms import ModelForm, ModelChoiceField, formset_factory, modelformset_factory, widgets
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from .models import *
from apps.kardex.models import *
from django.utils.translation import ugettext_lazy as _
from datetime import date

#class EquipoForm(forms.Form):
#	equipo = forms.CharField(max_length=100)

class FormularioEquipo(ModelForm):
	class Meta:
		model = Equipo
		fields = ['nombre_equipo']
		labels = {
			'nombre_equipo' : _('Nombre del Equipo'),
		}

class FormularioEntradaInforme(forms.ModelForm):
	class Meta:
		model = Entrada
		fields = ['tipo_entrada']
		labels = {'tipo_entrada': _('Tipo de Entrada')}
		widgets= {
			'tipo_entrada':forms.Select(attrs={'class':' form-control'}),
			}

class FormularioEntrada(forms.ModelForm):	
	class Meta:
		model = Entrada
		fields = '__all__'
		labels = {
            'equipo': _('Equipo'),
            'estado': _('Estado del Equipo'),
            'proveedor': _('Proveedor'),
            'tipo_entrada': _('Tipo de Entrada'),
            'cantidad': _('Cantidad ingresado'),
            'fecha': _('Fecha de entrada'),
            'precio': _('Precio del equipo'),
            'factura': _('Factura de la compra'),
            'observacion': _('Observación de la entrada'),

        }
		widgets= {
		'equipo':forms.Select(attrs={'class':' form-control select2'}),
		'proveedor':forms.Select(attrs={'class':' form-control select2'}),
		'fecha':forms.TextInput(attrs={'class':'datepicker form-control', 'placeholder': 'Fecha'}),
		'cantidad':forms.NumberInput(attrs={'class':' form-control','placeholder': 'Cantidad'}),
		'precio': forms.NumberInput(attrs={'class':' form-control', 'placeholder' : 'Precio'}),
		'factura': forms.NumberInput(attrs={'class':' form-control', 'placeholder' : 'Factura'}),
		}
	def clean_fecha(self):
		fecha = self.cleaned_data.get('fecha')
		if fecha > date.today():
			raise forms.ValidationError("Este campo tiene que ser menor o igual a la fecha actual (" + str(date.today()) + ")")
		return fecha
		
	def clean_cantidad(self):
		cantidad = self.cleaned_data.get('cantidad')
		if cantidad <= 0:
			raise forms.ValidationError("Este campo debe ser mayor a 0")
		return cantidad	

	def clean_precio(self):
		precio = self.cleaned_data.get('precio')
		tipo = self.cleaned_data.get('tipo_entrada')
		if precio is not None and precio <= 0:
			raise forms.ValidationError("Este campo debe ser mayor a 0")
		if tipo == "Compra" and precio <=0 :
			raise forms.ValidationError("Este campo es requerido ")

		return precio

class FormularioSalidaInforme(forms.ModelForm):
	class Meta:
		model = Salida
		fields = ['tecnico']
		labels = {'tecnico': _('Técnico')}
		widgets= {
			'tecnico':forms.Select(attrs={'class':'select2 form-control'}),
			}
	


class FormularioSalida(forms.ModelForm):
	class Meta:
		model = Salida
		fields = '__all__'
		widgets= {
		'equipo':forms.Select(attrs={'class':'form-control select2'}),
		'fecha':forms.TextInput(attrs={'class':'datepicker form-control', 'placeholder': 'Fecha'}),
		'cantidad':forms.NumberInput(attrs={'class':' form-control','placeholder': 'Cantidad'}),
		'no_entrada': forms.Select(attrs={'class':' form-control select2'}),
		}
		labels = {
            'equipo': _('Equipo'),
            'estado': _('Estado del Equipo'),
            'tecnico': _('Técnico'),
            'tipo_salida': _('Tipo de Salida'),
            'cantidad': _('Cantidad egresado'),
            'fecha': _('Fecha de salida'),
            'observacion': _('Observación de la salida'),
        }
	def clean_fecha(self):
		fecha = self.cleaned_data.get('fecha')
		if fecha > date.today():
			raise forms.ValidationError("Este campo debe ser menor o igual a la fecha actual (" + str(date.today()) + ")")
		return fecha

	

	

class FormularioProveedor(forms.ModelForm):
	class Meta:
		model = Proveedor
		fields = '__all__'


SalidaEquipoFormSet = inlineformset_factory(Salida, SalidaEquipo, fields='__all__',extra=1, can_delete=True)
