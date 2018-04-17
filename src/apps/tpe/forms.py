from django import forms
from django.urls import reverse_lazy
from django.forms import ModelForm
from django.db.models import Count
from apps.main.models import Departamento, Municipio
from django.contrib.auth.models import User

from apps.tpe import models as tpe_m
from apps.mye import models as mye_m
from apps.escuela import models as escuela_m
from apps.users.models import Perfil
from apps.escuela.forms import EscuelaBuscarForm


class EquipamientoNuevoForm(forms.ModelForm):
    class Meta:
        model = tpe_m.Equipamiento
        fields = ('id', 'escuela')
        labels = {
            'id': 'Número de entrega'}
        widgets = {
            'id': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
            'escuela': forms.HiddenInput()}


class EquipamientoForm(ModelForm):
    class Meta:
        model = tpe_m.Equipamiento
        fields = '__all__'
        exclude = ('id',)
        widgets = {
            'escuela': forms.HiddenInput(),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.TextInput(attrs={'class': 'form-control datepicker'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control'}),
            'cooperante': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'proyecto': forms.SelectMultiple(attrs={'class': 'form-control select2'})}

    def __init__(self, *args, **kwargs):
        super(EquipamientoForm, self).__init__(*args, **kwargs)
        if 'poblacion' in self.initial:
            self.fields['poblacion'].queryset = escuela_m.EscPoblacion.objects.filter(escuela=self.initial['escuela'])
        self.fields['poblacion'].label_from_instance = lambda obj: "%s (%s)" % (obj.fecha, obj.total_alumno)


class GarantiaForm(forms.ModelForm):
    class Meta:
        model = tpe_m.Garantia
        fields = '__all__'
        exclude = ('id', )
        widgets = {
            'equipamiento': forms.Select(attrs={'class': 'form-control select2'}),
            'fecha_vencimiento': forms.TextInput(attrs={'class': 'form-control datepicker'})
        }

    def __init__(self, *args, **kwargs):
        """
        Filtra el campo de `equipamiento` para que mostrar solo los que no tienen una :class:`Garantia`
        """
        super(GarantiaForm, self).__init__(*args, **kwargs)
        qs = self.fields['equipamiento'].queryset
        qs = qs.annotate(num_garantias=Count('garantias')).filter(num_garantias__lt=1)
        self.fields['equipamiento'].queryset = qs


class TicketSoporteForm(forms.ModelForm):
    class Meta:
        model = tpe_m.TicketSoporte
        fields = ('garantia', 'descripcion', 'contacto_reporta')
        widgets = {
            'garantia': forms.HiddenInput(),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TicketSoporteForm, self).__init__(*args, **kwargs)
        garantia = self.initial.get('garantia', None)
        if garantia is not None:
            contacto_qs = escuela_m.EscContacto.objects.filter(escuela=garantia.equipamiento.escuela)
            self.fields['contacto_reporta'].queryset = contacto_qs
        self.fields['contacto_reporta'].label_from_instance = lambda obj: "%s (%s)" % (str(obj), obj.telefono.first())


class TicketCierreForm(forms.ModelForm):
    class Meta:
        model = tpe_m.TicketSoporte
        fields = ('cerrado',)
        widgets = {
            'cerrado': forms.HiddenInput()
        }


class TicketRegistroForm(forms.ModelForm):
    class Meta:
        model = tpe_m.TicketRegistro
        fields = ('tipo', 'descripcion', 'foto')
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'foto': forms.URLInput(attrs={'class': 'form-control'}),
        }


class TicketRegistroUpdateForm(forms.ModelForm):
    class Meta:
        model = tpe_m.TicketRegistro
        fields = ('foto', )
        widgets = {
            'foto': forms.URLInput(attrs={'class': 'form-control'}),
        }


class TicketReparacionForm(forms.ModelForm):
    class Meta:
        model = tpe_m.TicketReparacion
        fields = ('triage', 'tipo_dispositivo', 'falla_reportada', 'tecnico_asignado')

    def __init__(self, *args, **kwargs):
        super(TicketReparacionForm, self).__init__(*args, **kwargs)
        self.fields['tecnico_asignado'].queryset = User.objects.filter(groups__name='tpe_tecnico')
        self.fields['tecnico_asignado'].label_from_instance = lambda obj: "%s" % obj.get_full_name()


class TicketReparacionListForm(forms.ModelForm):
    class Meta:
        model = tpe_m.TicketReparacion
        fields = ('estado', 'tecnico_asignado')

    def __init__(self, *args, **kwargs):
        super(TicketReparacionListForm, self).__init__(*args, **kwargs)
        self.fields['estado'].required = False
        self.fields['tecnico_asignado'].queryset = Perfil.objects.filter(
            user__in=tpe_m.TicketReparacion.objects.values('tecnico_asignado').distinct()
            )
        self.fields['tecnico_asignado'].required = False


class TicketReparacionUpdateForm(forms.ModelForm):
    class Meta:
        model = tpe_m.TicketReparacion
        fields = ('falla_encontrada', 'solucion_tipo', 'solucion_detalle')
        widgets = {
            'falla_encontrada': forms.Textarea(attrs={'class': 'form-control'}),
            'solucion_tipo': forms.Select(attrs={'class': 'form-control'}),
            'solucion_detalle': forms.Textarea(attrs={'class': 'form-control'}),
        }


class TicketReparacionRepuestoForm(forms.ModelForm):
    class Meta:
        model = tpe_m.TicketReparacionRepuesto
        fields = ('reparacion', 'tipo_dispositivo', 'costo', 'justificacion')
        widgets = {
            'reparacion': forms.HiddenInput(),
            'tipo_dispositivo': forms.Select(attrs={'class': 'form-control select2'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control'})
        }


class TicketReparacionRepuestoAuthForm(forms.ModelForm):
    class Meta:
        model = tpe_m.TicketReparacionRepuesto
        fields = ('autorizado', 'rechazado')
        widgets = {
            'autorizado': forms.HiddenInput(),
            'rechazado': forms.HiddenInput(),
        }


class TicketTransporteForm(forms.ModelForm):
    class Meta:
        model = tpe_m.TicketTransporte
        fields = '__all__'
        exclude = ('ticket', 'fecha')
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.0'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TicketTransporteForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].label_from_instance = lambda obj: "%s" % obj.get_full_name()


class EquipamientoListForm(EscuelaBuscarForm):
    ESTADO_CHOICES = (
        (None, 'No importa'),
        (False, 'No'),
        (True, 'Sí'),)
    nombre = forms.CharField(
        widget=forms.TextInput(),
        required=False)
    fecha_min = forms.CharField(
        label='Fecha mínima',
        widget=forms.TextInput(attrs={'class': 'datepicker'}),
        required=False)
    fecha_max = forms.CharField(
        label='Fecha máxima',
        widget=forms.TextInput(attrs={'class': 'datepicker'}),
        required=False)
    cooperante = forms.ModelChoiceField(
        label='Cooperante de equipamiento',
        queryset=mye_m.Cooperante.objects.all(),
        required=False)
    proyecto = forms.ModelChoiceField(
        label='Proyecto de equipamiento',
        queryset=mye_m.Proyecto.objects.all(),
        required=False)
    renovacion = forms.ChoiceField(
        label='Renovación',
        required=False,
        choices=ESTADO_CHOICES)

    def __init__(self, *args, **kwargs):
        super(EquipamientoListForm, self).__init__(*args, **kwargs)
        self.fields.pop('cooperante_tpe')
        self.fields.pop('proyecto_tpe')
        self.fields.pop('sector')
        self.fields.pop('poblacion_min')
        self.fields.pop('poblacion_max')
        self.fields.pop('validacion')
        self.fields.pop('validacion_id')
        self.fields.pop('solicitud')
        self.fields.pop('solicitud_id')
        self.fields.pop('equipamiento')


class MonitoreoListForm(forms.Form):
    usuario = forms.ModelChoiceField(
        label='Usuario',
        required=False,
        queryset=Perfil.objects.filter(user__in=tpe_m.Monitoreo.objects.values('creado_por').distinct()))
    fecha_min = forms.CharField(
        label='Fecha mínima',
        widget=forms.TextInput(attrs={'class': 'datepicker'}),
        required=False)
    fecha_max = forms.CharField(
        label='Fecha máxima',
        widget=forms.TextInput(attrs={'class': 'datepicker'}),
        required=False)


class TicketInformeForm(forms.Form):
    ESTADO_CHOICES = (
        (None, 'No importa'),
        (False, 'Abierto'),
        (True, 'Cerrado'),)
    estado = forms.ChoiceField(
        label='Estado',
        required=False,
        choices=ESTADO_CHOICES)
    fecha_abierto_min = forms.CharField(
        label='Fecha de inicio mínima',
        widget=forms.TextInput(attrs={'class': 'datepicker', 'placeholder': 'Cuándo se abrió el ticket'}),
        required=False)
    fecha_abierto_max = forms.CharField(
        label='Fecha de inicio máxima',
        widget=forms.TextInput(attrs={'class': 'datepicker', 'placeholder': 'Cuándo se abrió el ticket'}),
        required=False)
    fecha_cierre_min = forms.CharField(
        label='Fecha de cierre mínima',
        widget=forms.TextInput(attrs={'class': 'datepicker', 'placeholder': 'Cuándo se cerró el ticket'}),
        required=False)
    fecha_cierre_max = forms.CharField(
        label='Fecha de cierre máxima',
        widget=forms.TextInput(attrs={'class': 'datepicker', 'placeholder': 'Cuándo se cerró el ticket'}),
        required=False)


class TicketReparacionInformeForm(forms.Form):
    estado = forms.ModelChoiceField(
        label='Estado',
        required=False,
        queryset=tpe_m.TicketReparacionEstado.objects.all())
    ticket = forms.ModelChoiceField(
        label='Ticket',
        widget=forms.Select(attrs={'class': 'select2'}),
        required=False,
        queryset=tpe_m.TicketSoporte.objects.all())
    tipo_dispositivo = forms.ModelChoiceField(
        label='Tipo de dispositivo',
        widget=forms.Select(attrs={'class': 'select2'}),
        required=False,
        queryset=tpe_m.DispositivoTipo.objects.all())
    triage = forms.CharField(
        required=False)
    tecnico_asignado = forms.ModelChoiceField(
        label='Técnico asignado',
        queryset=User.objects.filter(groups__name='tpe_tecnico'),
        required=False)

    def __init__(self, *args, **kwargs):
        super(TicketReparacionInformeForm, self).__init__(*args, **kwargs)
        self.fields['tecnico_asignado'].label_from_instance = lambda obj: "%s" % obj.get_full_name()


class EvaluacionMonitoreoCreateForm(forms.ModelForm):

    """Este formulario se encarga de enviar la id del :model:`tpe.Monitoreo`
    para crear las :model:`tpe.EvaluacionMonitoreo` correspondientes.
    """

    evaluacion = forms.BooleanField(
        widget=forms.HiddenInput())

    class Meta:
        model = tpe_m.Monitoreo
        fields = ('id',)
        widgets = {
            'id': forms.HiddenInput()
        }


class EvaluacionMonitoreoForm(forms.ModelForm):
    class Meta:
        model = tpe_m.EvaluacionMonitoreo
        fields = '__all__'
        widgets = {
            'monitoreo': forms.HiddenInput(),
            'pregunta': forms.HiddenInput()
        }


class DispositivoReparacionListForm(forms.Form):
    TECNICOS_REPARACION = tpe_m.TicketReparacion.objects.values('tecnico_asignado').distinct()

    usuario = forms.ModelChoiceField(
        label='Técnico',
        required=False,
        queryset=User.objects.filter(id__in=TECNICOS_REPARACION))
    fecha_min = forms.CharField(
        label='Fecha mínima',
        widget=forms.TextInput(attrs={'class': 'datepicker'}),
        required=False)
    fecha_max = forms.CharField(
        label='Fecha máxima',
        widget=forms.TextInput(attrs={'class': 'datepicker'}),
        required=False)

    def __init__(self, *args, **kwargs):
        super(DispositivoReparacionListForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())


class VisitaMonitoreoCreateForm(forms.ModelForm):
    """ Aca se crea los campos que necesitemos que se miren cuando  incluimos el  en template
    el formulario
    """
    class Meta:
        model = tpe_m.VisitaMonitoreo
        fields = ('equipamiento',)


class VisitaMonitoreoForm(forms.ModelForm):
    """Este Formulario se encarga  de enviar la id de la class:'VisitaMonitoreo'
    para crear  los campos a mostrar en el template  visita_add
    """
    class Meta:
        model = tpe_m.VisitaMonitoreo
        fields = '__all__'
        exclude = ('equipamiento', 'encargado',)
        widgets = {
            'fecha_visita': forms.TextInput(attrs={'class': 'datepicker'}),
            'otras_personas': forms.SelectMultiple(attrs={'class': 'select2'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(VisitaMonitoreoForm, self).__init__(*args, **kwargs)
        qs_actual = self.fields['ticket'].queryset
        qs_nuevo = qs_actual.filter(garantia__equipamiento=self.instance.equipamiento)
        self.fields['ticket'].queryset = qs_nuevo

        qs_actual_contacto = self.fields['contacto'].queryset
        qs_nuevo_contacto = qs_actual_contacto.filter(escuela=self.instance.equipamiento.escuela)
        self.fields['contacto'].queryset = qs_nuevo_contacto
        self.fields['otras_personas'].label_from_instance = lambda obj: "%s" % obj.get_full_name()


class VisitaMonitoreoInformeForm(forms.Form):
    """Este Formulario se encarga de enviar los filtros para  su respectivo informe de visitas de monitoreo
    """
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'data-url': reverse_lazy('municipio_api_list')}),
        required=False)
    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False)
    encargado = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='Encargado',
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

    def __init__(self, *args, **kwargs):
        super(VisitaMonitoreoInformeForm, self).__init__(*args, **kwargs)
        qs_encargado = self.fields['encargado'].queryset
        qs_encargado = qs_encargado.annotate(total_visitas=Count('visitas_encargado')).filter(total_visitas__gte=1)
        self.fields['encargado'].queryset = qs_encargado
        self.fields['encargado'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())
