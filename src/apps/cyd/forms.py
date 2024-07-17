from django import forms
from django.forms.models import inlineformset_factory
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from apps.main.forms import GeoForm
from apps.main.models import Departamento, Municipio
from apps.cyd.models import (
    Curso, CrAsistencia, CrHito, Sede, Grupo, Participante, ParEtnia, ParEscolaridad, Asesoria, NotaAsistencia,Calendario)
from apps.escuela.models import Escuela


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        exclude = ('activo',)
        fields = '__all__'
        exclude = ['cyd_curso_creado_por',]


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
    extra=5,
    can_delete=True)


class SedeForm(forms.ModelForm):

    udi = forms.CharField(
        label='Escuela Beneficiada',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '13', 'required': 'true', 'placeholder': '00-00-0000-00', 'tabindex': '4'}))

    class Meta:
        model = Sede
        fields = '__all__'
        exclude = ('nombre', 'capacitador', 'escuela_beneficiada', 'mapa', 'activa', 'fecha_creacion','fecha_finalizacion',)
        #exclude = ('nombre', 'capacitador', 'escuela_beneficiada', 'mapa', 'activa')
        widgets = {
            'municipio': forms.Select(attrs={'class': 'select2', 'required': 'true', 'tabindex': '1'}),
            'direccion': forms.TextInput({'class': 'form-control', 'placeholder': 'Avenida, Calle, Zona','onkeyup': 'this.value = this.value.toUpperCase();' ,'tabindex': '2'}),
            'observacion': forms.Textarea({'class': 'form-control', 'tabindex': '3'}),
            'tipo_sede': forms.Select(attrs={'class': 'select2', 'required': 'true', 'tabindex': '5'}),
        }

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = '__all__'
        exclude = ('activo','cyd_grupo_creado_por',)
        widgets = {
            'sede': forms.Select(attrs={'class': 'select2'}),
            'numero': forms.NumberInput(attrs={'class': 'form-reset','size':'5'}),
        }
    def __init__(self, *args, **kwargs):
        super(GrupoForm, self).__init__(*args, **kwargs)
        self.fields['numero'].label = "Cantidad de grupos a crear"

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
        queryset=Sede.objects.filter(activa=True),
        widget=forms.Select(attrs={'class': 'form-control select2'}))

    def __init__(self, *args, **kwargs):
        super(SedeFilterForm, self).__init__(*args, **kwargs)
        self.fields['capacitador'].label_from_instance = lambda obj: "%s" % obj.get_full_name()

class SedeFilterFormInforme(forms.Form):
    capacitador = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='cyd_capacitador'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'}))
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
        queryset=Sede.objects.filter(activa=True),
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
        exclude = ('slug','activo','cyd_participante_creado_por', )
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
        queryset=Sede.objects.filter(activa=True),        
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('grupo_api_list')}),required=False)
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),        
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('participante_api_list')}),required=False)
    udi = forms.CharField(
        help_text="udi_help",
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '13', 'required': 'true', 'placeholder': '00-00-0000-00', 'data-url': reverse_lazy('escuela_api_list')}))

    dpi = forms.CharField(
        help_text="dpi_help",
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '13', 'placeholder': '0000000000000', 'data-url': reverse_lazy('participante_api_list')}))

    etnia = forms.ModelChoiceField(
        queryset=ParEtnia.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'select2'}))

    escolaridad = forms.ModelChoiceField(
        queryset=ParEscolaridad.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'select2'}))

    class Meta:
        model = Participante
        fields = [
            'sede', 'grupo', 'udi', 'nombre', 'apellido', 'dpi', 'genero', 'rol', 'mail', 'tel_movil', 'etnia', 'escolaridad','profesion','grado_impartido','chicos','chicas']
        exclude = ('slug','activo','cyd_participante_creado_por')

