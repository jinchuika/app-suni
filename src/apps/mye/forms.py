from django import forms
from django.forms import ModelForm
from django.utils import timezone
from .models import Cooperante, EscuelaCooperante, Proyecto, EscuelaProyecto, SolicitudVersion
from apps.escuela.models import Escuela

class CooperanteForm(ModelForm):
	class Meta:
		model = Cooperante
		fields = '__all__'
		widgets = { 'nombre': forms.TextInput(attrs={'class': 'form-control'})}

class EscuelaCooperanteForm(ModelForm):
	eliminar = False
	class Meta:
		model = Escuela
		fields = ['id', 'cooperante_asignado']
		widgets = {
			'id': forms.HiddenInput(),
			'cooperante_asignado': forms.SelectMultiple(attrs={'class': 'select2'})
		}

	def __init__(self, eliminar, *args, **kwargs):
		super(EscuelaCooperanteForm, self).__init__(*args, **kwargs)
		self.eliminar = eliminar

	def save(self, commit=True):
		instance = super(EscuelaCooperanteForm, self).save(commit=False)
		instance.asignacion_cooperante = instance.asignacion_cooperante.filter(activa=True)
		# Revisa que el usuario tenga permiso para eliminar
		if self.eliminar:
			# Revisa si un cooperante fue eliminado
			for asignacion in instance.asignacion_cooperante.all():
				if asignacion.cooperante not in self.cleaned_data['cooperante_asignado']:
					asignacion.activa = False
					asignacion.fecha_anulacion = timezone.now()
					asignacion.save()
		for cooperante in self.cleaned_data['cooperante_asignado']:
			if EscuelaCooperante.objects.filter(escuela=instance, cooperante=cooperante, activa=True).count() == 0:
				esc_coo = EscuelaCooperante(escuela=instance, cooperante=cooperante)
				esc_coo.save()

class ProyectoForm(ModelForm):
	class Meta:
		model = Proyecto
		fields = '__all__'
		widgets = { 'nombre': forms.TextInput(attrs={'class': 'form-control'})}

class EscuelaProyectoForm(ModelForm):
	eliminar = False
	class Meta:
		model = Escuela
		fields = ['id', 'proyecto_asignado']
		widgets = {
			'id': forms.HiddenInput(),
			'proyecto_asignado': forms.SelectMultiple(attrs={'class': 'select2'})
		}

	def __init__(self, eliminar, *args, **kwargs):
		super(EscuelaProyectoForm, self).__init__(*args, **kwargs)
		self.eliminar = eliminar

	def save(self, commit=True):
		instance = super(EscuelaProyectoForm, self).save(commit=False)
		instance.asignacion_proyecto = instance.asignacion_proyecto.filter(activa=True)
		# Revisa que el usuario tenga permiso para eliminar
		if self.eliminar:
			# Revisa si un proyecto fue eliminado
			for asignacion in instance.asignacion_proyecto.all():
				if asignacion.proyecto not in self.cleaned_data['proyecto_asignado']:
					asignacion.activa = False
					asignacion.fecha_anulacion = timezone.now()
					asignacion.save()
		for proyecto in self.cleaned_data['proyecto_asignado']:
			if EscuelaProyecto.objects.filter(escuela=instance, proyecto=proyecto, activa=True).count() == 0:
				esc_pro = EscuelaProyecto(escuela=instance, proyecto=proyecto)
				esc_pro.save()

class SolicitudVersionForm(ModelForm):
	class Meta:
		model = SolicitudVersion
		fields = '__all__'
		widgets = {
		'requisito': forms.CheckboxSelectMultiple()
		}