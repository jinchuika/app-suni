from datetime import datetime
from rest_framework import serializers
from apps.main.serializers import DynamicFieldsModelSerializer
from apps.escuela.serializers import EscuelaSerializer

from apps.kalite.models import Punteo, Evaluacion, Visita, Grado, EjerciciosGrado


class PunteoSerializer(DynamicFieldsModelSerializer):
    multiplicador = serializers.IntegerField(read_only=True)

    class Meta:
        model = Punteo
        fields = '__all__'
        read_only_fields = ('id', 'evaluacion', 'indicador', 'multiplicador')


class EvaluacionSerializer(DynamicFieldsModelSerializer):
    promedio = serializers.FloatField(read_only=True)

    class Meta:
        model = Evaluacion
        fields = '__all__'
        read_only_fields = ('id', 'visita', 'rubrica')


class VisitaSerializer(DynamicFieldsModelSerializer):
    promedio = serializers.FloatField(read_only=True)
    alcance = serializers.CharField(source='estado.alcance')
    escuela = EscuelaSerializer(fields='nombre,url,codigo')
    capacitador = serializers.StringRelatedField(source='capacitador.get_full_name')
    tipo_visita = serializers.StringRelatedField()
    municipio = serializers.StringRelatedField(source='escuela.municipio.nombre')
    departamento = serializers.StringRelatedField(source='escuela.municipio.departamento')

    class Meta:
        model = Visita
        fields = '__all__'
        read_only_fields = ('id', 'escuela')


class VisitaCalendarSerializer(DynamicFieldsModelSerializer):
    url = serializers.URLField(source='get_absolute_url')
    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()
    title = serializers.CharField(source='escuela')
    tip_title = serializers.SerializerMethodField()
    tip_text = serializers.SerializerMethodField()
    color = serializers.CharField(source='capacitador.perfil.color')

    class Meta:
        model = Visita
        fields = ('id', 'start', 'end', 'url', 'title', 'tip_title', 'tip_text', 'color')

    def get_start(self, object):
        if object.hora_inicio is not None:
            return datetime.combine(object.fecha, object.hora_inicio)
        else:
            return object.fecha

    def get_end(self, object):
        if object.hora_fin is not None:
            return datetime.combine(object.fecha, object.hora_fin)
        else:
            return object.fecha

    def get_tip_title(self, object):
        return 'Visita {} - {}'.format(object.numero, object.capacitador.get_full_name())

    def get_tip_text(self, object):
        return str(object.escuela.municipio)


class EjerciciosGradoSerializer(DynamicFieldsModelSerializer):
    url = serializers.CharField(source='get_api_url', read_only=True)
    grado_url = serializers.CharField(source='grado.get_api_url', read_only=True)

    class Meta:
        model = EjerciciosGrado
        fields = '__all__'


class GradoSerializer(DynamicFieldsModelSerializer):
    url = serializers.CharField(source='get_api_url', read_only=True)
    alcanzados = serializers.IntegerField()
    nivelar = serializers.IntegerField(read_only=True)
    total_estudiantes = serializers.IntegerField()
    total_ejercicios = serializers.IntegerField()
    promedio_ejercicios = serializers.FloatField(read_only=True)
    promedio_alcanzados = serializers.FloatField(read_only=True)

    class Meta:
        model = Grado
        fields = '__all__'
