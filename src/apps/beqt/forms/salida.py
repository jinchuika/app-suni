#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import forms
from apps.inventario import models as inv_m
from apps.beqt import models as beqt_m
from apps.crm import models as crm_m
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class SalidaInventarioForm(forms.ModelForm):
    """ Formulario para el control de las Salidas de Inventario
    """
    udi = forms.CharField(
        label='UDI',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = beqt_m.SalidaInventario
        fields = '__all__'
        exclude = ('creada_por', 'escuela', 'necesita_revision', 'entrada','entrega','url','capacitada','meses_garantia')
        widgets = {
            'en_creacion': forms.HiddenInput(),
            'estado': forms.HiddenInput(),
            'tipo_salida': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'fecha': forms.TextInput({'class': 'form-control datepicker', 'tabindex': '2'}),
            'escuela': forms.TextInput({'class': 'form-control', 'tabindex': '7'}),
            'observaciones': forms.Textarea({'class': 'form-control', 'tabindex': '5'}),
            'reasignado_por': forms.HiddenInput(),
            'garantia': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '4'}),
            'cooperante': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '8'}),
        }

    def __init__(self, *args, **kwargs):
        super(SalidaInventarioForm, self).__init__(*args, **kwargs)
        self.fields['garantia'].label="Ticket"
        if self.instance.en_creacion:
            self.fields['beneficiario'].widget = forms.Select(
                attrs={'style': "visibility:hidden", 'class': 'form-control select2', 'tabindex': '6'})
            self.fields['beneficiario'].queryset = crm_m.Donante.objects.all()
        else:
            self.fields['udi'].widget = forms.HiddenInput()


class SalidaInventarioUpdateForm(forms.ModelForm):
    """ Formulario para  la actualizacion de las salidas de inventario.
    """
    class Meta:
        model = beqt_m.SalidaInventario
        fields = ('cooperante', 'fecha', 'en_creacion', 'observaciones','url','capacitada','meses_garantia')
        labels = {
                'en_creacion': _('En Desarrollo'),
        }
        widgets = {
            'id': forms.HiddenInput(),
            'cooperante': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'fecha': forms.TextInput({'class': 'form-control datepicker', 'tabindex': '2'}),
            'observaciones': forms.Textarea({'class': 'form-control', 'tabindex': '4'}),
            'en_creacion': forms.CheckboxInput(attrs={'class': 'icheckbox_flat-green', 'tabindex': '3'}),
            'url': forms.TextInput({'class': 'form-control', 'tabindex': '4'}),
        }


class PaqueteCantidadForm(forms.ModelForm):
    """ Formulario para  la creacion de la cantidad de paquetes.
        """
    tipo_paquete = forms.ModelChoiceField(
        queryset=beqt_m.PaqueteTipoBeqt.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    cantidad = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    entrada = forms.ModelMultipleChoiceField(
        required=False,
        queryset=beqt_m.Entrada.objects.filter(tipo=5),
        widget=forms.SelectMultiple(attrs={
            'data-api-url': reverse_lazy('beqt_api:api_entrada_beqt-list')
        })
    )

    class Meta:
        model = beqt_m.PaqueteBeqt
        fields = ('tipo_paquete', 'cantidad', 'entrada',)


class RevisionSalidaCreateForm(forms.ModelForm):
    """Formulario para creación de :class:`RevisionSalida`.
    El campo `salida` usa un queryset que filtra únicamente a las salidas en creación que necesitan revisión.
    """

    salida = forms.ModelChoiceField(
        queryset=beqt_m.SalidaInventario.objects.filter(en_creacion=True, necesita_revision=True),
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )

    class Meta:
        model = beqt_m.RevisionSalidaBeqt
        fields = ('salida', 'tecnico')
        widgets = {
            'tecnico': forms.Select(attrs={'class': 'form-control select2'})
        }

    def __init__(self, *args, **kwargs):
        super(RevisionSalidaCreateForm, self).__init__(*args, **kwargs)
        self.fields['tecnico'].label_from_instance = lambda obj: "%s" % obj.get_full_name()


class RevisionSalidaUpdateForm(forms.ModelForm):
    """Formulario para edición de :class:`RevisionSalida`.
    """

    class Meta:
        model = beqt_m.RevisionSalidaBeqt
        fields = ('anotaciones', )
        widgets = {
            'anotaciones': forms.Textarea(attrs={'class': 'form-control'})
        }


class DispositivoPaqueteCreateForm(forms.ModelForm):
    """ Formulario para la asignacion de dispositivos a  paquetes
    """
    tipo = forms.ModelChoiceField(
        queryset=beqt_m.DispositivoTipoBeqt.objects.filter(usa_triage=True),
        label='Tipo de dispositivo',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    paquete = forms.ModelChoiceField(
        queryset=beqt_m.PaqueteBeqt.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    dispositivo = forms.ModelMultipleChoiceField(
        queryset=beqt_m.DispositivoBeqt.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    """dispositivo = forms.ModelChoiceField(
        queryset=inv_m.Dispositivo.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )"""

    class Meta:
        model = beqt_m.DispositivoPaquete
        fields = ('tipo', 'paquete', 'dispositivo')


class PaqueteUpdateForm(forms.ModelForm):
    """Formulario para actualizar una `SolicitudMovimiento`, usado principalmente para autorizar movimientos.
    El campo `dispositivos` sirve para crear un listado de dispositivos que serán cambiados.
    Los datos agregados al widget son para hacer filtros sobre el tipo de dispositivo y la etapa donde se encuentran,
    serán modificados en la vista para adaptarse a la solicitud de movimiento.
    """
    dispositivos = forms.ModelMultipleChoiceField(
        queryset=beqt_m.DispositivoBeqt.objects.none(),
        widget=forms.SelectMultiple(attrs={
            'data-api-url': reverse_lazy('beqt_api:api_dispositivo-list'),
            'data-etapa-inicial': '',
            'data-tipo-dispositivo': '',
        })
    )

    class Meta:
        model = beqt_m.PaqueteBeqt
        fields = ('dispositivos', )


class SalidaInventarioListForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Entradas
    """

    id = forms.IntegerField(
        label='No. Salida',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    tipo_salida = forms.ModelChoiceField(
        queryset=beqt_m.SalidaTipoBeqt.objects.all(),
        label='Tipo',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'}))

    estado = forms.ModelChoiceField(
        queryset=inv_m.SalidaEstado.objects.all(),
        label='Estado',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'}))

    fecha_min = forms.CharField(
        label='Fecha (min)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max = forms.CharField(
        label='Fecha (max)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
