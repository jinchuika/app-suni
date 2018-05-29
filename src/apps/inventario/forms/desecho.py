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
