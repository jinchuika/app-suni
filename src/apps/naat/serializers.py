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


class FacilitadorNaatSerializer(serializers.ModelSerializer):
    asignados_naat = AsignacionNaatSerializer(many=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'asignados_naat')
