from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from apps.inventario import models as inv_m
from apps.crm import models as crm_m


class EntradaForm(forms.ModelForm):
    """Formulario para la :`class`:`EntradaCreateView` que es la encargada de crear los datos
    de entrada.
    """
    class Meta:
        model = inv_m.Entrada
        fields = '__all__'
        exclude = ['en_creacion', 'creada_por']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control select2'}),
            'fecha': forms.TextInput({'class': 'form-control datepicker'}),
            'recibida_por': forms.Select(attrs={'class': 'form-control select2'}),
            'proveedor': forms.Select(attrs={'class': 'form-control select2'})
        }

    def __init__(self, *args, **kwargs):
        super(EntradaForm, self).__init__(*args, **kwargs)
        self.fields['recibida_por'].label_from_instance = lambda obj: "%s" % obj.get_full_name()


class EntradaUpdateForm(forms.ModelForm):
    """Formulario para la :`class`:`EntradaUpdateView` que es la encargada de actualizar los datos
    de entrada.
    """
    class Meta:
        model = inv_m.Entrada
        fields = '__all__'
        widgets = {
                'recibida_por': forms.Select(attrs={'class': 'form-control select2'}),
                'fecha': forms.TextInput({'class': 'form-control datepicker'}),
                'tipo': forms.HiddenInput(),
                'creada_por': forms.HiddenInput(),
                'proveedor': forms.HiddenInput()

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
        exclude = ['precio_unitario', 'precio_total', 'precio_descontado', 'creado_por']
        widgets = {
            'entrada': forms.HiddenInput(),
            'tipo_dispositivo': forms.Select(attrs={'class': 'form-control select2'}),
            'util': forms.TextInput({'class': 'form-control '}),
            'repuesto': forms.TextInput({'class': 'form-control'}),
            'desecho': forms.TextInput({'class': 'form-control '}),
            'total': forms.TextInput({'class': 'form-control r'}),
            'precio_subtotal': forms.TextInput({'class': 'form-control'}),

        }


class EntradaDetalleUpdateForm(forms.ModelForm):
    """docstring for EntradaDetalleUpdateForm.
    """
    class Meta:
        model = inv_m.EntradaDetalle
        fields = '__all__'
        exclude = [
                    'entrada',
                    'tipo_dispositivo',
                    'precio_unitario',
                    'precio_total',
                    'precio_descontado',
                    'creado_por',
                    'precio_subtotal']
        widgets = {
            'util': forms.TextInput({'class': 'form-control '}),
            'repuesto': forms.TextInput({'class': 'form-control'}),
            'desecho': forms.TextInput({'class': 'form-control '}),
            'total': forms.TextInput({'class': 'form-control r'}),

        }


class EntradaInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Entradas
    """
    proveedor = forms.ModelChoiceField(
        queryset=crm_m.Donante.objects.all(),
        label='Proveedor',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False)
    tipo = forms.ModelChoiceField(
        queryset=inv_m.EntradaTipo.objects.all(),
        label='Tipo',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))

    recibida_por = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='Persona Que Recibe',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))

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
