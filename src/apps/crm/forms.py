from django import forms
from django.urls import reverse_lazy
from django.forms import ModelForm
from django.contrib.auth.models import User

from apps.crm import models as crm_m
from apps.inventario import models as inv_m


class DonanteForm(forms.ModelForm):
    """Formulario para la  :class:`DonanteCreateView` y :class:`DonanteUpdateView`
    """
    class Meta:
        model = crm_m.Donante
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fax': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),  
            'pagina_web': forms.URLInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'referido': forms.TextInput(attrs={'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo_donante': forms.Select(attrs={'class': 'form-control select2'}),
            'nit': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control select2'}),
            'tratamiento': forms.Select(attrs={'class': 'form-control select2'}),
        }
        exclude = ['creado_por']

class ContactoForm(forms.ModelForm):
    """Formulario para la  :class:`ContactoCreateView` y :class:`ContactoDetailView`
    """
    class Meta:
        model = crm_m.DonanteContacto
        fields = '__all__'
        widgets = {
             'donante': forms.HiddenInput(attrs={'class': 'form-control'})
        }


class OfertaForm(forms.ModelForm):
    """Formulario para la :class:`OfertaCreateView` y :class:`OfertaUpdateView`
    """
    class Meta:
        model = crm_m.Oferta
        fields = '__all__'
        widgets = {
            'fecha_inicio': forms.TextInput({'class': 'form-control datepicker'}),
            'fecha_bodega': forms.TextInput({'class': 'form-control datepicker'}),
            'fecha_carta': forms.TextInput({'class': 'form-control datepicker'})

        }

    def __init__(self, *args, **kwargs):
        super(OfertaForm, self).__init__(*args, **kwargs)
        self.fields['recibido_por'].queryset = User.objects.filter(groups__name='tpe')
        self.fields['recibido_por'].label_from_instance = lambda obj: "%s" % obj.get_full_name()


class OfertaInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de Ofertas
    """
    donante = forms.ModelChoiceField(
        queryset=crm_m.Donante.objects.all(),
        label='Donante',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False)
    tipo_oferta = forms.ModelChoiceField(
        queryset=crm_m.OfertaTipo.objects.all(),
        label='Tipo de Oferta',
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


class TelefonoForm(forms.ModelForm):
    """Formulario para la Creacion de Telefonos de la :class:`TelefonoCreateView`
    """
    class Meta:
        model = crm_m.TelefonoCrm
        fields = '__all__'
        widgets = {
            'donante': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(TelefonoForm, self).__init__(*args, **kwargs)
        if "donante" in self.initial:
            qs_contacto = self.fields['contacto'].queryset
            qs_telefono_contacto = qs_contacto.filter(donante=self.initial['donante'])
            self.fields['contacto'].queryset = qs_telefono_contacto


class CorreoForm(forms.ModelForm):
    """Formulario para la Creacion de Correos de la :class:`CorreoCreateView`
    """
    class Meta:
        model = crm_m.MailCrm
        fields = '__all__'
        widgets = {
            'donante': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(CorreoForm, self).__init__(*args, **kwargs)
        if "donante" in self.initial:
            qs_contacto = self.fields['contacto'].queryset
            qs_correo_contacto = qs_contacto.filter(donante=self.initial['donante'])
            self.fields['contacto'].queryset = qs_correo_contacto

class InformeGatosDonantesForm(forms.Form):
    donante = forms.ModelChoiceField(
        queryset=crm_m.Donante.objects.all(),
        label='Proveedor',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False)
    tipo_dispositivo = forms.ModelMultipleChoiceField(
        queryset=inv_m.DispositivoTipo.objects.all(),
        label='Tipo de Dispositivo',
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2 form-control'}))

    fecha_min = forms.CharField(
        label='Fecha (min)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_max = forms.CharField(
        label='Fecha (max)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))