class ParticipanteFormList(ParticipanteBaseForm):
    """
    Este formulario se usa para crear participantes por listado
    Los campos tienen URL para que se consulte al API desde el template
    """
    sede = forms.ModelChoiceField(
        queryset=Sede.objects.filter(activa=True),
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('grupo_api_list')}),
        required=False
        )
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('participante_api_list')}),
        required=False
        )
    udi = forms.CharField(
        help_text="udi_help",
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '13', 'required': 'true', 'placeholder': '00-00-0000-00', 'data-url': reverse_lazy('escuela_api_list')}))

    class Meta:
        model = Participante
        fields = ['sede', 'grupo', 'udi']
        exclude = ('slug','activo','nombre', 'apellido', 'dpi', 'genero', 'rol', 'mail', 'tel_movil','cyd_participante_creado_por',)

class ParticipanteBuscarForm(ParticipanteForm, forms.ModelForm):
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'data-url': reverse_lazy('municipio_api_list')}),
        required=False)
    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False)
    dpi = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '13', 'placeholder': '0000000000000'}))
    nombre = forms.CharField(required=False)
    #capacitador = forms.ModelChoiceField(required=False,queryset=User.objects.filter(groups__name='cyd_capacitador'))

    class Meta:
        model = Participante
        fields = ['dpi', 'nombre', 'departamento', 'municipio',]

    def __init__(self, *args, **kwargs):
        super(ParticipanteBuscarForm, self).__init__(*args, **kwargs)        
        #self.fields['capacitador'].label_from_instance = lambda obj: "%s" % obj.get_full_name()
        self.fields.pop('udi')

class ParticipanteAsignarForm(ParticipanteFormList):
    # class ParticipanteAsignarForm(ParticipanteBaseForm):
    def __init__(self, *args, **kwargs):
        super(ParticipanteAsignarForm, self).__init__(*args, **kwargs)
        """if request.user.groups.filter(name="cyd_capacitador").exists():
            self.fields.pop('capacitador')"""


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
        exclude = ('cyd_asesorias_creado_por',)

class GrupoListForm(forms.Form):
    """Formulario para listar :model:`cyd.Grupo` en una :model:`cyd.Sede`.
    Se usa para copiar los participantes de un grupo a otros.
    """
    grupo = forms.ModelChoiceField(Grupo.objects.all())

