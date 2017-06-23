from rest_framework import serializers

from django.contrib.auth.models import User

from apps.cyd.serializers import ParticipanteSerializer, CapacitadorSerializer
from apps.cyd.models import Participante
from apps.naat.models import AsignacionNaat


class AsignacionNaatSerializer(serializers.ModelSerializer):
    participante = ParticipanteSerializer()

    class Meta:
        model = AsignacionNaat
        fields = ('participante',)


class ParticipanteNaatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = '__all__'


class ParticipanteAsignadoField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, AsignacionNaat):
            serializer = ParticipanteNaatSerializer(value.participante)
            return serializer.data
        else:
            raise Exception('Error al obtener datos')


class FacilitadorNaatSerializer(serializers.ModelSerializer):
    asignados_naat = serializers.SerializerMethodField('get_asignaciones_activas')

    def get_asignaciones_activas(self, obj):
        asignaciones_naat = AsignacionNaat.objects.filter(capacitador=obj, activa=True)
        print(asignaciones_naat)
        serializer = AsignacionNaatSerializer(asignaciones_naat, many=True)
        return serializer.data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'asignados_naat')
