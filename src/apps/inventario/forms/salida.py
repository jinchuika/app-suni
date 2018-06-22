#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import forms
from apps.inventario import models as inv_m


class SalidaInventarioForm(forms.ModelForm):
    """ Formulario para el control de las Salidas de Inventario
    """
    udi = forms.CharField(
        label='UDI',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = inv_m.SalidaInventario
        fields = '__all__'
        exclude = ('creada_por', 'escuela')
        widgets = {
            'en_creacion': forms.HiddenInput(),
            'tipo_salida': forms.Select(attrs={'class': 'form-control select2'}),
            'fecha': forms.TextInput({'class': 'form-control datepicker'}),
            'escuela': forms.TextInput({'class': 'form-control'}),
            'observaciones': forms.Textarea({'class': 'form-control'}),
        }


class SalidaInventarioUpdateForm(forms.ModelForm):
    """ Formulario para  la actualizacion de las salidas de inventario.
    """
    class Meta:
        model = inv_m.SalidaInventario
        fields = ('fecha', 'observaciones')
        widgets = {
            'fecha': forms.TextInput({'class': 'form-control datepicker'}),
            'observaciones': forms.Textarea({'class': 'form-control'})
        }


class PaqueteCantidadForm(forms.ModelForm):
    """ Formulario para  la creacion de la cantidad de paquetes.
        """
    cantidad = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = inv_m.SalidaInventario
        fields = ('cantidad', )


class RevisionSalidaCreateForm(forms.ModelForm):
    """Formulario para creación de :class:`RevisionSalida`.
    El campo `salida` usa un queryset que filtra únicamente a las salidas en creación que necesitan revisión.
    """

    salida = forms.ModelChoiceField(
        queryset=inv_m.SalidaInventario.objects.filter(en_creacion=True, necesita_revision=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = inv_m.RevisionSalida
        fields = ('salida', 'fecha_revision')
        widgets = {
            'fecha_revision': forms.TextInput(attrs={'class': 'form-control datepicker'})
        }


class RevisionSalidaUpdateForm(forms.ModelForm):
    """Formulario para edición de :class:`RevisionSalida`.
    """

    class Meta:
        model = inv_m.RevisionSalida
        fields = ('anotaciones', )
        widgets = {
            'anotaciones': forms.Textarea(attrs={'class': 'form-control'})
        }