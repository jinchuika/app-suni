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
from apps.conta import models as conta_m
from django.db.models import Count
from decimal import Decimal


class RepuestoInventarioViewSet(viewsets.ModelViewSet):
    """ViewSet para poder asignar repuesto  de la :clas:`Repuesto` y poder asignar los
      periodos fiscales de la :class:`PeriodoFiscal`, asignar los repuestos de la :class:`DispositivoRepuesto`
      llevar los movimientos de repuestos de la :class:`MovimientoRepuesto`

    """
    serializer_class = inv_s.RepuestoInventarioSerializer
    filter_fields = ('id', 'tipo', 'estado', 'tarima', 'marca', 'modelo', 'estado')

    def get_queryset(self):
        triage = self.request.query_params.get('id', None)
        estado = self.request.query_params.get('estado', None)
        tipo_dis = self.request.user.tipos_dispositivos.tipos.all()

        if triage or estado:
            return inv_m.Repuesto.objects.all().filter(tipo__in=tipo_dis)

        return inv_m.Repuesto.objects.all().filter(tipo__in=tipo_dis, valido=True)

    @action(methods=['post'], detail=False)
    def asignar_repuesto(self, request, pk=None):
        """ Metodo para asignar repuestos
        """
        try:
            triage = request.data['triage']
            repuesto_id = request.data['repuesto']
            comentario= request.data['comentario']

            repuesto = inv_m.Repuesto.objects.get(id=repuesto_id)
            dispositivo = inv_m.Dispositivo.objects.get(triage=triage)
            salida = repuesto.entrada

            if dispositivo.etapa.id != inv_m.DispositivoEtapa.AB and dispositivo.etapa.id != inv_m.DispositivoEtapa.TR:
                return Response({'mensaje': "El dispositivo ingresado no es válido.",'codigo':2 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if dispositivo.tipo != repuesto.tipo:
                return Response({'mensaje': "El dispositivo y el repuesto deben ser del mismo tipo.",'codigo':3 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Agregar Asignación Repuesto - Dispositivo
            repuesto_dispositivos = inv_m.DispositivoRepuesto(
                dispositivo=dispositivo,
                repuesto=repuesto,
                asignado_por=request.user
            )
            repuesto_dispositivos.save()
            repuesto.estado = inv_m.RepuestoEstado.objects.get(id=3)
            repuesto.save()
            
            # Agregar Comentario de Asignación
            comentario_asignacion = inv_m.RepuestoComentario(
                repuesto=repuesto,
                dispositivo=dispositivo,
                comentario=comentario,
                creado_por=request.user
            )
            comentario_asignacion.save() 
        except ObjectDoesNotExist as e:            
            return Response(
            {
                'mensaje': "El dispositivo no existe.",
                'codigo':1
            },
            status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                'mensaje': "Repuesto asignado al dispositivo."
            },
            status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def terminar_repuesto(self, request, pk=None):
        """ Metodo para terminar la asignacion de los repuestos
        """
        periodo_actual = conta_m.PeriodoFiscal.objects.get(actual=True)
        try:           
            repuesto_id = request.data['repuesto']
            repuesto = inv_m.Repuesto.objects.get(id=repuesto_id)
            precio_repuesto = conta_m.PrecioRepuesto.objects.get(repuesto=repuesto_id, activo=True)                      
            salida = repuesto.entrada

            repuesto.estado = inv_m.RepuestoEstado.objects.get(id=2)
            repuesto.valido = False
            repuesto.disponible = False
            repuesto.save()           
            movimiento = conta_m.MovimientoRepuesto(
                repuesto=repuesto,
                periodo_fiscal=periodo_actual,
                tipo_movimiento=conta_m.MovimientoRepuesto.BAJA,
                referencia='Salida {}'.format(salida),
                precio=precio_repuesto.precio)
            movimiento.save()

        except ObjectDoesNotExist as e:
            print("El dispositivo no existe ingrese otro")

        return Response(
            {
                'mensaje': "Repuesto usado  "
            },
            status=status.HTTP_200_OK)
