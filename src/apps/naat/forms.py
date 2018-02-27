from django import forms
from django.contrib.auth.models import User

from apps.naat import models as naat_m
from apps.cyd import forms as cyd_f
from apps.cyd import models as cyd_m


class AsignacionNaatForm(cyd_f.ParticipanteBaseForm):
    capacitador = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='naat_facilitador'),
        empty_label=None)

    class Meta:
        model = cyd_m.Participante
        fields = [
            'udi', 'nombre', 'apellido', 'dpi', 'genero', 'rol',
            'mail', 'tel_movil']
        exclude = ('slug',)

    def __init__(self, *args, **kwargs):
        super(AsignacionNaatForm, self).__init__(*args, **kwargs)
        self.fields['capacitador'].label_from_instance = lambda obj: '{}'.format(obj.get_full_name())


class CalendarFilterForm(forms.Form):
    capacitador = forms.ModelChoiceField(
        queryset=User.objects.filter(id__in=naat_m.SesionPresencial.objects.values('capacitador').distinct()),
        required=False)

    def __init__(self, *args, **kwargs):
        super(CalendarFilterForm, self).__init__(*args, **kwargs)
        self.fields['capacitador'].label_from_instance = lambda obj: '{}'.format(obj.get_full_name())
