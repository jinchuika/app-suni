import json
import codecs
import pandas as pd
from shapely.geometry import Point, shape

from rest_framework.renderers import JSONRenderer
from django.db.models import Count

from apps.ie.serializers import EscuelaSerializer
from apps.escuela.models import Escuela


class IEExporter():

    def __init__(self, *args, **kwargs):
        self.escuela_qs = Escuela.objects.annotate(labs=Count('laboratorios')).filter(labs__gt=0)

    def buscar_municipio(self, lat, lng, municipios):
        if lat is not None and lng is not None:
            punto = Point(lng, lat)

            for escuela in municipios['features']:
                polygon = shape(escuela['geometry'])
                if polygon.contains(punto):
                    return escuela['properties']['name']
            return 'otro'
        else:
            return 'ninguno'

    def exportar_escuela(self):
        esc_ser = EscuelaSerializer(self.escuela_qs, many=True)
        df_escuela = pd.read_json(JSONRenderer().render(esc_ser.data))

        # with open('src/static/ie/geojson/guate2.json', 'r') as data_file:
        data_file = json.load(codecs.open('src/static/ie/geojson/guate2.json', 'r', 'utf-8-sig'))
        # data_file = json.loads(open('src/static/ie/geojson/guate2.json').read().decode('utf-8-sig'))
        # print(data_file)
        # municipios = json.load(data_file)
        df_escuela['mapa_muni'] = df_escuela.apply(lambda row: self.buscar_municipio(df_escuela['lat'], df_escuela['lng'], data_file))

        with open('etc/media/ie/escuela.json', 'w') as output_file:
            json.dump(df_escuela.to_json(), output_file, ensure_ascii=False)
