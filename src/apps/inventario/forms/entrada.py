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
        exclude = {'creada_por', 'tipo', 'proveedor'}
        widgets = {
                'recibida_por': forms.Select(attrs={'class': 'form-control select2'}),
                'fecha': forms.TextInput({'class': 'form-control datepicker'})

            }

    def __init__(self, *args, **kwargs):
        super(EntradaUpdateForm, self).__init__(*args, **kwargs)
        self.fields['recibida_por'].label_from_instance = lambda obj: "%s" % obj.get_full_name()
