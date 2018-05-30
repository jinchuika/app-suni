from django import forms
from apps.inventario import models as inv_m


class DesechoEmpresaForm(forms.ModelForm):
    """ Formulario para el control de desechos de la empresa
    """
    class Meta:
        model = inv_m.DesechoEmpresa
        fields = '__all__'


class DesechoSalidaForm(forms.ModelForm):
    """Formulario para el control de salida de desechos de la empresa.
    """

    class Meta:
        model = inv_m.DesechoSalida
        fields = '__all__'
        exclude = {'precio_total', 'peso', 'creado_por', 'en_creacion'}


class DesechoSalidaUpdateForm(forms.ModelForm):
    """ Formulario para la actualizacion de salida  de desecho de la empresa
    """

    class Meta:
        model = inv_m.DesechoSalida
        fields = '__all__'
        exclude = ['creado_por']
        widgets = {
                'en_creacion': forms.HiddenInput(),
                'empresa': forms.Select(attrs={'class': 'form-control select2'}),
                'fecha': forms.TextInput({'class': 'form-control datepicker'}),
                'precio_total': forms.TextInput({'class': 'form-control'}),
                'peso': forms.TextInput({'class': 'form-control'}),
                'observaciones': forms.Textarea({'class': 'form-control'}),


            }


class DesechoDetalleForm(forms.ModelForm):
    """Formulario para ingresar nuevos detalles de  DesechoDetalle."""

    class Meta:
        model = inv_m.DesechoDetalle
        fields = '__all__'
        widgets = {
                'desecho': forms.HiddenInput(),
                'fecha': forms.TextInput({'class': 'form-control datepicker'}),
                'precio_total': forms.TextInput({'class': 'form-control'}),
                }
