import django_filters
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from braces.views import LoginRequiredMixin
from apps.inventario import (
    serializers as inv_s,
    models as inv_m
)
from apps.kardex import models as kax_m
from django.db.models import Count


class DispositivoFilter(filters.FilterSet):
    """Filtros para el ViewSet de Dispositivo"""
    buscador = filters.CharFilter(name='buscador', method='filter_buscador')
    asignaciones = filters.NumberFilter(name='asignacion', method='filter_asignacion')

    class Meta:
        model = inv_m.Dispositivo
        fields = ('tarima', 'id', 'etapa', 'estado', 'tipo', 'triage', 'marca', 'modelo')

    def filter_buscador(self, qs, name, value):
        return qs.filter(triage__istartswith=value)

    def filter_asignacion(self, qs, name, value):
        return qs.annotate(asignaciones=Count('asignacion')).filter(asignaciones=value)


class DispositivoViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informes de :class:`Dispositivo`
    """
    serializer_class = inv_s.DispositivoSerializer
    filter_class = DispositivoFilter
    ordering = ('entrada')

    def get_queryset(self):
        dispositivo = self.request.query_params.get('id', None)
        triage = self.request.query_params.get('triage', None)
        tipo = self.request.query_params.get('tipo', None)
        marca = self.request.query_params.get('marca', None)
        modelo = self.request.query_params.get('modelo', None)
        tarima = self.request.query_params.get('tarima', None)
        tipo_dis = self.request.user.tipos_dispositivos.tipos.all()

        if triage or dispositivo:
            return inv_m.Dispositivo.objects.all().filter(tipo__in=tipo_dis)
        elif tipo or marca or modelo or tarima:
            return inv_m.Dispositivo.objects.all().filter(valido=True, tipo__in=tipo_dis)
        else:
            return inv_m.Dispositivo.objects.all().filter(
                valido=True,
                tipo__in=tipo_dis,
                etapa=inv_m.DispositivoEtapa.TR)

    @action(methods=['get'], detail=False)
    def paquete(self, request, pk=None):
        """Encargada de filtrar los dispositivos que puedan ser elegidos para asignarse a `Paquete`"""
        queryset = inv_m.Dispositivo.objects.filter(
            estado=inv_m.DispositivoEstado.BN,
            etapa=inv_m.DispositivoEtapa.TR

        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def solicitud(self, request, pk=None):
        id = request.data['id']
        solicitudes_movimiento = inv_m.SolicitudMovimiento.objects.get(id=id)
        solicitudes_movimiento.recibida_por = self.request.user
        solicitudes_movimiento.recibida = True
        solicitudes_movimiento.save()
        return Response(
            {'mensaje': 'Solicitud Recibida'},
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False)
    def impresion_dispositivo(self, request, pk=None):
        if "inv_tecnico" in self.request.user.groups.values_list('name', flat=True):
            return Response(
                {'mensaje': 'No Tienes la Autorizacion para esta accion'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            triage = request.data['triage']
            dispositivo = inv_m.Dispositivo.objects.get(triage=triage)
            dispositivo.impreso = True
            dispositivo.save()
            return Response(
                {'mensaje': 'Dispositivo impreso'},
                status=status.HTTP_200_OK
            )

    @action(methods=['post'], detail=False)
    def solicitud_kardex(self, request, pk=None):
        id = request.data['id']
        respuesta = request.data['respuesta']
        if respuesta == str(1):
            solicitudes_movimiento = inv_m.SolicitudMovimiento.objects.get(id=id)
            usado = kax_m.EstadoEquipo.objects.get(estado='Usado')
            area_tecnica = kax_m.Proveedor.objects.get(nombre="AREA TECNICA")
            devolucion = kax_m.TipoEntrada.objects.get(tipo="Devolucion")
            if solicitudes_movimiento.devolucion is True:
                nuevo = kax_m.Entrada(
                    estado=usado,
                    proveedor=area_tecnica,
                    tipo=devolucion,
                    fecha=datetime.now(),
                    terminada=True)
                nuevo.save()
                salida_creada = kax_m.Entrada.objects.all().last()
                nuevo_detalle_kardez = kax_m.EntradaDetalle(
                    entrada=salida_creada,
                    equipo=kax_m.Equipo.objects.get(nombre=solicitudes_movimiento.tipo_dispositivo),
                    cantidad=solicitudes_movimiento.cantidad,
                    precio=0,
                )
                nuevo_detalle_kardez.save()
                solicitudes_movimiento.terminada = True
                solicitudes_movimiento.entrada_kardex = salida_creada
                solicitudes_movimiento.save()
            else:
                tipo_salida = kax_m.TipoSalida.objects.get(tipo="Inventario SUNI")
                nuevo = kax_m.Salida(
                    tecnico=self.request.user,
                    fecha=datetime.now(),
                    tipo=tipo_salida,
                    inventario_movimiento=solicitudes_movimiento,
                    terminada=True
                    )
                nuevo.save()
                nuevo_detalle = kax_m.Salida.objects.get(inventario_movimiento=id)
                detalle_salida = kax_m.SalidaDetalle(
                    salida=nuevo_detalle,
                    equipo=kax_m.Equipo.objects.get(nombre=solicitudes_movimiento.tipo_dispositivo),
                    cantidad=solicitudes_movimiento.cantidad
                    )
                detalle_salida.save()
                solicitudes_movimiento.terminada = True
                solicitudes_movimiento.salida_kardex = nuevo_detalle
                solicitudes_movimiento.save()
                return Response(
                    {'mensaje': nuevo_detalle.id},
                    status=status.HTTP_200_OK
                )
        else:
            print("se rechazo la salida")
        solicitudes_movimiento = inv_m.SolicitudMovimiento.objects.get(id=id)
        solicitudes_movimiento.rechazar = True
        solicitudes_movimiento.save()
        return Response(
            {'mensaje': 'Solicitud Recibida'},
            status=status.HTTP_200_OK
        )


class PaquetesFilter(filters.FilterSet):
    """ Filtros par el ViewSet de Paquete
    """

    tipo_paquete = django_filters.NumberFilter(name='tipo_paquete')
    tipo_dispositivo = django_filters.ModelChoiceFilter(
        queryset=inv_m.DispositivoTipo.objects.filter(usa_triage=True),
        name='tipo dispositivo',
        method='filter_tipo_dispositivo',
        )
    asignacion = filters.NumberFilter(name='asignacion', method='filter_asignacion')

    class Meta:
        model = inv_m.Paquete
        fields = ['tipo_paquete', 'salida', 'aprobado', 'aprobado_kardex', 'desactivado']

    def filter_tipo_dispositivo(self, qs, name, value):
        qs = qs.filter(tipo_paquete__tipo_dispositivo__tipo=value)
        return qs

    def filter_asignacion(self, qs, name, value):
        tipo_dis = self.request.user.tipos_dispositivos.tipos.all()
        tip_paquete = inv_m.PaqueteTipo.objects.filter(tipo_dispositivo__in=tipo_dis)
        qs = qs.filter(salida=value, tipo_paquete__in=tip_paquete)
        return qs


class PaquetesViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informe de  :class:`Paquete`
    """

    serializer_class = inv_s.PaqueteSerializer
    queryset = inv_m.Paquete.objects.all()
    filter_class = PaquetesFilter


