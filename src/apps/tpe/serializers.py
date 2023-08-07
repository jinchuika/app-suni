from datetime import datetime
from rest_framework import serializers

from apps.main import serializers as main_s
from apps.tpe import models as tpe_models
from apps.mye import serializers as mye_serializers
from apps.escuela import serializers as escuela_s


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
    creado_por = serializers.StringRelatedField(
        source='monitoreo.creado_por.get_full_name',
        read_only=True)

    class Meta:
        model = tpe_models.EvaluacionMonitoreo
        fields = '__all__'
        read_only_fields = ('monitoreo', 'pregunta', 'porcentaje')


class EvaluacionMonitoreoFullSerializer(EvaluacionMonitoreoSerializer):

    """Serializer para generar informes completos de :class:`EvaluacionMonitoreo`
    """

    pregunta = serializers.StringRelatedField()
    equipamiento = serializers.StringRelatedField(source='monitoreo.equipamiento', read_only=True)
    fecha = serializers.DateField(source='monitoreo.fecha', read_only=True)
    fecha_equipamiento = serializers.DateField(source='monitoreo.equipamiento.fecha', read_only=True)
    escuela = escuela_s.EscuelaSerializer(
        source='monitoreo.equipamiento.escuela',
        fields='id,nombre,codigo',
        read_only=True)


class EquipamientoSerializer(main_s.DynamicFieldsModelSerializer, serializers.ModelSerializer):
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
    alumnas = serializers.IntegerField(source='poblacion.alumna', default=None)
    alumnos = serializers.IntegerField(source='poblacion.alumno', default=None)
    total_alumnos = serializers.IntegerField(source='poblacion.total_alumno', default=None)
    maestras = serializers.IntegerField(source='poblacion.maestra', default=None)
    maestros = serializers.IntegerField(source='poblacion.maestro', default=None)
    total_maestros = serializers.IntegerField(source='poblacion.total_maestro', default=None)
    longitud =  serializers.StringRelatedField(source='escuela.mapa.lng')
    latitud = serializers.StringRelatedField(source='escuela.mapa.lat')
    nivel = serializers.StringRelatedField(source='escuela.nivel.nivel')
    sector = serializers.StringRelatedField(source='escuela.sector.sector')
    
    class Meta:
        model = tpe_models.Equipamiento
        fields = (
            'entrega', 'entrega_url', 'escuela', 'escuela_url', 'escuela_codigo', 'fecha',
            'renovacion', 'khan', 'cantidad', 'tipo_red', 'cooperante', 'proyecto',
            'municipio', 'departamento', 'direccion', 'alumnas', 'alumnos', 'total_alumnos',
            'maestras', 'maestros', 'total_maestros', 'longitud', 'latitud','nivel', 'sector' )


class EquipamientoCalendarSerializer(main_s.CalendarSerializer):
    tip_title = serializers.CharField(source='escuela.municipio')
    tip_text = serializers.CharField(source='escuela.direccion')

    class Meta:
        model = tpe_models.Equipamiento
        fields = ('start', 'title', 'url', 'tip_text', 'tip_title')


class DispositivoTipoSerializer(main_s.DynamicFieldsModelSerializer):

    """Serializer para :class:`DispositivoTipo`.
    Usado de forma interna, por ahora no tiene vista ni endpoint expuesto
    """

    class Meta:
        model = tpe_models.DispositivoTipo
        fields = '__all__'


class DispositivoReparacionSerializar(serializers.ModelSerializer):

    """Para listar la cantidad de :class:`TicketReparacion`es por cada
    :class:`DispositivoTipo`.
    """

    total = serializers.IntegerField()
    tipo = serializers.CharField(source='tipo_dispositivo__tipo')
    tipo_id = serializers.IntegerField(source='tipo_dispositivo')

    class Meta:
        model = tpe_models.TicketReparacion
        fields = ('tipo_id', 'tipo', 'total')


class VisitaMonitoreoCalendarSerializer(serializers.ModelSerializer):
    """ Serializer para :class:`VisitaMonitoreo` encargada de mostrar los datos
    con DRF para el calendario de visitas
    """
    url = serializers.URLField(source='get_absolute_url')
    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()
    title = serializers.CharField(source='equipamiento.escuela')
    tip_title = serializers.CharField(source='equipamiento.escuela.municipio')
    tip_text = serializers.CharField(source='equipamiento.escuela.direccion')
    color = serializers.CharField(source='encargado.perfil.color')

    class Meta:
        model = tpe_models.VisitaMonitoreo
        fields = ('start', 'end', 'url', 'title', 'tip_title', 'tip_text', 'color')

    def get_start(self, object):
        if object.hora_inicio is not None:
            return datetime.combine(object.fecha_visita, object.hora_inicio)
        else:
            return object.fecha_visita

    def get_end(self, object):
        if object.hora_final is not None:
            return datetime.combine(object.fecha_visita, object.hora_final)
        else:
            return object.fecha_visita


class VisitaMonitoreoSerializer(serializers.ModelSerializer):
    """ Serializer para :class:`VisitaMonitoreo` encargada de mostrar los datos
    con DRF para los informes que se necesita
    """
    id = serializers.IntegerField(source='__str__')
    urlequipamiento = serializers.URLField(source='equipamiento.get_absolute_url')
    urlvisita = serializers.URLField(source='get_absolute_url')
    urlescuela = serializers.URLField(source='equipamiento.escuela.get_absolute_url')
    equipamientos = serializers.StringRelatedField(source='equipamiento', read_only=True)
    municipio = serializers.CharField(source='equipamiento.escuela.municipio.nombre')
    escuela = serializers.CharField(source='equipamiento.escuela')
    departamento = serializers.StringRelatedField(source='equipamiento.escuela.municipio.departamento.nombre')
    fecha = serializers.SerializerMethodField()
    encargado = serializers.SerializerMethodField()

    class Meta:
        model = tpe_models.VisitaMonitoreo
        fields = (
                'id',
                'urlvisita',
                'urlescuela',
                'urlequipamiento',
                'equipamientos',
                'escuela',
                'fecha',
                'departamento',
                'municipio',
                'encargado'
                )

    def get_fecha(self, object):
        return object.fecha_visita

    def get_encargado(self, obj):
        return obj.encargado.get_full_name()


class EquipamientoMapaSerializer(serializers.ModelSerializer):
    escuela = serializers.StringRelatedField()
    coordenadas = main_s.CoordenadaSerializer(fields='lat,lng', source='escuela.mapa')
    cooperante = mye_serializers.CooperanteSerializer(many=True, fields='nombre')
    proyecto = mye_serializers.ProyectoSerializer(many=True, fields='nombre')
    municipio = serializers.StringRelatedField(source='escuela.municipio')
    departamento = serializers.StringRelatedField(source='escuela.municipio.departamento')
    poblacion = escuela_s.EscPoblacionSerializer(fields='total_alumno,total_maestro')

    class Meta:
        model = tpe_models.Equipamiento
        fields = ('poblacion', 'fecha', 'escuela', 'cooperante', 'proyecto', 'coordenadas', 'municipio', 'departamento',)
