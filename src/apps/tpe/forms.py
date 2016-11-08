from django import forms
from django.forms import ModelForm
from apps.tpe.models import Equipamiento


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
