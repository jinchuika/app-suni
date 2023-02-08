from django import forms
from datetime import date
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from apps.inventario import models as inv_m
from apps.crm import models as crm_m
from apps.kardex import models as kax_m

class EntradaForm(forms.ModelForm):
    """Formulario para la :`class`:`EntradaCreateView` que es la encargada de crear los datos
    de entrada.
    """
    fecha = forms.DateField(
        initial=date.today(),
        widget=forms.TextInput({'class': 'form-control datepicker', 'tabindex': '2'}))

    class Meta:
        model = inv_m.Entrada
        fields = '__all__'
        exclude = ['en_creacion', 'creada_por', 'recibida_por', 'fecha_cierre']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'proveedor': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '3'}),
            'factura': forms.NumberInput({'class': 'form-control', 'tabindex': '4'}),
            'observaciones': forms.Textarea({'class': 'form-control', 'tabindex': '5'}),
        }

    def clean(self):
        cleaned_data = super(EntradaForm, self).clean()

        id_tipo = cleaned_data.get('tipo')
        factura = cleaned_data.get('factura')

        tipo_entrada = inv_m.EntradaTipo.objects.get(nombre=str(id_tipo))
        if tipo_entrada.contable:
            if factura <= 0:
                self.add_error(None, ValidationError('NO. FACTURA DEBE SER MAYOR A 0.'))

        return cleaned_data


class EntradaUpdateForm(forms.ModelForm):
    """Formulario para la :`class`:`EntradaUpdateView` que es la encargada de actualizar los datos
    de entrada.
    """
    class Meta:
        model = inv_m.Entrada
        fields = '__all__'
        exclude = ['factura', 'fecha_cierre']
        labels = {
                'en_creacion': _('En Desarrollo'),
        }
        widgets = {
                'recibida_por': forms.HiddenInput(),
                'fecha': forms.HiddenInput(),
                'tipo': forms.HiddenInput(),
                'creada_por': forms.HiddenInput(),
                'proveedor': forms.HiddenInput(),
                'observaciones': forms.Textarea({'class': 'form-control', 'tabindex': '1'}),
                'en_creacion': forms.CheckboxInput({'class': 'icheckbox_flat-green', 'tabindex': '2'}),
        }

    def __init__(self, *args, **kwargs):
        super(EntradaUpdateForm, self).__init__(*args, **kwargs)
        self.fields['recibida_por'].label_from_instance = lambda obj: "%s" % obj.get_full_name()


class EntradaDetalleForm(forms.ModelForm):
    """ Formulario para la :`class`:`EntradaDetalleView` que es la encargada de crear  los datos
    de los detalles de entrada
    """
    class Meta:
        model = inv_m.EntradaDetalle
        fields = '__all__'
        exclude = [
            'precio_unitario',
            'precio_total',
            'precio_descontado',
            'creado_por',
            'dispositivos_creados',
            'repuestos_creados',
            'qr_repuestos',
            'qr_dispositivo',
            'impreso',
            'util',
            'repuesto',
            'desecho',
            'fecha_dispositivo',
            'fecha_repuesto',
            'enviar_kardex',
            'ingresado_kardex', 
            'pendiente_autorizar',
            'autorizado'           
            ]
        widgets = {
            'entrada': forms.HiddenInput(),
            'tipo_dispositivo': forms.Select(attrs={'class': 'form-control select2'}),
            'total': forms.TextInput({'class': 'form-control', 'min': 1, 'type': 'number'}),
            'precio_subtotal': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput({'class': 'form-control'}),
            'proveedor_kardex': forms.Select(attrs={'class': 'form-control select2'}),
            'estado_kardex': forms.Select(attrs={'class': 'form-control select2'}),
            'tipo_entrada_kardex': forms.Select(attrs={'class': 'form-control select2'})
        }

    def __init__(self, *args, **kwargs):
        entrada = kwargs.pop('initial', None)['entrada']
        super(EntradaDetalleForm, self).__init__(*args, **kwargs)
        self.fields['entrada'].initial = entrada

        if entrada.tipo.contenedor:
            self.fields['total'].widget = forms.NumberInput(
                attrs={'class': 'form-control', 'min': "0"})

        if not entrada.tipo.contable:            
            self.fields['precio_subtotal'].empty_label = None
            self.fields['precio_subtotal'].label = ''
            self.fields['precio_subtotal'].widget = forms.NumberInput(
                attrs={'class': 'form-control', 'style': "visibility:hidden"})
            self.fields['precio_subtotal'].initial = ""
        else:            
            self.fields['precio_subtotal'].widget = forms.NumberInput(
                attrs={'class': 'form-control','step':".01"})

