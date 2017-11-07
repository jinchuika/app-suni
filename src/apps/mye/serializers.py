from rest_framework import serializers
from apps.mye import models as mye_models


class CooperanteSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url')

    class Meta:
        model = mye_models.Cooperante
        fields = '__all__'


class ProyectoSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url')

    class Meta:
        model = mye_models.Proyecto
        fields = '__all__'
