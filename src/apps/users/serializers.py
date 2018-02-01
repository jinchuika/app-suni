from rest_framework import serializers
from apps.main.serializers import DynamicFieldsModelSerializer
from django.contrib.auth.models import User


class UserSerializer(DynamicFieldsModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'full_name')

    def get_full_name(self, obj):
        return obj.get_full_name()
