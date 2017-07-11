from rest_framework import serializers
from django.contrib.auth.models import User
from apps.main.serializers import DynamicFieldsModelSerializer
from apps.cyd.models import (
    Sede, Grupo, Calendario, Participante,
    NotaAsistencia, NotaHito, Asignacion)
from apps.escuela.serializers import EscuelaSerializer


class CalendarioSerializer(serializers.ModelSerializer):
    cr_asistencia = serializers.SlugRelatedField(read_only=True, slug_field='modulo_num')
    url = serializers.SerializerMethodField('get_api_url')

    class Meta:
        model = Calendario
        fields = '__all__'

    def get_api_url(self, calendario):
        return calendario.get_api_url()


class GrupoSerializer(serializers.ModelSerializer):
    sede = serializers.StringRelatedField()
    curso = serializers.StringRelatedField()
    asistencias = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Grupo
        fields = ('id', 'sede', 'numero', 'curso', 'asistencias')


class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = '__all__'


class ParticipanteSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    escuela = EscuelaSerializer(read_only=True, fields='codigo,nombre,url')

    class Meta:
        model = Participante
        fields = '__all__'


class CapacitadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class NotaAsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaAsistencia
        exclude = ('asignacion',)


class NotaHitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaHito
        exclude = ('asignacion',)


class AsignacionSerializer(serializers.ModelSerializer):
    notas_asistencias = NotaAsistenciaSerializer(many=True, read_only=True)
    notas_hitos = NotaHitoSerializer(many=True, read_only=True)

    class Meta:
        model = Asignacion
        fields = ('id', 'grupo', 'participante', 'notas_asistencias', 'notas_hitos')