class DispositivosPaqueteFilter(filters.FilterSet):
    """ Filtros par el ViewSet de Paquete
    """
    salida = filters.NumberFilter(name="salida", method='filter_salida')
    listo = filters.NumberFilter(name="salida aprobada", method='filter_listo')

    class Meta:
        model = inv_m.DispositivoPaquete
        fields = ['salida', 'listo', 'aprobado']

    def filter_salida(self, qs, name, value):
        qs = qs.filter(
            paquete__salida=value,
            dispositivo__etapa=inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.CC))
        return qs

    def filter_listo(self, qs, name, value):
        qs = qs.filter(
            paquete__salida=value,
            dispositivo__etapa=inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.LS))
        return qs


class DispositivosPaquetesViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informe de  :class:`DisposiitivoPaquete`
    """
    serializer_class = inv_s.DispositivoPaqueteSerializerConta
    queryset = inv_m.DispositivoPaquete.objects.all()
    filter_class = DispositivosPaqueteFilter

    @action(methods=['post'], detail=False)
    def aprobar_conta_dispositivos(self, request, pk=None):
        """ Metodo para aprobar los dispositivo en el area de contabilidad
        """
        kardex = request.data["kardex"]
        if kardex == 'true':
            paquete = request.data["paquete"]
            nuevo_paquete = inv_m.Paquete.objects.get(id=paquete)
            nuevo_paquete.aprobado = True
            nuevo_paquete.save()
        else:
            triage = request.data["triage"]
            salida = request.data["salida"]
            print(triage)
            print(salida)
            dispositivo_salida = inv_m.DispositivoPaquete.objects.filter(dispositivo__triage=triage, paquete__salida=salida)
            if len(dispositivo_salida) > 0:
                cambio_estado = inv_m.Dispositivo.objects.get(triage=triage)
                cambio_estado.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.LS)
                cambio_estado.save()
            else:
                return Response({
                    'mensaje': 'El dispositivo no pertenece a esta salida'},
                    status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'mensaje': 'El dispositivo a sido Aprobado'
        },
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False)
    def rechazar_conta_dispositivos(self, request, pk=None):
        """ Metodo para rechazar los dispositivo en el area de contabilidad
        """
        kardex = request.data["kardex"]
        if kardex == 'true':
            paquete = request.data["paquete"]
            nuevo_paquete = inv_m.Paquete.objects.get(id=paquete)
            nuevo_paquete.aprobado_kardex = False
            nuevo_paquete.save()
        else:
            triage = request.data["triage"]
            cambio_estado = inv_m.Dispositivo.objects.get(triage=triage)
            cambio_estado.estado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.PD)
            cambio_estado.save()
            desasignar_paquete = inv_m.DispositivoPaquete.objects.get(dispositivo__triage=triage)
            desasignar_paquete.aprobado = False
            desasignar_paquete.save()
        return Response({
            'mensaje': 'El dispositivo a sido Rechazado'
        },
            status=status.HTTP_200_OK
        )
