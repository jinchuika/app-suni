from django import forms
from django.forms import ModelForm
from apps.inventario import models as inv_m


class EntradaForm(forms.ModelForm):
    """Formulario para la :`class`:`EntradaCreateView` que es la encargada de crear los datos
    de entrada.
    """
    class Meta:
        model = inv_m.Entrada
        fields = '__all__'
        exclude = {'en_creacion', 'creada_por'}
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
        # exclude = {'creada_por', 'tipo', 'proveedor'}
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
        widgets = {
            'entrada': forms.HiddenInput(),
            'tipo_dispositivo': forms.Select(attrs={'class': 'form-control select2'}),
            'util': forms.TextInput({'class': 'form-control '}),
            'repuesto': forms.TextInput({'class': 'form-control'}),
            'desecho': forms.TextInput({'class': 'form-control '}),
            'total': forms.TextInput({'class': 'form-control r'}),
            'precio_subtotal': forms.TextInput({'class': 'form-control'}),
            'precio_unitario': forms.HiddenInput(),
            'precio_total': forms.HiddenInput(),
            'precio_descontado': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),

        }
