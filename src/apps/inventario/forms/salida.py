from django import forms
from apps.inventario import models as inv_m


class SalidaInventarioForm(forms.ModelForm):
    """ Formulario para el control de las Salidas de Inventario
    """
    UDI = forms.CharField(
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
