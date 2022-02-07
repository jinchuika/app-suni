from django import forms

from apps.kardex.models import *


class EquipoForm(forms.ModelForm):

    """Para creación de un :model:`kardex.Equipo`.
    """

    class Meta:
        model = Equipo
        fields = '__all__'
        exclude = ('creado_por',)

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        exclude = ('creado_por',)

class EntradaForm(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = '__all__'
        exclude = ('terminada','creado_por',)
        widgets = {
            'equipo': forms.Select(attrs={'class': 'select2'}),
            'proveedor': forms.Select(attrs={'class': 'select2'}),
            'fecha': forms.TextInput(attrs={'class': 'datepicker'})
        }


class EntradaDetalleForm(forms.ModelForm):

    """Para agregar un :model:`kardex.EntradaDetalle` a una
    :model:`kardex.Entrada`.
    """

    class Meta:
        model = EntradaDetalle
        fields = '__all__'
        widgets = {
            'equipo': forms.Select(attrs={'class': 'select2'}),
            'entrada': forms.HiddenInput()
        }

class EntradaCerrarForm(forms.ModelForm):

    """Para marcar una :model:`kardex.Entrada` como `terminada`.
    """

    class Meta:
        model = Entrada
        fields = ('terminada',)
        widgets = {
            'terminada': forms.HiddenInput()
        }


class SalidaForm(forms.ModelForm):
    class Meta:
        model = Salida
        fields = '__all__'
        exclude = ('terminada','inventario_movimiento')
        widgets = {
            'equipo': forms.Select(attrs={'class': 'select2'}),
            'fecha': forms.TextInput(attrs={'class': 'datepicker'})
        }

    def __init__(self, *args, **kwargs):
        """Para filtrar el queryset de los usuarios a elegir. De esta manera
        lista solo los activos y muestra su nombre.
        """
        super(SalidaForm, self).__init__(*args, **kwargs)
        self.fields['tecnico'].queryset = self.fields['tecnico'].queryset.filter(is_active=True)
        self.fields['tecnico'].label_from_instance = lambda obj: "%s" % obj.get_full_name()


class SalidaCerrarForm(forms.ModelForm):

    """Para marcar una salida como `terminada`.
    """

    class Meta:
        model = Salida
        fields = ('terminada',)
        widgets = {
            'terminada': forms.HiddenInput()
        }


class SalidaDetalleForm(forms.ModelForm):

    """Para añadir un :model:`kardex.SalidaDetalle` a una
    :model:`kardex.Salida`.
    """

    class Meta:
        model = SalidaDetalle
        fields = '__all__'
        widgets = {
            'salida': forms.HiddenInput(),
            'equipo': forms.Select(attrs={'class': 'select2 form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'})
        }


class KardexInformeForm(forms.Form):

    """Formulario de filtros para el informe de inventario en Kardex.
    """

    equipo = forms.ModelChoiceField(
        required=False,
        queryset=Equipo.objects.all(),
        widget=forms.Select(attrs={'class': 'select2 form-control', 'name': 'id'}))
    fecha_inicio = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'datepicker form-control'}))
    fecha_fin = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'datepicker form-control'}))
