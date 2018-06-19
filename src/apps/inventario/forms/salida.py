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
    """docstring for SalidaInventarioUpdateForm."""
    class Meta:
        model = inv_m.SalidaInventario
        fields = ('fecha', 'observaciones')
        widgets = {

            'fecha': forms.TextInput({'class': 'form-control datepicker'}),
            'observaciones': forms.Textarea({'class': 'form-control'})


        }


class PaqueteCantidadForm(forms.ModelForm):
    cantidad = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = inv_m.SalidaInventario
        fields = ('cantidad', )
