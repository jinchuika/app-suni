from datetime import datetime

from rest_framework import serializers
from django.contrib.auth.models import User

from apps.main import serializers as main_s
from apps.cyd.serializers import ParticipanteSerializer
from apps.cyd.models import Participante
from apps.naat import models as naat_m


class ParticipanteNaatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        exclude = ('slug', 'avatar',)


class AsignacionNaatSerializer(serializers.ModelSerializer):
    participante = ParticipanteNaatSerializer()

    class Meta:
        model = naat_m.AsignacionNaat
        fields = ('participante',)


class ParticipanteAsignadoField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, naat_m.AsignacionNaat):
            serializer = ParticipanteNaatSerializer(value.participante)
            return serializer.data
        else:
            raise Exception('Error al obtener datos')


class FacilitadorNaatSerializer(serializers.ModelSerializer):
    asignados_naat = serializers.SerializerMethodField('get_asignaciones_activas')

    @staticmethod
    def get_asignaciones_activas(obj):
        asignaciones_naat = naat_m.AsignacionNaat.objects.filter(proceso__capacitador=obj, activa=True)
        serializer = AsignacionNaatSerializer(asignaciones_naat, many=True)
        return serializer.data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'asignados_naat')


class SesionCalendarSerializer(main_s.CalendarSerializer):
    title = serializers.StringRelatedField(source='proceso.escuela')
    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()
    tip_title = serializers.StringRelatedField(source='proceso.capacitador.get_full_name')
    tip_text = serializers.SerializerMethodField()
    color = serializers.CharField(source='proceso.capacitador.perfil.color')

    class Meta:
        model = naat_m.SesionPresencial
        fields = ('start', 'end', 'title', 'url', 'tip_title', 'tip_text', 'color')

    @staticmethod
    def get_start(obj):
        if obj.hora_inicio is not None:
            return datetime.combine(obj.fecha, obj.hora_inicio)
        else:
            return obj.fecha

    @staticmethod
    def get_end(obj):
        if obj.hora_fin is not None:
            return datetime.combine(obj.fecha, obj.hora_fin)
        else:
            return obj.fecha

    @staticmethod
    def get_tip_text(obj):
        return '{}'.format(obj.proceso.escuela.municipio)
