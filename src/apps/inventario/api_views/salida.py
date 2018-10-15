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
from django.db.models import Count, Sum
from decimal import Decimal


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
                print("asignacon dispositivo" + str(asignacion_dispositivo))
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
                print("nueva asignacion:" + str(nueva_asignacion))
                print(nueva_asignacion.dispositivo.etapa)
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
        id_paquete = request.data["paquete"]
        paquete = inv_m.DispositivoPaquete.objects.filter(paquete=id_paquete)
        for dispositivos in paquete:
            print(str(dispositivos.dispositivo)+"dis")
            print(str(dispositivos.aprobado)+"status")
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
        id_salida = request.data['primary_key']
        tipo = request.data['tipo']
        tipo_salida = inv_m.SalidaTipo.objects.get(id=tipo)
        estado = inv_m.SalidaInventario.objects.get(id=id_salida)
        if(str(estado.estado) == "Listo"):
            if not tipo_salida.especial:
                tipo_dis = self.request.user.tipos_dispositivos.tipos.all()
                tipo_paquete = inv_m.PaqueteTipo.objects.filter(tipo_dispositivo__in=tipo_dis)
                cantidad_paquetes = inv_m.Paquete.objects.filter(
                    salida=id_salida,
                    tipo_paquete__in=tipo_paquete).aggregate(total_cantidad=Sum('cantidad'))
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
            print(tipo_salida.especial)
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
                                                aprobado=True)
        for paquete in paquetes:
            dispositivosPaquetes = inv_m.DispositivoPaquete.objects.filter(paquete=paquete.id,
                                                                           aprobado=True)
            for dispositivos in dispositivosPaquetes:
                dispositivos.dispositivo.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.EN)
                dispositivos.dispositivo.valido = False
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
                    precio_dispositivo = conta_m.MovimientoDispositivo.objects.get(dispositivo__triage=triage)
                    movimiento = conta_m.MovimientoDispositivo(
                        dispositivo=dispositivos.dispositivo,
                        periodo_fiscal=periodo_actual,
                        tipo_movimiento=conta_m.MovimientoDispositivo.BAJA,
                        referencia='Salida {}'.format(salida),
                        precio=precio_dispositivo.precio)
                    movimiento.save()
                dispositivos.dispositivo.save()
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
        """ Metodo para rechazar los dispositivos
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
            'mensaje': 'El dispositivo a sido rechazado'
        },
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=['post'], detail=True)
    def aprobar_dispositivo(self, request, pk=None):
        triage = request.data["triage"]
        paquete = request.data["paquete"]
        id_paquete = request.data["idpaquete"]
        asignaciones_aprobadas = inv_m.DispositivoPaquete.objects.filter(paquete=id_paquete, aprobado=True).count()
        asignaciones = inv_m.DispositivoPaquete.objects.filter(paquete=id_paquete, aprobado=False)
        cantidad_paquetes = inv_m.Paquete.objects.get(id=id_paquete)
        cambio_estado = inv_m.Dispositivo.objects.get(triage=triage)
        for aprobar in asignaciones:
            aprobar.aprobado = True
            aprobar.save()
        cambio_estado.estado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.BN)
        cambio_estado.save()
        if asignaciones_aprobadas == cantidad_paquetes.cantidad:
            cantidad_paquetes.aprobado = True
            cantidad_paquetes.save()
        else:
            return Response(
                {
                    'mensaje': 'Faltan Dispositivos por aprobar'

                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            'mensaje': 'Dispositivo aprobado'
        },
            status=status.HTTP_200_OK
        )
