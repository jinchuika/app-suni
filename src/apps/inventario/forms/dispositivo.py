from django import forms
# from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
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
            'marca': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'tabindex': '2'}),
            'serie': forms.TextInput({'class': 'form-control', 'tabindex': '3'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '4'}),
            'puerto': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '6'}),
            'clase': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '7'}),
            'descripcion': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control', 'tabindex': '5'}),
            'caja': forms.TextInput({'class': 'form-control', 'tabindex': '8'}),
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
            'marca': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'tabindex': '2'}),
            'serie': forms.TextInput({'class': 'form-control', 'tabindex': '3'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '4'}),
            'puerto': forms.Select(attrs={'class': 'form-control select2'}),
            'cantidad_puertos': forms.TextInput({'class': 'form-control'}),
            'ram': forms.NumberInput({'class': 'form-control', 'tabindex': '9'}),
            'ram_medida': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '10'}),
            'disco_duro': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '8'}),
            'version_sistema': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '7'}),
            'procesador': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '6'}),
            'descripcion': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control', 'tabindex': '5'}),
            'servidor': forms.CheckboxInput({'class': 'icheckbox_square-red', 'tabindex': '11'}),
            'all_in_one': forms.CheckboxInput({'class': 'icheckbox_square-red', 'tabindex': '12'}),
            'clase': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '13'}),
        }

    def __init__(self, *args, **kwargs):
        super(CPUForm, self).__init__(*args, **kwargs)        
        self.fields['disco_duro'].queryset = inv_m.HDD.objects.filter(valido=True)


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
            'marca': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'tabindex': '2'}),
            'serie': forms.TextInput({'class': 'form-control', 'tabindex': '3'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '4'}),
            'procesador': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '6'}),
            'version_sistema': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '7'}),
            'disco_duro': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '8'}),
            'ram': forms.NumberInput({'class': 'form-control', 'tabindex': '9'}),
            'ram_medida': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '10'}),
            'pulgadas': forms.NumberInput({'class': 'form-control', 'tabindex': '11'}),
            'descripcion': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control', 'tabindex': '5'}),
            'clase': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '11'}),
        }

    def __init__(self, *args, **kwargs):
        super(LaptopForm, self).__init__(*args, **kwargs)
        self.fields['disco_duro'].queryset = inv_m.HDD.objects.filter(valido=True)


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
            'marca': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'tabindex': '2'}),
            'serie': forms.TextInput({'class': 'form-control ', 'tabindex': '3'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '4'}),
            'tipo_monitor': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '6'}),
            'pulgadas': forms.NumberInput({'class': 'form-control', 'tabindex': '8'}),
            'puerto': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '7'}),
            'descripcion': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control', 'tabindex': '5'}),
            'clase': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '9'}),
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
            'marca': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'tabindex': '2'}),
            'serie': forms.TextInput({'class': 'form-control ', 'tabindex': '3'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '4'}),
            'tipo_mouse': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '7'}),
            'puerto': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '6'}),
            'descripcion': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control', 'tabindex': '5'}),
            'clase': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '8'}),
            'caja': forms.TextInput(attrs={'class': 'form-control', 'tabindex': '9'}),
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
            'marca': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'tabindex': '2'}),
            'serie': forms.TextInput({'class': 'form-control ', 'tabindex': '3'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '4'}),
            'cantidad_puertos': forms.NumberInput({'class': 'form-control', 'tabindex': '6'}),
            'puerto': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '7'}),
            'velocidad': forms.NumberInput({'class': 'form-control', 'tabindex': '8'}),
            'velocidad_medida': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '9'}),
            'descripcion': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control', 'tabindex': '5'}),
            'clase': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '10'}),
        }


