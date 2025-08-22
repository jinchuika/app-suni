from django.db.utils import OperationalError
from django.core.exceptions import ObjectDoesNotExist
import django_filters
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from braces.views import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.db.models import Sum
from apps.inventario import (
    serializers as inv_s,
    models as inv_m
)
from apps.kardex import models as kax_m
import json
from django.forms.models import model_to_dict
from django.utils.datastructures import MultiValueDictKeyError


class DetalleInformeFilter(filters.FilterSet):
    """ Filtro para generar los informes de Detalles de Entrada
    """
    tipo = django_filters.CharFilter(name='entrada')
    asignacion = filters.NumberFilter(name='asignacion', method='filter_asignacion')
    desecho = filters.NumberFilter(lookup_expr='gt', method='filter_desecho')

    class Meta:
        model = inv_m.EntradaDetalle
        fields = ['entrada', 'tipo_dispositivo', 'desecho']

    def filter_asignacion(self, qs, name, value):
        tipo_dis = self.request.user.tipos_dispositivos.tipos.all()
        return qs.filter(entrada=value, tipo_dispositivo__in=tipo_dis)

    def filter_desecho(self, qs, name, value):
        queryset = qs.filter(entrada__fecha__gte='2019-01-01')
        queryset = [obj for obj in queryset if obj.existencia_desecho > value]
        return queryset


class EntradaDetalleViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar las tablas de la :class:'EntradaDetalle'
    """
    serializer_class = inv_s.EntradaDetalleSerializer
    queryset = inv_m.EntradaDetalle.objects.all()
    filter_class = DetalleInformeFilter

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

    @action(methods=['post'], detail=False)
    def imprimir_qr(self, request, pk=None):
        """Metodo para imprimir los qr de dispositivo y repuestos por medio del detalle
        de entrada
        """
        if "inv_bodega" in self.request.user.groups.values_list('name', flat=True):
            diferenciar = request.data['tipo']
            detalles_id = request.data['detalles_id']
            if(diferenciar == "dispositivo"):
                entrada_detalle = inv_m.EntradaDetalle.objects.get(id=detalles_id)
                entrada_detalle.qr_dispositivo = True
                entrada_detalle.save()
            else:
                entrada_detalle = inv_m.EntradaDetalle.objects.get(id=detalles_id)
                entrada_detalle.qr_repuestos = True
                entrada_detalle.save()
            return Response(
                {'mensaje': 'Dispositivos impresos.'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'mensaje': 'No tienes la autorización para realizar esta acción.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

    @action(methods=['post'], detail=False)
    def cuadrar_salida(self, request, pk=None):
        """ Metodo para cuadrar los dispositivos de la :class:`EntradaDetalle`
        """

        if "inv_bodega" in self.request.user.groups.values_list('name', flat=True):
            mensaje_cuadrar = ""
            entrad_id = request.data['primary_key']
            entrada = inv_m.Entrada.objects.get(pk=entrad_id)

            detalles_kardex = inv_m.EntradaDetalle.objects.filter(
                entrada=entrad_id,
                ingresado_kardex=False,
                enviar_kardex=True,
                util__gt=0).count()
            dispositivos_utiles = inv_m.EntradaDetalle.objects.filter(Q(entrada=entrad_id), Q(util__gt=0)).count()
            repuestos_utiles = inv_m.EntradaDetalle.objects.filter(Q(entrada=entrad_id), Q(repuesto__gt=0)).count()
            if (entrada.tipo.especial):
                validar_dispositivos = inv_m.EntradaDetalle.objects.filter(
                    Q(entrada=entrad_id),
                    Q(util__gt=0)).count()
            else:
                validar_dispositivos = inv_m.EntradaDetalle.objects.filter(
                    Q(entrada=entrad_id),
                    Q(util__gt=0),
                    dispositivos_creados=True).count()
            validar_repuestos = inv_m.EntradaDetalle.objects.filter(
                Q(entrada=entrad_id),
                Q(repuesto__gt=0),
                repuestos_creados=True).count()
            tipo_dispositivo = inv_m.EntradaDetalle.objects.filter(
                entrada=entrad_id
                ).values('tipo_dispositivo').distinct()
            tipos_sin_cuadrar = []
            for tipo in tipo_dispositivo:
                acumulado_totales = 0
                acumulador_total = 0
                cuadrar_dispositivo = inv_m.EntradaDetalle.objects.filter(
                    entrada=entrad_id,
                    tipo_dispositivo=tipo['tipo_dispositivo'])
                for datos in cuadrar_dispositivo:
                    acumulado_totales = acumulado_totales + datos.util + datos.repuesto + datos.desecho
                    acumulador_total = acumulador_total + datos.total
                    mensaje_cuadrar = datos.tipo_dispositivo
                if(acumulador_total != acumulado_totales):
                    tipos_sin_cuadrar.append("<br><b>" + str(datos.descripcion) + "</b>")
            if(len(tipos_sin_cuadrar) > 0 ):
                return Response(
                      {'mensaje': 'La entrada no esta cuadrada, revisar los siguientes dispositivos:'
                       + ', '.join(str(x) for x in tipos_sin_cuadrar)},
                      status=status.HTTP_400_BAD_REQUEST
                  )
            elif(dispositivos_utiles != validar_dispositivos or repuestos_utiles != validar_repuestos and not entrada.tipo.especial):
                return Response(
                    {'mensaje': 'Faltan dispositivos / repuestos por crear.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif(detalles_kardex > 0 and not entrada.tipo.especial):
                return Response(
                    {'mensaje': 'Faltan dispositivos por agregar a Kardex'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                fecha_cierre = inv_m.Entrada.objects.get(id=entrad_id)
                fecha_cierre.fecha_cierre = datetime.now()
                fecha_cierre.save()
                return Response(
                    {'mensaje': 'Entrada Cuadrada'},
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                {'mensaje': 'No tienes la autorización para realizar esta acción.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

    @action(methods=['post'], detail=True)
    def crear_dispositivos(self, request, pk=None):
        """ Metodo para la Creacion de Dispositivos
        """
        if "inv_bodega" in self.request.user.groups.values_list('name', flat=True):
            entrada_detalle = self.get_object()
            try:
                entrada = entrada_detalle.entrada
                if not entrada.tipo.contenedor:
                    total = entrada_detalle.util + entrada_detalle.repuesto + entrada_detalle.desecho
                    if entrada_detalle.total != total:
                        return Response(
                            {'mensaje': 'La línea de detalle no cuadra, revisar la depuración.'},
                            status=status.HTTP_400_BAD_REQUEST)

                creacion = entrada_detalle.crear_dispositivos()
                validar_dispositivos = inv_m.EntradaDetalle.objects.get(id=pk)
                validar_dispositivos.dispositivos_creados = True
                validar_dispositivos.fecha_dispositivo = datetime.now()
                validar_dispositivos.save()
                return Response(
                    creacion,
                    status=status.HTTP_200_OK)
            except OperationalError as e:
                return Response(
                    {'mensaje': str(e)},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'mensaje': 'No tienes la autorización para realizar esta acción'},
                status=status.HTTP_401_UNAUTHORIZED
            )

    @action(methods=['post'], detail=True)
    def crear_repuestos(self, request, pk=None):
        """ Metodo para la creacion de Repuestos
        """
        if "inv_bodega" in self.request.user.groups.values_list('name', flat=True):
            entrada_detalle = self.get_object()
            try:
                entrada = entrada_detalle.entrada
                if not entrada.tipo.contenedor:
                    total = entrada_detalle.util + entrada_detalle.repuesto + entrada_detalle.desecho
                    if entrada_detalle.total != total:
                        return Response(
                            {'mensaje': 'La línea de detalle no cuadra, revisar la depuración.'},
                            status=status.HTTP_400_BAD_REQUEST)

                creacion = entrada_detalle.crear_repuestos()
                validar_dispositivos = inv_m.EntradaDetalle.objects.get(id=pk)
                validar_dispositivos.repuestos_creados = True
                validar_dispositivos.fecha_repuesto = datetime.now()
                validar_dispositivos.save()
                return Response(
                    creacion,
                    status=status.HTTP_200_OK
                )
            except OperationalError as e:
                return Response(
                    {'mensaje': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'mensaje': 'No tienes la autorización para realizar esta acción'},
                status=status.HTTP_401_UNAUTHORIZED
            )

    @action(methods=['post'], detail=True)
    def crear_kardex(self, request, pk=None):
        if "inv_bodega" in self.request.user.groups.values_list('name', flat=True):
            id = request.data['detalle_entrada']
            entrada_detalle = inv_m.EntradaDetalle.objects.get(id=id)
            total = entrada_detalle.util + entrada_detalle.repuesto + entrada_detalle.desecho
            if entrada_detalle.total != total:
                return Response(
                    {'mensaje': 'La línea de detalle no cuadra, revisar la depuración.'},
                    status=status.HTTP_400_BAD_REQUEST)

            entrada_detalle.ingresado_kardex = True
            entrada_detalle.save()
            if entrada_detalle.precio_unitario is None:
                precio_unitario = 0
            else:
                precio_unitario = entrada_detalle.precio_unitario

            equipo_kardex = kax_m.Equipo.objects.get(nombre=entrada_detalle.tipo_dispositivo)
            try:
                entrada_kardex = kax_m.Entrada.objects.get(inventario_entrada=entrada_detalle.entrada)
                nuevo_detalle_kardez = kax_m.EntradaDetalle(
                    entrada=entrada_kardex,
                    equipo=equipo_kardex,
                    cantidad=entrada_detalle.util,
                    precio=precio_unitario
                )
                nuevo_detalle_kardez.save()
            except ObjectDoesNotExist as e:
                descripcion = "Entrada de Inventario No. " + str(entrada_detalle.entrada.id) + " " + entrada_detalle.entrada.observaciones
                nuevo = kax_m.Entrada(
                    inventario_entrada=entrada_detalle.entrada,
                    estado=entrada_detalle.estado_kardex,
                    proveedor=entrada_detalle.proveedor_kardex,
                    tipo=entrada_detalle.tipo_entrada_kardex,
                    fecha=datetime.now(),
                    factura=entrada_detalle.entrada.factura,
                    observacion=descripcion,
                    terminada=True)
                nuevo.save()
                entrada_kardex = kax_m.Entrada.objects.get(inventario_entrada=entrada_detalle.entrada)
                nuevo_detalle_kardez = kax_m.EntradaDetalle(
                    entrada=entrada_kardex,
                    equipo=kax_m.Equipo.objects.get(nombre=entrada_detalle.tipo_dispositivo),
                    cantidad=entrada_detalle.util,
                    precio=precio_unitario,
                )
                nuevo_detalle_kardez.save()
                return Response(
                    {'mensaje': "Dispositivo ingresado a kardex con éxito."},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'mensaje': 'Dispositivo ingresado a kardex con éxito.'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'mensaje': 'No tienes la autorización para realizar esta acción'},
                status=status.HTTP_401_UNAUTHORIZED
            )

    @action(methods=['post'], detail=False)
    def validar_solicitud_movimientos(self, request, pk=None):
        tipo_dispositivo = request.data['tipo_dispositivo']
        etapa_transito = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.AB)
        estado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.PD)
        validar_dispositivos = inv_m.DispositivoTipo.objects.get(tipo=tipo_dispositivo)
        if(validar_dispositivos.kardex):
            cantidad_kardex = kax_m.Equipo.objects.get(nombre=tipo_dispositivo)
            numero_dispositivos = cantidad_kardex.existencia
        else:
            numero_dispositivos = inv_m.Dispositivo.objects.filter(
                tipo=validar_dispositivos,
                etapa=etapa_transito,
                estado=estado).count()
        return Response(
                {'mensaje': numero_dispositivos},
                status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def validar_devoluciones(self, request, pk=None):
        bln_inventariointerno = request.data['inventario_interno']
        tipo_dispositivo = request.data['tipo_dispositivo']
        no_salida = request.data['no_salida']
        no_inventariointerno = request.data['no_inventariointerno']

        etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.TR)
        estado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.PD)
        validar_dispositivos = inv_m.DispositivoTipo.objects.get(tipo=tipo_dispositivo)
        numero_dispositivos = 0

        if no_salida != "" or no_inventariointerno != "":
            if(validar_dispositivos.kardex):
                sum_solicitudes = sum_devoluciones = sum_paquetes = 0
                if bln_inventariointerno == "false":
                    solicitudes = inv_m.SolicitudMovimiento.objects.filter(no_salida=no_salida, tipo_dispositivo=validar_dispositivos, terminada=True, recibida=True, devolucion=False).aggregate(Sum('cantidad'))
                    devoluciones = inv_m.SolicitudMovimiento.objects.filter(no_salida=no_salida, tipo_dispositivo=validar_dispositivos, terminada=True, recibida=True, devolucion=True).aggregate(Sum('cantidad'))
                    paquetes = inv_m.Paquete.objects.filter(salida=no_salida, tipo_paquete__tipo_dispositivo=validar_dispositivos, desactivado=False).aggregate(Sum('cantidad'))
                else:
                    solicitudes = inv_m.SolicitudMovimiento.objects.filter(no_inventariointerno=no_inventariointerno, tipo_dispositivo=validar_dispositivos, terminada=True, recibida=True, devolucion=False).aggregate(Sum('cantidad'))
                    devoluciones = inv_m.SolicitudMovimiento.objects.filter(no_inventariointerno=no_inventariointerno, tipo_dispositivo=validar_dispositivos, terminada=True, recibida=True, devolucion=True).aggregate(Sum('cantidad'))
                    paquetes['cantidad__sum'] = inv_m.IInternoDispositivo.objects.filter(no_asignacion=no_inventariointerno, dispositivo__tipo=validar_dispositivos).count()

                if solicitudes['cantidad__sum'] is not None:
                    sum_solicitudes = solicitudes['cantidad__sum']

                if devoluciones['cantidad__sum'] is not None:
                    sum_devoluciones = devoluciones['cantidad__sum']

                if paquetes['cantidad__sum'] is not None:
                    sum_paquetes = paquetes['cantidad__sum']

                numero_dispositivos = sum_solicitudes - sum_devoluciones - sum_paquetes
            else:
                if bln_inventariointerno == "false":
                    dispositivos_salida = inv_m.CambioEtapa.objects.filter(solicitud__no_salida=no_salida, etapa_final=etapa).values('dispositivo')
                else:
                    dispositivos_salida = inv_m.CambioEtapa.objects.filter(solicitud__no_inventariointerno=no_inventariointerno, etapa_final=etapa).values('dispositivo')
                numero_dispositivos = inv_m.Dispositivo.objects.filter(
                    id__in=dispositivos_salida,
                    tipo=validar_dispositivos,
                    etapa=etapa,
                    estado=estado).count()

        return Response(
            {'mensaje': numero_dispositivos},
            status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def validar_kardex(self, request, pk=None):
        tipo_dispositivo = request.data['tipo_dispositivo']
        validar_dispositivos = inv_m.DispositivoTipo.objects.get(id=tipo_dispositivo)
        if validar_dispositivos.kardex is False:
            return Response(
                {'mensaje': 'Usa Triage'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'mensaje': 'NO usa Triage'},
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False)
    def autorizar_detalles(self, request, pk=None):
        """ autoriza  el detalle de dispositivo  para que los usuarios de bodega puedan
        crear los dispositivos
        """
        id = request.data['id']
        autorizado = request.data.get("autorizado") == "true"
        entrada_detalle = inv_m.EntradaDetalle.objects.get(id=id)
        pendiente_autorizar = request.data.get("pendiente_autorizar") == "true"
        rechazada = request.data.get("rechazada") == "true"
        motivo_rechazo = request.data.get("motivo_rechazo", "")
        if entrada_detalle.pendiente_autorizar is False:
            entrada_detalle.pendiente_autorizar = True
            entrada_detalle.save()
        else:
            if autorizado is True:
                entrada_detalle.autorizado = True
                entrada_detalle.save()
            else:
                entrada_detalle.autorizado = False
                entrada_detalle.pendiente_autorizar = False
                entrada_detalle.rechazada = True
                entrada_detalle.cant_rechazada += 1
                entrada_detalle.motivo_rechazo = motivo_rechazo
                entrada_detalle.save()

        return Response(
            {'mensaje': 'Autorizado'},
            status=status.HTTP_200_OK
        )


    @action(methods=['post'], detail=False)
    def nuevo_grid(self, request, pk=None):
        """ Este se conecta con el grid para editar la informacion de los dipositivos y guardarlos
        """
        entrada_detalle = request.data['entrada_detalle']
        entrada = request.data['entrada']
        tipo = inv_m.EntradaDetalle.objects.get(id=entrada_detalle).tipo_dispositivo
        tipos = inv_m.DispositivoMarca.objects.all().values()
        puertos = inv_m.DispositivoPuerto.objects.all().values()
        medida = inv_m.DispositivoMedida.objects.all().values()
        version_sis = inv_m.VersionSistema.objects.all().values()
        procesador = inv_m.Procesador.objects.all().values()
        os = inv_m.Software.objects.all().values()
        disco = inv_m.HDD.objects.filter(
            estado=inv_m.DispositivoEstado.PD,
            etapa=inv_m.DispositivoEtapa.AB).values('triage')
        if str(tipo) == "MOUSE":
            tipos_mouse = inv_m.MouseTipo.objects.all().values()
            data = inv_m.Mouse.objects.filter(
                entrada_detalle=entrada_detalle
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'puerto',
                'tipo_mouse',
                'caja',
                'clase')
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'tipo': list(tipos_mouse),
                'puertos': list(puertos),
                'dispositivo': str(tipo)
                })
        elif str(tipo) == "TECLADO":
            data = inv_m.Teclado.objects.filter(
                entrada_detalle=entrada_detalle
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'puerto',
                'caja',
                'clase'
                )
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'puertos': list(puertos),
                'dispositivo': str(tipo)
                })
        elif str(tipo) == "MONITOR":
            tipos_monitor = inv_m.MonitorTipo.objects.all().values()
            data = inv_m.Monitor.objects.filter(
                entrada_detalle=entrada_detalle
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'tipo_monitor',
                'puerto',
                'pulgadas',
                'clase')
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'tipo': list(tipos_monitor),
                'puertos': list(puertos),
                'dispositivo': str(tipo)
                })
        elif str(tipo) == "CPU":
            data = inv_m.CPU.objects.filter(
                entrada_detalle=entrada_detalle
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'procesador',
                'version_sistema',
                'disco_duro__triage',
                'ram',
                'ram_medida',
                'servidor',
                'all_in_one',
                'clase'
                ).order_by('triage')
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'puertos': list(puertos),
                'medida': list(medida),
                'dispositivo': str(tipo),
                'sistemas': list(version_sis),
                'procesador': list(procesador),
                'hdd': list(disco)
                })
        elif str(tipo) == "TABLET":
            data = inv_m.Tablet.objects.filter(
                entrada_detalle=entrada_detalle
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'procesador',
                'version_sistema',
                'so_id',
                'almacenamiento',
                'medida_almacenamiento',
                'ram',
                'medida_ram',
                'almacenamiento_externo',
                'pulgadas',
                'clase'
                )
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'medida': list(medida),
                'dispositivo': str(tipo),
                'sistemas': list(version_sis),
                'procesador': list(procesador),
                'hdd': list(disco),
                'os': list(os)
                })
        elif str(tipo) == "LAPTOP":
            data = inv_m.Laptop.objects.filter(
                entrada_detalle=entrada_detalle
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'procesador',
                'version_sistema',
                'disco_duro__triage',
                'ram',
                'ram_medida',
                'pulgadas',
                'clase',
                'servidor'
                )
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'medida': list(medida),
                'dispositivo': str(tipo),
                'sistemas': list(version_sis),
                'procesador': list(procesador),
                'hdd': list(disco)
                })
        elif str(tipo) == "HDD":
            data = inv_m.HDD.objects.filter(
                entrada_detalle=entrada_detalle
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'puerto',
                'capacidad',
                'medida',
                'clase'
                )
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'puertos': list(puertos),
                'medida': list(medida),
                'dispositivo': str(tipo)
                })
        elif str(tipo) == "SWITCH":
            data = inv_m.DispositivoRed.objects.filter(
                entrada_detalle=entrada_detalle
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'puerto',
                'cantidad_puertos',
                'velocidad',
                'velocidad_medida',
                'clase'
                )
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'puertos': list(puertos),
                'medida': list(medida),
                'dispositivo': str(tipo)
                })

        elif str(tipo) == "ACCESS POINT":
            data = inv_m.AccessPoint.objects.filter(
                entrada_detalle=entrada_detalle
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'puerto',
                'cantidad_puertos',
                'velocidad',
                'velocidad_medida',
                'clase'
                )
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'puertos': list(puertos),
                'medida': list(medida),
                'dispositivo': str(tipo)
                })



class EntradaFilter(filters.FilterSet):
    """ Filtros para generar informe de Entrada
    """
    id = django_filters.NumberFilter(name="id")
    proveedor = django_filters.CharFilter(name='proveedor')
    recibida_por = django_filters.CharFilter(name='recibida_por')
    tipo = django_filters.CharFilter(name='tipo')
    fecha_min = django_filters.DateFilter(name='fecha_min', method='filter_fecha')
    fecha_max = django_filters.DateFilter(name='fecha_max', method='filter_fecha')

    class Meta:
        model = inv_m.Entrada
        fields = ['proveedor', 'recibida_por', 'tipo', 'fecha_min', 'fecha_max']

    def filter_fecha(self, queryset, name, value):
        if value and name == 'fecha_min':
            queryset = queryset.filter(fecha__gte=value)
        if value and name == 'fecha_max':
            queryset = queryset.filter(fecha__lte=value)
        return queryset


class EntradaViewSet(viewsets.ModelViewSet):
    """ Serializer para generar las tablas de la :class:'Entrada'
    """
    serializer_class = inv_s.EntradaSerializer
    queryset = inv_m.Entrada.objects.all()
    filter_class = EntradaFilter

    def get_queryset(self):
        tipo_entrada = []
        try:
            tipo_entrada = self.request.query_params.getlist('tipo[]')
            if len(tipo_entrada) == 0:
                tipo = self.request.query_params.get('tipo')
                if tipo != None:
                    tipo_entrada.append(tipo)
        except MultiValueDictKeyError as e:
            tipo_entrada = 0

        id = self.request.query_params.get('id', None)
        proveedor = self.request.query_params.get('proveedor', None)
        recibida_por = self.request.query_params.get('recibida_por', None)
        fecha_min = self.request.query_params.get('fecha_min', None)
        fecha_max = self.request.query_params.get('fecha_max', None)

        if id or proveedor or recibida_por or fecha_min or fecha_max:
            return inv_m.Entrada.objects.all()

        if len(tipo_entrada) > 0:
            return inv_m.Entrada.objects.all().filter(tipo__in=tipo_entrada)

        return inv_m.Entrada.objects.all().filter(en_creacion=True)
