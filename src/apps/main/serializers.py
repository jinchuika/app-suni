from rest_framework import serializers

from apps.main.models import Departamento, Municipio


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    Un ModelSerializer que toma el argumento `fields`
    para especificar qué campos utiliza el ModelSerializer que
    hereda esta clase.
    """

    def __init__(self, *args, **kwargs):
        # Instancia de la clase `super` para inicializar el padre
        fields = kwargs.pop('fields', None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if not fields:
            fields = self.context['request'].query_params.get('fields') if 'request' in self.context else None
        if fields:
            fields = fields.split(',')
            # Elimina los campos que no se encuentren en `fields`.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'


class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = '__all__'
