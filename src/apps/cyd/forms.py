from django import forms
from django.forms.models import inlineformset_factory
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from apps.main.forms import GeoForm
from apps.cyd.models import (
    Curso, CrAsistencia, CrHito, Sede, Grupo, Participante, Asesoria)


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        exclude = ('activo',)
        fields = '__all__'


CrHitoFormSet = inlineformset_factory(
    Curso,
    CrHito,
    fields='__all__',
    extra=5,
    can_delete=True)
CrAsistenciaFormSet = inlineformset_factory(
    Curso,
    CrAsistencia,
    fields='__all__',
    extra=6,
    can_delete=True)


class SedeForm(forms.ModelForm):
    capacitador = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='cyd_capacitador'),
        empty_label=None)
    lat = forms.CharField(max_length=25, required=False)
    lng = forms.CharField(max_length=25, required=False)

    class Meta:
        model = Sede
        fields = '__all__'
        exclude = ('mapa','activa')
        widgets = {
            'municipio': forms.Select(attrs={'class': 'select2'})
        }

    def __init__(self, *args, **kwargs):
        capacitador = kwargs.pop('capacitador', None)
        super(SedeForm, self).__init__(*args, **kwargs)
        if capacitador:
            self.fields['capacitador'].queryset = self.fields['capacitador'].queryset.filter(id=capacitador.id)
        self.fields['capacitador'].label_from_instance = lambda obj: '{}'.format(obj.get_full_name())


class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = '__all__'
        exclude = ('activo',)
        widgets = {
            'sede': forms.Select(attrs={'class': 'select2'})
        }


class SedeFilterForm(forms.Form):
    ESTADO_CHOICES = (
        (0, '----------'),
        (1, 'Capacitación'),
        (2, 'Asesoría'),)
    tipo = forms.ChoiceField(
        label='Tipo',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        choices=ESTADO_CHOICES)

    capacitador = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='cyd_capacitador'),
        widget=forms.Select(attrs={'class': 'form-control select2', 'data-url': reverse_lazy('sede_api_list')}))
    sede = forms.ModelChoiceField(
        queryset=Sede.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'})) 
    
    def __init__(self, *args, **kwargs):
        super(SedeFilterForm, self).__init__(*args, **kwargs)
        self.fields['capacitador'].label_from_instance = lambda obj: "%s" % obj.get_full_name()

class SedeFilterFormInforme(forms.Form):
    capacitador = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='cyd_capacitador'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'data-url': reverse_lazy('sede_api_list')}))
    id = forms.ModelChoiceField(
        label='Sede',
        queryset=Sede.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))
    activa = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.HiddenInput(),
        label=''
        )

    def __init__(self, *args, **kwargs):
        super(SedeFilterFormInforme, self).__init__(*args, **kwargs)
        self.fields['capacitador'].label_from_instance = lambda obj: "%s" % obj.get_full_name()


class CalendarioFilterForm(forms.Form):    
    sede = forms.ModelChoiceField(
        queryset=Sede.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'data-url': reverse_lazy('grupo_api_list')}))
    grupo = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'data-url': reverse_lazy('calendario_api_list')}))
    


class ParticipanteBaseForm(forms.ModelForm):
    """
    Formulario básico para la creación de un :class:`Participante`
    """
    udi = forms.CharField(
        widget=forms.TextInput(attrs={'data-url': reverse_lazy('escuela_api_list')}))

    class Meta:
        model = Participante
        fields = [
            'udi', 'nombre', 'apellido', 'dpi', 'genero', 'rol',
            'mail', 'tel_movil']
        exclude = ('slug','activo',)
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-reset'}),
            'apellido': forms.TextInput(attrs={'class': 'form-reset'}),
            'dpi': forms.TextInput(attrs={'class': 'form-reset', 'data-url': reverse_lazy('participante_api_list')}),
            'mail': forms.TextInput(attrs={'class': 'form-reset'}),
            'tel_movil': forms.TextInput(attrs={'class': 'form-reset'})
        }


class ParticipanteForm(ParticipanteBaseForm):
    """
    Este formulario se usa para crear participantes por listado
    Los campos tienen URL para que se consulte al API desde el template
    """
    sede = forms.ModelChoiceField(
        queryset=Sede.objects.all(),
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('grupo_api_list')}))
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('participante_api_list')}))

    class Meta:
        model = Participante
        fields = [
            'sede', 'grupo', 'udi', 'nombre', 'apellido', 'dpi', 'genero', 'rol',
            'mail', 'tel_movil']
        exclude = ('slug','activo')

class ParticipanteFormList(ParticipanteBaseForm):
    """
    Este formulario se usa para crear participantes por listado
    Los campos tienen URL para que se consulte al API desde el template
    """
    sede = forms.ModelChoiceField(
        queryset=Sede.objects.all(),
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('grupo_api_list')}))
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('participante_api_list')}))

    class Meta:
        model = Participante
        fields = [
            'sede', 'grupo', 'udi']
        exclude = ('slug','activo','nombre', 'apellido', 'dpi', 'genero', 'rol',
            'mail', 'tel_movil')


class ParticipanteBuscarForm(ParticipanteForm, GeoForm, forms.ModelForm):
    nombre = forms.CharField(required=False)    
    capacitador = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='cyd_capacitador'))

    class Meta:
        model = Participante
        fields = ['nombre', 'capacitador']

    def __init__(self, *args, **kwargs):
        super(ParticipanteBuscarForm, self).__init__(*args, **kwargs)
        self.fields['capacitador'].label_from_instance = lambda obj: "%s" % obj.get_full_name()
        #self.fields.pop('grupo')


class ParticipanteAsignarForm(ParticipanteFormList):
    # class ParticipanteAsignarForm(ParticipanteBaseForm):
    def __init__(self, *args, **kwargs):
        super(ParticipanteAsignarForm, self).__init__(*args, **kwargs)
        self.fields.pop('udi')


class AsesoriaForm(forms.ModelForm):
    """Formulario para crear :model:`cyd.Asesoria` desde el perfil de la sede."""

    class Meta:
        model = Asesoria
        fields = '__all__'
        widgets = {
            'sede': forms.HiddenInput(),
            'fecha': forms.TextInput(attrs={'class': 'datepicker form-control'}),
            'hora_inicio': forms.TextInput(attrs={'class': 'form-control'}),
            'hora_fin': forms.TextInput(attrs={'class': 'form-control'}),
            'observacion': forms.TextInput(attrs={'class': 'form-control'})
        }


class GrupoListForm(forms.Form):
    """Formulario para listar :model:`cyd.Grupo` en una :model:`cyd.Sede`.
    Se usa para copiar los participantes de un grupo a otros.
    """
    grupo = forms.ModelChoiceField(Grupo.objects.all())

class GrupoFilterFormInforme(forms.Form):
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'data-url': reverse_lazy('sede_api_list')}))
    sede = forms.ModelChoiceField(
        label='Sede',
        queryset=Sede.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))
    numero = forms.IntegerField(
        label='No. Grupo',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    activo = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.HiddenInput(),
        label=''
        )

class ControlAcademicoGrupoForm(forms.Form):
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'select2 form-control', 'data-url': reverse_lazy('sede_api_list')}))
    sede = forms.ModelChoiceField(
        label='Sede',
        queryset=Sede.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'select2 form-control'}))
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('participante_api_list')}))

class InformeAsistenciaForm(forms.Form):    
    sede = forms.ModelChoiceField(
        label='Sede',
        queryset=Sede.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'select2 form-control'}))
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('participante_api_list')}))
   
    

