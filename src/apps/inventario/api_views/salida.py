import django_filters
from django.db.utils import OperationalError
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

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
from apps.escuela import models as escuela_m
from apps.crm import models as crm_m
from django.db.models import Count, Sum
from decimal import Decimal


class SalidaInventarioViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informe de la :class: `SalidaInventario`.
    """
    serializer_class = inv_s.SalidaInventarioSerializer
    queryset = inv_m.SalidaInventario.objects.all().order_by('fecha')

    @action(methods=['post'], detail=True)
    def stock_kardex(self, request, pk=None):
        """Metodo para obtener la existencia que hay de insumons en kardex
        """
        tipo_dispositivo = request.data['tipo_dispositivo']
        validar_dispositivo = inv_m.PaqueteTipo.objects.get(id=tipo_dispositivo)
        if validar_dispositivo.tipo_dispositivo.usa_triage is False:
                altas = inv_m.SolicitudMovimiento.objects.filter(
                    recibida=True,
                    tipo_dispositivo__tipo=validar_dispositivo).aggregate(altas_cantidad=Sum('cantidad'))
                if altas['altas_cantidad'] is None:
                    altas['altas_cantidad'] = 0
                bajas = inv_m.SolicitudMovimiento.objects.filter(
                    recibida=True,
                    devolucion=True,
                    tipo_dispositivo__tipo=validar_dispositivo).aggregate(bajas_cantidad=Sum('cantidad'))
                if bajas['bajas_cantidad'] is None:
                    bajas['bajas_cantidad'] = 0
                salidas = inv_m.Paquete.objects.filter(
                    tipo_paquete=validar_dispositivo,
                    desactivado=False
                ).aggregate(salidas_cantidad=Sum('cantidad'))
                if salidas['salidas_cantidad'] is None:
                    salidas['salidas_cantidad'] = 0
                total = altas['altas_cantidad'] - (bajas['bajas_cantidad'] + salidas['salidas_cantidad'])
                return Response(
                    {'mensaje': total},
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                {'mensaje': 'Usa Triage'},
                status=status.HTTP_200_OK
            )

        return Response(
            {'mensaje': 'Exitoso'},
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=True)
    def asignar_paquetes(self, request, pk=None):
        try:
            paquete_id = request.data['paquete']
            paquete = inv_m.Paquete.objects.get(id=paquete_id)
            """ Validacion de Paquete que la salida esta consultado
            """
            if self.get_object() != paquete.salida:
                return Response(
                    {'mensaje': 'Paquete no existe'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            dispositivo_id = request.data['dispositivo']
            dispositivo = inv_m.Dispositivo.objects.get(triage=dispositivo_id)
            etapa_transito = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.TR)
            etapa_control = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.CC)
            try:
                asignacion_dispositivo = inv_m.DispositivoPaquete.objects.get(
                    paquete=paquete_id,
                    dispositivo__tipo=dispositivo.tipo
                )
                if asignacion_dispositivo.dispositivo.etapa == etapa_transito:
                    asignacion_dispositivo.dispositivo.etapa = etapa_transito
                    asignacion_dispositivo.dispositivo.save()
                else:
                    asignacion_dispositivo.dispositivo.etapa = etapa_transito
                    asignacion_dispositivo.dispositivo.save()
                asignacion_dispositivo.dispositivo = dispositivo
                asignacion_dispositivo.dispositivo.etapa = etapa_control
                asignacion_dispositivo.dispositivo.save()
                asignacion_dispositivo.save()
            except ObjectDoesNotExist as e:
                nueva_asignacion = inv_m.DispositivoPaquete(
                    dispositivo=dispositivo,
                    paquete=paquete,
                    asignado_por=request.user
                )
                nueva_asignacion.dispositivo.etapa = etapa_control
                nueva_asignacion.dispositivo.save()
                nueva_asignacion.save()
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

    @action(methods=['post'], detail=True)
    def cambios_etapa(self, request, pk=None):
        """Metodo para cambiar de esta los dipositivos para que contabiliadad pueda verlos
        """
        id_paquete = request.data["paquete"]
        paquete = inv_m.DispositivoPaquete.objects.filter(paquete=id_paquete)
        for dispositivos in paquete:
            dispositivos.aprobado = True
            dispositivos.dispositivo.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.LS)
            dispositivos.dispositivo.save()
            dispositivos.save()
        aprobarpaquete = inv_m.Paquete.objects.get(id=id_paquete)
        aprobarpaquete.aprobado = True
        aprobarpaquete.save()
        return Response(
            {
                'mensaje': 'Actualizacion completa'
            },
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False)
    def cuadrar_salida(self, request, pk=None):
        """Metodo para cuadrar las salidas
        """
        id_salida = request.data['primary_key']
        tipo = request.data['tipo']
        tipo_salida = inv_m.SalidaTipo.objects.get(id=tipo)
        estado = inv_m.SalidaInventario.objects.get(id=id_salida)
        if(str(estado.estado) == "Listo"):
            if not tipo_salida.especial:
                tipo_dis = self.request.user.tipos_dispositivos.tipos.all()
                tipo_paquete = inv_m.PaqueteTipo.objects.filter(
                    tipo_dispositivo__in=tipo_dis).exclude(tipo_dispositivo__usa_triage=False)
                cantidad_paquetes = inv_m.Paquete.objects.filter(
                    salida=id_salida,
                    tipo_paquete__in=tipo_paquete).aggregate(total_cantidad=Sum('cantidad'))
                if(cantidad_paquetes['total_cantidad'] is None):
                    cantidad_paquetes['total_cantidad'] = 0
                cantidad_dispositivos = inv_m.DispositivoPaquete.objects.filter(
                    paquete__salida=id_salida,
                    paquete__tipo_paquete__in=tipo_paquete).count()
                cantidad_dispositivos_aprovados = inv_m.DispositivoPaquete.objects.filter(
                    paquete__salida=id_salida,
                    paquete__tipo_paquete__in=tipo_paquete,
                    aprobado=True).count()
                if cantidad_paquetes['total_cantidad'] != cantidad_dispositivos:
                    return Response(
                        {
                            'mensaje': 'Faltan Dispositivos por asignar'

                        },
                        status=status.HTTP_400_BAD_REQUEST

                    )
                else:
                    if(cantidad_dispositivos_aprovados < cantidad_dispositivos):
                        return Response(
                            {
                                'mensaje': 'Faltan dispositivos por aprobar'

                            },
                            status=status.HTTP_400_BAD_REQUEST
                            )
                    else:
                        estado_entregado = inv_m.SalidaEstado.objects.get(nombre="Entregado")
                        estado.en_creacion = False
                        estado.estado = estado_entregado
                        estado.save()
        else:
            if tipo_salida.especial:
                estado_entregado = inv_m.SalidaEstado.objects.get(nombre="Entregado")
                estado.en_creacion = False
                estado.estado = estado_entregado
                estado.save()
            else:
                return Response(
                    {
                        'mensaje': 'El estado de la salida es Pendiente'

                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {
                'mensaje': 'Salida Cuadrada'
            },
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False)
    def reasignar_salida(self, request, pk=None):
        """Metodo para reasignar salida a un nuevo beneficiario
        """
        id_salida = request.data['id_salida']
        data = request.data['data']
        es_beneficiario = request.data['beneficiario']
        nueva_reasignar = inv_m.SalidaInventario.objects.get(id=id_salida)
        if(es_beneficiario == 'true'):
            try:
                nuevo_beneficiario = crm_m.Donante.objects.get(id=data)
                nueva_reasignar.beneficiario = nuevo_beneficiario
                nueva_reasignar.reasignado_por = request.user
                nueva_reasignar.save()
            except ObjectDoesNotExist as e:
                    return Response(
                        {
                            'mensaje': 'EL Beneficiario no existe'
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
        else:
            try:
                asignacion = escuela_m.Escuela.objects.get(codigo=data)
                nueva_reasignar.escuela = asignacion
                nueva_reasignar.reasignado_por = request.user
                nueva_reasignar.save()
            except ObjectDoesNotExist as e:
                return Response(
                    {
                        'mensaje': 'La Escuela  no existe'
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(
            {
                'mensaje': 'Salida reasignada'
            },
            status=status.HTTP_200_OK
        )


class RevisionSalidaFilter(filters.FilterSet):
    """ Filtros para generar infome de Entrada
    """
    estado = filters.NumberFilter(name="estado", method='filter_estado')

    class Meta:
        model = inv_m.RevisionSalida
        fields = ['aprobada']

    def filter_estado(self, qs, name, value):
        pendiente = inv_m.SalidaEstado.objects.get(nombre="Pendiente")
        return qs.filter(salida__estado=pendiente)


class RevisionSalidaViewSet(viewsets.ModelViewSet):
    """ViewSet para generar  informe de la :class: `RevisionSalida`.
    """
    serializer_class = inv_s.RevisionSalidaSerializer
    queryset = inv_m.RevisionSalida.objects.all()
    filter_class = RevisionSalidaFilter

    @action(methods=['post'], detail=True)
    def aprobado(self, request, pk=None):
        """ Metodo para aprobar la salida
        """

        id_salida = request.data["salida"]
        finalizar_salida = inv_m.SalidaInventario.objects.get(id=id_salida)
        salida = inv_m.RevisionSalida.objects.get(salida=id_salida)
        paquetes = inv_m.Paquete.objects.filter(salida=id_salida,
                                                aprobado=True).exclude(tipo_paquete__tipo_dispositivo__usa_triage=False)

        for paquete in paquetes:
            dispositivosPaquetes = inv_m.DispositivoPaquete.objects.filter(paquete=paquete.id,
                                                                           aprobado=True)

            for dispositivos in dispositivosPaquetes:
                dispositivos.dispositivo.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.EN)
                dispositivos.dispositivo.valido = False
                dispositivos.dispositivo.save()
                try:
                    cambios_etapa = inv_m.CambioEtapa.objects.get(dispositivo__triage=dispositivos.dispositivo)
                    cambios_etapa.etapa_final = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.EN)
                    cambios_etapa.creado_por = request.user
                    cambios_etapa.save()
                except ObjectDoesNotExist as e:
                    print("EL DISPOSITIVO NO EXISTE")
                """ Metodo para movimiento de dispositivos
                """
                periodo_actual = conta_m.PeriodoFiscal.objects.get(actual=True)
                salida = dispositivos.paquete.salida
                triage = dispositivos.dispositivo
                precio_dispositivo = conta_m.PrecioDispositivo.objects.get(dispositivo__triage=triage, activo=True)
                movimiento = conta_m.MovimientoDispositivo(
                    dispositivo=dispositivos.dispositivo,
                    periodo_fiscal=periodo_actual,
                    tipo_movimiento=conta_m.MovimientoDispositivo.BAJA,
                    referencia='Salida {}'.format(salida),
                    precio=precio_dispositivo.precio)
                movimiento.save()
        salida.aprobada = True
        salida.save()
        finalizar_salida.en_creacion = False
        finalizar_salida.necesita_revision = False
        finalizar_salida.save()
        return Response(
            {
                'mensaje': 'El estatus a sido Aprobado'
            }
        )

    @action(methods=['post'], detail=True)
    def rechazar_dispositivo(self, request, pk=None):
        """ Metodo para rechazar los dispositivos en control de calidad
        """
        triage = request.data["triage"]
        id_paquete = request.data["paquete"]
        paquete = inv_m.Paquete.objects.get(id=id_paquete)
        paquete.aprobado = False
        dispositivo = inv_m.Dispositivo.objects.get(triage=triage)
        dispositivo.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.TR)
        asignacion_dispositivo = inv_m.DispositivoPaquete.objects.get(dispositivo__triage=triage)
        paquete.save()
        asignacion_dispositivo.delete()
        dispositivo.save()
        return Response({
            'mensaje': 'El dispositivo ha sido rechazado'
        },
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=True)
    def aprobar_dispositivo(self, request, pk=None):
        """Metodo para aprobar dispositivos en area de control de calidad
        """
        triage = request.data["triage"]
        paquete = request.data["paquete"]
        id_paquete = request.data["idpaquete"]        
        asignacion_fecha = inv_m.DispositivoPaquete.objects.get(dispositivo__triage=triage)
        asignacion_fecha.aprobado = True
        asignacion_fecha.fecha_aprobacion = datetime.now()
        asignacion_fecha.save()
        cantidad_paquetes = inv_m.Paquete.objects.get(id=id_paquete)
        cambio_estado = inv_m.Dispositivo.objects.get(triage=triage)
        asignaciones_aprobadas = inv_m.DispositivoPaquete.objects.filter(paquete=id_paquete, aprobado=True).count()
        cambio_estado.estado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.BN)
        cambio_estado.save()
        if asignaciones_aprobadas == cantidad_paquetes.cantidad:
            cantidad_paquetes.aprobado = True
            cantidad_paquetes.save()
        return Response({
            'mensaje': 'Dispositivo aprobado'
        },
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=True)
    def aprobar_paquete_kardex(self, request, pk=None):
        """Metodo para aprobar los paquetes de kardex en Control de calidad
        """
        id_paquete = request.data["id_paquete"]
        paquete = inv_m.Paquete.objects.get(id=id_paquete)
        paquete.aprobado_kardex = True
        paquete.save()
        return Response({
            'mensaje': 'Paquete de kardex aprobada'
        },
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=True)
    def rechazar_paquete_kardex(self, request, pk=None):
        """Metodo para rechazar los paquetes de kardex en Control de calidad
        """
        id_paquete = request.data["id_paquete"]
        paquete = inv_m.Paquete.objects.get(id=id_paquete)
        paquete.desactivado = True
        paquete.save()
        return Response({
            'mensaje': 'Paquete de kardex rechazado'
        },
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=True)
    def aprobar_revision(self, request, pk=None):
        """Metodo para aprobar la revicion de una salida designanda
        """
        id_salida = request.data["salida"]
        finalizar_salida = inv_m.SalidaInventario.objects.get(id=id_salida)
        estado_bueno = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.BN)
        etapa_listo = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.LS)
        paquetes_aprobados = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida=id_salida,
            paquete__aprobado=True).count()
        dispositivos_paquetes = inv_m.DispositivoPaquete.objects.filter(paquete__salida=id_salida).count()
        dispositivos_aprobados = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida=id_salida,
            dispositivo__etapa=etapa_listo,
            dispositivo__estado=estado_bueno).count()
        if(dispositivos_aprobados != dispositivos_paquetes):
            return Response({
                'mensaje': 'Faltan Dispositivos por aprobar'
            },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            if(paquetes_aprobados < dispositivos_paquetes):
                return Response({
                    'mensaje': 'Faltan Paquetes  por aprobar'
                },
                    status=status.HTTP_400_BAD_REQUEST
                )
        finalizar_salida.estado = inv_m.SalidaEstado.objects.get(nombre="Listo")
        finalizar_salida.save()
        return Response({
            'mensaje': 'Revision aprobada'
        },
            status=status.HTTP_200_OK
        )
