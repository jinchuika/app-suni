from django import forms
from django.contrib.auth.models import User

from apps.main import models as main_m
from apps.main.forms import GeoDateForm

from apps.kalite import models as kalite_models


class TipoVisitaForm(forms.ModelForm):
    class Meta:
        model = kalite_models.TipoVisita
        fields = '__all__'
        widgets = {
            'rubricas': forms.CheckboxSelectMultiple()
        }
        exclude = ('tipo_visita_creada_por',)


class RubricaForm(forms.ModelForm):
    class Meta:
        model = kalite_models.Rubrica
        fields = '__all__'
        exclude = ('rubrica_creada_por',)

class IndicadorForm(forms.ModelForm):
    class Meta:
        model = kalite_models.Indicador
        fields = '__all__'
        widgets = {
            'rubrica': forms.HiddenInput()
        }
        exclude = ('indicador_creada_por',)

class VisitaForm(forms.ModelForm):
    class Meta:
        model = kalite_models.Visita
        fields = ('numero', 'tipo_visita', 'escuela', 'fecha', 'hora_inicio', 'hora_fin')
        widgets = {
            'escuela': forms.HiddenInput(),
            'fecha': forms.TextInput(attrs={'class': 'datepicker'})
        }


class GradoForm(forms.ModelForm):
    class Meta:
        model = kalite_models.Grado
        fields = '__all__'
        widgets = {
            'visita': forms.HiddenInput()
        }
        exclude = ('grado_creada_por',)

class VisitaInformeForm(GeoDateForm):

    """Formulario para el informe de :class:`Visita
    """

    capacitador = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='cyd_capacitador'),
        required=False)

    def __init__(self, *args, **kwargs):
        super(VisitaInformeForm, self).__init__(*args, **kwargs)
        self.fields['capacitador'].label_from_instance = lambda obj: "%s" % obj.get_full_name()


class CalendarFilterForm(forms.Form):
    capacitador = forms.ModelChoiceField(
        queryset=User.objects.filter(id__in=kalite_models.Visita.objects.values('capacitador').distinct()),
        required=False)

    def __init__(self, *args, **kwargs):
        super(CalendarFilterForm, self).__init__(*args, **kwargs)
        self.fields['capacitador'].label_from_instance = lambda obj: "%s" % obj.get_full_name()


class VisitaEscuelaForm(forms.Form):
    departamento = forms.ModelChoiceField(
        queryset=main_m.Departamento.objects.all(),
        required=False
    )
    municipio = forms.ModelChoiceField(
        queryset=main_m.Municipio.objects.all(),
        required=False
    )
