from rest_framework import serializers
from django.contrib.auth.models import User
from apps.cyd.models import Grupo, Calendario, Participante


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


class ParticipanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = '__all__'


class CapacitadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
