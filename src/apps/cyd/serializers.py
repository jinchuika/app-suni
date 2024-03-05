from datetime import datetime
from rest_framework import serializers
from django.contrib.auth.models import User
from apps.main.serializers import DynamicFieldsModelSerializer
from apps.cyd.models import (
    Sede, Grupo, Calendario, Participante,
    NotaAsistencia, NotaHito, Asignacion,
    ParRol, Asesoria, RecordatorioCalendario )
from apps.escuela.serializers import EscuelaSerializer


class CalendarioSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    cr_asistencia = serializers.SlugRelatedField(read_only=True, slug_field='modulo_num')
    curso = serializers.StringRelatedField(source="__str__")
    asistentes = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField('get_api_url')
    fecha_fin=serializers.SerializerMethodField()

    class Meta:
        model = Calendario
        fields = '__all__'

    def get_api_url(self, calendario):
        return calendario.get_api_url()

    def get_asistentes(self, calendario):
        return calendario.count_asistentes()

    def get_fecha_fin(self,calendario):
        fecha_nueva=Calendario.objects.filter(grupo=calendario.grupo).values('fecha').last()
        return fecha_nueva


class EscuelaCalendarioSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    cr_asistencia = serializers.SlugRelatedField(read_only=True, slug_field='modulo_num')
    asistentes = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField('get_api_url')
    participantes=serializers.SerializerMethodField()
    escuela=serializers.SerializerMethodField()

    class Meta:
        model = Calendario
        fields = '__all__'

    def get_api_url(self, calendario):
        return calendario.get_api_url()

    def get_asistentes(self, calendario):
        return calendario.count_asistentes()

    def get_participantes(self, obj, pk=None):        
        asignacion= Asignacion.objects.filter(grupo=obj.grupo)        
        return asignacion.values('participante').count()

    def get_escuela(self, obj, pk=None):
        asignacion= Asignacion.objects.filter(grupo=obj.grupo)
        return asignacion.values('participante','participante__genero__id','participante__escuela__nombre','grupo__sede__capacitador')


class GrupoSerializer(serializers.ModelSerializer):
    sede = serializers.StringRelatedField()
    curso = serializers.StringRelatedField()
    curso_id = serializers.StringRelatedField(source="curso.id")
    asistencias = serializers.IntegerField(source="asignados.count", read_only=True)
    capacitador = serializers.StringRelatedField(source="cyd_grupo_creado_por.get_full_name")
    urlgrupo = serializers.StringRelatedField(source ="get_absolute_url")
    urlsede = serializers.StringRelatedField(source ="sede.get_absolute_url")
    fecha_creacion = serializers.DateTimeField(source= "sede.fecha_creacion", format='%Y')


    class Meta:
        model = Grupo
        fields = ('id', 'sede', 'numero', 'curso','curso_id' ,'asistencias', 'comentario','capacitador','urlgrupo', 'urlsede', 'fecha_creacion')


class SedeSerializer(serializers.ModelSerializer):
    escuela = serializers.StringRelatedField(source='escuela_beneficiada.codigo')
    urlescuela = serializers.StringRelatedField(source='escuela_beneficiada.get_absolute_url')
    municipio= serializers.StringRelatedField(source='municipio.nombre')
    departamento = serializers.StringRelatedField(source='municipio.departamento')
    capacitador = serializers.StringRelatedField(source='capacitador.get_full_name')
    grupos = serializers.StringRelatedField(source='grupos.count')
    urlsede=serializers.StringRelatedField(source='get_absolute_url')
    fecha_creacion = serializers.DateTimeField(format='%Y')

    class Meta:
        model = Sede
        fields = '__all__'


class AsesoriaSerializer(serializers.ModelSerializer):
    """Para crear y listar periodos de :model:`cyd.Asesoria`."""
    url = serializers.HyperlinkedIdentityField(view_name='asesoria_api_detail', lookup_field='pk')
    #cyd_asesoria_creado_por = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Asesoria
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'asesoria_api_detail', 'lookup_field': 'id'},
        }


class AsesoriaCalendarSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    """Para listar periodos de :model:`cyd.Asesoria` y mostrarlos
    en el calendario general de capacitación."""

    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()
    title = serializers.CharField(source='sede.capacitador.get_full_name')
    tip_title = serializers.SerializerMethodField()
    tip_text = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    #color = serializers.CharField(source='sede.capacitador.perfil.color')
    #color_asesoria = serializers.SerializerMethodField()

    class Meta:
        model = Asesoria
        fields = ('id', 'start', 'end', 'title', 'tip_title', 'tip_text', 'color')

    def get_start(self, object):
        return datetime.combine(object.fecha, object.hora_inicio)

    def get_end(self, object):
        return datetime.combine(object.fecha, object.hora_fin)

    def get_tip_title(self, object):
        return 'Asesoría - {}'.format(object.sede)

    def get_tip_text(self, object):
        return str(object.sede.municipio)
    
    def get_color(self, object):
        return "#FFA500"


class AsignacionResumenSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    grupo = serializers.StringRelatedField()

    class Meta:
        model = Asignacion
        fields = ['grupo']


class ParticipanteSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url')
    escuela = EscuelaSerializer(read_only=True, fields='codigo,nombre,url')
    asignaciones = AsignacionResumenSerializer(read_only=True, many=True)
    genero_nombre =serializers.StringRelatedField(source='genero.genero') 
    etnia=serializers.StringRelatedField(source='etnia.nombre')
    escolaridad = serializers.StringRelatedField(source ='escolaridad.nombre') 
    rol_nombre = serializers.StringRelatedField(source='rol.nombre')    
    profesion_nombre = serializers.StringRelatedField(source='profesion.nombre')  
    grado_impartido_nombre = serializers.StringRelatedField(source='grado_impartido.grado_asignado')       


    class Meta:
        model = Participante
        fields = '__all__'
        extra_kwargs = {'dpi': {'required': 'True'}}


class CapacitadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class NotaAsistenciaSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotaAsistencia
        exclude = ('asignacion',)

    def update(self, instance, validated_data):
        if validated_data['nota'] <= instance.gr_calendario.cr_asistencia.punteo_max:
            instance.save()
        else:
            raise serializers.ValidationError(
                {'nota': ['La nota no puede exceder el punteo máximo ({}).'.format(
                    instance.gr_calendario.cr_asistencia.punteo_max)]})
        return super(NotaAsistenciaSerializer, self).update(instance, validated_data)


class NotaHitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaHito
        exclude = ('asignacion',)

    def update(self, instance, validated_data):
        if validated_data['nota'] <= instance.cr_hito.punteo_max:
            instance.save()
        else:
            print("No valido")
            raise serializers.ValidationError(
                {'nota': ['La nota no puede exceder el punteo máximo ({}).'.format(
                    instance.cr_hito.punteo_max)]})
        return super(NotaHitoSerializer, self).update(instance, validated_data)


class AsignacionSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    """Serializer de uso general para :model:`cyd.Asignacion`."""
    #notas_asistencias = NotaAsistenciaSerializer(many=True, read_only=True)
    #notas_hitos = NotaHitoSerializer(many=True, read_only=True)
    curso=serializers.StringRelatedField(source='grupo.curso')
    sede=serializers.StringRelatedField(source='grupo.sede')
    sede_id=serializers.StringRelatedField(source='grupo.sede.id')
    grupo_nombre=serializers.StringRelatedField(source='grupo')
    class Meta:
        model = Asignacion
        fields = '__all__'


class ParRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParRol
        fields = '__all__'

class RecordatorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordatorioCalendario
        fields = '__all__'
