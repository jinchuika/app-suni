from django import forms 
from django.forms import ModelForm, ModelChoiceField, formset_factory, modelformset_factory, widgets
from .models import *


#class EquipoForm(forms.Form):
#	equipo = forms.CharField(max_length=100)

class FormularioEquipo(ModelForm):
	class Meta:
		model = Equipo
		fields = ['nombre_equipo']


class FormularioEntrada(forms.ModelForm):	
	class Meta:
		model = Entrada
		fields = '__all__'
		widgets= {
		'equipo':forms.Select(attrs={'class':' form-control select2'}),
		'fecha':forms.TextInput(attrs={'class':'datepicker form-control', 'placeholder': 'Fecha'}),
		'cantidad':forms.NumberInput(attrs={'class':' form-control','placeholder': 'Cantidad'}),
		'precio': forms.NumberInput(attrs={'class':' form-control', 'placeholder' : 'Precio'}),
		'factura': forms.NumberInput(attrs={'class':' form-control', 'placeholder' : 'Factura'}),
			

		}

	def clean_cantidad(self):
		cantidad = self.cleaned_data.get('cantidad')
		if cantidad <= 0:
			raise forms.ValidationError("Este campo tiene que ser mayor a 0")
		return cantidad	

	def clean_precio(self):
		precio = self.cleaned_data.get('precio')
		if precio is not None and precio <= 0:
			raise forms.ValidationError("Este campo tiene que ser mayor a 0")
		tipo= self.cleaned_data.get('tipo_entrada')
		if tipo == "Compra" and precio <=0 :
			raise forms.ValidationError("Este campo es requerido ")

		return precio
	


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

	def clean_cantidad(self):
		cantidad = self.cleaned_data.get('cantidad')
		if cantidad <= 0:
			raise forms.ValidationError("Este campo tiene que ser mayor a 0")

		existente = self.cleaned_data.get('equipo').existencia
		if cantidad > existente:
			raise forms.ValidationError("El campo tiene que ser menor o igual a la existente (" + str(existente) + ")" )	
		return cantidad	

	

class FormularioProveedor(forms.ModelForm):
	class Meta:
		model = Proveedor
		fields = '__all__'
