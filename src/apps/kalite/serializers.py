from rest_framework import serializers
from apps.main.serializers import DynamicFieldsModelSerializer

from apps.kalite.models import Punteo, Evaluacion, Visita, Grado, EjerciciosGrado


class PunteoSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    multiplicador = serializers.IntegerField(read_only=True)

    class Meta:
        model = Punteo
        fields = '__all__'
        read_only_fields = ('id', 'evaluacion', 'indicador', 'multiplicador')


class EvaluacionSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    promedio = serializers.FloatField(read_only=True)

    class Meta:
        model = Evaluacion
        fields = '__all__'
        read_only_fields = ('id', 'visita', 'rubrica')


class VisitaSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    promedio = serializers.FloatField(read_only=True)

    class Meta:
        model = Visita
        fields = '__all__'
        read_only_fields = ('id', 'escuela')


class GradoSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Grado
        fields = '__all__'


class EjerciciosGradoSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = EjerciciosGrado
        fields = '__all__'
