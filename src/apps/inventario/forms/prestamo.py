from django import forms
from django.utils import timezone
from apps.inventario import models as inv_m
from django.contrib.auth.models import User


class PrestamoForm(forms.ModelForm):
    """ Formulario para  la creacion de prestamos.
    """
    dispositivo = forms.ModelMultipleChoiceField(
        queryset=inv_m.Dispositivo.objects.filter(
            estado=inv_m.DispositivoEstado.PD,
            etapa=inv_m.DispositivoEtapa.AB
        ),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )

    class Meta:
        model = inv_m.Prestamo
        fields = ('tipo_prestamo', 'prestado_a', 'dispositivo')
        widgets = {
            'tipo_prestamo': forms.Select(attrs={'class': 'form-control select2 '}),
            'prestado_a': forms.Select(attrs={'class': 'form-control select2'}),



        }

    def __init__(self, *args, **kwargs):
        super(PrestamoForm, self).__init__(*args, **kwargs)
        self.fields['prestado_a'].label_from_instance = lambda obj: "%s" % obj.get_full_name()


class PrestamoInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de prestamos
    """
    ESTADO_CHOICES = (
        (None, '----------'),
        (False, 'Pendiende'),
        (True, 'Devuelto'),)
    tipo_prestamo = forms.ModelChoiceField(
        queryset=inv_m.PrestamoTipo.objects.all(),
        label='Tipo de Prestamo',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False)
    prestado_a = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='Prestado a',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))

    fecha_inicio = forms.CharField(
        label='Fecha (min)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    fecha_fin = forms.CharField(
        label='Fecha (max)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    devuelto = forms.ChoiceField(
        label='Estado',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=ESTADO_CHOICES)

    def __init__(self, *args, **kwargs):
        super(PrestamoInformeForm, self).__init__(*args, **kwargs)
        self.fields['prestado_a'].label_from_instance = lambda obj: "%s" % obj.get_full_name()