class GrupoFilterFormInforme(forms.Form):
    capacitador = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='cyd_capacitador'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2', 'data-url': reverse_lazy('sede_api_list')}))
    sede = forms.ModelChoiceField(
        label='Sede',
        queryset=Sede.objects.filter(activa=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2', 'data-url': reverse_lazy('sede_api_list')}))
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.filter(activo=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2', 'data-url': reverse_lazy('sede_api_list')}))

    def __init__(self, *args, **kwargs):
        super(GrupoFilterFormInforme, self).__init__(*args, **kwargs)
        self.fields['capacitador'].label_from_instance = lambda obj: "%s" % obj.get_full_name()

class ControlAcademicoGrupoForm(forms.Form):

    sede = forms.ModelChoiceField(
        label='Sede',
        queryset=Sede.objects.filter(activa=True),
        required=False,
        widget=forms.Select(attrs={'class': 'select2 form-control', 'data-url': reverse_lazy('grupo_api_list')}))
    
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'select2 form-control', 'data-url': reverse_lazy('asignacion_api_list')}))
    
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        required=False,
        widget = forms.Select(attrs={'class': 'select2 form-control', 'data-url': reverse_lazy('participante_api_list')})
       )
    ESTADO_CHOICES = (
        (0, '----------'),
        (1, 'Simple'),
        (2, 'Completo'),)  
    """escuela = forms.ModelChoiceField(
         queryset=Escuela.objects.all(),
    
         required=False,
         widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('participante_api_list')}))
    """
    """udi = forms.CharField(
        help_text="udi_help",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '13',  'placeholder': '00-00-0000-00', 'data-url': reverse_lazy('escuela_api_list')}))"""

    
    def __init__(self, *args, **kwargs):  
        
        usuario = kwargs.pop('user',None)
        super(ControlAcademicoGrupoForm, self).__init__(*args, **kwargs)         
        if usuario.groups.filter(name="cyd_admin").exists(): 
            self.fields['grupo'] = forms.ModelChoiceField(            
                queryset=Grupo.objects.all(),
                required=False,
                widget = forms.Select(attrs={'class': 'select2 form-control', 'data-url': reverse_lazy('participante_api_list')})
                )
            self.fields['sede'] = forms.ModelChoiceField(
                queryset=Sede.objects.filter(activa=True),             
                required=False,
                widget=forms.Select(attrs={'class': 'select2 form-control', 'data-url': reverse_lazy('grupo_api_list')})
                )
            
            self.fields['curso'] = forms.ModelChoiceField(            
                queryset=Curso.objects.all(),   
                required=False,
                widget=forms.Select(attrs={'class': 'select2 form-control', 'data-url': reverse_lazy('asignacion_api_list')}))
        else:
            self.fields['grupo'] = forms.ModelChoiceField(            
            queryset=Grupo.objects.filter(cyd_grupo_creado_por = usuario),           
            required=False,
            widget = forms.Select(attrs={'class': 'select2 form-control', 'data-url': reverse_lazy('participante_api_list')})
            )
            self.fields['sede'] = forms.ModelChoiceField(
                queryset=Sede.objects.filter(capacitador = usuario, activa=True),                             
                required=False,
                widget=forms.Select(attrs={'class': 'select2 form-control', 'data-url': reverse_lazy('grupo_api_list')})
                )
            
            self.fields['curso'] = forms.ModelChoiceField(
                queryset=Curso.objects.all(), 
                required=False,
                widget=forms.Select(attrs={'class': 'select2 form-control', 'data-url': reverse_lazy('asignacion_api_list')}))
             
            
            
        
        
        
        

class InformeAsistenciaForm(forms.Form):
    #aca toca ahorita la base
    sede = forms.ModelChoiceField(
        label='Sede',
        queryset=Sede.objects.filter(activa=True),
        required=False,
        widget=forms.Select(attrs={'class': 'select2 form-control','data-url': reverse_lazy('grupo_api_list')}))
    curso = forms.ModelChoiceField(
        required=False,
        queryset=Curso.objects.all(),
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('asignacion_api_list')}))
    grupo = forms.ModelChoiceField(
        required=False,
        queryset=Grupo.objects.all(),
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('participante_api_list')}))
    udi = forms.CharField(
        help_text="udi_help",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '13', 'placeholder': '00-00-0000-00', 'data-url': reverse_lazy('escuela_api_list')}))

class InformeAsistenciaFinalForm(forms.Form):
    sede = forms.ModelChoiceField(
        label='Sede',
        queryset=Sede.objects.filter(activa=True),
        required=False,
        widget=forms.Select(attrs={'class': 'select2 form-control','data-url': reverse_lazy('grupo_api_list')}))
    curso = forms.ModelChoiceField(
        required=True,
        queryset=Curso.objects.all(),
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('participante_api_list')}))
    nombre = forms.CharField(
        label='Nombre',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    udi = forms.CharField(
        help_text="udi_help",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '13', 'placeholder': '00-00-0000-00', 'data-url': reverse_lazy('escuela_api_list')}))

class InformeCapacitadorForm(forms.Form):
    capacitador = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='cyd_capacitador'),
        widget=forms.Select(attrs={'class': 'select2 form-control'}),
        required=False
        )
    fecha_min = forms.CharField(
        label='Fecha mínima',
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}),
        required=False)
    fecha_max = forms.CharField(
        label='Fecha máxima',
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}),
        required=False)

    def __init__(self, *args, **kwargs):
        super(InformeCapacitadorForm ,self).__init__(*args, **kwargs)
        self.fields['capacitador'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())