class EntradaDetalleUpdateForm(forms.ModelForm):
    """ Formulario para la :`class`:`EntradaDetalleView` que es la encargada de actualizar  los datos
    de los detalles de entrada
    """
    class Meta:
        model = inv_m.EntradaDetalle
        fields = '__all__'
        exclude = [
                    'tipo_dispositivo',
                    'precio_unitario',
                    'precio_total',
                    'precio_descontado',
                    'precio_subtotal',
                    'dispositivos_creados',
                    'repuestos_creados',
                    'qr_repuestos',
                    'qr_dispositivo',
                    'impreso',
                    'fecha_dispositivo',
                    'fecha_repuesto',
                    'enviar_kardex',
                    'ingresado_kardex',
                    'proveedor_kardex',
                    'tipo_entrada_kardex',
                    'estado_kardex',
                    'pendiente_autorizar',
                    'autorizado' 
                    ]
        widgets = {
            'util': forms.NumberInput({'class': 'form-control'}),
            'repuesto': forms.NumberInput({'class': 'form-control'}),
            'desecho': forms.NumberInput({'class': 'form-control '}),
            'total': forms.NumberInput({'class': 'form-control '}),
            'descripcion': forms.TextInput({'class': 'form-control'}),
            'dispositivos_creados': forms.HiddenInput(),
            'repuestos_creados': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'entrada': forms.HiddenInput(),

        }

    def __init__(self, *args, **kwargs):
        super(EntradaDetalleUpdateForm, self).__init__(*args, **kwargs)
        self.fields['creado_por'].label_from_instance = lambda obj: "%s" % obj.get_full_name()
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['total'].widget.attrs['readonly'] = True
            self.fields['descripcion'].widget.attrs['readonly'] = True

    def clean(self):
        total = self.cleaned_data['total']
        util = self.cleaned_data['util']
        repuesto = self.cleaned_data['repuesto']
        desecho = self.cleaned_data['desecho']
        id_entrada = self.cleaned_data['entrada']
        entrada = inv_m.Entrada.objects.get(pk=str(id_entrada))

        if not entrada.tipo.contenedor or (entrada.tipo.contenedor and total > 0):
            suma = util + repuesto + desecho
            if total < suma:
                raise forms.ValidationError(
                    _('Los valores de depuración superan el total de dispositivos.')
                )

    def as_table(self):
        "Returns this form rendered as HTML <tr>s -- excluding the <table></table>."
        return self._html_output(
            normal_row=u'<tr%(html_class_attr)s><th>%(label)s</th><td>%(errors)s%(field)s%(help_text)s</td></tr>',
            error_row=u'<tr style="display:none"><td colspan="2">%s</td></tr>',
            row_ender=u'</td></tr>',
            help_text_html=u'<br /><span class="helptext">%s</span>',
            errors_on_separate_row=False)


class EntradaInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Entradas
    """

    id = forms.IntegerField(
        label='No. Entrada',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    proveedor = forms.ModelChoiceField(
        queryset=crm_m.Donante.objects.all(),
        label='Proveedor',
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False)
    tipo = forms.ModelMultipleChoiceField(
        queryset=inv_m.EntradaTipo.objects.all(),
        label='Tipo',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))

    recibida_por = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name="inventario"),
        label='Persona Que Recibe',
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

    def __init__(self, *args, **kwargs):
        super(EntradaInformeForm, self).__init__(*args, **kwargs)
        self.fields['recibida_por'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())
