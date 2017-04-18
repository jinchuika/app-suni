from rest_framework import serializers
from apps.tpe.models import Garantia


class GarantiaSerializer(serializers.ModelSerializer):
    class Model:
        model = Garantia
        fields = '__all__'
