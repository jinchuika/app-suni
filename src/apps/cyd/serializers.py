from rest_framework import serializers
from django.contrib.auth.models import User
from apps.cyd.models import Grupo, Calendario, Participante


class CalendarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendario
        fields = '__all__'


class GrupoSerializer(serializers.ModelSerializer):
    sede = serializers.StringRelatedField()
    asistencias = CalendarioSerializer(many=True, read_only=True)

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
