from rest_framework import serializers

from apps.main.serializers import CalendarSerializer, DynamicFieldsModelSerializer
from apps.escuela.serializers import EscuelaSerializer
from apps.mye import models as mye_m


class CooperanteSerializer(DynamicFieldsModelSerializer):
    url = serializers.URLField(source='get_absolute_url')
    cantidad_equipamientos = serializers.SerializerMethodField(read_only=True)
    cantidad_computadoras = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = mye_m.Cooperante
        fields = '__all__'

    def get_cantidad_equipamientos(self, obj):
        return obj.equipamientos.count()

    def get_cantidad_computadoras(self, obj):
        return sum(e.cantidad_equipo for e in obj.equipamientos.all())


class ProyectoSerializer(DynamicFieldsModelSerializer):
    url = serializers.URLField(source='get_absolute_url')
    cantidad_equipamientos = serializers.IntegerField(read_only=True)

    class Meta:
        model = mye_m.Proyecto
        fields = '__all__'


class ValidacionCalendarSerializer(CalendarSerializer):
    start = serializers.DateField(source='fecha_equipamiento')
    tip_title = serializers.StringRelatedField(source='escuela.municipio')
    tip_text = serializers.StringRelatedField(source='escuela.direccion')

    class Meta:
        model = mye_m.Validacion
        fields = ('start', 'title', 'url', 'tip_title', 'tip_text')


class SolicitudComentarioSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = mye_m.SolicitudComentario
        fields = '__all__'


class SolicitudSerializer(serializers.ModelSerializer):
    departamento = serializers.StringRelatedField(source='escuela.municipio.departamento')
    municipio = serializers.StringRelatedField(source='escuela.municipio.nombre')
    escuela = EscuelaSerializer(fields='nombre,codigo,url')
    requisitos = serializers.StringRelatedField(source='porcentaje_requisitos')
    alumnos = serializers.IntegerField(source='poblacion.total_alumno')
    maestros = serializers.IntegerField(source='poblacion.total_maestro')
    equipada = serializers.BooleanField(source='escuela.equipada')
    comentarios_solicitud = SolicitudComentarioSerializer(many=True, fields='comentario')

    class Meta:
        model = mye_m.Solicitud
        fields = (
            'departamento',
            'municipio',
            'escuela',
            'requisitos',
            'alumnos',
            'maestros',
            'equipada',
            'fecha',
            'comentarios_solicitud')


class ValidacionComentarioSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = mye_m.ValidacionComentario
        fields = '__all__'


class ValidacionSerializer(serializers.ModelSerializer):

    """Serializer para generar un API endpoint hacie el modelo de
    :class:`Validacion`.
    """

    departamento = serializers.StringRelatedField(source='escuela.municipio.departamento')
    municipio = serializers.StringRelatedField(source='escuela.municipio.nombre')
    escuela = EscuelaSerializer(fields='nombre,codigo,url')
    requisitos = serializers.StringRelatedField(source='porcentaje_requisitos')
    estado = serializers.SerializerMethodField()
    fecha = serializers.DateField(source='fecha_inicio')
    comentarios = ValidacionComentarioSerializer(many=True, fields='comentario')
    observacion = serializers.StringRelatedField()

    class Meta:
        model = mye_m.Validacion
        fields = (
            'departamento', 'municipio', 'escuela', 'requisitos',
            'estado', 'fecha', 'fecha_equipamiento', 'comentarios', 'observacion')

    def get_estado(self, obj):
        """Devuelve un texto indicando si la :class:`Validacion`
        está completa o no.
        """
        return 'Completa' if obj.completada is True else 'Pendiente'
