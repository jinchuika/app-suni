from django import forms
# from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from apps.beqt import models as beqt_m
from apps.inventario import models as inv_m
from django.urls import reverse_lazy

class LaptopForm(forms.ModelForm):
    """Formulario para la actuliazacion de :class:`Laptop`.
    Se utiliza desde la vistas de Laptop."""
    class Meta:
        model = beqt_m.LaptopBeqt
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
            'creada_por',
            'disco_duro'
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
            'almacenamiento': forms.NumberInput({'class': 'form-control', 'tabindex': '12'}),
            'medida_almacenamiento': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '13'}),
            'cargador': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '14'}),
        }

    def __init__(self, *args, **kwargs):
        super(LaptopForm, self).__init__(*args, **kwargs)
        #self.fields['disco_duro'].queryset = beqt_m.HDDBeqt.objects.filter(valido=True, asignado=False)




class DispositivoAccessPointForm(forms.ModelForm):
    """Formulario para la creación de :class:`AccessPoint`.
    Se utiliza desde la vistas de AccessPoint."""
    class Meta:
        model = beqt_m.AccessPointBeqt
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
            'creada_por'
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
        model = beqt_m.TabletBeqt
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
            'creada_por'
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
            'estuche': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '16'}),
            'cargador': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '17'}),    
        }
    def __init__(self, *args, **kwargs):
        super(TabletForm, self).__init__(*args, **kwargs)        
        #indice = str(self.instance).split("-")[1] 
        #asignar = beqt_m.CargadorTabletBeqt.objects.get(triage="CTB-"+indice)      
        


class CargadorTabletForm(forms.ModelForm):
    """Formulario para la creación de :class:`Tablet`.
    Se utiliza desde la vistas de Tablet."""
    class Meta:
        model = beqt_m.CargadorTabletBeqt
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
            'creada_por'
            ]
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'tabindex': '2'}),
            'serie': forms.TextInput({'class': 'form-control ', 'tabindex': '3'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '4'}),          
            'descripcion': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control', 'tabindex': '5'}),
            'clase': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '15'}),
            'alimentacion': forms.TextInput(attrs={'class': 'form-control'}),
            'salida': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CargadorLaptopForm(forms.ModelForm):
    """Formulario para la creación de :class:`Tablet`.
    Se utiliza desde la vistas de Tablet."""
    class Meta:
        model = beqt_m.CargadorLaptopBeqt
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
            'creada_por'
            ]
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'tabindex': '2'}),
            'serie': forms.TextInput({'class': 'form-control ', 'tabindex': '3'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '4'}),          
            'descripcion': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control', 'tabindex': '5'}),
            'clase': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '15'}),
            'voltaje': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CaseTabletForm(forms.ModelForm):
    """Formulario para la creación de :class:`Tablet`.
    Se utiliza desde la vistas de Tablet."""
    class Meta:
        model = beqt_m.CaseTabletBeqt
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
            'creada_por'
            ]
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'tabindex': '2'}),
            'serie': forms.TextInput({'class': 'form-control ', 'tabindex': '3'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '4'}),          
            'descripcion': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control', 'tabindex': '5'}),
            'clase': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '15'}),
            'compatibilidad': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'estilo': forms.TextInput(attrs={'class': 'form-control'}),
            'material': forms.TextInput(attrs={'class': 'form-control'}),
            'dimensiones': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RegletaForm(forms.ModelForm):
    """Formulario para la creación de :class:`Tablet`.
    Se utiliza desde la vistas de Tablet."""
    class Meta:
        model = beqt_m.RegletaBeqt
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
            'creada_por'
            ]
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'tabindex': '2'}),
            'serie': forms.TextInput({'class': 'form-control ', 'tabindex': '3'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '4'}),          
            'descripcion': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control', 'tabindex': '5'}),
            'clase': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '15'}),            
            'conexiones': forms.TextInput(attrs={'class': 'form-control'}),
            'voltaje': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UpsForm(forms.ModelForm):
    """Formulario para la creación de :class:`Tablet`.
    Se utiliza desde la vistas de Tablet."""
    class Meta:
        model = beqt_m.UpsBeqt
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
            'creada_por'
            ]
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'tabindex': '2'}),
            'serie': forms.TextInput({'class': 'form-control ', 'tabindex': '3'}),
            'tarima': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '4'}),          
            'descripcion': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'class': 'form-control', 'tabindex': '5'}),
            'clase': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '15'}),            
            'conexiones': forms.TextInput(attrs={'class': 'form-control'}),
            'voltaje': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DispositivoRedForm(forms.ModelForm):
    """Formulario para la creación de :class:`DispositivoRed`.
    Se utiliza desde la vistas de DispositivoRed."""
    class Meta:
        model = beqt_m.DispositivoRedBeqt
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
            'creada_por'
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

class HDDForm(forms.ModelForm):
    """Formulario para la actuliazacion de :class:`HDD`.
    Se utiliza desde la vistas de HDD."""
    class Meta:
        model = beqt_m.HDDBeqt
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
            'asignado',
            'creada_por'
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


class DispositivoInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Entradas
    """

    triage = forms.CharField(
        label='Triage',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    tipo = forms.ModelChoiceField(
        queryset=beqt_m.DispositivoTipoBeqt.objects.filter(usa_triage=True),
        label='Tipo',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'}))

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
    procesador= forms.ModelChoiceField(
        queryset=inv_m.Procesador.objects.all(),
        label='Procesador',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'})

    )


class AsignacionTecnicoForm(forms.ModelForm):
    """Formulario para manipulación de :class:`AsignacionTecnico`
    """
    tipos = forms.ModelMultipleChoiceField(
        queryset=beqt_m.DispositivoTipoBeqt.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = beqt_m.AsignacionTecnico
        fields = '__all__'
        widgets = {
            'usuario': forms.Select(attrs={'class': 'select2 form-control'})
        }
        exclude = ('creada_por', )

    def __init__(self, *args, **kwargs):
        super(AsignacionTecnicoForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].queryset = User.objects.filter(groups__name="inventario")
        self.fields['usuario'].label_from_instance = lambda usuario: usuario.get_full_name()


class SolicitudMovimientoCreateForm(forms.ModelForm):
    """Formulario para el control de las Solicitud de Movimiento de la empresa.
    """
    field_order = ['no_salida', 'tipo_dispositivo', 'cantidad', 'observaciones']

    no_salida = forms.ModelChoiceField(
        queryset=beqt_m.SalidaInventario.objects.filter(en_creacion=True, estado__nombre="Pendiente"),
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )   

    class Meta:
        model = beqt_m.SolicitudMovimientoBeqt
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
            'no_salida': forms.Select(attrs={'class': 'form-control select2', 'tabindex': '1', 'required': 'false'}),
            'tipo_dispositivo': forms.Select(attrs={'id': 'tipo_dispositivo_movimiento', 'class': 'form-control select2', 'tabindex': '2'}),
            'cantidad': forms.TextInput({'class': 'form-control', 'tabindex': '3'}),
            'observaciones': forms.Textarea({'class': 'form-control', 'tabindex': '4'}),
        }

    def __init__(self, *args, **kwargs):
        super(SolicitudMovimientoCreateForm, self).__init__(*args, **kwargs)        
        self.fields['no_salida'].required = False



class SolicitudMovimientoInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Entradas
    """
    ESTADO_CHOICES = (
        (None,"--------"),
        (False,"Solicitud"),
        (True,"Devolución"),
    )
    ETAPA_CHOICES = (
        (None,"--------"),
        (0,"Pendiente"),
        (1,"Entregado"),
        (2,"Recibido"),
        (3,"Rechazada"),
    )

    devolucion = forms.MultipleChoiceField(
        label='Tipo',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        choices=ESTADO_CHOICES)

    estado = forms.MultipleChoiceField(
        label='Estado',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        choices=ETAPA_CHOICES)

    tipo_dispositivo = forms.ModelMultipleChoiceField(
        queryset=beqt_m.DispositivoTipoBeqt.objects.filter(usa_triage=True),
        label='Dispositivo',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))

    fecha_min = forms.CharField(
        label='Fecha (min)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max = forms.CharField(
        label='Fecha (max)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))

class SolicitudMovimientoUpdateForm(forms.ModelForm):
    """Formulario para actualizar una `SolicitudMovimiento`, usado principalmente para autorizar movimientos.
    El campo `dispositivos` sirve para crear un listado de dispositivos que serán cambiados.
    Los datos agregados al widget son para hacer filtros sobre el tipo de dispositivo y la etapa donde se encuentran,
    serán modificados en la vista para adaptarse a la solicitud de movimiento.
    """
    dispositivos = forms.ModelMultipleChoiceField(
        queryset=beqt_m.DispositivoBeqt.objects.none(),
        widget=forms.SelectMultiple(attrs={
            'data-api-url': reverse_lazy('beqt_api:api_dispositivo-list'),
            'data-etapa-inicial': '',
            'data-tipo-dispositivo': ''
        })
    )

    class Meta:
        model = beqt_m.SolicitudMovimientoBeqt
        fields = ('dispositivos', )


class DispositivoTipoForm(forms.ModelForm):
    """Formulario para  crear  tipos de dispositivos usando la :class:`DispositivoTipoForm`."""
    class Meta:
        model = beqt_m.DispositivoTipoBeqt
        fields = '__all__'
        widgets = {
            'tipo': forms.TextInput({'class': 'form-control'}),
            'slug': forms.TextInput({'class': 'form-control'}),
            }
        exclude = ('creada_por', )


class DispositivosTarimaForm(forms.ModelForm):
    """ Este Formulario se encarga de enviar los filtros de tarima para la class `Dispositivo`
    """
    class Meta:
        model = beqt_m.DispositivoBeqt
        fields = ('tarima', 'tipo', 'estado', 'etapa',)
        widgets = {
            'tarima': forms.TextInput({'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.HiddenInput(),
            'etapa': forms.HiddenInput(),
        }
        exclude =('creada_por', )

class DispositivosTarimaFormNew(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Ofertas
    """
    tarima = forms.CharField(
        label='Tarima',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    tipo = forms.ModelChoiceField(
        queryset=beqt_m.DispositivoTipoBeqt.objects.all(),
        label='Tipo',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True) 
