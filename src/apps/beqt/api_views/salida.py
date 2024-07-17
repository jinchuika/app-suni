import django_filters
from django.db.utils import OperationalError
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.contrib.auth.models import User

from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from braces.views import LoginRequiredMixin
from apps.beqt import (
    serializers as beqt_s,
    models as beqt_m
)
from apps.inventario import models as inv_m
from apps.conta import models as conta_m
from apps.escuela import models as escuela_m
from apps.crm import models as crm_m
from django.db.models import Count, Sum
from decimal import Decimal


class SalidaInventarioFilter(filters.FilterSet):
    """ Filtros para generar informe de  Salida
    """
    id = django_filters.NumberFilter(name="id")
    tipo_salida= django_filters.CharFilter(name='tipo_salida')
    estado = django_filters.CharFilter(name='estado')
    fecha_min = django_filters.DateFilter(name='fecha_min', method='filter_fecha')
    fecha_max = django_filters.DateFilter(name='fecha_max', method='filter_fecha')

    class Meta:
        model = beqt_m.SalidaInventario
        fields = ['id', 'tipo_salida', 'estado', 'fecha_min', 'fecha_max']

    def filter_fecha(self, queryset, name, value):
        if value and name == 'fecha_min':
            queryset = queryset.filter(fecha__gte=value)
        if value and name == 'fecha_max':
            queryset = queryset.filter(fecha__lte=value)
        return queryset


class SalidaInventarioViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informe de la :class: `SalidaInventario`.
    """
    serializer_class = beqt_s.SalidaInventarioSerializer
    queryset = beqt_m.SalidaInventario.objects.all().order_by('fecha')
    #filter_fields = ('id','tipo_salida','estado')
    filter_class = SalidaInventarioFilter
    
    @action(methods=['post'], detail=True)
    def stock_kardex(self, request, pk=None):
        """Metodo para obtener la existencia que hay de insumons en kardex
        """
        tipo_dispositivo = request.data['tipo_dispositivo']
        salida = request.data['salida']
        validar_dispositivo = beqt_m.PaqueteTipoBeqt.objects.get(id=tipo_dispositivo)

        if validar_dispositivo.tipo_dispositivo:
                altas = beqt_m.SolicitudMovimientoBeqt.objects.filter(
                    recibida=True,
                    devolucion=False,
                    no_salida=salida,
                    tipo_dispositivo__tipo=validar_dispositivo).aggregate(altas_cantidad=Sum('cantidad'))
                if altas['altas_cantidad'] is None:
                    altas['altas_cantidad'] = 0

                bajas = beqt_m.SolicitudMovimientoBeqt.objects.filter(
                    recibida=True,
                    devolucion=True,
                    no_salida=salida,
                    tipo_dispositivo__tipo=validar_dispositivo).aggregate(bajas_cantidad=Sum('cantidad'))
                if bajas['bajas_cantidad'] is None:
                    bajas['bajas_cantidad'] = 0

                salidas = beqt_m.PaqueteBeqt.objects.filter(
                    tipo_paquete=validar_dispositivo,
                    desactivado=False,
                    salida=salida
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
                {'mensaje': 'Dispositivo no Existe'},
                status=status.HTTP_400_BAD_REQUEST
            )
    @action(methods=['post'], detail=True)
    def stock_paquete(self, request, pk=None):
        salida = request.data['salida']
        tipo_paquete = beqt_m.PaqueteTipoBeqt.objects.all()
        lista = []

        for tipo in tipo_paquete:
            paquete_salida = {}

            altas = beqt_m.SolicitudMovimientoBeqt.objects.filter(
                recibida=True,
                devolucion=False,
                no_salida=salida,
                tipo_dispositivo__tipo=tipo).aggregate(altas_cantidad=Sum('cantidad'))
            if altas['altas_cantidad'] is None:
                altas['altas_cantidad'] = 0

            bajas = beqt_m.SolicitudMovimientoBeqt.objects.filter(
                recibida=True,
                devolucion=True,
                no_salida=salida,
                tipo_dispositivo__tipo=tipo).aggregate(bajas_cantidad=Sum('cantidad'))
            if bajas['bajas_cantidad'] is None:
                bajas['bajas_cantidad'] = 0

            salidas = beqt_m.PaqueteBeqt.objects.filter(
                tipo_paquete=tipo,
                desactivado=False,
                salida=salida
                ).aggregate(salidas_cantidad=Sum('cantidad'))
            if salidas['salidas_cantidad'] is None:
                salidas['salidas_cantidad'] = 0

            total = altas['altas_cantidad'] - (bajas['bajas_cantidad'] + salidas['salidas_cantidad'])

            paquete_salida['id'] = tipo.id
            paquete_salida['nombre'] = tipo.nombre
            paquete_salida['existencia'] = total
            lista.append(paquete_salida)

        return Response(lista)

    @action(methods=['post'], detail=True)
    def asignar_paquetes(self, request, pk=None):
        try:
            paquete_id = request.data['paquete']
            paquete = beqt_m.PaqueteBeqt.objects.get(id=paquete_id)
            """ Validacion de Paquete que la salida esta consultado
            """
            if self.get_object() != paquete.salida:
                return Response(
                    {'mensaje': 'Paquete no existe'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            dispositivo_id = request.data['dispositivo']
            dispositivo = beqt_m.DispositivoBeqt.objects.get(triage=dispositivo_id)
            etapa_transito = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.TR)
            etapa_control = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.CC)
            try:
                asignacion_dispositivo = beqt_m.DispositivoPaquete.objects.get(
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
                nueva_asignacion = beqt_m.DispositivoPaquete(
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
        paquete = beqt_m.DispositivoPaquete.objects.filter(paquete=id_paquete)
        for dispositivos in paquete:
            dispositivos.aprobado = True
            dispositivos.dispositivo.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.LS)
            dispositivos.dispositivo.save()
            dispositivos.save()
        aprobarpaquete = beqt_m.PaqueteBeqt.objects.get(id=id_paquete)
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
        tipo_salida = beqt_m.SalidaTipoBeqt.objects.get(id=tipo)
        estado = beqt_m.SalidaInventario.objects.get(id=id_salida)
        if(str(estado.estado) == "Listo"):
            if not tipo_salida.especial:
                tipo_dis = self.request.user.tipos_dispositivos_beqt.tipos.all()
                tipo_paquete = beqt_m.PaqueteTipoBeqt.objects.filter(
                    tipo_dispositivo__in=tipo_dis).exclude(tipo_dispositivo__usa_triage=False)
                cantidad_paquetes = beqt_m.PaqueteBeqt.objects.filter(
                    salida=id_salida,
                    tipo_paquete__in=tipo_paquete).aggregate(total_cantidad=Sum('cantidad'))
                if(cantidad_paquetes['total_cantidad'] is None):
                    cantidad_paquetes['total_cantidad'] = 0
                cantidad_dispositivos = beqt_m.DispositivoPaquete.objects.filter(
                    paquete__salida=id_salida,
                    paquete__tipo_paquete__in=tipo_paquete).count()
                cantidad_dispositivos_aprovados = beqt_m.DispositivoPaquete.objects.filter(
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
        print("ingresar a reasignar salida  beqt")
        id_salida = request.data['id_salida']
        data = request.data['data']
        es_beneficiario = request.data['beneficiario']
        nueva_reasignar = beqt_m.SalidaInventario.objects.get(id=id_salida)
        if(es_beneficiario == 'true'):
            print("ingresar a reasignar salida  beqt1")
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
            print("ingresar a reasignar salida  beqt2")
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
        model = beqt_m.RevisionSalidaBeqt
        fields = ['aprobada']

    def filter_estado(self, qs, name, value):
        pendiente = inv_m.SalidaEstado.objects.get(nombre="Pendiente")
        return qs.filter(salida__estado=pendiente)


class RevisionSalidaViewSet(viewsets.ModelViewSet):
    """ViewSet para generar  informe de la :class: `RevisionSalida`.
    """
    serializer_class = beqt_s.RevisionSalidaSerializer
    queryset = beqt_m.RevisionSalidaBeqt.objects.all()
    filter_class = RevisionSalidaFilter

    @action(methods=['post'], detail=True)
    def aprobado(self, request, pk=None):
        """ Metodo para aprobar la salida
        """

        id_salida = request.data["salida"]
        finalizar_salida = beqt_m.SalidaInventario.objects.get(id=id_salida)
        salida = beqt_m.RevisionSalidaBeqt.objects.get(salida=id_salida)
        paquetes = beqt_m.PaqueteBeqt.objects.filter(salida=id_salida,
                                                aprobado=True).exclude(tipo_paquete__tipo_dispositivo__usa_triage=False)



        for paquete in paquetes:
            dispositivosPaquetes = beqt_m.DispositivoPaquete.objects.filter(paquete=paquete.id,
                                                                           aprobado=True)
            
            
            for dispositivos in dispositivosPaquetes:

                dispositivos.dispositivo.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.EN)
                dispositivos.dispositivo.valido = False
                dispositivos.dispositivo.save()
                try:                
                    cambios_etapa = beqt_m.CambioEtapaBeqt.objects.filter(dispositivo__triage=dispositivos.dispositivo).order_by("-id")[0]
                    cambios_etapa.etapa_final = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.EN)
                    cambios_etapa.creado_por = request.user
                    cambios_etapa.save()
                except ObjectDoesNotExist as e:
                    print("EL DISPOSITIVO NO EXISTE")
                """ Metodo para movimiento de dispositivos
                """                
                salida = dispositivos.paquete.salida
                triage = dispositivos.dispositivo                
                movimiento_dispositivo = conta_m.MovimientoDispositivoBeqt.objects.filter(dispositivo__triage = triage, tipo_movimiento = conta_m.MovimientoDispositivo.BAJA)
                if len(movimiento_dispositivo) == 0:
                    movimiento = conta_m.MovimientoDispositivoBeqt(
                        dispositivo=dispositivos.dispositivo,                        
                        tipo_movimiento=conta_m.MovimientoDispositivo.BAJA,
                        referencia='Salida {}'.format(salida),                       
                        fecha = finalizar_salida.fecha,
                        creado_por=self.request.user)
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
        paquete = beqt_m.PaqueteBeqt.objects.get(id=id_paquete)
        paquete.aprobado = False
        dispositivo = beqt_m.DispositivoBeqt.objects.get(triage=triage)
        dispositivo.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.TR)
        asignacion_dispositivo = beqt_m.DispositivoPaquete.objects.get(dispositivo__triage=triage)
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
        #Cambio para PROTECTOR TABLETS
        triage = request.data["triage"]
        paquete = request.data["paquete"]
        id_paquete = request.data["idpaquete"]
        tipo = request.data["tipo"]
        try:
            asignacion_fecha = beqt_m.DispositivoPaquete.objects.get(dispositivo__triage=triage)
            if str(id_paquete) == str(asignacion_fecha.paquete.id):
                asignacion_fecha.aprobado = True
                asignacion_fecha.fecha_aprobacion = datetime.now()
                asignacion_fecha.save()
                cantidad_paquetes = beqt_m.PaqueteBeqt.objects.get(id=id_paquete)                
                if tipo == "HDD":
                    cambio_estado = beqt_m.HDDBeqt.objects.get(triage=triage) 
                elif tipo == "TABLET":
                    cambio_estado = beqt_m.TabletBeqt.objects.get(triage=triage)
                elif tipo == "LAPTOP":
                    cambio_estado = beqt_m.LaptopBeqt.objects.get(triage=triage)
                elif tipo == "SWITCH":
                    cambio_estado = beqt_m.DispositivoRedBeqt.objects.get(triage=triage)
                elif tipo == "ACCESS POINT":
                    cambio_estado = beqt_m.AccessPointBeqt.objects.get(triage=triage)
                elif tipo == "ADAPTADOR RED":
                    cambio_estado = beqt_m.DispositivoRedBeqt.objects.get(triage=triage)
                elif tipo == "CARGADOR TABLET":
                    cambio_estado = beqt_m.CargadorTabletBeqt.objects.get(triage=triage)
                elif tipo == "CARGADOR LAPTOP":
                    cambio_estado = beqt_m.CargadorLaptopBeqt.objects.get(triage=triage)
                elif tipo == "ESTUCHE TABLET":
                    cambio_estado = beqt_m.CaseTabletBeqt.objects.get(triage=triage)
                elif tipo == "REGLETA":
                    cambio_estado = beqt_m.RegletaBeqt.objects.get(triage=triage)
                elif tipo == "UPS":
                    cambio_estado = beqt_m.UpsBeqt.objects.get(triage=triage) 
                else:
                    cambio_estado = beqt_m.DispositivoBeqt.objects.get(triage=triage)
                asignaciones_aprobadas = beqt_m.DispositivoPaquete.objects.filter(paquete=id_paquete, aprobado=True).count()
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
            else:
                return Response({
                    'mensaje': 'El dispositivo no pertenece a este paquete'
                },
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            return Response({
                'mensaje': 'Dispositivo no encontrado'
            },
                status=status.HTTP_200_OK
            )

  

    @action(methods=['post'], detail=True)
    def aprobar_revision(self, request, pk=None):
        """Metodo para aprobar la revicion de una salida designanda
        """
        id_salida = request.data["salida"]
        finalizar_revision = beqt_m.RevisionSalidaBeqt.objects.get(salida=id_salida)
        finalizar_salida = beqt_m.SalidaInventario.objects.get(id=id_salida)
        estado_bueno = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.BN)
        etapa_listo = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.LS)
        paquetes_aprobados = beqt_m.DispositivoPaquete.objects.filter(
            paquete__salida=id_salida,
            paquete__aprobado=True).count()
        dispositivos_paquetes = beqt_m.DispositivoPaquete.objects.filter(paquete__salida=id_salida).count()
        dispositivos_aprobados = beqt_m.DispositivoPaquete.objects.filter(
            paquete__salida=id_salida,
            dispositivo__etapa=etapa_listo,
            dispositivo__estado=estado_bueno).count()
        if(paquetes_aprobados < dispositivos_paquetes):
            return Response({
                'mensaje': 'No se ha podido finalizar la revisión, ya que existen paquetes que aún están pendientes de revisar en Control de Calidad'
            },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            if(dispositivos_aprobados != dispositivos_paquetes):
                return Response({
                    'mensaje': 'No se ha podido finalizar la revisión, ya que existen Dispositivos que aún están pendientes de revisar en Contabilidad'
                },
                    status=status.HTTP_400_BAD_REQUEST
                )
        finalizar_salida.estado = inv_m.SalidaEstado.objects.get(nombre="Listo")
        finalizar_salida.save()
        finalizar_revision.aprobada = True
        finalizar_revision.save()
        return Response({
            'mensaje': 'la revision ha sido aprobada',
            'usuario':  str(request.user.perfil)
        },
            status=status.HTTP_200_OK
        )

   