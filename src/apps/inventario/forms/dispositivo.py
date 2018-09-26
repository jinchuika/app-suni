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
        exclude = [
            'indice',
            'entrada',
            'tipo',
            'impreso',
            'entrada_detalle',
            'impreso',
            'estado',
            'etapa',
            'valido',
            'codigo_qr']
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control select2'}),
            'modelo': forms.Select(attrs={'class': 'form-control select2'}),
            'serie': forms.TextInput({'class': 'form-control'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2'}),
            'puerto': forms.Select(attrs={'class': 'form-control select2'}),
                   }


class CPUForm(forms.ModelForm):
    """Formulario para la actuliazacion de :class:`CPU`.
    Se utiliza desde la vistas de CPU."""
    class Meta:
        model = inv_m.CPU
        fields = '__all__'
        exclude = [
            'indice',
            'entrada',
            'tipo',
            'entrada_detalle',
            'impreso',
            'estado',
            'etapa',
            'valido',
            'codigo_qr'
            ]
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control select2'}),
            'modelo': forms.Select(attrs={'class': 'form-control select2'}),
            'serie': forms.TextInput({'class': 'form-control'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2'}),
            'puerto': forms.Select(attrs={'class': 'form-control select2'}),
            'cantidad_puertos': forms.TextInput({'class': 'form-control'}),
            'ram': forms.TextInput({'class': 'form-control'}),
            'ram_medida': forms.Select(attrs={'class': 'form-control select2'}),
            'disco_duro': forms.Select(attrs={'class': 'form-control select2'}),
            'version_sistema': forms.Select(attrs={'class': 'form-control select2'}),
            'procesador': forms.Select(attrs={'class': 'form-control select2'}),
        }


class LaptopForm(forms.ModelForm):
    """Formulario para la actuliazacion de :class:`Laptop`.
    Se utiliza desde la vistas de Laptop."""
    class Meta:
        model = inv_m.Laptop
        fields = '__all__'
        exclude = [
            'indice',
            'entrada',
            'tipo',
            'entrada_detalle',
            'impreso',
            'estado',
            'etapa',
            'valido',
            'codigo_qr'
            ]
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control select2'}),
            'modelo': forms.Select(attrs={'class': 'form-control select2'}),
            'serie': forms.TextInput({'class': 'form-control'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2'}),
            'procesador': forms.Select(attrs={'class': 'form-control select2'}),
            'version_sistema': forms.Select(attrs={'class': 'form-control select2'}),
            'disco_duro': forms.Select(attrs={'class': 'form-control select2'}),
            'cantidad_puertos': forms.TextInput({'class': 'form-control'}),
            'ram': forms.TextInput({'class': 'form-control'}),
            'ram_medida': forms.Select(attrs={'class': 'form-control select2'}),
            'pulgadas': forms.TextInput({'class': 'form-control'}),
        }


class MonitorForm(forms.ModelForm):
    """Formulario para la creación de :class:`Monitor`.
    Se utiliza desde la vistas de Monitor."""
    class Meta:
        model = inv_m.Monitor
        fields = '__all__'
        exclude = [
            'indice',
            'entrada',
            'tipo',
            'entrada_detalle',
            'impreso',
            'estado',
            'etapa',
            'valido',
            'codigo_qr'
            ]
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control select2'}),
            'modelo': forms.Select(attrs={'class': 'form-control select2'}),
            'serie': forms.TextInput({'class': 'form-control '}),
            'tarima': forms.Select(attrs={'class': 'form-control select2'}),
            'tipo_monitor': forms.Select(attrs={'class': 'form-control select2'}),
            'pulgadas': forms.TextInput({'class': 'form-control'}),
            'puerto': forms.Select(attrs={'class': 'form-control select2'}),
        }


class MouseForm(forms.ModelForm):
    """Formulario para la creación de :class:`Mouse`.
    Se utiliza desde la vistas de Mouse."""
    class Meta:
        model = inv_m.Mouse
        fields = '__all__'
        exclude = [
            'indice',
            'entrada',
            'tipo',
            'entrada_detalle',
            'impreso',
            'estado',
            'etapa',
            'valido',
            'codigo_qr'
            ]
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control select2'}),
            'modelo': forms.Select(attrs={'class': 'form-control select2'}),
            'serie': forms.TextInput({'class': 'form-control '}),
            'tarima': forms.Select(attrs={'class': 'form-control select2'}),
            'tipo_mouse': forms.Select(attrs={'class': 'form-control select2'}),
            'puerto': forms.Select(attrs={'class': 'form-control select2'}),
        }


class DispositivoRedForm(forms.ModelForm):
    """Formulario para la creación de :class:`DispositivoRed`.
    Se utiliza desde la vistas de DispositivoRed."""
    class Meta:
        model = inv_m.DispositivoRed
        fields = '__all__'
        exclude = [
            'indice',
            'entrada',
            'tipo',
            'entrada_detalle',
            'impreso',
            'estado',
            'etapa',
            'valido',
            'codigo_qr'
            ]
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control select2'}),
            'modelo': forms.Select(attrs={'class': 'form-control select2'}),
            'serie': forms.TextInput({'class': 'form-control '}),
            'tarima': forms.Select(attrs={'class': 'form-control select2'}),
            'procesador': forms.Select(attrs={'class': 'form-control select2'}),
            'version_sistema': forms.Select(attrs={'class': 'form-control select2'}),
            'disco_duro': forms.Select(attrs={'class': 'form-control select2'}),
            'cantidad_puertos': forms.TextInput({'class': 'form-control'}),
            'puerto': forms.Select(attrs={'class': 'form-control select2'}),
            'velocidad': forms.TextInput({'class': 'form-control'}),
            'velocidad_medida': forms.Select(attrs={'class': 'form-control select2'}),
        }