class DispositivoAccessPointForm(forms.ModelForm):
    """Formulario para la creación de :class:`DispositivoRed`.
    Se utiliza desde la vistas de DispositivoRed."""
    class Meta:
        model = inv_m.AccessPoint
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
            'marca': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'tabindex': '2'}),
            'serie': forms.TextInput({'class': 'form-control ', 'tabindex': '3'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '4'}),
            'cantidad_puertos': forms.NumberInput({'class': 'form-control', 'tabindex': '6'}),
            'puerto': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '7'}),
            'velocidad': forms.NumberInput({'class': 'form-control', 'tabindex': '8'}),
            'velocidad_medida': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '9'}),
            'descripcion': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control', 'tabindex': '5'}),
            'clase': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '11'}),
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
            'marca': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'tabindex': '2'}),
            'serie': forms.TextInput({'class': 'form-control ', 'tabindex': '3'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '4'}),
            'version_sistema': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '6'}),
            'so_id': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '7'}),
            'almacenamiento': forms.NumberInput({'class': 'form-control', 'tabindex': '8'}),
            'medida_almacenamiento': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '9'}),
            'pulgadas': forms.NumberInput({'class': 'form-control', 'tabindex': '10'}),
            'procesador': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '11'}),
            'ram': forms.NumberInput({'class': 'form-control', 'tabindex': '12'}),
            'medida_ram': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '13'}),
            'almacenamiento_externo': forms.CheckboxInput({'class': 'icheckbox_square-red', 'tabindex': '14'}),
            'descripcion': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control', 'tabindex': '5'}),
            'clase': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '15'}),
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
            'codigo_qr',
            'asignado'
            ]
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'tabindex': '2'}),
            'serie': forms.TextInput({'class': 'form-control', 'tabindex': '3'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '4'}),
            'medida': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '8'}),
            'puerto': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '6'}),
            'capacidad': forms.NumberInput({'class': 'form-control', 'tabindex': '7'}),
            'descripcion': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control', 'tabindex': '5'}),
            'clase': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '9'}),
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

    marca = forms.ModelChoiceField(
        queryset=inv_m.DispositivoMarca.objects.all(),
        label='Marca',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'}))

    modelo = forms.CharField(
        label='Modelo',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    tarima = forms.ModelChoiceField(
        queryset=inv_m.Tarima.objects.all(),
        label='Tarima',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'}))
    etapa= forms.ModelChoiceField(
        queryset=inv_m.DispositivoEtapa.objects.all(),
        label='Etapa',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'})

    )


class AsignacionTecnicoForm(forms.ModelForm):
    """Formulario para manipulación de :class:`AsignacionTecnico`
    """
    tipos = forms.ModelMultipleChoiceField(
        queryset=inv_m.DispositivoTipo.objects.all(),
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
        self.fields['usuario'].queryset = User.objects.filter(groups__name="inventario")
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
            'recibida_por',
            'devolucion',
            'desecho',
            'rechazar',
            'salida_kardex',
            'entrada_kardex'

            ]
        widgets = {
            'tipo_dispositivo': forms.Select(attrs={'id': 'tipo_dispositivo_movimiento', 'class': 'form-control select2', 'tabindex': '1'}),
            'cantidad': forms.TextInput({'class': 'form-control', 'tabindex': '2'}),
            'observaciones': forms.Textarea({'class': 'form-control', 'tabindex': '3'}),
        }


class SolicitudMovimientoInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Entradas
    """
    ESTADO_CHOICES = (
        (None,"--------"),
        (False,"Solicitud"),
        (True,"Devolucion"),
    )
    ETAPA_CHOICES = (
        (None,"--------"),
        (True,"Pendiente"),
        (False,"Terminada"),
    )

    devolucion = forms.ChoiceField(
        label='Estado',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=ESTADO_CHOICES)

    terminada = forms.ChoiceField(
        label='Etapa',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=ETAPA_CHOICES)

    tipo_dispositivo = forms.ModelChoiceField(
        queryset=inv_m.DispositivoTipo.objects.filter(usa_triage=True),
        label='Tipo',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))

    fecha_min = forms.CharField(
        label='Fecha (min)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max = forms.CharField(
        label='Fecha (max)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    

class DevolucionCreateForm(forms.ModelForm):
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
            'recibida_por',
            'devolucion',
            'rechazar',
            'salida_kardex',
            'entrada_kardex'
            ]
        widgets = {
            'tipo_dispositivo': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'cantidad': forms.TextInput({'class': 'form-control', 'tabindex': '2'}),
            'desecho': forms.CheckboxInput({'class': 'icheckbox_square-red', 'tabindex': '3'}),
            'observaciones': forms.Textarea({'class': 'form-control', 'tabindex': '4'}),
        }


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
        fields = ('tarima', 'tipo', 'estado', 'etapa',)
        widgets = {
            'tarima': forms.TextInput({'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.HiddenInput(),
            'etapa': forms.HiddenInput(),
        }


class DispositivosTarimaFormNew(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Ofertas
    """
    tarima = forms.CharField(
        label='Tarima',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    tipo = forms.ModelChoiceField(
        queryset=inv_m.DispositivoTipo.objects.all(),
        label='Tipo',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True)


class CPUFormUpdate(forms.ModelForm):
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
            'marca': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'tabindex': '2'}),
            'serie': forms.TextInput({'class': 'form-control', 'tabindex': '3'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '4'}),
            'puerto': forms.Select(attrs={'class': 'form-control select2'}),
            'cantidad_puertos': forms.TextInput({'class': 'form-control'}),
            'ram': forms.NumberInput({'class': 'form-control', 'tabindex': '9'}),
            'ram_medida': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '10'}),
            'disco_duro': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '8'}),
            'version_sistema': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '7'}),
            'procesador': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '6'}),
            'descripcion': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control', 'tabindex': '5'}),
            'servidor': forms.CheckboxInput({'class': 'icheckbox_square-red', 'tabindex': '11'}),
            'all_in_one': forms.CheckboxInput({'class': 'icheckbox_square-red', 'tabindex': '12'}),
            'clase': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '13'}),
        }

    def __init__(self, *args, **kwargs):
        super(CPUFormUpdate, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance',None) 
        self.fields['disco_duro'].queryset = inv_m.HDD.objects.filter(valido=True,asignado=False)