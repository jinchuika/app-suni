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
from apps.beqt import (
    serializers as beqt_s,
    models as beqt_m
)
from apps.inventario import models as inv_m
from apps.kardex import models as kax_m
import json
from django.forms.models import model_to_dict
from django.utils.datastructures import MultiValueDictKeyError


class DetalleInformeFilter(filters.FilterSet):
    """ Filtro para generar los informes de Detalles de Entrada
    """
    tipo = django_filters.CharFilter(name='entrada')
    asignacion = filters.NumberFilter(name='asignacion', method='filter_asignacion')
   

    class Meta:
        model = beqt_m.EntradaDetalleBeqt
        fields = ['entrada', 'tipo_dispositivo']

    def filter_asignacion(self, qs, name, value):
        tipo_dis = self.request.user.tipos_dispositivos_beqt.tipos.all()        
        return qs.filter(entrada=value, tipo_dispositivo__in=tipo_dis)

    


class EntradaDetalleViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar las tablas de la :class:'EntradaDetalle'
    """
    serializer_class = beqt_s.EntradaDetalleSerializer
    queryset = beqt_m.EntradaDetalleBeqt.objects.all()
    filter_class = DetalleInformeFilter

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

    @action(methods=['post'], detail=False)
    def imprimir_qr(self, request, pk=None):
        """Metodo para imprimir los qr de dispositivo y repuestos por medio del detalle
        de entrada
        """
        if "beqt_bodega" in self.request.user.groups.values_list('name', flat=True):
            diferenciar = request.data['tipo']
            detalles_id = request.data['detalles_id']
            if(diferenciar == "dispositivo"):
                entrada_detalle = beqt_m.EntradaDetalleBeqt.objects.get(id=detalles_id)
                entrada_detalle.qr_dispositivo = True
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

        if "beqt_bodega" in self.request.user.groups.values_list('name', flat=True):            
            mensaje_cuadrar = ""
            entrad_id = request.data['primary_key']
            entrada = beqt_m.Entrada.objects.get(pk=entrad_id)
            dispositivos_utiles = beqt_m.EntradaDetalleBeqt.objects.filter(Q(entrada=entrad_id), Q(total__gt=0)).count()
            
            if (entrada.tipo.especial):
                validar_dispositivos = beqt_m.EntradaDetalleBeqt.objects.filter(
                    Q(entrada=entrad_id),
                    Q(total__gt=0)).count()
            else:
                validar_dispositivos = beqt_m.EntradaDetalleBeqt.objects.filter(
                    Q(entrada=entrad_id),
                    Q(total__gt=0),
                    dispositivos_creados=True).count()           
            tipo_dispositivo = beqt_m.EntradaDetalleBeqt.objects.filter(
                entrada=entrad_id
                ).values('tipo_dispositivo').distinct()
            tipos_sin_cuadrar = []
            for tipo in tipo_dispositivo:
                acumulado_totales = 0
                acumulador_total = 0
                cuadrar_dispositivo = beqt_m.EntradaDetalleBeqt.objects.filter(
                    entrada=entrad_id,
                    tipo_dispositivo=tipo['tipo_dispositivo'])
                for datos in cuadrar_dispositivo:
                    acumulado_totales = acumulado_totales + datos.total 
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
            elif(dispositivos_utiles != validar_dispositivos and not entrada.tipo.especial):
                return Response(
                    {'mensaje': 'Faltan dispositivos / repuestos por crear.'},
                    status=status.HTTP_400_BAD_REQUEST
                )            
            else:
                fecha_cierre = beqt_m.Entrada.objects.get(id=entrad_id)
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
        if "beqt_bodega" in self.request.user.groups.values_list('name', flat=True):            
            entrada_detalle = self.get_object()            
            try:
                """entrada = entrada_detalle.entrada
                if not entrada.tipo.contenedor:
                    total = entrada_detalle.util
                    if entrada_detalle.total != total:
                        return Response(
                            {'mensaje': 'La línea de detalle no cuadra, revisar la depuración.'},
                            status=status.HTTP_400_BAD_REQUEST)"""

                creacion = entrada_detalle.crear_dispositivos()
                #creacion = entrada_detalle                            
                validar_dispositivos = beqt_m.EntradaDetalleBeqt.objects.get(id=pk)
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
    

    @action(methods=['post'], detail=False)
    def validar_solicitud_movimientos(self, request, pk=None):
        tipo_dispositivo = request.data['tipo_dispositivo']
        etapa_transito = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.AB)
        estado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.PD)
        validar_dispositivos = beqt_m.DispositivoTipoBeqt.objects.get(tipo=tipo_dispositivo)
        numero_dispositivos = beqt_m.DispositivoBeqt.objects.filter(
                tipo=validar_dispositivos,
                etapa=etapa_transito,
                estado=estado).count()
        return Response(
                {'mensaje': numero_dispositivos},
                status=status.HTTP_200_OK)
    

    @action(methods=['post'], detail=False)
    def autorizar_detalles(self, request, pk=None):
        """ autoriza  el detalle de dispositivo  para que los usuarios de bodega puedan
        crear los dispositivos
        """
        id = request.data['id']
        autorizado = request.data['autorizado']
        pendiente_autorizar = request.data['pendiente_autorizar']
        entrada_detalle = beqt_m.EntradaDetalleBeqt.objects.get(id=id)
        if entrada_detalle.pendiente_autorizar is False:
            entrada_detalle.pendiente_autorizar = True
            entrada_detalle.save()
        else:
            if entrada_detalle.autorizado is False:
                entrada_detalle.autorizado = True
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
        tipo = beqt_m.EntradaDetalleBeqt.objects.get(id=entrada_detalle).tipo_dispositivo
        tipos = inv_m.DispositivoMarca.objects.all().values()
        puertos = inv_m.DispositivoPuerto.objects.all().values()
        medida = inv_m.DispositivoMedida.objects.all().values()
        version_sis = inv_m.VersionSistema.objects.all().values()
        procesador = inv_m.Procesador.objects.all().values()
        estuche = beqt_m.CaseTabletBeqt.objects.all().values()
        cargador_tablet = beqt_m.CargadorTabletBeqt.objects.all().values()
        cargador_laptop = beqt_m.CargadorLaptopBeqt.objects.all().values()
        os = inv_m.Software.objects.all().values()
        disco = beqt_m.HDDBeqt.objects.filter(
            estado=inv_m.DispositivoEstado.PD,
            etapa=inv_m.DispositivoEtapa.AB).values('triage')        
        if str(tipo) == "TABLET":
            data = beqt_m.TabletBeqt.objects.filter(
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
                'clase',
                'cargador__triage',
                'estuche__triage',
                'codigo_rti'
                )
            print(data)
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'medida': list(medida),
                'dispositivo': str(tipo),
                'sistemas': list(version_sis),
                'procesador': list(procesador),
                'hdd': list(disco),
                'os': list(os),
                'cargador':list(cargador_tablet),
                'estuche': list(estuche)
                })
        elif str(tipo) == "LAPTOP":
            data = beqt_m.LaptopBeqt.objects.filter(
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
                'almacenamiento',
                'medida_almacenamiento',
                'ram',
                'ram_medida',
                'pulgadas',
                'clase',
                'servidor',
                'cargador__triage',
                'codigo_rti'
                )
            print(data)
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'medida': list(medida),
                'dispositivo': str(tipo),
                'sistemas': list(version_sis),
                'procesador': list(procesador),
                'hdd': list(disco),
                'cargador': list(cargador_laptop),
                })
        elif str(tipo) == "HDD":
            data = beqt_m.HDDBeqt.objects.filter(
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
                'clase',
                'codigo_rti'
                )
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'puertos': list(puertos),
                'medida': list(medida),
                'dispositivo': str(tipo)
                })
        elif str(tipo) == "SWITCH":
            data = beqt_m.DispositivoRedBeqt.objects.filter(
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
                'clase',
                'codigo_rti'
                )
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'puertos': list(puertos),
                'medida': list(medida),
                'dispositivo': str(tipo)
                })

        elif str(tipo) == "ACCESS POINT":
            data = beqt_m.AccessPointBeqt.objects.filter(
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
                'clase',
                'codigo_rti'
                )
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'puertos': list(puertos),
                'medida': list(medida),
                'dispositivo': str(tipo)
                })

        elif str(tipo) == "ADAPTADOR RED":
            data = beqt_m.DispositivoRedBeqt.objects.filter(
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
                'clase',
                'codigo_rti'
                )
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'puertos': list(puertos),
                'medida': list(medida),
                'dispositivo': str(tipo)
                })
        elif str(tipo) == "CARGADOR TABLET":
            data = beqt_m.CargadorTabletBeqt.objects.filter(
                entrada_detalle=entrada_detalle
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'alimentacion',
                'salida',
                'clase',
                'codigo_rti'
                )
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'puertos': list(puertos),
                'medida': list(medida),
                'dispositivo': str(tipo)
                })
        elif str(tipo) == "CARGADOR LAPTOP":
            data = beqt_m.CargadorLaptopBeqt.objects.filter(
                entrada_detalle=entrada_detalle
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'voltaje',
                'clase',
                'codigo_rti'

                )
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'puertos': list(puertos),
                'medida': list(medida),
                'dispositivo': str(tipo)
                })

        elif str(tipo) == "ESTUCHE TABLET":
            data = beqt_m.CaseTabletBeqt.objects.filter(
                entrada_detalle=entrada_detalle
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'compatibilidad',
                'color',
                'estilo',
                'material',
                'dimensiones',
                'clase',
                'codigo_rti'
                )
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'puertos': list(puertos),
                'medida': list(medida),
                'dispositivo': str(tipo)
                })
        elif str(tipo) == "REGLETA":
            data = beqt_m.RegletaBeqt.objects.filter(
                entrada_detalle=entrada_detalle
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'conexiones',
                'voltaje',
                'clase',
                'codigo_rti',
                'regulador',
                )
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'puertos': list(puertos),
                'medida': list(medida),
                'dispositivo': str(tipo)
                })

        elif str(tipo) == "UPS":
            data = beqt_m.UpsBeqt.objects.filter(
                entrada_detalle=entrada_detalle
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'conexiones',
                'voltaje',
                'clase',
                'codigo_rti'
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
        model = beqt_m.Entrada
        fields = ['proveedor', 'recibida_por', 'tipo', 'fecha_min', 'fecha_max']

    def filter_fecha(self, queryset, name, value):
        if value and name == 'fecha_min':
            queryset = queryset.filter(fecha__gte=value)
        if value and name == 'fecha_max':
            queryset = queryset.filter(fecha__lte=value)
        return queryset


class EntradaViewSet(viewsets.ModelViewSet):
    """ Serializer para generar las tablas de la :class:'Entrada' de beqt
    """
    serializer_class = beqt_s.EntradaSerializer
    queryset = beqt_m.Entrada.objects.all()
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
            return beqt_m.Entrada.objects.all()

        if len(tipo_entrada) > 0:
            return beqt_m.Entrada.objects.all().filter(tipo__in=tipo_entrada)

        return beqt_m.Entrada.objects.all().filter(en_creacion=True)