class TabletForm(forms.ModelForm):
    """Formulario para la creación de :class:`Tablet`.
    Se utiliza desde la vistas de Tablet."""
    class Meta:
        model = inv_m.Tablet
        fields = '__all__'
        exclude = [
            'indice',
            'entrada',
            'tipo',
            'entrada_detalle',
            'impreso',
            'estado',
            'etapa',
            'valido',
            'codigo_qr'
            ]
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control select2'}),
            'modelo': forms.Select(attrs={'class': 'form-control select2'}),
            'serie': forms.TextInput({'class': 'form-control '}),
            'tarima': forms.Select(attrs={'class': 'form-control select2'}),
            'version_sistema': forms.Select(attrs={'class': 'form-control select2'}),
            'so_id': forms.Select(attrs={'class': 'form-control select2'}),
            'almacenamiento': forms.TextInput({'class': 'form-control'}),
            'medida_almacenamiento': forms.Select(attrs={'class': 'form-control select2'}),
            'pulgadas': forms.TextInput({'class': 'form-control'}),
            'procesador': forms.Select(attrs={'class': 'form-control select2'}),
            'ram': forms.TextInput({'class': 'form-control'}),
            'medida_ram': forms.Select(attrs={'class': 'form-control select2'}),
        }


class HDDForm(forms.ModelForm):
    """Formulario para la actuliazacion de :class:`HDD`.
    Se utiliza desde la vistas de HDD."""
    class Meta:
        model = inv_m.HDD
        fields = '__all__'
        exclude = [
            'indice',
            'entrada',
            'tipo',
            'entrada_detalle',
            'impreso',
            'estado',
            'etapa',
            'valido',
            'codigo_qr'
            ]
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control select2'}),
            'modelo': forms.Select(attrs={'class': 'form-control select2'}),
            'serie': forms.TextInput({'class': 'form-control'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2'}),
            'medida': forms.Select(attrs={'class': 'form-control select2'}),
            'puerto': forms.Select(attrs={'class': 'form-control select2'}),
            'capacidad': forms.TextInput({'class': 'form-control'}),
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
        queryset=inv_m.DispositivoTipo.objects.filter(usa_triage=True),
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
        exclude = [
            'autorizada_por',
            'terminada',
            'creada_por',
            'fecha_creacion',
            'etapa_inicial',
            'etapa_final',
            'recibida',
            'recibida_por'
            ]
        widgets = {
            'tipo_dispositivo': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.TextInput({'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(SolicitudMovimientoCreateForm, self).__init__(*args, **kwargs)
        self.fields['tipo_dispositivo'].queryset = inv_m.DispositivoTipo.objects.filter(usa_triage=True)

    """def clean(self):
        cleaned_data = super(SolicitudMovimientoCreateForm, self).clean()
        if cleaned_data['etapa_inicial'] == cleaned_data['etapa_final']:
            raise forms.ValidationError('Las etapas no pueden ser iguales.')"""


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
        fields = ('dispositivos', )


class DispositivoTipoForm(forms.ModelForm):
    """Formulario para  crear  tipos de dispositivos usando la :class:`DispositivoTipoForm`."""
    class Meta:
        model = inv_m.DispositivoTipo
        fields = '__all__'
        widgets = {
            'tipo': forms.TextInput({'class': 'form-control'}),
            'slug': forms.TextInput({'class': 'form-control'}),
            }


class DispositivosTarimaForm(forms.ModelForm):
    """ Este Formulario se encarga de enviar los filtros de tarima para la class `Dispositivo`
    """
    class Meta:
        model = inv_m.Dispositivo
        fields = ('tarima', 'estado', 'etapa', )
        widgets = {
            'tarima': forms.TextInput({'class': 'form-control'}),
            'estado': forms.HiddenInput(),
            'etapa': forms.HiddenInput(),
        }