class InformeEscuelaForm(forms.Form):
    escuela__codigo = forms.CharField(
        label='Ingrese el UDI',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

class InformeAsistenciaPeriodoForm(forms.Form):

    sede = forms.ModelChoiceField(
        label='Sede',
        queryset=Sede.objects.filter(activa=True),
        required=False,
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('grupo_api_list')}))
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('calendario_api_list')}))
    asistencia = forms.ModelChoiceField(
        required=True,
        queryset=Calendario.objects.all().distinct(),
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('participante_api_list')}))
    udi = forms.CharField(
        help_text="udi_help",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '13', 'placeholder': '00-00-0000-00', 'data-url': reverse_lazy('escuela_api_list')}))
    def __init__(self, *args, **kwargs):
        super(InformeAsistenciaPeriodoForm,self).__init__(*args, **kwargs)
        self.fields['asistencia'].label_from_instance = lambda obj: "%s" % ("A"+str(obj.cr_asistencia.modulo_num) +"-"+str(obj.fecha) )


class InformeSedeForm(forms.Form):
    sede = forms.ModelChoiceField(
        label='Sede',
        queryset=Sede.objects.filter(activa=True),
        required=False,
        widget=forms.Select(attrs={'class': 'select2 form-control'}))


class InformeEscuelalistadoForm(forms.Form):
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'data-url': reverse_lazy('municipio_api_list')}),
        required=False)
    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False)
    capacitador = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='cyd_capacitador'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))
    fecha_min = forms.CharField(
        label='Fecha mínima',
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}),
        required=False)
    fecha_max = forms.CharField(
        label='Fecha máxima',
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}),
        required=False)
    def __init__(self, *args, **kwargs):
        super(InformeEscuelalistadoForm ,self).__init__(*args, **kwargs)
        self.fields['capacitador'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())



class InformeEscuelaSedeslistadoForm(forms.Form):
    departamento = forms.ModelMultipleChoiceField(
        queryset=Departamento.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2', 'data-url': reverse_lazy('municipio_api_list')}),
        required=False)
    municipio = forms.ModelMultipleChoiceField(
        queryset=Municipio.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        required=False)
    capacitador = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='cyd_capacitador'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))
        
    fecha_min = forms.CharField(
        label='Fecha mínima',
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}),
        required=False)
    fecha_max = forms.CharField(
        label='Fecha máxima',
        widget=forms.TextInput(attrs={'class': 'form-control datepicker'}),
        required=False)
    def __init__(self, *args, **kwargs):
        super(InformeEscuelaSedeslistadoForm ,self).__init__(*args, **kwargs)
        self.fields['capacitador'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())

class InformeAsistenciaWebForm(forms.Form):
    #aca toca modificar
    sede = forms.ModelChoiceField(
        label='Sede',
        queryset=Sede.objects.filter(activa=True),
        required=False,
        widget=forms.Select(attrs={'class': 'select2 form-control','data-url': reverse_lazy('grupo_api_list')}))
    curso = forms.ModelChoiceField(
        required=False,
        queryset=Curso.objects.all(),
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('asignacion_api_list')}))
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('calendario_api_list')}))
    asistencia = forms.ModelChoiceField(
        required=False,
        queryset=Calendario.objects.all().distinct(),
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('participante_api_list')}))
    def __init__(self, *args, **kwargs):
        super(InformeAsistenciaWebForm,self).__init__(*args, **kwargs)
        self.fields['asistencia'].label_from_instance = lambda obj: "%s" % ("A"+str(obj.cr_asistencia.modulo_num) +"-"+str(obj.fecha) )


class AsignacionWebForm(forms.Form):
    sede = forms.ModelChoiceField(
        label='Sede',
        queryset=Sede.objects.filter(activa=True),
        required=False,
        widget=forms.Select(attrs={'class': 'select2 form-control', 'data-url': reverse_lazy('grupo_api_list')}))
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        widget=forms.Select(attrs={'class': 'select2', 'data-url': reverse_lazy('participante_api_list')}))
