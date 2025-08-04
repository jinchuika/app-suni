from django import forms
from django.urls import reverse_lazy
from django.forms import ModelForm
from django.contrib.auth.models import User

from apps.conta import models as conta_m
from apps.inventario import models as inv_m
from apps.crm import models as crm_m
from apps.inventario import models as inventario_m
from apps.escuela import models as escuela_m
from apps.beqt import models as beqt_m


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
        exclude = ['creado_por']

class PeriodoFiscalUpdateForm(forms.ModelForm):
    """ Formulario para la actualizacion de los periodos fiscales
    """
    class Meta:
        model = conta_m.PeriodoFiscal
        fields = '__all__'
        exclude = ['fecha_fin', 'fecha_inicio','creado_por']


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
        exclude = ['creado_por']

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
        label='Tipo de Salida',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple'}))

    donaciones = forms.BooleanField(
        label="Donaciones",
        required=False,
        widget=forms.CheckboxInput({'class': 'flat-red'}))

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
    
class ExistenciaDispositivosInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Resumen
    """
    fecha_min = forms.CharField(
        label='Fecha (min)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max = forms.CharField(
        label='Fecha (max)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    
    tipo_dispositivo = forms.ModelMultipleChoiceField(
        queryset=inv_m.DispositivoTipo.objects.filter(usa_triage=True),
        label='Dispositivo',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))

    """tipo_dispositivo = forms.ModelChoiceField(
        queryset=inv_m.DispositivoTipo.objects.filter(usa_triage=True),
        label='Dispositivo',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'}))"""
    
class RastreoDesechoInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Resumen
    """
    entrada = forms.ModelMultipleChoiceField(
        queryset=inv_m.DesechoSalida.objects.all(),
        label='No. Desecho',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))
    entrada_inventario = forms.ModelMultipleChoiceField(
        queryset=inv_m.Entrada.objects.all(),
        label='No. Entrada Inventario',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))

    tipo_entrada = forms.ModelMultipleChoiceField(
        queryset=inv_m.EntradaTipo.objects.all().exclude(id=5),
        label='Tipo Entrada',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))
    
    tipo_dispositivo = forms.ModelMultipleChoiceField(
        queryset=inv_m.DispositivoTipo.objects.all(),
        label='Dispositivo',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))
    
    fecha_min = forms.CharField(
        label='Fecha Desecho (min)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max = forms.CharField(
        label='Fecha Desecho (max)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_min_entrada = forms.CharField(
        label='Fecha Entrada Inventario (min)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max_entrada = forms.CharField(
        label='Fecha Entrada Inventario (max)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    
class RastreoRepuestoInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Resumen
    """
    repuesto = forms.ModelMultipleChoiceField(
        queryset=inv_m.Repuesto.objects.all(),
        label='Triage Repuesto',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))
    estado_repuesto = forms.ModelMultipleChoiceField(
        queryset=inv_m.RepuestoEstado.objects.all(),
        label='Estado',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))
    entrada_inventario = forms.ModelMultipleChoiceField(
        queryset=inv_m.Entrada.objects.all(),
        label='No. Entrada Inventario',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))

    tipo_entrada = forms.ModelMultipleChoiceField(
        queryset=inv_m.EntradaTipo.objects.all().exclude(id=5),
        label='Tipo Entrada',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))
    
    tipo_dispositivo = forms.ModelMultipleChoiceField(
        queryset=inv_m.DispositivoTipo.objects.all(),
        label='Dispositivo',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))
    
    fecha_min = forms.CharField(
        label='Fecha  (min)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max = forms.CharField(
        label='Fecha  (max)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
   
    


##Formularios de BEQT
class EntradaDispositivoBeqtInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Dispositivos por Entrada
    """
    no_entrada = forms.IntegerField(
        label='No. Entrada',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    tipo_dispositivo = forms.ModelChoiceField(
        queryset=beqt_m.DispositivoTipoBeqt.objects.filter(usa_triage=True),
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
    

class SalidasBeqtInformeForm(forms.Form):
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
        queryset=inv_m.SalidaTipo.objects.filter(id=1),
        label='Tipo de Salida',
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
    


class ResumenInformeBeqtForm(forms.Form):
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
        queryset=beqt_m.DispositivoTipoBeqt.objects.filter(usa_triage=True),
        label='Dispositivo',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))
    

    
class PlanillaForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  de selección de planilla
    """
    pagos=[('1','Quincena'),('2','Fin de mes'),('3','Bono 14'),('4','Aguinaldo')]
    tipo_de_planilla = forms.ChoiceField(widget=forms.RadioSelect, choices=pagos)
    agrupacion=[('1','Individual'),('2','Listado')]
    disposicion_planilla = forms.ChoiceField(widget=forms.RadioSelect, choices=agrupacion)
    enviar_correo = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'icheckbox_flat-green'}),required=False)

class RastreoDispositivoInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Dispositivos por Entrada
    """

    triage = forms.CharField(
        label='Triage',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    no_entrada = forms.IntegerField(
        label='No. Entrada',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    tipo_dispositivo = forms.ModelChoiceField(
        queryset=inv_m.DispositivoTipo.objects.filter(usa_triage=True),
        label='Tipo de Dispositivo',
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
                                                                        
