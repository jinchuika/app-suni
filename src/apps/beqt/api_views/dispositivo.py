import django_filters
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from datetime import datetime
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings
from django.template import loader
import time
from braces.views import LoginRequiredMixin
from apps.beqt import (
    serializers as beqt_s,
    models as beqt_m
)
from apps.inventario import models as inv_m
from django.contrib.auth.models import User
from django.db.models import Count
import json


class DispositivoFilter(filters.FilterSet):
    """Filtros para el ViewSet de Dispositivo"""
    buscador = filters.CharFilter(name='buscador', method='filter_buscador')
    asignaciones = filters.NumberFilter(name='asignacion', method='filter_asignacion')
    procesador = filters.NumberFilter(name='procesador', method='filter_procesadores')

    class Meta:
        model = beqt_m.DispositivoBeqt
        fields = ('tarima', 'id', 'etapa', 'estado', 'tipo', 'triage', 'marca', 'modelo')

    def filter_buscador(self, qs, name, value):
        return qs.filter(triage__istartswith=value)

    def filter_asignacion(self, qs, name, value):
        return qs.annotate(asignaciones=Count('asignacion')).filter(asignaciones=value)   

    def filter_procesadores(self, qs, name , value):        
        procesador = inv_m.Procesador.objects.get(id=value)
        tipo_dispositivo= qs.last()        
        if tipo_dispositivo.tipo.id == 7:          
            return qs.filter(laptop__procesador= procesador)
        elif tipo_dispositivo.tipo.id == 4:           
            return qs.filter(procesador = procesador)
        elif tipo_dispositivo.tipo.id == 6:            
            return qs.filter(procesador = procesador)
        else:
            return  Response(
                        {'mensaje': "Esta opcion soloe esta disponible para CPU, TABLET y LAPTOP"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            


class DispositivoViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informes de :class:`Dispositivo`
    """
    serializer_class = beqt_s.DispositivoSerializer
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
        etapa = self.request.query_params.get('etapa', None)
        estado = self.request.query_params.get('estado', None)
        salida = self.request.query_params.get('id_salida', None)
        solicitud = self.request.query_params.get('solicitud', None)     
        lista_dispositivos = []      
        if bool(solicitud):           
            if estado == "1"  and etapa == "1":                
                return beqt_m.DispositivoBeqt.objects.filter(triage=triage)
            else:
                return"Dispositivo no aceptado"      
        else:             
            if tipo is None:
                tipo_dis = self.request.user.tipos_dispositivos_beqt.tipos.all()            
            else:            
                tipo_dis = beqt_m.DispositivoTipoBeqt.objects.filter(id=tipo)
                    

            if  dispositivo or etapa:                
                #nueva_salida  = inv_m.SalidaInventario.objects.get(id=salida)                      
                dispositivos_salida = beqt_m.CambioEtapaBeqt.objects.filter(
                    solicitud__no_salida = salida,
                    dispositivo__tipo__in = tipo_dis
                )                         
                for data in dispositivos_salida.values('dispositivo'):
                    lista_dispositivos.append(data['dispositivo'])            
                return beqt_m.DispositivoBeqt.objects.all().filter(id__in=lista_dispositivos)
           
            elif triage:               
                return beqt_m.DispositivoBeqt.objects.filter(triage=triage)
            elif tipo or marca or modelo or tarima:                
                # Se encarga de mostrar mas rapido los dispositivos que se usan con mas frecuencia
                # o mayor cantidad en el inventario
                if (tipo == str(1)):
                    return beqt_m.HDDBeqt.objects.filter(valido=True)
                elif(tipo == str(2)):
                    return beqt_m.TabletBeqt.objects.filter(valido=True)
                elif(tipo == str(3)):
                    return beqt_m.LaptopBeqt.objects.filter(valido=True)
                elif(tipo == str(4)):
                    return beqt_m.AccessPointBeqt.objects.filter(valido=True)
                elif(tipo == str(5)):
                    return beqt_m.CargadorLaptopBeqt.objects.filter(valido=True)
                elif(tipo == str(6)):
                    return beqt_m.UpsBeqt.objects.filter(valido=True)
                elif(tipo == str(7)):
                    return beqt_m.RegletaBeqt.objects.filter(valido=True)
                elif(tipo == str(8)):
                    return beqt_m.DispositivoRedBeqt.objects.filter(valido=True)
                elif(tipo == str(9)):
                    return beqt_m.CargadorTabletBeqt.objects.filter(valido=True)
                elif(tipo == str(10)):
                    return beqt_m.CaseTabletBeqt.objects.filter(valido=True)
                elif(tipo == str(11)):
                    return beqt_m.ProtectorTabletBeqt.objects.filter(valido=True)
                else:
                    return beqt_m.DispositivoBeqt.objects.filter(valido=True, tipo__in=tipo_dis)
            else:
                return beqt_m.DispositivoBeqt.objects.all().filter(
                    valido=True,
                    tipo__in=tipo_dis,
                    etapa=inv_m.DispositivoEtapa.TR)


    @action(methods=['get'], detail=False)
    def asignar_dispositivo(self,request, pk=None):
        """ Asigna los dispositos a los paquetes de la entrada
        """
        
        if request.GET.get('etapa') == '2':
            queryset = beqt_m.DispositivoBeqt.objects.filter(id=request.GET.get('id'))          
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response(
            {'mensaje': 'Dispositivo no encontrado'},
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False)
    def cambiar_cantidad(self,request, pk=None):
        """ Metodo  que cambia la cantidad de un paquete
        """
        paquete= request.data['idpaquete']
        cantidad = request.data['cantidad']
        new_cantidad= beqt_m.PaqueteBeqt.objects.get(id=paquete)
        new_cantidad.cantidad = cantidad
        new_cantidad.save()
        return Response(
            {'mensaje': 'Cambio Aceptado'},
            status=status.HTTP_200_OK
        )

    @action(methods=['get'], detail=False)
    def paquete(self, request, pk=None):
        """Encargada de filtrar los dispositivos que puedan ser elegidos para asignarse a `Paquete`"""
        queryset = beqt_m.DispositivoBeqt.objects.filter(
            estado=inv_m.DispositivoEstado.BN,
            etapa=inv_m.DispositivoEtapa.TR

        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)    

    @action(methods=['post'], detail=False)
    def grid_paquetes(self, request, pk=None):
        """ Este se conecta con el grid para editar la informacion de los dipositivos y guardarlos
        """
        paquete = request.data['paquete']
        newtipo = beqt_m.DispositivoPaquete.objects.filter(paquete=paquete)
        paquetes = beqt_m.DispositivoPaquete.objects.filter(paquete=paquete).values('dispositivo__triage')
        tipo = newtipo.first().paquete.tipo_paquete
        tipos = inv_m.DispositivoMarca.objects.all().values()
        puertos = inv_m.DispositivoPuerto.objects.all().values()
        medida = inv_m.DispositivoMedida.objects.all().values()
        version_sis = inv_m.VersionSistema.objects.all().values()
        procesador = inv_m.Procesador.objects.all().values()
        os = inv_m.Software.objects.all().values()
        estuche = beqt_m.CaseTabletBeqt.objects.all().values()
        protector = beqt_m.ProtectorTabletBeqt.objects.all().values()
        cargador_tablet = beqt_m.CargadorTabletBeqt.objects.all().values()
        cargador_laptop = beqt_m.CargadorLaptopBeqt.objects.all().values()
        disco = beqt_m.HDDBeqt.objects.filter(
            estado=inv_m.DispositivoEstado.PD,
            etapa=inv_m.DispositivoEtapa.AB).values('triage')        
        if str(tipo) == "TABLET":
            data = beqt_m.TabletBeqt.objects.filter(
                triage__in=paquetes
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
                'protector__triage',
                ).order_by('triage')
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
                'estuche': list(estuche),
                'protector': list(protector)
                })
        elif str(tipo) == "LAPTOP":
            data = beqt_m.LaptopBeqt.objects.filter(
                triage__in=paquetes
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
                'cargador__triage'
                ).order_by('triage')
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
            data = inv_m.HDD.objects.filter(
                triage__in=paquetes
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
                ).order_by('triage')
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'puertos': list(puertos),
                'medida': list(medida),
                'dispositivo': str(tipo)
                })  
        elif str(tipo) == "ACCESS POINT":
            data = beqt_m.AccessPointBeqt.objects.filter(
                triage__in=paquetes
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
                ).order_by('triage')
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'puertos': list(puertos),
                'medida': list(medida),
                'dispositivo': str(tipo)
                })
        elif str(tipo) == "SWITCH":
            data = beqt_m.DispositivoRedBeqt.objects.filter(
                triage__in=paquetes
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

        elif str(tipo) == "ADAPTADOR RED":
            data = beqt_m.DispositivoRedBeqt.objects.filter(
                triage__in=paquetes
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'puerto',
                'cantidad_puertos',
                'velocidad',
                'clase'
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
                etriage__in=paquetes
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'alimentacion',
                'salida',
                'clase'
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
                triage__in=paquetes
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'voltaje',
                'clase'
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
                triage__in=paquetes
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
                'clase'
                )
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'puertos': list(puertos),
                'medida': list(medida),
                'dispositivo': str(tipo)
                })
        
        elif str(tipo) == "PROTECTOR TABLET":
            data = beqt_m.ProtectorTabletBeqt.objects.filter(
                triage__in=paquetes
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'compatibilidad',
                'color',
                'material',
                'dimensiones',
                'clase'
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
                triage__in=paquetes
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'conexiones',
                'voltaje',
                'clase'
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
                triage__in=paquetes
            ).values(
                'triage',
                'marca',
                'modelo',
                'serie',
                'tarima',
                'conexiones',
                'voltaje',
                'clase'
                )
            return JsonResponse({
                'data': list(data),
                'marcas': list(tipos),
                'puertos': list(puertos),
                'medida': list(medida),
                'dispositivo': str(tipo)
                })


        return Response(
            {'mensaje': 'Solicitud Recibida'},
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False)
    def solicitud(self, request, pk=None):
        id = request.data['id']
        solicitudes_movimiento = beqt_m.SolicitudMovimientoBeqt.objects.get(id=id)
        solicitudes_movimiento.recibida_por = self.request.user
        solicitudes_movimiento.terminada = True
        solicitudes_movimiento.recibida = True
        solicitudes_movimiento.save()
        return Response(
            {'mensaje': 'Solicitud Recibida'},
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False)
    def impresion_dispositivo(self, request, pk=None):
        if "beqt_tecnico" in self.request.user.groups.values_list('name', flat=True):
            return Response(
                {'mensaje': 'No Tienes la Autorizacion para esta accion'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            triage = request.data['triage']
            dispositivo = beqt_m.DispositivoBeqt.objects.get(triage=triage)
            dispositivo.impreso = True
            dispositivo.save()
            return Response(
                {'mensaje': 'Dispositivo impreso'},
                status=status.HTTP_200_OK
            )
 

    @action(methods=['post'], detail=False)
    def colocar_tarima(self, request, pk=None):
        """ Este se conecta a la app para poder colocar los dipositivos a las tarimas
        """
        id = request.data['id']
        tarima = request.data['tarima']
        asignar_tarima = inv_m.Tarima.objects.get(id=tarima)
        nueva_tarima = beqt_m.DispositivoBeqt.objects.get(id=id)
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
        queryset=beqt_m.DispositivoTipoBeqt.objects.filter(usa_triage=True),
        name='tipo dispositivo',
        method='filter_tipo_dispositivo',
        )
    asignacion = filters.NumberFilter(name='asignacion', method='filter_asignacion')

    class Meta:
        model = beqt_m.PaqueteBeqt
        fields = ['tipo_paquete', 'salida', 'aprobado', 'aprobado_kardex', 'desactivado']

    def filter_tipo_dispositivo(self, qs, name, value):
        qs = qs.filter(tipo_paquete__tipo_dispositivo__tipo=value)
        return qs

    def filter_asignacion(self, qs, name, value):
        tipo_dis = self.request.user.tipos_dispositivos_beqt.tipos.all()
        tip_paquete = beqt_m.PaqueteTipoBeqt.objects.filter(tipo_dispositivo__in=tipo_dis)
        qs = qs.filter(salida=value, tipo_paquete__in=tip_paquete)
        return qs

class PaquetesViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informe de  :class:`Paquete`
    """

    serializer_class = beqt_s.PaqueteSerializer
    queryset = beqt_m.PaqueteBeqt.objects.all()
    filter_class = PaquetesFilter

class DispositivoPaqueteViewset(viewsets.ModelViewSet):
    serializer_class = beqt_s.DispositivoPaqueteSerializer
    queryset = beqt_m.DispositivoPaquete.objects.all()
    filter_fields = ('paquete',)


class DispositivosPaqueteFilter(filters.FilterSet):
    """ Filtros par el ViewSet de Paquete
    """
    salida = filters.NumberFilter(name="salida", method='filter_salida')
    listo = filters.NumberFilter(name="salida aprobada", method='filter_listo')

    class Meta:
        model = beqt_m.DispositivoPaquete
        fields = ['salida', 'listo', 'aprobado', 'paquete']

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
    serializer_class = beqt_s.DispositivoPaqueteSerializerConta
    queryset = beqt_m.DispositivoPaquete.objects.all()
    filter_class = DispositivosPaqueteFilter

    @action(methods=['post'], detail=False)
    def aprobar_conta_dispositivos(self, request, pk=None):
        """ Metodo para aprobar los dispositivo en el area de contabilidad       """
      
        triage = request.data["triage"]
        salida = request.data["salida"]
        tipo = request.data["tipo"]
        dispositivo_salida = beqt_m.DispositivoPaquete.objects.filter(dispositivo__triage=triage, paquete__salida=salida)
        if len(dispositivo_salida) > 0:
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
            elif tipo == "PROTECTOR TABLET":
                cambio_estado = beqt_m.ProtectorTabletBeqt.objects.get(triage=triage)
            elif tipo == "REGLETA":
                cambio_estado = beqt_m.RegletaBeqt.objects.get(triage=triage)
            elif tipo == "UPS":
                cambio_estado = beqt_m.UpsBeqt.objects.get(triage=triage)   
            else:
                cambio_estado = beqt_m.DispositivoBeqt.objects.get(triage=triage)
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
        
        triage = request.data["triage"]
        cambio_estado = beqt_m.DispositivoBeqt.objects.get(triage=triage)
        cambio_estado.estado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.PD)
        cambio_estado.save()
        desasignar_paquete = beqt_m.DispositivoPaquete.objects.get(dispositivo__triage=triage)
        desasignar_paquete.aprobado = False
        desasignar_paquete.save()
        desasignar_paquete.paquete.aprobado = False
        desasignar_paquete.paquete.save()
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
        if tipo == "LAPTOP":
            for datos in dispositivos:
                print(datos["codigo_rti"])
                new_dispositivo = beqt_m.LaptopBeqt.objects.get(triage=datos['triage'])
                try:
                    new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                except ObjectDoesNotExist as e:
                    print("Marca no necesita actualizar")
                try:
                    new_dispositivo.modelo = datos['modelo']
                except ObjectDoesNotExist as e:
                    print("Modelo no necesita actualizacion")
                try:
                    new_dispositivo.serie = datos['serie']
                except ObjectDoesNotExist as e:
                    print("Serie no necesita actualizacion")
                try:
                    new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                except ObjectDoesNotExist as e:
                    print("Tarima no necesita actualizacion")
                try:
                    new_dispositivo.procesador = inv_m.Procesador.objects.get(id=datos['procesador'])
                except ObjectDoesNotExist as e:
                    print("Procesador no necesita actualizacion")
                try:
                    new_dispositivo.version_sistema = inv_m.VersionSistema.objects.get(id=datos['version_sistema'])
                except ObjectDoesNotExist as e:
                    print("La version del sistema no necisita actualizacion")
                try:
                    new_dispositivo.disco_duro = beqt_m.HDDBeqt.objects.get(triage=datos['disco_duro__triage'])
                except ObjectDoesNotExist as e:
                    print("El disco duro no necesita actualizacion")

                try:
                    new_dispositivo.cargador = beqt_m.CargadorLaptopBeqt.objects.get(triage=datos['cargador__triage'])
                except ObjectDoesNotExist as e:
                    print("El cargador no necesita actualizacion")
                try:
                    new_dispositivo.ram = datos['ram']
                except ObjectDoesNotExist as e:
                    print("Memoria ram no necesita actualizacion")
                try:
                    new_dispositivo.ram_medida = inv_m.DispositivoMedida.objects.get(id=datos['ram_medida'])
                except ObjectDoesNotExist as e:
                    print("Medidad de ram no necesita actualizacion")
                try:
                    new_dispositivo.pulgadas = datos['pulgadas']
                except ObjectDoesNotExist as e:
                    print("Pulgadas del monitor no necesita actualizacion")
                try:
                    new_dispositivo.clase = inv_m.DispositivoClase.objects.get(id=datos['clase'])
                except ObjectDoesNotExist as e:
                    print("Clase no necesita actualizacion")
                try:
                    new_dispositivo.almacenamiento = datos['almacenamiento']
                except ObjectDoesNotExist as e:
                    print("Almacenamiento no necesita actualizacion")
                try:
                    new_dispositivo.medida_almacenamiento = inv_m.DispositivoMedida.objects.get(id=datos['medida_almacenamiento'])
                except ObjectDoesNotExist as e:
                    print("Medida de almacenamiento no necesita actualizacion")
                try:
                    if datos['servidor']:
                        new_dispositivo.servidor = True
                    else:
                         new_dispositivo.servidor = False
                except ObjectDoesNotExist as e:
                    print("Servidor no necesita actualizacion")
                try:
                    new_dispositivo.codigo_rti =  datos["codigo_rti"]
                except ObjectDoesNotExist as e:
                    print("No necesita codigo RTI")                 
                new_dispositivo.save()
            
        elif tipo == "HDD":
            for datos in dispositivos:
                new_dispositivo = beqt_m.HDDBeqt.objects.get(triage=datos['triage'])
                try:
                    new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                except ObjectDoesNotExist as e:
                    print("Marca no necesita actualizar")
                try:
                    new_dispositivo.modelo = datos['modelo']
                except ObjectDoesNotExist as e:
                    print("Modelo no necesita actualizacion")
                try:
                    new_dispositivo.serie = datos['serie']
                except ObjectDoesNotExist as e:
                    print("Serie no necesita actualizacion")
                try:
                    new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                except ObjectDoesNotExist as e:
                    print("Tarima no necesita actualizacion")
                try:
                    new_dispositivo.puerto = inv_m.DispositivoPuerto.objects.get(id=datos['puerto'])
                except ObjectDoesNotExist as e:
                    print("Puerto no necesita actualizacion")
                try:
                    new_dispositivo.capacidad = datos['capacidad']
                except ObjectDoesNotExist as e:
                    print("Capacidad no necesita actualizacion")
                try:
                    new_dispositivo.medida = inv_m.DispositivoMedida.objects.get(id=datos['medida'])
                except ObjectDoesNotExist as e:
                    print("Medida no necesita actualizacion")
                try:
                    new_dispositivo.clase = inv_m.DispositivoClase.objects.get(id=datos['clase'])
                except ObjectDoesNotExist as e:
                    print("Clase no necesita actualizacion")
                try:
                    new_dispositivo.codigo_rti =  datos["codigo_rti"]
                except ObjectDoesNotExist as e:
                    print("No necesita codigo RTI") 
                new_dispositivo.save()
       
        elif tipo == "TABLET":
            
            for datos in dispositivos:
                new_dispositivo = beqt_m.TabletBeqt.objects.get(triage=datos['triage'])     
                try:
                    new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                except ObjectDoesNotExist as e:
                    print("Marca no necesita actualizar")
                try:
                    new_dispositivo.modelo = datos['modelo']
                except ObjectDoesNotExist as e:
                    print("Modelo no necesita actualizacion")
                try:
                    new_dispositivo.serie = datos['serie']
                except ObjectDoesNotExist as e:
                    print("Serie no necesita actualizacion")
                try:
                    new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                except ObjectDoesNotExist as e:
                    print("Tarima no necesita actualizacion")
                try:
                    new_dispositivo.procesador = inv_m.Procesador.objects.get(id=datos['procesador'])
                except ObjectDoesNotExist as e:
                    print("Procesador no necesita actualizacion")
                try:
                    new_dispositivo.version_sistema = inv_m.VersionSistema.objects.get(id=datos['version_sistema'])
                except ObjectDoesNotExist as e:
                    print("La version del sistema no necisita actualizacion")
                try:
                    new_dispositivo.ram = datos['ram']
                except ObjectDoesNotExist as e:
                    print("Memoria ram no necesita actualizacion")
                try:
                    new_dispositivo.medida_ram = inv_m.DispositivoMedida.objects.get(id=datos['medida_ram'])
                except ObjectDoesNotExist as e:
                    print("Medidad de ram no necesita actualizacion")
                try:
                    new_dispositivo.so_id = inv_m.Software.objects.get(id=datos['so_id'])
                except ObjectDoesNotExist as e:
                    print("Sistema operativo no necesita actualizacion")
                try:
                    new_dispositivo.pulgadas = datos['pulgadas']
                except ObjectDoesNotExist as e:
                    print("Pulgadas del monitor no necesita actualizacion")
                try:
                    new_dispositivo.almacenamiento = datos['almacenamiento']
                except ObjectDoesNotExist as e:
                    print("Almacenamiento no necesita actualizacion")
                try:
                    new_dispositivo.medida_almacenamiento = inv_m.DispositivoMedida.objects.get(
                        id=datos['medida_almacenamiento']
                        )
                except ObjectDoesNotExist as e:
                    print("Medida de almacenamiento no necesita actualizacion")
                # Datos del checkbox
                try:
                    if(str(datos['almacenamiento_externo']) == "false"):
                        new_dispositivo.almacenamiento_externo = False
                    else:
                        new_dispositivo.almacenamiento_externo = True
                except ObjectDoesNotExist as e:
                    print("almacenamiento externo no necesita actualizacion")
                try:
                    new_dispositivo.clase = inv_m.DispositivoClase.objects.get(id=datos['clase'])
                except ObjectDoesNotExist as e:
                    print("Clase no necesita actualizacion")
                try:
                    new_dispositivo.cargador = beqt_m.CargadorTabletBeqt.objects.get(triage=datos['cargador__triage'])
                except ObjectDoesNotExist as e:
                    print("El cargador no necesita actualizacion")
                try:
                    new_dispositivo.estuche = beqt_m.CaseTabletBeqt.objects.get(triage=datos['estuche__triage'])
                except ObjectDoesNotExist as e:
                    print("El cargador no necesita actualizacion")
                try:
                    new_dispositivo.protector = beqt_m.ProtectorTabletBeqt.objects.get(triage=datos['protector__triage'])
                except ObjectDoesNotExist as e:
                    print("El cargador no necesita actualizacion")
                try:
                    new_dispositivo.codigo_rti =  datos["codigo_rti"]
                except ObjectDoesNotExist as e:
                    print("No necesita codigo RTI") 
                new_dispositivo.save()      
        elif tipo == "ACCESS POINT":
            for datos in dispositivos:
                new_dispositivo = beqt_m.AccessPointBeqt.objects.get(triage=datos['triage'])
                try:
                    new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                except ObjectDoesNotExist as e:
                    print("Marca no necesita actualizar")
                try:
                    new_dispositivo.modelo = datos['modelo']
                except ObjectDoesNotExist as e:
                    print("Modelo no necesita actualizacion")
                try:
                    new_dispositivo.serie = datos['serie']
                except ObjectDoesNotExist as e:
                    print("Serie no necesita actualizacion")
                try:
                    new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                except ObjectDoesNotExist as e:
                    print("Tarima no necesita actualizacion")
                try:
                    new_dispositivo.puerto = inv_m.DispositivoPuerto.objects.get(id=datos['puerto'])
                except ObjectDoesNotExist as e:
                    print("Puerto no necesita actualizacion")
                try:
                    new_dispositivo.cantidad_puertos = datos['cantidad_puertos']
                except ObjectDoesNotExist as e:
                    print("Cantidad de puerto no necesita actualizacion")
                try:
                    new_dispositivo.velocidad = datos['velocidad']
                except ObjectDoesNotExist as e:
                    print("Velocidad de trasmicon no necesita actualizacion")
                try:
                    new_dispositivo.velocidad_medida = inv_m.DispositivoMedida.objects.get(id=datos['velocidad_medida'])
                except ObjectDoesNotExist as e:
                    print("Velocidad medida no necesita actualizacion")
                try:
                    new_dispositivo.clase = inv_m.DispositivoClase.objects.get(id=datos['clase'])
                except ObjectDoesNotExist as e:
                    print("Clase no necesita actualizacion")
                try:
                    new_dispositivo.codigo_rti =  datos["codigo_rti"]
                except ObjectDoesNotExist as e:
                    print("No necesita codigo RTI") 
                new_dispositivo.save()
        elif tipo == "SWITCH":
            for datos in dispositivos:
                new_dispositivo = beqt_m.DispositivoRedBeqt.objects.get(triage=datos['triage'])
                try:
                    new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                except ObjectDoesNotExist as e:
                    print("Marca no necesita actualizar")
                try:
                    new_dispositivo.modelo = datos['modelo']
                except ObjectDoesNotExist as e:
                    print("Modelo no necesita actualizacion")
                try:
                    new_dispositivo.serie = datos['serie']
                except ObjectDoesNotExist as e:
                    print("Serie no necesita actualizacion")
                try:
                    new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                except ObjectDoesNotExist as e:
                    print("Tarima no necesita actualizacion")
                try:
                    new_dispositivo.puerto = inv_m.DispositivoPuerto.objects.get(id=datos['puerto'])
                except ObjectDoesNotExist as e:
                    print("Puerto no necesita actualizacion")
                try:
                    new_dispositivo.cantidad_puertos = datos['cantidad_puertos']
                except ObjectDoesNotExist as e:
                    print("Cantidad de puerto no necesita actualizacion")
                try:
                    new_dispositivo.velocidad = datos['velocidad']
                except ObjectDoesNotExist as e:
                    print("Velocidad de trasmicon no necesita actualizacion")                
                try:
                    new_dispositivo.clase = inv_m.DispositivoClase.objects.get(id=datos['clase'])
                except ObjectDoesNotExist as e:
                    print("Clase no necesita actualizacion")
                try:
                    new_dispositivo.codigo_rti =  datos["codigo_rti"]
                except ObjectDoesNotExist as e:
                    print("No necesita codigo RTI") 
                new_dispositivo.save()
        elif tipo == "ADAPTADOR RED":
            for datos in dispositivos:
                new_dispositivo = beqt_m.DispositivoRedBeqt.objects.get(triage=datos['triage'])
                try:
                    new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                except ObjectDoesNotExist as e:
                    print("Marca no necesita actualizar")
                try:
                    new_dispositivo.modelo = datos['modelo']
                except ObjectDoesNotExist as e:
                    print("Modelo no necesita actualizacion")
                try:
                    new_dispositivo.serie = datos['serie']
                except ObjectDoesNotExist as e:
                    print("Serie no necesita actualizacion")
                try:
                    new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                except ObjectDoesNotExist as e:
                    print("Tarima no necesita actualizacion")
                try:
                    new_dispositivo.puerto = inv_m.DispositivoPuerto.objects.get(id=datos['puerto'])
                except ObjectDoesNotExist as e:
                    print("Puerto no necesita actualizacion")
                try:
                    new_dispositivo.cantidad_puertos = datos['cantidad_puertos']
                except ObjectDoesNotExist as e:
                    print("Cantidad de puerto no necesita actualizacion")
                try:
                    new_dispositivo.velocidad = datos['velocidad']
                except ObjectDoesNotExist as e:
                    print("Velocidad de trasmicon no necesita actualizacion")                
                try:
                    new_dispositivo.clase = inv_m.DispositivoClase.objects.get(id=datos['clase'])
                except ObjectDoesNotExist as e:
                    print("Clase no necesita actualizacion")
                try:
                    new_dispositivo.codigo_rti =  datos["codigo_rti"]
                except ObjectDoesNotExist as e:
                    print("No necesita codigo RTI") 
                new_dispositivo.save()

        elif tipo == "CARGADOR TABLET":
            for datos in dispositivos:
                new_dispositivo = beqt_m.CargadorTabletBeqt.objects.get(triage=datos['triage'])
                try:
                    new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                except ObjectDoesNotExist as e:
                    print("Marca no necesita actualizar")
                try:
                    new_dispositivo.modelo = datos['modelo']
                except ObjectDoesNotExist as e:
                    print("Modelo no necesita actualizacion")
                try:
                    new_dispositivo.serie = datos['serie']
                except ObjectDoesNotExist as e:
                    print("Serie no necesita actualizacion")
                try:
                    new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                except ObjectDoesNotExist as e:
                    print("Tarima no necesita actualizacion")
                try:
                    new_dispositivo.alimentacion = datos['alimentacion']
                except ObjectDoesNotExist as e:
                    print("Alimentacion electrica no necesita actualizacion")
                try:
                    new_dispositivo.salida = datos['salida']
                except ObjectDoesNotExist as e:
                    print("Salida de Voltaje no necesita actualizacion")                             
                try:
                    new_dispositivo.clase = inv_m.DispositivoClase.objects.get(id=datos['clase'])
                except ObjectDoesNotExist as e:
                    print("Clase no necesita actualizacion")
                try:
                    new_dispositivo.codigo_rti =  datos["codigo_rti"]
                except ObjectDoesNotExist as e:
                    print("No necesita codigo RTI") 
                new_dispositivo.save()
        elif tipo == "CARGADOR LAPTOP":
            for datos in dispositivos:
                new_dispositivo = beqt_m.CargadorLaptopBeqt.objects.get(triage=datos['triage'])
                try:
                    new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                except ObjectDoesNotExist as e:
                    print("Marca no necesita actualizar")
                try:
                    new_dispositivo.modelo = datos['modelo']
                except ObjectDoesNotExist as e:
                    print("Modelo no necesita actualizacion")
                try:
                    new_dispositivo.serie = datos['serie']
                except ObjectDoesNotExist as e:
                    print("Serie no necesita actualizacion")
                try:
                    new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                except ObjectDoesNotExist as e:
                    print("Tarima no necesita actualizacion")                
                try:
                    new_dispositivo.voltaje = datos['voltaje']
                except ObjectDoesNotExist as e:
                    print("Voltaje no necesita actualizacion")                             
                try:
                    new_dispositivo.clase = inv_m.DispositivoClase.objects.get(id=datos['clase'])
                except ObjectDoesNotExist as e:
                    print("Clase no necesita actualizacion")
                try:
                    new_dispositivo.codigo_rti =  datos["codigo_rti"]
                except ObjectDoesNotExist as e:
                    print("No necesita codigo RTI") 
                new_dispositivo.save()
        elif tipo == "ESTUCHE TABLET":
            for datos in dispositivos:
                new_dispositivo = beqt_m.CaseTabletBeqt.objects.get(triage=datos['triage'])
                try:
                    new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                except ObjectDoesNotExist as e:
                    print("Marca no necesita actualizar")
                try:
                    new_dispositivo.modelo = datos['modelo']
                except ObjectDoesNotExist as e:
                    print("Modelo no necesita actualizacion")
                try:
                    new_dispositivo.serie = datos['serie']
                except ObjectDoesNotExist as e:
                    print("Serie no necesita actualizacion")
                try:
                    new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                except ObjectDoesNotExist as e:
                    print("Tarima no necesita actualizacion")                
                try:
                    new_dispositivo.compatibilidad = datos['compatibilidad']
                except ObjectDoesNotExist as e:
                    print("Compatibilidad no necesita actualizacion") 

                try:
                    new_dispositivo.color = datos['color']
                except ObjectDoesNotExist as e:
                    print("Color no necesita actualizacion")
                try:
                    new_dispositivo.estilo = datos['estilo']
                except ObjectDoesNotExist as e:
                    print("Estilo no necesita actualizacion") 

                try:
                    new_dispositivo.material = datos['material']
                except ObjectDoesNotExist as e:
                    print("Material no necesita actualizacion") 

                try:
                    new_dispositivo.dimensiones = datos['dimensiones']
                except ObjectDoesNotExist as e:
                    print("Dimensiones no necesita actualizacion")                              
                try:
                    new_dispositivo.clase = inv_m.DispositivoClase.objects.get(id=datos['clase'])
                except ObjectDoesNotExist as e:
                    print("Clase no necesita actualizacion")
                try:
                    new_dispositivo.codigo_rti =  datos["codigo_rti"]
                except ObjectDoesNotExist as e:
                    print("No necesita codigo RTI") 
                new_dispositivo.save()


        elif tipo == "PROTECTOR TABLET": #Agregado a Cambios Protector Tablet
            for datos in dispositivos:
                new_dispositivo = beqt_m.ProtectorTabletBeqt.objects.get(triage=datos['triage'])
                try:
                    new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                except ObjectDoesNotExist as e:
                    print("Marca no necesita actualizar")
                try:
                    new_dispositivo.modelo = datos['modelo']
                except ObjectDoesNotExist as e:
                    print("Modelo no necesita actualizacion")
                try:
                    new_dispositivo.serie = datos['serie']
                except ObjectDoesNotExist as e:
                    print("Serie no necesita actualizacion")
                try:
                    new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                except ObjectDoesNotExist as e:
                    print("Tarima no necesita actualizacion")                
                try:
                    new_dispositivo.compatibilidad = datos['compatibilidad']
                except ObjectDoesNotExist as e:
                    print("Compatibilidad no necesita actualizacion") 

                try:
                    new_dispositivo.color = datos['color']
                except ObjectDoesNotExist as e:
                    print("Color no necesita actualizacion")

                try:
                    new_dispositivo.material = datos['material']
                except ObjectDoesNotExist as e:
                    print("Material no necesita actualizacion") 

                try:
                    new_dispositivo.dimensiones = datos['dimensiones']
                except ObjectDoesNotExist as e:
                    print("Dimensiones no necesita actualizacion")                              
                try:
                    new_dispositivo.clase = inv_m.DispositivoClase.objects.get(id=datos['clase'])
                except ObjectDoesNotExist as e:
                    print("Clase no necesita actualizacion")
                try:
                    new_dispositivo.codigo_rti =  datos["codigo_rti"]
                except ObjectDoesNotExist as e:
                    print("No necesita codigo RTI") 
                new_dispositivo.save()

        elif tipo == "REGLETA":
            for datos in dispositivos:
                new_dispositivo = beqt_m.RegletaBeqt.objects.get(triage=datos['triage'])
                try:
                    new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                except ObjectDoesNotExist as e:
                    print("Marca no necesita actualizar")
                try:
                    new_dispositivo.modelo = datos['modelo']
                except ObjectDoesNotExist as e:
                    print("Modelo no necesita actualizacion")
                try:
                    new_dispositivo.serie = datos['serie']
                except ObjectDoesNotExist as e:
                    print("Serie no necesita actualizacion")
                try:
                    new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                except ObjectDoesNotExist as e:
                    print("Tarima no necesita actualizacion")                
                try:
                    new_dispositivo.conexiones = datos['conexiones']
                except ObjectDoesNotExist as e:
                    print("Conexiones no necesita actualizacion")
                try:
                    new_dispositivo.voltaje = datos['voltaje']
                except ObjectDoesNotExist as e:
                    print("Voltaje no necesita actualizacion")                             
                try:
                    new_dispositivo.clase = inv_m.DispositivoClase.objects.get(id=datos['clase'])
                except ObjectDoesNotExist as e:
                    print("Clase no necesita actualizacion")
                try:
                    new_dispositivo.codigo_rti =  datos["codigo_rti"]
                except ObjectDoesNotExist as e:
                    print("No necesita codigo RTI")
                try:
                    if datos['regulador']:
                        new_dispositivo.regulador = True
                    else:
                         new_dispositivo.regulador = False
                except ObjectDoesNotExist as e:
                    print("No actualizar regulador") 
                new_dispositivo.save()

        elif tipo == "UPS":
            for datos in dispositivos:
                new_dispositivo = beqt_m.UpsBeqt.objects.get(triage=datos['triage'])
                try:
                    new_dispositivo.marca = inv_m.DispositivoMarca.objects.get(id=datos['marca'])
                except ObjectDoesNotExist as e:
                    print("Marca no necesita actualizar")
                try:
                    new_dispositivo.modelo = datos['modelo']
                except ObjectDoesNotExist as e:
                    print("Modelo no necesita actualizacion")
                try:
                    new_dispositivo.serie = datos['serie']
                except ObjectDoesNotExist as e:
                    print("Serie no necesita actualizacion")
                try:
                    new_dispositivo.tarima = inv_m.Tarima.objects.get(id=datos['tarima'])
                except ObjectDoesNotExist as e:
                    print("Tarima no necesita actualizacion")                
                try:
                    new_dispositivo.conexiones = datos['conexiones']
                except ObjectDoesNotExist as e:
                    print("Conexiones no necesita actualizacion")
                try:
                    new_dispositivo.voltaje = datos['voltaje']
                except ObjectDoesNotExist as e:
                    print("Voltaje no necesita actualizacion")                             
                try:
                    new_dispositivo.clase = inv_m.DispositivoClase.objects.get(id=datos['clase'])
                except ObjectDoesNotExist as e:
                    print("Clase no necesita actualizacion")
                try:
                    new_dispositivo.codigo_rti =  datos["codigo_rti"]
                except ObjectDoesNotExist as e:
                    print("No necesita codigo RTI") 
                new_dispositivo.save()
        else:
            for datos in dispositivos:
                new_dispositivo = beqt_m.DispositivoBeqt.objects.get(triage=datos['triage'])
                new_dispositivo.serie = datos['serie']
                new_dispositivo.codigo_rti = datos['codigo_rti']
                new_dispositivo.save()


        return Response({
            'mensaje': 'Actualizados'
        },
            status=status.HTTP_200_OK)

class SolicitudMovimientoFilter(filters.FilterSet):
    """ Filtros para generar informe de  Salida
    """
    estado = django_filters.NumberFilter(name='estado', method='filter_estado')
    fecha_min = django_filters.DateFilter(name='fecha_min', method='filter_fecha')
    fecha_max = django_filters.DateFilter(name='fecha_max', method='filter_fecha')

    class Meta:
        model = beqt_m.SolicitudMovimientoBeqt
        fields = ['estado','tipo_dispositivo','fecha_min', 'fecha_max']

    def filter_fecha(self, queryset, name, value):
        if value and name == 'fecha_min':
            queryset = queryset.filter(fecha_creacion__gte=value)
        if value and name == 'fecha_max':
            queryset = queryset.filter(fecha_creacion__lte=value)
        return queryset

    def filter_estado(self, queryset, name, value):
        if value == 0:
            queryset = queryset.filter(terminada=False, recibida=False, rechazar=False)
        if value == 1:
            queryset = queryset.filter(terminada=True, recibida=False, rechazar=False)
        if value == 2:
            queryset = queryset.filter(terminada=True, recibida=True, rechazar=False)
        if value == 3:
            queryset = queryset.filter(rechazar=True)
        return queryset

class SolicitudMovimientoViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar los informe de la :class:`SolicitudMovimiento`
    """
    serializer_class = beqt_s.SolicitudMovimientoSerializer
    filter_class = SolicitudMovimientoFilter
    ordering = ('-id')

    def get_queryset(self):
        """ Este queryset se encarga de filtar las solicitudes que se van a mostrar en el listado general
        """

        fecha_min = self.request.query_params.get('fecha_min', None)
        fecha_max = self.request.query_params.get('fecha_max', None)
        filtros = False

        # Obtener valores de lista para tipo
        try:
            tipo_solicitud = []
            tipo_solicitud = self.request.GET.getlist('devolucion[]')
            if len(tipo_solicitud) == 0:
                tipo = self.request.GET['devolucion']
                tipo_solicitud.append(tipo)
        except MultiValueDictKeyError as e:
            tipo_solicitud = 0

        # Obtener valores de lista para estado
        try:
            estado = []
            estado = self.request.GET.getlist('estado[]')
            if len(estado) == 0:
                tipo = self.request.GET['estado']
                estado.append(tipo)
        except MultiValueDictKeyError as e:
            estado = 0

        # Obtener valores de lista para tipo de dispositivo
        try:
            tipo_dispositivo = []
            tipo_dispositivo = self.request.GET.getlist('tipo_dispositivo[]')
            if len(tipo_dispositivo) == 0:
                tipo = self.request.GET['tipo_dispositivo']
                tipo_dispositivo.append(tipo)
        except MultiValueDictKeyError as e:
            tipo_dispositivo = 0

        # Filtrar por tipos de dispositivos seleccionados
        if tipo_dispositivo == 0 or not tipo_dispositivo:
            tipo_dis = self.request.user.tipos_dispositivos_beqt.tipos.all()
        else:
            tipo_dis = tipo_dispositivo
            filtros = True
        queryset = beqt_m.SolicitudMovimientoBeqt.objects.all().filter(tipo_dispositivo__in=tipo_dis)

        # Filtrar por estados seleccionados
        if estado and estado != 0:
            filtros = True
            init_solicitudes = beqt_m.SolicitudMovimientoBeqt.objects.none()
            queryset_pendientes = queryset_entregados = queryset_recibidos = queryset_rechazados = init_solicitudes
            if '0' in estado:
                queryset_pendientes = queryset.filter(terminada=False, recibida=False, rechazar=False)
            if '1' in estado:
                queryset_entregados = queryset.filter(terminada=True, recibida=False, rechazar=False)
            if '2' in estado:
                queryset_recibidos = queryset.filter(terminada=True, recibida=True, rechazar=False)
            if '3' in estado:
                queryset_rechazados = queryset.filter(rechazar=True)

            queryset = queryset_pendientes | queryset_entregados | queryset_recibidos | queryset_rechazados

        if tipo_solicitud and tipo_solicitud != 0:
            filtros = True

        # Obtener data en caso no hayan seleccionado filtros
        if not filtros and fecha_min is None and fecha_max is None:
            if "beqt_bodega" in self.request.user.groups.values_list('name', flat=True):
                queryset = queryset.filter(recibida=False, rechazar=False)
            else:
                queryset = queryset.filter(recibida=False)



        # Obtener data en caso sean técnicos.
        # if "inv_tecnico" in self.request.user.groups.values_list('name', flat=True) or "inv_cc" in self.request.user.groups.values_list('name', flat=True):
        #    queryset = queryset.filter(creada_por=self.request.user)

        return queryset
