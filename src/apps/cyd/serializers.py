from rest_framework import serializers
from apps.cyd.models import Grupo, Calendario


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
