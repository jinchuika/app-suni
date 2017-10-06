import apps.tpe.serializers as tpe_serializers
from rest_framework import viewsets
from apps.tpe.models import TicketReparacion, EvaluacionMonitoreo


class TicketReparacionViewSet(viewsets.ModelViewSet):
    serializer_class = tpe_serializers.TicketReparacionSerializer
    queryset = TicketReparacion.objects.all()
    filter_fields = (
        'ticket',
        'tecnico_asignado',
        'estado',
        'triage',
        'tipo_dispositivo',
        'ticket__garantia__equipamiento__escuela')


class EvaluacionMonitoreoViewSet(viewsets.ModelViewSet):
    serializer_class = tpe_serializers.EvaluacionMonitoreoSerializer
    queryset = EvaluacionMonitoreo.objects.all()
    filter_fields = ('monitoreo', 'pregunta')
