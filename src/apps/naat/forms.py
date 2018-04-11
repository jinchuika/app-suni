from django import forms
from django.contrib.auth.models import User

from apps.naat import models as naat_m
from apps.cyd import forms as cyd_f
from apps.cyd import models as cyd_m


class ProcesoNaatForm(forms.ModelForm):
    """Formulario para crear un :class:`ProcesoNaat`
    """
    udi = forms.CharField(
        label='UDI de la escuela',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = naat_m.ProcesoNaat
        fields = ('udi', 'fecha_inicio', 'fecha_fin')
        widgets = {
            'fecha_inicio': forms.TextInput(attrs={'class': 'form-control datepicker'}),
            'fecha_fin': forms.TextInput(attrs={'class': 'form-control datepicker'}),
        }


class AsignacionNaatForm(cyd_f.ParticipanteBaseForm):
    """Formulario para crear un :class:`Participante` y asignarlo a un capacitador por medio
    de :class:`AsignacionNaat` (esta lógica para en la vista, el formulario únicamente sirve para
    tomar los datos).
    La lógica para filtrar al capacitador se realizará en la vista.
    """
    proceso = forms.ModelChoiceField(
        queryset=naat_m.ProcesoNaat.objects.all(),
        empty_label=None)

    class Meta:
        model = cyd_m.Participante
        fields = [
            'udi', 'nombre', 'apellido', 'dpi', 'genero', 'rol',
            'mail', 'tel_movil']
        exclude = ('slug',)


class CalendarFilterForm(forms.Form):
    """Formulario para filtrar los eventos mostrados en el calendario con base en el capacitador."""
    capacitador = forms.ModelChoiceField(
        queryset=User.objects.filter(id__in=naat_m.SesionPresencial.objects.values('proceso__capacitador').distinct()),
        required=False)

    def __init__(self, *args, **kwargs):
        super(CalendarFilterForm, self).__init__(*args, **kwargs)
        self.fields['capacitador'].label_from_instance = lambda obj: '{}'.format(obj.get_full_name())


class SesionPresencialCreateForm(forms.ModelForm):

    """Formulario para crear una nueva :class:`SesionPresencial`
    """

    class Meta:
        model = naat_m.SesionPresencial
        fields = ('fecha', 'hora_inicio', 'hora_fin', 'proceso')
        widgets = {
            'fecha': forms.TextInput(attrs={'class': 'form-control datepicker'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control'}),
            'proceso': forms.Select(attrs={'class': 'form-control'})
        }


class SesionPresencialForm(forms.ModelForm):
    class Meta:
        model = naat_m.SesionPresencial
        fields = ('fecha', 'hora_inicio', 'hora_fin', 'observaciones', 'asistentes')
        widgets = {
            'fecha': forms.TextInput(attrs={'class': 'form-control datepicker'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
            'asistentes': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(SesionPresencialForm, self).__init__(*args, **kwargs)
        self.fields['asistentes'].label_from_instance = lambda obj: '{}'.format(obj.participante)
