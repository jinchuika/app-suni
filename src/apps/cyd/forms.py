from django import forms
from django.forms.models import inlineformset_factory

from django.contrib.auth.models import User
from apps.cyd.models import Curso, CrAsistencia, CrHito, Sede, Grupo


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'


CrHitoFormSet = inlineformset_factory(
    Curso,
    CrHito,
    fields='__all__',
    extra=10,
    can_delete=True)
CrAsistenciaFormSet = inlineformset_factory(
    Curso,
    CrAsistencia,
    fields='__all__',
    extra=10,
    can_delete=True)


class SedeForm(forms.ModelForm):
    capacitador = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='cyd_capacitador'))
    lat = forms.CharField(max_length=25, required=False)
    lng = forms.CharField(max_length=25, required=False)

    class Meta:
        model = Sede
        fields = '__all__'
        exclude = ('mapa',)
        widgets = {
            'municipio': forms.Select(attrs={'class': 'select2'})
        }

    def __init__(self, *args, **kwargs):
        capacitador = kwargs.pop('capacitador', None)
        super(SedeForm, self).__init__(*args, **kwargs)
        if capacitador:
            self.fields['capacitador'].queryset = self.fields['capacitador'].queryset.filter(id=capacitador.id)
        self.fields['capacitador'].label_from_instance = lambda obj: "%s" % obj.get_full_name()


class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = '__all__'
        widgets = {
            'sede': forms.Select(attrs={'class': 'select2'})
        }
