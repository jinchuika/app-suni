from django import forms
from django.forms import ModelForm
from django.db.models import Count
from django.core.urlresolvers import reverse_lazy

from apps.tpe.models import Equipamiento, Garantia, TicketSoporte, TicketRegistro
from apps.escuela.forms import BuscarEscuelaForm


class EquipamientoNuevoForm(forms.ModelForm):
    class Meta:
        model = Equipamiento
        fields = ('id', 'escuela')
        labels = {
            'id': 'Número de entrega'}
        widgets = {
            'id': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
            'escuela': forms.HiddenInput()}


class EquipamientoForm(ModelForm):
    class Meta:
        model = Equipamiento
        fields = '__all__'
        exclude = ('id',)
        widgets = {
            'escuela': forms.HiddenInput(),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.TextInput(attrs={'class': 'form-control datepicker'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control'}),
            'cooperante': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'proyecto': forms.SelectMultiple(attrs={'class': 'form-control select2'})}


class GarantiaForm(forms.ModelForm):
    class Meta:
        model = Garantia
        fields = '__all__'
        widgets = {
            'equipamiento': forms.Select(attrs={'class': 'select2'}),
            'fecha_vencimiento': forms.TextInput(attrs={'class': 'datepicker'})
        }

    def __init__(self, *args, **kwargs):
        super(GarantiaForm, self).__init__(*args, **kwargs)
        self.fields['equipamiento'].queryset = self.fields['equipamiento'].queryset.annotate(num_garantias=Count('garantias')).filter(num_garantias__lt=1)


class TicketSoporteForm(forms.ModelForm):
    class Meta:
        model = TicketSoporte
        fields = ('garantia', 'descripcion',)
        widgets = {
            'garantia': forms.HiddenInput(),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'})
        }


class TicketCierreForm(forms.ModelForm):
    class Meta:
        model = TicketSoporte
        fields = ('cerrado',)
        widgets = {
            'cerrado': forms.HiddenInput()
        }


class TicketRegistroForm(forms.ModelForm):
    class Meta:
        model = TicketRegistro
        fields = ('tipo', 'descripcion', 'costo_reparacion', 'costo_envio')
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'costo_reparacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'costo_envio': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class EquipamientoListForm(BuscarEscuelaForm):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'data-ajax--url': reverse_lazy('equipamiento_list_backend')}),
        required=False)
    fecha_min = forms.CharField(
        label='Fecha mínima',
        widget=forms.TextInput(attrs={'class': 'datepicker'}),
        required=False)
    fecha_max = forms.CharField(
        label='Fecha máxima',
        widget=forms.TextInput(attrs={'class': 'datepicker'}),
        required=False)

    def __init__(self, *args, **kwargs):
        super(EquipamientoListForm, self).__init__(*args, **kwargs)
        self.fields.pop('nombre')
        self.fields.pop('cooperante_mye')
        self.fields.pop('proyecto_mye')
        self.fields.pop('poblacion_min')
        self.fields.pop('poblacion_max')
        self.fields.pop('solicitud')
        self.fields.pop('solicitud_id')
        self.fields.pop('equipamiento')
