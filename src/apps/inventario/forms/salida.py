#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import forms
from apps.inventario import models as inv_m
from apps.crm import models as crm_m
from django.urls import reverse_lazy


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
        exclude = ('creada_por', 'escuela', 'necesita_revision', 'entrada')
        widgets = {
            'en_creacion': forms.HiddenInput(),
            'estado': forms.HiddenInput(),
            'tipo_salida': forms.Select(attrs={'class': 'form-control select2'}),
            'fecha': forms.TextInput({'class': 'form-control datepicker'}),
            'escuela': forms.TextInput({'class': 'form-control'}),
            'observaciones': forms.Textarea({'class': 'form-control'}),
            'reasignado_por': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(SalidaInventarioForm, self).__init__(*args, **kwargs)
        if self.instance.en_creacion:
            self.fields['beneficiario'].empty_label = None
            self.fields['beneficiario'].label = ' '
            self.fields['beneficiario'].widget = forms.Select(
                attrs={'class': 'form-control', 'style': "visibility:hidden"})
            self.fields['beneficiario'].initial = "-----------"
            self.fields['beneficiario'].queryset = crm_m.Donante.objects.all()
        else:
            self.fields['udi'].widget = forms.HiddenInput()


class SalidaInventarioUpdateForm(forms.ModelForm):
    """ Formulario para  la actualizacion de las salidas de inventario.
    """
    class Meta:
        model = inv_m.SalidaInventario
        fields = ('fecha', 'en_creacion')
        widgets = {
            'fecha': forms.TextInput({'class': 'form-control datepicker'}),

        }


class PaqueteCantidadForm(forms.ModelForm):
    """ Formulario para  la creacion de la cantidad de paquetes.
        """
    cantidad = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    tipo_paquete = forms.ModelChoiceField(
        queryset=inv_m.PaqueteTipo.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    entrada = forms.ModelMultipleChoiceField(
        required=False,
        queryset=inv_m.Entrada.objects.none(),
        widget=forms.SelectMultiple(attrs={
            'data-api-url': reverse_lazy('inventario_api:api_entrada-list')
        })
    )

    class Meta:
        model = inv_m.Paquete
        fields = ('cantidad', 'tipo_paquete', 'entrada',)


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
        fields = ('salida', 'tecnico')
        widgets = {            
            'tecnico': forms.Select(attrs={'class': 'form-control select2'})
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


class DispositivoPaqueteCreateForm(forms.ModelForm):
    """ Formulario para la asignacion de dispositivos a  paquetes
    """
    tipo = forms.ModelChoiceField(
        queryset=inv_m.DispositivoTipo.objects.filter(usa_triage=True),
        label='Tipo de dispositivo',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    paquete = forms.ModelChoiceField(
        queryset=inv_m.Paquete.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    dispositivo = forms.ModelMultipleChoiceField(
        queryset=inv_m.Dispositivo.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    """dispositivo = forms.ModelChoiceField(
        queryset=inv_m.Dispositivo.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )"""

    class Meta:
        model = inv_m.DispositivoPaquete
        fields = ('tipo', 'paquete', 'dispositivo')


class PaqueteUpdateForm(forms.ModelForm):
    """Formulario para actualizar una `SolicitudMovimiento`, usado principalmente para autorizar movimientos.
    El campo `dispositivos` sirve para crear un listado de dispositivos que serán cambiados.
    Los datos agregados al widget son para hacer filtros sobre el tipo de dispositivo y la etapa donde se encuentran,
    serán modificados en la vista para adaptarse a la solicitud de movimiento.
    """
    dispositivos = forms.ModelMultipleChoiceField(
        queryset=inv_m.Dispositivo.objects.none(),
        widget=forms.SelectMultiple(attrs={
            'data-api-url': reverse_lazy('inventario_api:api_dispositivo-list'),
            'data-etapa-inicial': '',
            'data-tipo-dispositivo': '',
        })
    )

    class Meta:
        model = inv_m.Paquete
        fields = ('dispositivos', )
