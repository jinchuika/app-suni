import django_filters
from django.db.utils import OperationalError
from django.core.exceptions import ObjectDoesNotExist

from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from braces.views import LoginRequiredMixin
from apps.inventario import (
    serializers as inv_s,
    models as inv_m
)
from django.db.models import Count


class SalidaInventarioViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informe de la :class: `SalidaInventario`.
    """
    serializer_class = inv_s.SalidaInventarioSerializer
    queryset = inv_m.SalidaInventario.objects.all()

    @action(methods=['post'], detail=True)
    def asignar_paquetes(self, request, pk=None):
        try:
            paquete_id = request.data['paquete']
            paquete = inv_m.Paquete.objects.get(id=paquete_id)
            """ Validacion de Paquete que la salida esta consultado
            """
            if self.get_object() != paquete.salida:
                return Response(
                    {'mensaje': 'No sea mudo'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            dispositivo_id = request.data['dispositivo']
            dispositivo = inv_m.Dispositivo.objects.get(triage=dispositivo_id)
            try:
                asignacion_dispositivo = inv_m.DispositivoPaquete.objects.get(
                    paquete=paquete_id,
                    dispositivo__tipo=dispositivo.tipo
                )
                asignacion_dispositivo.dispositivo = dispositivo
                asignacion_dispositivo.save()
            except ObjectDoesNotExist as e:
                nueva_asignacion = inv_m.DispositivoPaquete(
                    dispositivo=dispositivo,
                    paquete=paquete,
                    asignado_por=request.user
                )
                nueva_asignacion.save()
                print(nueva_asignacion)
        except KeyError as e:
            return Response(
                {
                    'mensaje': 'Error al enviar el campo {}'.format(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except ObjectDoesNotExist as e:
            return Response(
                {
                    'mensaje': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                'mensaje': "Paquete creado "
            },
            status=status.HTTP_200_OK)
