from datetime import datetime
from rest_framework import serializers

from apps.main.serializers import DynamicFieldsModelSerializer
from apps.tpe import models as tpe_models
from apps.mye import serializers as mye_serializers


class GarantiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = tpe_models.Garantia
        fields = '__all__'


class TicketReparacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = tpe_models.TicketReparacion
        fields = '__all__'


class MonitoreoSerializer(serializers.ModelSerializer):
    creado_por = serializers.SerializerMethodField(read_only=True)
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    fecha = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = tpe_models.Monitoreo
        fields = '__all__'
        read_only_fields = ('creado_por', 'fecha')

    def get_fecha(self, obj):
        return datetime.now()

    def get_creado_por(self, obj):
        return obj.creado_por.get_full_name()


class EvaluacionMonitoreoSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    porcentaje = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = tpe_models.EvaluacionMonitoreo
        fields = '__all__'
        read_only_fields = ('monitoreo', 'pregunta', 'porcentaje')


class EquipamientoSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    entrega_url = serializers.URLField(source='get_absolute_url')
    entrega = serializers.IntegerField(source='id')
    escuela = serializers.StringRelatedField()
    escuela_url = serializers.URLField(source='escuela.get_absolute_url')
    escuela_codigo = serializers.StringRelatedField(source='escuela.codigo')
    renovacion = serializers.SerializerMethodField()
    khan = serializers.SerializerMethodField()
    cantidad = serializers.IntegerField(source='cantidad_equipo')
    tipo_red = serializers.SerializerMethodField()

    cooperante = mye_serializers.CooperanteSerializer(many=True)
    proyecto = mye_serializers.ProyectoSerializer(many=True)

    class Meta:
        model = tpe_models.Equipamiento
        fields = (
            'entrega', 'entrega_url', 'escuela', 'escuela_url',
            'escuela_codigo', 'fecha', 'renovacion', 'khan',
            'cantidad', 'tipo_red', 'cooperante', 'proyecto')

    @staticmethod
    def get_renovacion(obj):
        """

        :str: Texto indicando que es o no renovación
        """
        return 'Sí' if obj.renovacion else 'No'

    @staticmethod
    def get_khan(obj):
        """

        :str: Texto indicando si tiene servidor de Khan
        """
        return 'Sí' if obj.servidor_khan else 'No'

    @staticmethod
    def get_tipo_red(obj):
        return str(obj.tipo_red) if obj.red else 'No'


class EquipamientoFullSerializer(EquipamientoSerializer):
    departamento = serializers.StringRelatedField(source='escuela.municipio.departamento')
    municipio = serializers.StringRelatedField(source='escuela.municipio.nombre')
    direccion = serializers.CharField(source='escuela.direccion')
    alumnas = serializers.IntegerField(source='poblacion.alumna')
    alumnos = serializers.IntegerField(source='poblacion.alumno')
    total_alumnos = serializers.IntegerField(source='poblacion.total_alumno')
    maestras = serializers.IntegerField(source='poblacion.maestra')
    maestros = serializers.IntegerField(source='poblacion.maestro')
    total_maestros = serializers.IntegerField(source='poblacion.total_maestro')

    class Meta:
        model = tpe_models.Equipamiento
        fields = (
            'entrega', 'entrega_url', 'escuela', 'escuela_url', 'escuela_codigo', 'fecha',
            'renovacion', 'khan', 'cantidad', 'tipo_red', 'cooperante', 'proyecto',
            'municipio', 'departamento', 'direccion', 'alumnas', 'alumnos', 'total_alumnos',
            'maestras', 'maestros', 'total_maestros')
