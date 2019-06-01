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
    filter_fields = ('id', 'tipo', 'estado', 'tarima', 'marca', 'modelo')

    def get_queryset(self):
        triage = self.request.query_params.get('id', None)
        tipo_dis = self.request.user.tipos_dispositivos.tipos.all()

        if triage:
            return inv_m.Repuesto.objects.all().filter(tipo__in=tipo_dis)

        return inv_m.Repuesto.objects.all().filter(tipo__in=tipo_dis, valido=True)

    @action(methods=['post'], detail=False)
    def asignar_repuesto(self, request, pk=None):
        """ Metodo para asignar repuestos
        """
        periodo_actual = conta_m.PeriodoFiscal.objects.get(actual=True)
        try:
            triage = request.data['triage']
            repuesto_id = request.data['repuesto']
            repuesto = inv_m.Repuesto.objects.get(id=repuesto_id)
            dispositivo = inv_m.Dispositivo.objects.get(triage=triage)
            salida = repuesto.entrada
            precio_dispositivo = conta_m.MovimientoRepuesto.objects.get(repuesto=repuesto_id)
            repuesto_dispositivos = inv_m.DispositivoRepuesto(
                dispositivo=dispositivo,
                repuesto=repuesto,
                asignado_por=request.user
            )
            repuesto_estado = inv_m.Repuesto.objects.get(id=repuesto_id)
            repuesto_estado.estado = inv_m.RepuestoEstado.objects.get(id=2)
            repuesto_estado.save()
            repuesto_dispositivos.save()
            movimiento = conta_m.MovimientoRepuesto(
                repuesto=repuesto,
                periodo_fiscal=periodo_actual,
                tipo_movimiento=conta_m.MovimientoRepuesto.BAJA,
                referencia='Salida {}'.format(salida),
                precio=precio_dispositivo.precio)
            movimiento.save()

        except ObjectDoesNotExist as e:
            print("El dispositivo no existe ingrese otro")

        return Response(
            {
                'mensaje': "Repuesto asignado al dispositivo "
            },
            status=status.HTTP_200_OK)
