import django_filters
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
import time
from braces.views import LoginRequiredMixin
from apps.inventario import (
    serializers as inv_s,
    models as inv_m
)
from apps.kardex import models as kax_m
from django.db.models import Count
import json


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
        """ Este queryset se encarga de filtrar los dispositivo que se van a mostrar en lista
            general
        """
        dispositivo = self.request.query_params.get('id', None)
        triage = self.request.query_params.get('triage', None)
        tipo = self.request.query_params.get('tipo', None)
        marca = self.request.query_params.get('marca', None)
        modelo = self.request.query_params.get('modelo', None)
        tarima = self.request.query_params.get('tarima', None)
        nuevo_tipo = self.request.query_params.get('newtipo', None)
        if nuevo_tipo is None:
            tipo_dis = self.request.user.tipos_dispositivos.tipos.all()
        else:
            tipo_dis = inv_m.DispositivoTipo.objects.filter(tipo=nuevo_tipo)
        if triage or dispositivo:
            return inv_m.Dispositivo.objects.all().filter(tipo__in=tipo_dis)
        elif tipo or marca or modelo or tarima:
            # Se encarga de mostrar mas rapido los dispositivos que se usan con mas frecuencia
            # o mayor cantidad en el inventario
            if (tipo == str(1)):
                return inv_m.Teclado.objects.filter(valido=True)
            elif(tipo == str(2)):
                return inv_m.Mouse.objects.filter(valido=True)
            elif(tipo == str(3)):
                return inv_m.HHD.objects.filter(valido=True)
            elif(tipo == str(4)):
                return inv_m.Tablet.objects.filter(valido=True)
            elif(tipo == str(5)):
                return inv_m.Monitor.objects.filter(valido=True)
            elif(tipo == str(6)):
                return inv_m.CPU.objects.filter(valido=True)
            else:
                return inv_m.Dispositivo.objects.filter(valido=True, tipo__in=tipo_dis)
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
                    observacion=solicitudes_movimiento.observaciones,
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
                solicitudes_movimiento.autorizada_por = self.request.user
                solicitudes_movimiento.terminada = True
                solicitudes_movimiento.entrada_kardex = salida_creada
                solicitudes_movimiento.autorizada_por = self.request.user
                solicitudes_movimiento.save()
            else:
                tipo_salida = kax_m.TipoSalida.objects.get(tipo="Inventario SUNI")
                nuevo = kax_m.Salida(
                    tecnico=self.request.user,
                    fecha=datetime.now(),
                    tipo=tipo_salida,
                    inventario_movimiento=solicitudes_movimiento,
                    observacion=solicitudes_movimiento.observaciones,
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
                solicitudes_movimiento.autorizada_por = self.request.user
                solicitudes_movimiento.terminada = True
                solicitudes_movimiento.salida_kardex = nuevo_detalle
                solicitudes_movimiento.autorizada_por = self.request.user
                solicitudes_movimiento.save()
                return Response(
                    {'mensaje': nuevo_detalle.id},
                    status=status.HTTP_200_OK
                )
        else:
            solicitudes_movimiento = inv_m.SolicitudMovimiento.objects.get(id=id)
            solicitudes_movimiento.autorizada_por = self.request.user
            solicitudes_movimiento.terminada = True
            solicitudes_movimiento.rechazar = True
            solicitudes_movimiento.save()
            return Response(
                {'mensaje': 'Solicitud Rechazada'},
                status=status.HTTP_200_OK
            )

    @action(methods=['post'], detail=False)
    def colocar_tarima(self, request, pk=None):
        id = request.data['id']
        tarima = request.data['tarima']
        asignar_tarima = inv_m.Tarima.objects.get(id=tarima)
        nueva_tarima = inv_m.Dispositivo.objects.get(id=id)
        nueva_tarima.tarima = asignar_tarima
        nueva_tarima.save()
        return Response(
            {'mensaje': 'Asignado correctamente'},
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
            tipo = request.data["tipo"]
            dispositivo_salida = inv_m.DispositivoPaquete.objects.filter(dispositivo__triage=triage, paquete__salida=salida)
            if len(dispositivo_salida) > 0:
                if tipo == "TECLADO":
                    cambio_estado = inv_m.Teclado.objects.get(triage=triage)
                elif tipo == "MOUSE":
                    cambio_estado = inv_m.Mouse.objects.get(triage=triage)
                elif tipo == "HDD":
                    cambio_estado = inv_m.HDD.objects.get(triage=triage)
                elif tipo == "MONITOR":
                    cambio_estado = inv_m.Monitor.objects.get(triage=triage)
                elif tipo == "CPU":
                    cambio_estado = inv_m.CPU.objects.get(triage=triage)
                elif tipo == "TABLET":
                    cambio_estado = inv_m.Tablet.objects.get(triage=triage)
                elif tipo == "LAPTOP":
                    cambio_estado = inv_m.Laptop.objects.get(triage=triage)
                elif tipo == "SWITCH":
                    cambio_estado = inv_m.DispositivoRed.objects.get(triage=triage)
                elif tipo == "ACCESS POINT":
                    cambio_estado = inv_m.AccessPoint.objects.get(triage=triage)
                else:
                    cambio_estado = inv_m.Dispositivo.objects.get(triage=triage)
                cambio_estado.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.LS)
                cambio_estado.save()
            else:
                return Response({
                    'mensaje': 'El dispositivo no pertenece a esta salida',
                    'code': 1},

                    status=status.HTTP_200_OK)

        return Response({
            'mensaje': 'El dispositivo ha sido Aprobado'
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

    @action(methods=['post'], detail=False)
    def actualizar_dispositivos(self, request, pk=None):
        """ Metodo para actualizar nuevos dispositivos mediante el grid
        """
        dispositivos = json.loads(request.data["datos_actualizar"])
        tipo = request.data["dispositivo"]
        if tipo == "TECLADO":
            for datos in dispositivos:
                new_dispositivo = inv_m.Teclado.objects.get(triage=datos['triage'])
                new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                new_dispositivo.modelo = datos['modelo']
                new_dispositivo.serie = datos['serie']
                new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                new_dispositivo.puerto = inv_m.DispositivoPuerto.objects.get(id=datos['puerto'])
                new_dispositivo.caja = datos['caja']
                new_dispositivo.save()
        elif tipo == "MOUSE":
            for datos in dispositivos:
                new_dispositivo = inv_m.Mouse.objects.get(triage=datos['triage'])
                new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                new_dispositivo.modelo = datos['modelo']
                new_dispositivo.serie = datos['serie']
                new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                new_dispositivo.puerto = inv_m.DispositivoPuerto.objects.get(id=datos['puerto'])
                new_dispositivo.caja = datos['caja']
                new_dispositivo.save()
        elif tipo == "HDD":
            for datos in dispositivos:
                new_dispositivo = inv_m.HDD.objects.get(triage=datos['triage'])
                new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                new_dispositivo.modelo = datos['modelo']
                new_dispositivo.serie = datos['serie']
                new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                new_dispositivo.puerto = inv_m.DispositivoPuerto.objects.get(id=datos['puerto'])
                new_dispositivo.capacidad = datos['capacidad']
                new_dispositivo.medida = inv_m.DispositivoMedida.objects.get(id=datos['medida'])
                new_dispositivo.save()
        elif tipo == "MONITOR":
            for datos in dispositivos:
                new_dispositivo = inv_m.Monitor.objects.get(triage=datos['triage'])
                new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                new_dispositivo.modelo = datos['modelo']
                new_dispositivo.serie = datos['serie']
                new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                new_dispositivo.puerto = inv_m.DispositivoPuerto.objects.get(id=datos['puerto'])
                new_dispositivo.tipo_monitor = inv_m.MonitorTipo.objects.get(id=datos['tipo_monitor'])
                new_dispositivo.pulgadas = datos['pulgadas']
                new_dispositivo.save()
        elif tipo == "CPU":
            for datos in dispositivos:
                new_dispositivo = inv_m.CPU.objects.get(triage=datos['triage'])
                new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                new_dispositivo.modelo = datos['modelo']
                new_dispositivo.serie = datos['serie']
                new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                new_dispositivo.procesador = inv_m.Procesador.objects.get(id=datos['procesador'])
                new_dispositivo.version_sistema = inv_m.VersionSistema.objects.get(id=datos['version_sistema'])
                new_dispositivo.disco_duro = inv_m.HDD.objects.get(triage=datos['disco_duro__triage'])
                new_dispositivo.ram = datos['ram']
                new_dispositivo.ram_medida = inv_m.DispositivoMedida.objects.get(id=datos['ram_medida'])
                new_dispositivo.servidor = datos['servidor']
                new_dispositivo.all_in_one = datos['all_in_one']
                new_dispositivo.save()
        elif tipo == "TABLET":
            for datos in dispositivos:
                new_dispositivo = inv_m.Tablet.objects.get(triage=datos['triage'])
                new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                new_dispositivo.modelo = datos['modelo']
                new_dispositivo.serie = datos['serie']
                new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                new_dispositivo.procesador = inv_m.Procesador.objects.get(id=datos['procesador'])
                new_dispositivo.version_sistema = inv_m.VersionSistema.objects.get(id=datos['version_sistema'])
                new_dispositivo.so_id = inv_m.Software.objects.get(id=datos['so_id'])
                new_dispositivo.ram = datos['ram']
                new_dispositivo.medida_ram = inv_m.DispositivoMedida.objects.get(id=datos['medida_ram'])
                new_dispositivo.pulgadas = datos['pulgadas']
                new_dispositivo.almacenamiento = datos['almacenamiento']
                new_dispositivo.medida_almacenamiento = inv_m.DispositivoMedida.objects.get(
                    id=datos['medida_almacenamiento']
                    )
                if(str(datos['almacenamiento_externo']) == "false"):
                    new_dispositivo.almacenamiento_externo = False
                else:
                    new_dispositivo.almacenamiento_externo = True
                new_dispositivo.save()
        elif tipo == "LAPTOP":
            for datos in dispositivos:
                new_dispositivo = inv_m.Laptop.objects.get(triage=datos['triage'])
                new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                new_dispositivo.modelo = datos['modelo']
                new_dispositivo.serie = datos['serie']
                new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                new_dispositivo.procesador = inv_m.Procesador.objects.get(id=datos['procesador'])
                new_dispositivo.version_sistema = inv_m.VersionSistema.objects.get(id=datos['version_sistema'])
                new_dispositivo.disco_duro = inv_m.HDD.objects.get(triage=datos['disco_duro__triage'])
                new_dispositivo.ram = datos['ram']
                new_dispositivo.ram_medida = inv_m.DispositivoMedida.objects.get(id=datos['ram_medida'])
                new_dispositivo.pulgadas = datos['pulgadas']
                new_dispositivo.save()
        elif tipo == "SWITCH":
            for datos in dispositivos:
                new_dispositivo = inv_m.DispositivoRed.objects.get(triage=datos['triage'])
                new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                new_dispositivo.modelo = datos['modelo']
                new_dispositivo.serie = datos['serie']
                new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                new_dispositivo.puerto = inv_m.DispositivoPuerto.objects.get(id=datos['puerto'])
                new_dispositivo.cantidad_puertos = datos['cantidad_puertos']
                new_dispositivo.velocidad = datos['velocidad']
                new_dispositivo.velocidad_medida = inv_m.DispositivoMedida.objects.get(id=datos['velocidad_medida'])
                new_dispositivo.save()
        elif tipo == "ACCESS POINT":
            for datos in dispositivos:
                new_dispositivo = inv_m.AccessPoint.objects.get(triage=datos['triage'])
                new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                new_dispositivo.modelo = datos['modelo']
                new_dispositivo.serie = datos['serie']
                new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                new_dispositivo.puerto = inv_m.DispositivoPuerto.objects.get(id=datos['puerto'])
                new_dispositivo.cantidad_puertos = datos['cantidad_puertos']
                new_dispositivo.velocidad = datos['velocidad']
                new_dispositivo.velocidad_medida = inv_m.DispositivoMedida.objects.get(id=datos['velocidad_medida'])
                new_dispositivo.save()
        else:
            for datos in dispositivos:
                new_dispositivo = inv_m.Dispositivo.objects.get(triage=datos['triage'])
                new_dispositivo.serie = datos['serie']
                new_dispositivo.save()

        return Response({
            'mensaje': 'El dispositivo a sido Rechazado'
        },
            status=status.HTTP_200_OK)
