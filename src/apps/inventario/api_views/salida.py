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
from apps.inventario import (
    serializers as inv_s,
    models as inv_m
)
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
        model = inv_m.SalidaInventario
        fields = ['id', 'tipo_salida', 'estado', 'fecha_min', 'fecha_max','en_creacion']

    def filter_fecha(self, queryset, name, value):
        if value and name == 'fecha_min':
            queryset = queryset.filter(fecha__gte=value)
        if value and name == 'fecha_max':
            queryset = queryset.filter(fecha__lte=value)
        return queryset


class SalidaInventarioViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informe de la :class: `SalidaInventario`.
    """
    serializer_class = inv_s.SalidaInventarioSerializer
    queryset = inv_m.SalidaInventario.objects.all().order_by('fecha')
    #filter_fields = ('id','tipo_salida','estado')
    filter_class = SalidaInventarioFilter

    @action(methods=['post'], detail=True)
    def stock_kardex(self, request, pk=None):
        """Metodo para obtener la existencia que hay de insumons en kardex
        """
        tipo_dispositivo = request.data['tipo_dispositivo']
        salida = request.data['salida']
        validar_dispositivo = inv_m.PaqueteTipo.objects.get(id=tipo_dispositivo)

        if validar_dispositivo.tipo_dispositivo:
                altas = inv_m.SolicitudMovimiento.objects.filter(
                    recibida=True,
                    devolucion=False,
                    no_salida=salida,
                    tipo_dispositivo__tipo=validar_dispositivo).aggregate(altas_cantidad=Sum('cantidad'))
                if altas['altas_cantidad'] is None:
                    altas['altas_cantidad'] = 0

                bajas = inv_m.SolicitudMovimiento.objects.filter(
                    recibida=True,
                    devolucion=True,
                    no_salida=salida,
                    tipo_dispositivo__tipo=validar_dispositivo).aggregate(bajas_cantidad=Sum('cantidad'))
                if bajas['bajas_cantidad'] is None:
                    bajas['bajas_cantidad'] = 0

                salidas = inv_m.Paquete.objects.filter(
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
        tipo_paquete = inv_m.PaqueteTipo.objects.all()
        lista = []

        for tipo in tipo_paquete:
            paquete_salida = {}

            altas = inv_m.SolicitudMovimiento.objects.filter(
                recibida=True,
                devolucion=False,
                no_salida=salida,
                tipo_dispositivo__tipo=tipo).aggregate(altas_cantidad=Sum('cantidad'))
            if altas['altas_cantidad'] is None:
                altas['altas_cantidad'] = 0

            bajas = inv_m.SolicitudMovimiento.objects.filter(
                recibida=True,
                devolucion=True,
                no_salida=salida,
                tipo_dispositivo__tipo=tipo).aggregate(bajas_cantidad=Sum('cantidad'))
            if bajas['bajas_cantidad'] is None:
                bajas['bajas_cantidad'] = 0

            salidas = inv_m.Paquete.objects.filter(
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
        """Metodo para cuadrar las salidas tomando en cuenta que  los dipositivos fueron aprobados por contabilidad y la revicion de contabilidad
           ya fue finalizada  y el estado de la salida tiene que ser `Listo` cambia el estado  a Pendiente y la etapa a Almacenado en bodega
        """

        id_salida = request.data['primary_key']
        tipo = request.data['tipo']
        tipo_salida = inv_m.SalidaTipo.objects.get(id=tipo)
        estado = inv_m.SalidaInventario.objects.get(id=id_salida)         
        estado_dispositivo = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.PD)
        etapa_dispositivo  = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.AB)        
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
                    aprobado=True)
                if cantidad_paquetes['total_cantidad'] != cantidad_dispositivos:
                    return Response(
                        {
                            'mensaje': 'Faltan Dispositivos por asignar'

                        },
                        status=status.HTTP_400_BAD_REQUEST

                    )
                else:
                    if(cantidad_dispositivos_aprovados.count() < cantidad_dispositivos):
                        return Response(
                            {
                                'mensaje': 'Faltan dispositivos por aprobar'

                            },
                            status=status.HTTP_400_BAD_REQUEST
                            )
                    else:
                        if(tipo_salida.id == 6 or tipo_salida.nombre=="Caja de repuestos"):                                                        
                            for data in cantidad_dispositivos_aprovados:                                
                                dispositivo_baja = conta_m.MovimientoDispositivo.objects.filter(dispositivo=data.dispositivo,tipo_movimiento=-1).count()
                                if dispositivo_baja == 0:
                                    dispositivo_caja = inv_m.Dispositivo.objects.get(triage=data.dispositivo)
                                    dispositivo_caja.estado = estado_dispositivo
                                    dispositivo_caja.etapa = etapa_dispositivo
                                    dispositivo_caja.save()
                        else:
                            pass                            
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
    @action(methods=['post'], detail=False)
    def asignar_caja_repuesto(self, request, pk=None):
        """Metodo para asignar el dipositivo a la  salida  desde la caja de repuestos
        """
        dispositivo_bueno = request.data["dispositivo_bueno"]
        dispositivo_malo = request.data["dispositivo_malo"]
        observaciones = request.data["observaciones"]
        descripcion = request.data["descripcion"]       
        obtener_dispositivo_bueno = inv_m.Dispositivo.objects.get(triage=dispositivo_bueno)
        obtener_dispositivo_malo = inv_m.Dispositivo.objects.get(triage=dispositivo_malo)        
        if(obtener_dispositivo_malo.etapa.id != 6 and obtener_dispositivo_malo.estado.id !=2):            
            return Response(
                    {
                        'mensaje': 'El dispositivo no es apto para sustituirlo por las Etapa Estado ponganse contacto con el Administrador de IT para solucionar el problema' 

                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            if (obtener_dispositivo_bueno.etapa.id == 5 and obtener_dispositivo_bueno.estado.id ==2):                
                movimiento_dispositivo_bueno= conta_m.MovimientoDispositivo.objects.filter(dispositivo=obtener_dispositivo_bueno)
                movimiento_dispositivo_malo = conta_m.MovimientoDispositivo.objects.filter(dispositivo=obtener_dispositivo_malo)                
                if (movimiento_dispositivo_bueno.count() ==1):
                    if(movimiento_dispositivo_malo.count() ==2):                       
                        paquete_dispositivo_malo = inv_m.DispositivoPaquete.objects.get(dispositivo=obtener_dispositivo_malo)
                        paquete_dispositivo_bueno = inv_m.DispositivoPaquete.objects.get(dispositivo=obtener_dispositivo_bueno)                        
                        if  paquete_dispositivo_bueno.paquete.salida.en_creacion:
                            #creacion del movimiento de dispositivo
                            periodo_actual = conta_m.PeriodoFiscal.objects.get(actual=True)
                            movimiento = conta_m.MovimientoDispositivo(
                                        dispositivo=obtener_dispositivo_bueno,
                                        periodo_fiscal=periodo_actual,
                                        tipo_movimiento=conta_m.MovimientoDispositivo.BAJA,
                                        referencia='Salida {}'.format(paquete_dispositivo_bueno.paquete.salida),
                                        precio=movimiento_dispositivo_bueno.first().precio,
                                        fecha = paquete_dispositivo_bueno.paquete.salida.fecha,
                                        creado_por=self.request.user
                                        )                        
                            movimiento.save()
                            #Creacion del registro de caja
                            registro_caja = inv_m.CajaRepuestos(
                                dispositivo_bueno = paquete_dispositivo_bueno.dispositivo,
                                dispositivo_malo = paquete_dispositivo_malo.dispositivo,                                
                                tecnico_asignado = self.request.user,
                                descripcion_equipo = descripcion,
                                observaciones = observaciones

                            )
                            registro_caja.save()
                        else:
                            return Response(
                                {
                                    'mensaje': 'La entrega se encuentra en desarrollo por termine el desarrollo para poder asignar dispositivos '

                                },
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    else:                        
                        return Response(
                    {
                        'mensaje': 'El dispositivo malo que esta intentado asignaro tiene un error pongase en contacto con IT'

                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:                    
                    return Response(
                    {
                        'mensaje': 'este dispositivo no es compatible este dispositivo ya se dio de baja'

                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
            else:
                return Response(
                    {
                        'mensaje': 'Dispositivo no aplica para ser reemplazado'

                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        return Response({
            'mensaje': 'Dispositivo asignado correctamente',
            'usuario':  "usuario"
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
        """ Metodo para aprobar la salida que se ejecuta despues de `cuadrar_salida` para darle de baja a todos los dipositivos que estan 
        en los diferentes paquetes
        """

        id_salida = request.data["salida"]
        finalizar_salida = inv_m.SalidaInventario.objects.get(id=id_salida)  
        salida = inv_m.RevisionSalida.objects.get(salida=id_salida)
        paquetes = inv_m.Paquete.objects.filter(salida=id_salida,
                                                aprobado=True).exclude(tipo_paquete__tipo_dispositivo__usa_triage=False)
        if finalizar_salida.tipo_salida.id != 6 or finalizar_salida.tipo_salida != "Caja de repuestos":           
            for paquete in paquetes:
                dispositivosPaquetes = inv_m.DispositivoPaquete.objects.filter(paquete=paquete.id,
                                                                            aprobado=True)

                for dispositivos in dispositivosPaquetes:

                    if dispositivos.dispositivo.tipo == inv_m.DispositivoTipo.objects.get(tipo="CPU"):
                        dd = inv_m.CPU.objects.get(triage = dispositivos.dispositivo.triage)                    
                        if not dd.disco_duro is None:
                            dd.disco_duro.estado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.EN)
                            dd.disco_duro.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.EN)
                            dd.disco_duro.save()
                            periodo_actual = conta_m.PeriodoFiscal.objects.get(actual=True)
                            precio_dispositivo = conta_m.PrecioDispositivo.objects.get(dispositivo__triage=dd.disco_duro, activo=True)
                            movimiento_dispositivo = conta_m.MovimientoDispositivo.objects.filter(dispositivo__triage = dd.disco_duro, tipo_movimiento = conta_m.MovimientoDispositivo.BAJA)
                            if len(movimiento_dispositivo) == 0:
                                movimiento = conta_m.MovimientoDispositivo(
                                    dispositivo=dd.disco_duro,
                                    periodo_fiscal=periodo_actual,
                                    tipo_movimiento=conta_m.MovimientoDispositivo.BAJA,
                                    referencia='Salida {}'.format(finalizar_salida),
                                    precio=precio_dispositivo.precio,
                                    fecha = finalizar_salida.fecha,
                                    creado_por=self.request.user
                                    )
                                movimiento.save()
                        else:
                            return Response(
                                {
                                    'mensaje': 'No hay discos duros asignados por favor asigne los respectivos discos duros a los CPU o Laptop '
                                },
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )

                    dispositivos.dispositivo.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.EN)
                    dispositivos.dispositivo.valido = False
                    dispositivos.dispositivo.save()
                    try:
                        cambios_etapa = inv_m.CambioEtapa.objects.filter(dispositivo__triage=dispositivos.dispositivo).order_by('-id')[0]
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
                    movimiento_dispositivo = conta_m.MovimientoDispositivo.objects.filter(dispositivo__triage = triage, tipo_movimiento = conta_m.MovimientoDispositivo.BAJA)
                    if len(movimiento_dispositivo) == 0:
                        movimiento = conta_m.MovimientoDispositivo(
                            dispositivo=dispositivos.dispositivo,
                            periodo_fiscal=periodo_actual,
                            tipo_movimiento=conta_m.MovimientoDispositivo.BAJA,
                            referencia='Salida {}'.format(salida),
                            precio=precio_dispositivo.precio,
                            fecha = finalizar_salida.fecha,
                            creado_por=self.request.user)
                        movimiento.save()
        else:
            print("SI SI es caja de herramientas")
            for paquete in paquetes:
                dispositivosPaquetes = inv_m.DispositivoPaquete.objects.filter(paquete=paquete.id,
                                                                            aprobado=True)

                for dispositivos in dispositivosPaquetes:  
                    """if dispositivos.dispositivo.tipo == inv_m.DispositivoTipo.objects.get(tipo="CPU"):
                        dd = inv_m.CPU.objects.get(triage = dispositivos.dispositivo.triage)                    
                        if not dd.disco_duro is None:
                            dd.disco_duro.estado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.EN)
                            dd.disco_duro.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.EN)
                            dd.disco_duro.save()                            
                        else:
                            return Response(
                                {
                                    'mensaje': 'No hay discos duros asignados '
                                },
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )"""

                    dispositivos.dispositivo.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.EN)
                    dispositivos.dispositivo.valido = False
                    dispositivos.dispositivo.save()
                    try:
                        cambios_etapa = inv_m.CambioEtapa.objects.filter(dispositivo__triage=dispositivos.dispositivo).order_by('-id')[0]
                        cambios_etapa.etapa_final = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.EN)
                        cambios_etapa.creado_por = request.user
                        cambios_etapa.save()
                    except ObjectDoesNotExist as e:
                        print("EL DISPOSITIVO NO EXISTE")                   

        estado_entregado = inv_m.SalidaEstado.objects.get(nombre="Entregado")
        finalizar_salida.estado = estado_entregado 
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
        """ Metodo para rechazar los dispositivos en control de calidad y les asigna la etapa a cada dispositivo "En transito"
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
        """Metodo para aprobar dispositivos en area de control de calidad y le asigna a los dipositivos el estado "Bueno o BN"
        """
        triage = request.data["triage"]
        paquete = request.data["paquete"]
        id_paquete = request.data["idpaquete"]
        tipo = request.data["tipo"]
        try:
            asignacion_fecha = inv_m.DispositivoPaquete.objects.get(dispositivo__triage=triage)
            if str(id_paquete) == str(asignacion_fecha.paquete.id):
                asignacion_fecha.aprobado = True
                asignacion_fecha.fecha_aprobacion = datetime.now()
                asignacion_fecha.save()
                cantidad_paquetes = inv_m.Paquete.objects.get(id=id_paquete)
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
        finalizar_revision = inv_m.RevisionSalida.objects.get(salida=id_salida)
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
    
    
   