from rest_framework import serializers
from apps.main.serializers import DynamicFieldsModelSerializer
from apps.cyd import models


class EscuelaSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = models.Escuela
        fields = '__all__'
