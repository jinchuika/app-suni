from django import forms
from django.urls import reverse_lazy
from django.forms import ModelForm
from django.contrib.auth.models import User

from apps.conta import models as conta_m
from apps.inventario import models as inv_m
from apps.crm import models as crm_m
from apps.inventario import models as inventario_m
from apps.escuela import models as escuela_m


class PeriodoFiscalForm(forms.ModelForm):
    """ Formulario para el control de los periodos fiscales
    """
    class Meta:
        model = conta_m.PeriodoFiscal
        fields = '__all__'
        widgets = {
            'fecha_inicio': forms.TextInput({'class': 'form-control datepicker'}),
            'fecha_fin': forms.TextInput({'class': 'form-control datepicker'})
        }


class PeriodoFiscalUpdateForm(forms.ModelForm):
    """ Formulario para la actualizacion de los periodos fiscales
    """
    class Meta:
        model = conta_m.PeriodoFiscal
        fields = '__all__'
        exclude = ['fecha_fin', 'fecha_inicio']


class PrecioEstandarForm(forms.ModelForm):
    """ Formulario para la crecion de :class:`PrecioEstandar`
    """
    class Meta:
        model = conta_m.PrecioEstandar
        fields = '__all__'
        exclude = ['periodo', 'creado_por','revaluar']
        widgets = {
            'tipo_dispositivo': forms.Select(attrs={'class': 'form-control select2'}),
            'activo': forms.HiddenInput(),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'inventario': forms.Select(attrs={'class': 'form-control select2'})
        }


class PrecioEstandarInformeForm(forms.Form):
    """ Formulario para la aplicacion de filtros de busqueda de precio estandar
    """
    periodo = forms.ModelChoiceField(
        queryset=conta_m.PeriodoFiscal.objects.all(),
        label="Periodo Fiscal",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    tipo_dispositivo = forms.ModelChoiceField(
        queryset=inventario_m.DispositivoTipo.objects.all().exclude(usa_triage=False),
        label="Tipo de Dispositivo",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )


class CantidadInformeForm(forms.Form):
    """ Formulario para la aplicacion de filtros de busqueda de precio estandar
    """
    inventario = (('', '----------'), ('1', 'Dispositivos'), ('2', 'Repuestos'))
    periodo = forms.ModelChoiceField(
        queryset=conta_m.PeriodoFiscal.objects.all(),
        label="Periodo Fiscal",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    dispositivo = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=inventario,
        label="Tipo")


class EntradaInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Ofertas
    """
    donante = forms.ModelChoiceField(
        queryset=crm_m.Donante.objects.all(),
        label='Proveedor / Donante',
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False)
    tipo_entrada = forms.ModelMultipleChoiceField(
        queryset=inv_m.EntradaTipo.objects.all().exclude(nombre='Especial'),
        label='Tipo de Entrada',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple'}))

    tipo_dispositivo = forms.ModelChoiceField(
        queryset=inv_m.DispositivoTipo.objects.filter(usa_triage=True),
        label='Tipo de Dispositivo',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control select2'}))

    fecha_min = forms.CharField(
        label='Fecha (min)',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max = forms.CharField(
        label='Fecha (max)',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))

class EntradaDispositivoInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Dispositivos por Entrada
    """
    no_entrada = forms.IntegerField(
        label='No. Entrada',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    tipo_dispositivo = forms.ModelChoiceField(
        queryset=inv_m.DispositivoTipo.objects.filter(usa_triage=True),
        label='Tipo de Dispositivo',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control select2'}))

    fecha_min = forms.CharField(
        label='Fecha (min)',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max = forms.CharField(
        label='Fecha (max)',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))

class SalidasInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Salidas
    """
    udi = forms.CharField(
        label='UDI',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    beneficiado = forms.ModelChoiceField(
        queryset=crm_m.Donante.objects.all(),
        label='Beneficiado',
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False)
    tipo_salida = forms.ModelMultipleChoiceField(
        queryset=inv_m.SalidaTipo.objects.all().exclude(especial=True),
        label='Tipo de Entrada',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple'}))

    compras = forms.BooleanField(
        label="Compras",
        required=False,
        widget=forms.CheckboxInput({'class': 'flat-red'}))

    tipo_dispositivo = forms.ModelChoiceField(
        queryset=inv_m.DispositivoTipo.objects.filter(usa_triage=True),
        label='Tipo de Dispositivo',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control select2'}))

    fecha_min = forms.CharField(
        label='Fecha (min)',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max = forms.CharField(
        label='Fecha (max)',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))


class DesechoInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Salidas por desecho
    """
    empresa = forms.ModelChoiceField(
        queryset=inv_m.DesechoEmpresa.objects.all(),
        label='Recolectora',
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False)

    tipo_dispositivo = forms.ModelChoiceField(
        queryset=inv_m.DispositivoTipo.objects.filter(usa_triage=True),
        label='Tipo de Dispositivo',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control select2'}))

    fecha_min = forms.CharField(
        label='Fecha (min)',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max = forms.CharField(
        label='Fecha (max)',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))

class ResumenInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Resumen
    """
    fecha_min = forms.CharField(
        label='Fecha (min)',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max = forms.CharField(
        label='Fecha (max)',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))

    tipo_dispositivo = forms.ModelMultipleChoiceField(
        queryset=inv_m.DispositivoTipo.objects.filter(usa_triage=True),
        label='Dispositivo',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))