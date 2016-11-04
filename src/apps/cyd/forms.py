from django.forms import ModelForm
from apps.cyd.models import Curso, CrAsistencia, CrHito
from django.forms.models import inlineformset_factory


class CursoForm(ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'


CrHitoFormSet = inlineformset_factory(Curso, CrHito, fields='__all__', extra=1, can_delete=True)
CrAsistenciaFormSet = inlineformset_factory(Curso, CrAsistencia, fields='__all__', extra=1, can_delete=True)
