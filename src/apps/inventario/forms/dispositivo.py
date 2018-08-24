from django import forms
# from django.core.exceptions import ValidationError

from apps.inventario import models as inv_m
from django.urls import reverse_lazy


class TecladoForm(forms.ModelForm):
    """Formulario para la creación de :class:`Teclado`.
    Se utiliza desde la vistas de teclado."""
    class Meta:
        model = inv_m.Teclado
        fields = '__all__'
        exclude = ['indice', 'entrada', 'tipo']
        widgets = {
            'codigo_qr': forms.URLInput(attrs={'class': 'form-control'})
                   }


class DispositivoFallaCreateForm(forms.ModelForm):
    """Formulario para la creación de :class:`DispositivoFalla`.
    Se utiliza desde la vista de detalle de cada dispositivo."""
    class Meta:
        model = inv_m.DispositivoFalla
        fields = ('dispositivo', 'descripcion_falla',)
        widgets = {
            'dispositivo': forms.HiddenInput(),
            'descripcion_falla': forms.Textarea(attrs={'class': 'form-control'})
        }


class DispositivoFallaUpdateForm(forms.ModelForm):
    """Formulario para edición de :class:`DispositivoFalla`
    """
    class Meta:
        model = inv_m.DispositivoFalla
        fields = ('descripcion_falla', 'descripcion_solucion', 'terminada')
        widgets = {
            'descripcion_falla': forms.Textarea(attrs={'class': 'form-control'}),
            'descripcion_solucion': forms.Textarea(attrs={'class': 'form-control'})
        }


class DispositivoInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Entradas
    """

    triage = forms.CharField(
        label='Triage',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    tipo = forms.ModelChoiceField(
        queryset=inv_m.DispositivoTipo.objects.all(),
        label='Tipo',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))


class AsignacionTecnicoForm(forms.ModelForm):
    """Formulario para manipulación de :class:`AsignacionTecnico`
    """
    tipos = forms.ModelMultipleChoiceField(
        queryset=inv_m.DispositivoTipo.objects.filter(usa_triage=True),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = inv_m.AsignacionTecnico
        fields = '__all__'
        widgets = {
            'usuario': forms.Select(attrs={'class': 'select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(AsignacionTecnicoForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].label_from_instance = lambda usuario: usuario.get_full_name()


class SolicitudMovimientoCreateForm(forms.ModelForm):
    """Formulario para el control de las Solicitud de Movimiento de la empresa.
    """
    class Meta:
        model = inv_m.SolicitudMovimiento
        exclude = ['autorizada_por', 'terminada', 'creada_por']
        widgets = {
            'etapa_inicial': forms.Select(attrs={'class': 'form-control '}),
            'etapa_final': forms.Select(attrs={'class': 'form-control '}),
            'tipo_dispositivo': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.TextInput({'class': 'form-control'}),
            'fecha_creacion': forms.DateInput(attrs={'class': 'form-control datepicker'}),
        }

    def __init__(self, *args, **kwargs):
        super(SolicitudMovimientoCreateForm, self).__init__(*args, **kwargs)
        self.fields['tipo_dispositivo'].queryset = inv_m.DispositivoTipo.objects.filter(usa_triage=True)

    def clean(self):
        cleaned_data = super(SolicitudMovimientoCreateForm, self).clean()
        if cleaned_data['etapa_inicial'] == cleaned_data['etapa_final']:
            raise forms.ValidationError('Las etapas no pueden ser iguales.')


class SolicitudMovimientoUpdateForm(forms.ModelForm):
    """Formulario para actualizar una `SolicitudMovimiento`, usado principalmente para autorizar movimientos.
    El campo `dispositivos` sirve para crear un listado de dispositivos que serán cambiados.
    Los datos agregados al widget son para hacer filtros sobre el tipo de dispositivo y la etapa donde se encuentran,
    serán modificados en la vista para adaptarse a la solicitud de movimiento.
    """
    dispositivos = forms.ModelMultipleChoiceField(
        queryset=inv_m.Dispositivo.objects.none(),
        widget=forms.SelectMultiple(attrs={
            'data-api-url': reverse_lazy('inventario_api:api_dispositivo-list'),
            'data-etapa-inicial': '',
            'data-tipo-dispositivo': ''
        })
    )

    class Meta:
        model = inv_m.SolicitudMovimiento
        fields = ('dispositivos', 'terminada')


class DispositivoTipoForm(forms.ModelForm):
    """Formulario para  crear  tipos de dispositivos usando la :class:`DispositivoTipoForm`."""
    class Meta:
        model = inv_m.DispositivoTipo
        fields = '__all__'
        widgets = {
            'tipo': forms.TextInput({'class': 'form-control'}),
            'slug': forms.TextInput({'class': 'form-control'}),
            }
