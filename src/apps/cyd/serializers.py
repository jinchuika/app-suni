from rest_framework import serializers
from django.contrib.auth.models import User
from apps.main.serializers import DynamicFieldsModelSerializer
from apps.cyd.models import (
    Sede, Grupo, Calendario, Participante,
    NotaAsistencia, NotaHito, Asignacion,
    ParRol)
from apps.escuela.serializers import EscuelaSerializer


class CalendarioSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    cr_asistencia = serializers.SlugRelatedField(read_only=True, slug_field='modulo_num')
    asistentes = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField('get_api_url')

    class Meta:
        model = Calendario
        fields = '__all__'

    def get_api_url(self, calendario):
        return calendario.get_api_url()

    def get_asistentes(self, calendario):
        return calendario.count_asistentes()


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
    notas_asistencias = NotaAsistenciaSerializer(many=True, read_only=True)
    notas_hitos = NotaHitoSerializer(many=True, read_only=True)

    class Meta:
        model = Asignacion
        fields = ('id', 'grupo', 'participante', 'notas_asistencias', 'notas_hitos', 'nota_final', 'aprobado')


class ParRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParRol
        fields = '__all__'
