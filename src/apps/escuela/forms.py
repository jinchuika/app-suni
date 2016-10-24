from django import forms
from django.forms.models import inlineformset_factory
from django.core.urlresolvers import reverse_lazy

from apps.escuela.models import Escuela, EscContacto, EscContactoTelefono, EscContactoMail
from apps.main.models import Departamento, Municipio
from apps.mye.models import Cooperante, Proyecto


class FormEscuelaCrear(forms.ModelForm):
    class Meta:
        model = Escuela
        fields = '__all__'
        exclude = ['cooperante_asignado', 'proyecto_asignado']
        widgets = {
            'municipio': forms.Select(attrs={'class': 'select2'})
        }


class BuscarEscuelaForm(forms.ModelForm):
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        required=False)
    cooperante = forms.ModelMultipleChoiceField(
        queryset=Cooperante.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False)
    proyecto = forms.ModelMultipleChoiceField(
        queryset=Proyecto.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False)
    codigo = forms.CharField(
        required=False)
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'data-ajax--url': reverse_lazy('escuela_buscar_backend')}),
        required=False)
    direccion = forms.CharField(
        widget=forms.TextInput(),
        required=False)
    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all(),
        required=False)

    class Meta:
        model = Escuela
        fields = ['codigo', 'nombre', 'municipio']


class ContactoForm(forms.ModelForm):
    class Meta:
        model = EscContacto
        fields = '__all__'
        widgets = {
            'escuela': forms.HiddenInput()
        }


ContactoTelefonoFormSet = inlineformset_factory(EscContacto, EscContactoTelefono, fields='__all__', extra=1, can_delete=True)
ContactoMailFormSet = inlineformset_factory(EscContacto, EscContactoMail, fields='__all__', extra=1, can_delete=True)
