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
        fields = ('fecha', 'empresa', 'observaciones')
        exclude = ('precio_total', 'peso', 'creado_por', 'en_creacion')
        widgets = {
                'empresa': forms.Select(attrs={'class': 'form-control select2'}),
                'fecha': forms.TextInput({'class': 'form-control datepicker'}),
                'observaciones': forms.Textarea({'class': 'form-control'}),
            }


class DesechoSalidaUpdateForm(forms.ModelForm):
    """ Formulario para la actualizacion de salida  de desecho de la empresa
    """

    class Meta:
        model = inv_m.DesechoSalida
        fields = '__all__'
        exclude = ('creado_por',)
        widgets = {
                'en_creacion': forms.HiddenInput(),
                'empresa': forms.Select(attrs={'class': 'form-control select2'}),
                'fecha': forms.TextInput({'class': 'form-control datepicker'}),
                'precio_total': forms.TextInput({'class': 'form-control'}),
                'peso': forms.TextInput({'class': 'form-control'}),
                'observaciones': forms.Textarea({'class': 'form-control'}),
                'url': forms.TextInput({'class': 'form-control'}),
            }


class DesechoDetalleForm(forms.ModelForm):
    """Formulario para ingresar nuevos detalles de  DesechoDetalle."""

    class Meta:
        model = inv_m.DesechoDetalle
        fields = ['tipo_dispositivo', 'entrada_detalle', 'cantidad', 'desecho']
        exclude = ('aprobado',)
        widgets = {
                'desecho': forms.HiddenInput(),
                'tipo_dispositivo': forms.Select(attrs={'class': 'form-control select2'}),
                'entrada_detalle': forms.Select(attrs={'class': 'form-control select2'}),
                'cantidad': forms.TextInput({'class': 'form-control'}),
                }

class DesechoDispositivoForm(forms.ModelForm):
    """Formulario para ingresar dispositivos a desechar"""
    dispositivo = forms.ModelMultipleChoiceField(
        queryset=inv_m.Dispositivo.objects.filter(
            estado=inv_m.DispositivoEstado.DS,
            etapa=inv_m.DispositivoEtapa.AB
        ),
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )

    class Meta:
        model = inv_m.DesechoDispositivo
        fields = '__all__'
        exclude = ('aprobado',)
        widgets = {
                'desecho': forms.HiddenInput(),
                }

    def __init__(self, *args, **kwargs):
        super(DesechoDispositivoForm, self).__init__(*args, **kwargs)
        dispositivos_desecho = inv_m.DesechoDispositivo.objects.all().values('dispositivo')
        dispositivos_desechados = inv_m.Dispositivo.objects.filter(estado=inv_m.DispositivoEstado.DS, etapa=inv_m.DispositivoEtapa.AB)
        self.fields['dispositivo'].queryset = inv_m.Dispositivo.objects.filter(estado=inv_m.DispositivoEstado.DS, etapa=inv_m.DispositivoEtapa.AB).exclude(id__in=dispositivos_desecho)

