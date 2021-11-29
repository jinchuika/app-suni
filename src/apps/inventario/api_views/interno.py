import django_filters
from django.db.utils import OperationalError
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_framework import status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from braces.views import LoginRequiredMixin
from apps.inventario import (
    serializers as inv_s,
    models as inv_m
)
from apps.users import serializers as users_s
from apps.crm import models as crm_m
from django.db.models import Count, Sum
from decimal import Decimal

class InventarioInternoViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informe de la :class 'InventarioInterno'
    """
    serializer_class = inv_s.InventarioInternoSerializer
    queryset = inv_m.InventarioInterno.objects.all().order_by('estado')

    @action(methods=['post'], detail=False)
    def reasignar_registro(self, request, pk=None):
        """ Método para reasignar una salida de inventario interno """
        id_asignacion = request.data['id_asignacion']
        data = request.data['data']

        asignacion_ii = inv_m.InventarioInterno.objects.get(id=id_asignacion)
        if asignacion_ii:
            try:
                usuario = User.objects.get(id=data)
                asignacion_ii.colaborador_asignado = usuario
                asignacion_ii.creada_por = request.user
                asignacion_ii.fecha_asignacion = datetime.now()
                asignacion_ii.save()
                return Response({'mensaje': 'Asignación Reasignada'}, status=status.HTTP_200_OK  )
            except ObjectDoesNotExist as e:
                return Response({'mensaje': 'El usuario no existe'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'mensaje': 'No se encontró la asignación'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], detail=False)
    def entregar_asignacion(self, request, pk=None):
        """ Método para finalizar la asignación de inventario interno """
        if "inv_interno" not in self.request.user.groups.values_list('name', flat=True):
            return Response(
                {'mensaje': 'No Tienes la Autorizacion para esta accion'}, status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            id_asignacion = request.data["id"]
            asignacion_ii = inv_m.InventarioInterno.objects.get(id=id_asignacion)

            if asignacion_ii.dispositivos.count() == 0:
                return Response({'mensaje': 'No tienes dispositivos asignados'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if asignacion_ii.dispositivos.filter(fecha_aprobacion = None).count() > 0:
                return Response({'mensaje': 'Tienes dispositivos pendientes de aprobar'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            dispositivos_solicitados = inv_m.SolicitudMovimiento.objects.filter(no_inventariointerno=asignacion_ii, devolucion=False, recibida=True).aggregate(total_cantidad=Sum('cantidad'))
            if(dispositivos_solicitados['total_cantidad'] is None):
                    dispositivos_solicitados['total_cantidad'] = 0
            devoluciones = inv_m.SolicitudMovimiento.objects.filter(no_inventariointerno=asignacion_ii, devolucion=True, recibida=True).aggregate(total_cantidad=Sum('cantidad'))
            if(devoluciones['total_cantidad'] is None):
                    devoluciones['total_cantidad'] = 0
            total = (dispositivos_solicitados['total_cantidad'] - devoluciones['total_cantidad']) - asignacion_ii.dispositivos.count()

            if total == 0:
                for dispositivo in asignacion_ii.dispositivos.all():
                    dispositivo_asignado = dispositivo.dispositivo
                    dispositivo_asignado.estado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.EN)
                    dispositivo_asignado.save()

                asignacion_ii.estado = inv_m.IInternoEstado.objects.get(id=inv_m.IInternoEstado.AS)
                asignacion_ii.borrador = False
                asignacion_ii.save()
                return Response({'mensaje': 'Asignación Entregada'}, status=status.HTTP_200_OK  )
            else:
                return Response({'mensaje': 'Tienes dispositivos pendientes de asignar'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], detail=False)
    def devolver_asignacion(self, request, pk=None):
        """ Método para devolver el equipo prestado en la asignación """
        if "inv_interno" not in self.request.user.groups.values_list('name', flat=True):
            return Response(
                {'mensaje': 'No Tienes la Autorizacion para esta accion'}, status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            id_asignacion = request.data["id"]
            asignacion_ii = inv_m.InventarioInterno.objects.get(id=id_asignacion)

            if asignacion_ii.estado.id != inv_m.IInternoEstado.AS:
                return Response({'mensaje': 'Solamente pueden devolverse dispositivos asignados'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            for dispositivo in asignacion_ii.dispositivos.all():
                dispositivo_asignado = dispositivo.dispositivo
                dispositivo_asignado.estado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.PD)
                dispositivo_asignado.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.AB)
                dispositivo_asignado.save()

            asignacion_ii.estado = inv_m.IInternoEstado.objects.get(id=inv_m.IInternoEstado.DV)
            asignacion_ii.fecha_devolucion = datetime.now()
            asignacion_ii.save()
            return Response({'mensaje': 'Dispositivos Devueltos'}, status=status.HTTP_200_OK  )

class IInternoDispositivoFilter(filters.FilterSet):
    """ Filtros para generar informe de inventario interno"""
    no_asignacion = django_filters.NumberFilter(name="no_asignacion")
    estado = django_filters.NumberFilter(name="no_asignacion__estado")
    colaborador = django_filters.NumberFilter(name="no_asignacion__colaborador_asignado")
    tipo_dispositivo = django_filters.NumberFilter(name="dispositivo__tipo")
    fecha_min = django_filters.DateFilter(name='no_asignacion__fecha_asignacion', lookup_expr='gte')
    fecha_max = django_filters.DateFilter(name='no_asignacion__fecha_asignacion', lookup_expr='lte')

    class Meta:
        model = inv_m.IInternoDispositivo
        fields = ['no_asignacion', 'estado', 'colaborador', 'tipo_dispositivo', 'fecha_min', 'fecha_max']

class IInternoDispositivoViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informe de la :class 'IInternoDispositivo'
    """
    serializer_class = inv_s.IInternoDispositivoSerializer
    queryset = inv_m.IInternoDispositivo.objects.all().order_by('indice')
    filter_class = IInternoDispositivoFilter
    filter_fields = ('no_asignacion',)

    def get_queryset(self):
        no_asignacion = self.request.query_params.get('no_asignacion', None)
        estado = self.request.query_params.get('estado', None)
        colaborador = self.request.query_params.get('colaborador', None)
        tipo_dispositivo = self.request.query_params.get('tipo_dispositivo', None)
        fecha_min = self.request.query_params.get('fecha_min', None)
        fecha_max = self.request.query_params.get('fecha_max', None)

        if no_asignacion or estado or colaborador or tipo_dispositivo or fecha_min or fecha_max:
            print("Todos")
            queryset = inv_m.IInternoDispositivo.objects.all()
        else:
            print("Estado")
            queryset = inv_m.IInternoDispositivo.objects.filter(no_asignacion__estado__id=inv_m.IInternoEstado.AS)

        print(queryset)
        return queryset

    @action(methods=['post'], detail=False)
    def aprobar_dispositivo(self, request, pk=None):
        """ Método para aprobar dispositivos asignados a inventario interno """
        if "inv_cc" not in self.request.user.groups.values_list('name', flat=True):
            return Response(
                {'mensaje': 'No Tienes la Autorizacion para esta accion'}, status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            id_detalle = request.data["detalle"]
            
            detalle = inv_m.IInternoDispositivo.objects.get(id=id_detalle)
            detalle.fecha_aprobacion = datetime.now()
            detalle.aprobado_por = self.request.user
            detalle.save()
            
            if detalle.dispositivo.tipo.usa_triage:
                dispositivo = detalle.dispositivo
                dispositivo.estado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.BN)
                dispositivo.save()

            return Response(
                {'mensaje': 'Dispositivo Aprobado'}, status=status.HTTP_200_OK
            )

    @action(methods=['post'], detail=False)
    def rechazar_dispositivo(self, request, pk=None):
        """Método para rechazar dispositivos asignados a inventario interno"""
        if "inv_cc" not in self.request.user.groups.values_list('name', flat=True):
            return Response(
                {'mensaje': 'No Tienes la Autorizacion para esta accion'}, status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            id_detalle = request.data["detalle"]
            comentario = request.data["comentario"]
            
            detalle = inv_m.IInternoDispositivo.objects.get(id=id_detalle)

            comentario_rechazar_detalle = inv_m.IIRevisionComentario(
                no_asignacion = detalle.no_asignacion,
                revisado_por = self.request.user,
                comentario = comentario,
                dispositivo = detalle.dispositivo
            )
            comentario_rechazar_detalle.save()

            if detalle.dispositivo.tipo.usa_triage:
                dispositivo = detalle.dispositivo
                dispositivo.estado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.PD)
                dispositivo.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.TR)
                dispositivo.save()

            detalle.delete()

            return Response(
                {'mensaje': 'Dispositivo Rechazado'}, status=status.HTTP_200_OK
            )

class UsuarioListView(viewsets.ModelViewSet):
    serializer_class = users_s.UserSerializer
    queryset = User.objects.filter(is_active=True)