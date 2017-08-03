from rest_framework import viewsets
from apps.tpe.serializers import TicketReparacionSerializer
from apps.tpe.models import TicketReparacion


class TicketReparacionViewSet(viewsets.ModelViewSet):
    serializer_class = TicketReparacionSerializer
    queryset = TicketReparacion.objects.all()
    filter_fields = (
        'ticket',
        'tecnico_asignado',
        'estado',
        'triage',
        'tipo_dispositivo',
        'ticket__garantia__equipamiento__escuela')
