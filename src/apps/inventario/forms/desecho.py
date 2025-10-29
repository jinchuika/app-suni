from django import forms
from apps.inventario import models as inv_m


class DesechoEmpresaForm(forms.ModelForm):
    """ Formulario para el control de desechos de la empresa
    """
    class Meta:
        model = inv_m.DesechoEmpresa
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput({'class': 'form-control'}),
            'encargado':forms.TextInput({'class': 'form-control'}),
            'telefono': forms.TextInput({'class': 'form-control'}),
            'dpi':forms.TextInput({'class': 'form-control'}),
        }
        exclude = ('creada_por', )

class DesechoSalidaForm(forms.ModelForm):
    """Formulario para el control de salida de desechos de la empresa.
    """

    class Meta:
        model = inv_m.DesechoSalida
        fields = ('fecha', 'empresa', 'observaciones')
        exclude = ('precio_total', 'peso', 'creado_por', 'en_creacion','codigo_qr')
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
        exclude = ('creado_por','codigo_qr','revision_sub_jefe','revision_jefe')
        widgets = {
                'en_creacion': forms.HiddenInput(),
                'empresa': forms.Select(attrs={'class': 'form-control select2'}),
                'fecha': forms.TextInput({'class': 'form-control datepicker'}),
                'precio_total': forms.TextInput({'class': 'form-control'}),
                'comprobante': forms.TextInput({'class': 'form-control'}),
                'peso': forms.TextInput({'class': 'form-control'}),
                'observaciones': forms.Textarea({'class': 'form-control'}),
                'url': forms.TextInput({'class': 'form-control'}),
            }


class DesechoDetalleForm(forms.ModelForm):
    """Formulario para ingresar nuevos detalles de  DesechoDetalle."""

    class Meta:
        model = inv_m.DesechoDetalle
        fields = ['tipo_dispositivo', 'entrada_detalle', 'cantidad', 'desecho']
        exclude = ('aprobado','creada_por', )
        widgets = {
                'desecho': forms.HiddenInput(),
                'tipo_dispositivo': forms.Select(attrs={'class': 'form-control select2'}),
                'entrada_detalle': forms.Select(attrs={'class': 'form-control select2', 'required': 'true'}),
                'cantidad': forms.NumberInput({'class': 'form-control', 'required': 'true', 'min': 1}),
                }

    def __init__(self, *args, **kwargs):
        super(DesechoDetalleForm, self).__init__(*args, **kwargs)
        self.fields['cantidad'].widget = forms.NumberInput(
                attrs={'class': 'form-control', 'min': "1"})

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
        exclude = ('aprobado','creada_por')
        widgets = {
                'desecho': forms.HiddenInput(),
                }

    def __init__(self, *args, **kwargs):
        super(DesechoDispositivoForm, self).__init__(*args, **kwargs)
        dispositivos_desecho = inv_m.DesechoDispositivo.objects.all().values('dispositivo')
        dispositivos_desechados = inv_m.Dispositivo.objects.filter(estado=inv_m.DispositivoEstado.DS, etapa=inv_m.DispositivoEtapa.AB)
        self.fields['dispositivo'].queryset = inv_m.Dispositivo.objects.filter(estado=inv_m.DispositivoEstado.DS, etapa=inv_m.DispositivoEtapa.AB).exclude(id__in=dispositivos_desecho)

class DesechoSolicitudForm(forms.ModelForm):
    """Formulario para seleccionar solicitudes de movimeiento de tipo desecho"""    
    solicitud = forms.ModelChoiceField(
        queryset=inv_m.SolicitudMovimiento.objects.filter(desecho=True, etapa_final=inv_m.DispositivoEtapa.TR, recibida=True, terminada=True).order_by('-id'),
        label="Solicitud de Desecho",
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'select-solicitud'})
    )

    class Meta:
        model = inv_m.SolicitudMovimiento
        fields = ()
        exclude = ('etapa_inicial','fecha_creacion','creada_por','recibida_por','autorizada_por','terminada',
                   'recibida','devolucion','rechazar','desecho','salida_kardex','entrada_kardex','observaciones',
                   'no_salida','no_inventariointerno','tipo_dispositivo','cantidad','tipo_dispositivo','cantidad')
        
        widgets = {
            'tipo_dispositivo': forms.Select(attrs={'class': 'form-control select2'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
    def __init__(self, *args, **kwargs):
        super(DesechoSolicitudForm, self).__init__(*args, **kwargs)
        self.fields['solicitud'].label_from_instance = lambda obj: '{} | Tipo: {} | Cantidad: {}'.format(obj.id, obj.tipo_dispositivo, obj.cantidad)

class DesechoInventarioListForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Entradas
    """
    ESTADO_CHOICES = (
        (None, '----------'),
        (True, 'Pendiende'),
        (False, 'Entregado'),)
    id = forms.IntegerField(
        label='No. Desecho',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    en_creacion = forms.ChoiceField(
        label='Estado',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=ESTADO_CHOICES)

    fecha_min = forms.CharField(
        label='Fecha (min)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max = forms.CharField(
        label='Fecha (max)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))


class SolicitudMovimientoDesechoCreateForm(forms.ModelForm):
    """Formulario para el control de las Solicitud de Movimiento que van a desecho.
    """
    field_order = ['tipo_dispositivo','observaciones']

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
            'recibida_por',
            'devolucion',
            'desecho',
            'rechazar',
            'salida_kardex',
            'entrada_kardex',
            'inventario_interno',
            'no_inventariointerno',
            'no_salida', 
            'cantidad'
            ]
        widgets = {
            'tipo_dispositivo': forms.Select(attrs={'id': 'tipo_dispositivo_movimiento', 'class': 'form-control select2', 'tabindex': '2'}),
            'observaciones': forms.Textarea({'class': 'form-control', 'tabindex': '4'}),
        }
        
    def save(self, commit=True):
        instance = super(SolicitudMovimientoDesechoCreateForm, self).save(commit=False)
        instance.cantidad = 0
        instance.etapa_inicial = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.AB)
        instance.etapa_final = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.TR)
        instance.desecho = True
        if commit:
            instance.save()
        return instance