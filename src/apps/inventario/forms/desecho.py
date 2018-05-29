from django import forms
from apps.inventario import models as inv_m


class DesechoEmpresaForm(forms.ModelForm):
    """ Formulario para el control de desechos de la empresa
    """
    class Meta:
        model = inv_m.DesechoEmpresa
        fields = '__all__'
