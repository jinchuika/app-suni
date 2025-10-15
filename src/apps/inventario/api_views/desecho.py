import django_filters
from django_filters import rest_framework as filter
from django_filters import rest_framework as filters
from rest_framework import status, viewsets, views
from rest_framework.decorators import action
from rest_framework.response import Response
from braces.views import LoginRequiredMixin
from apps.conta import models as conta_m
from apps.inventario import (
    serializers as inv_s,
    models as inv_m
)


class DesechoDetalleViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar los detalles de la :class:`DesechoDetalle`
    """
    serializer_class = inv_s.DesechoDetalleSerializer
    queryset = inv_m.DesechoDetalle.objects.all()
    filter_fields = ('desecho',)


class DesechoDispositivoViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar las tablas de la :class:'EntradaDetalle'
    """
    serializer_class = inv_s.DesechoDispositivoSerializer
    queryset = inv_m.DesechoDispositivo.objects.all()
    filter_fields = ('desecho',)

    @action(methods=['post'], detail=False)
    def aprobar_detalle(self, request, pk=None):
        """Metodo para devolver los dispositivos que fueron prestados
        """
        if "inv_bodega" in self.request.user.groups.values_list('name', flat=True):
            return Response(
                {'mensaje': 'No Tienes la Autorizacion para esta accion'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            id_detalle = request.data["detalle"]
            detalle = inv_m.DesechoDetalle.objects.get(id=id_detalle)
            detalle.aprobado = True
            detalle.save()
            return Response(
                    {
                        'mensaje': 'Detalle Aprobado'
                    },
                    status=status.HTTP_200_OK
                )

    @action(methods=['post'], detail=False)
    def rechazar_detalle(self, request, pk=None):
        """Metodo para devolver los dispositivos que fueron prestados
        """
        if "inv_bodega" in self.request.user.groups.values_list('name', flat=True):
            return Response(
                {'mensaje': 'No Tienes la Autorizacion para esta accion'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            id_detalle = request.data["detalle"]
            comentario = request.data["comentario"]
            detalle = inv_m.DesechoDetalle.objects.get(id=id_detalle)
            comentario_rechazar_detalle=inv_m.DesechoComentario(
                desecho= detalle.desecho,
                comentario = comentario,
                creado_por= self.request.user,
                entrada_detalle= detalle.entrada_detalle
            )
            comentario_rechazar_detalle.save()
            detalle.delete()
            return Response(
                    {
                        'mensaje': 'Detalle Eliminado'
                    },
                    status=status.HTTP_200_OK
                )

    @action(methods=['post'], detail=False)
    def aprobar_dispositivo(self, request, pk=None):
        """Metodo para devolver los dispositivos que fueron prestados
        """
        if "inv_bodega" in self.request.user.groups.values_list('name', flat=True):
            return Response(
                {'mensaje': 'No Tienes la Autorizacion para esta accion'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            id_detalle = request.data["detalle"]
            detalle = inv_m.DesechoDispositivo.objects.get(id=id_detalle)
            detalle.aprobado = True
            detalle.save()
            return Response(
                    {
                        'mensaje': 'Dispositivo Aprobado'
                    },
                    status=status.HTTP_200_OK
                )

    @action(methods=['post'], detail=False)
    def rechazar_dispositivo(self, request, pk=None):
        """Metodo para devolver los dispositivos que fueron prestados
        """
        if "inv_bodega" in self.request.user.groups.values_list('name', flat=True):
            return Response(
                {'mensaje': 'No Tienes la Autorizacion para esta accion'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            id_detalle = request.data["detalle"]
            comentario = request.data["comentario"]
            detalle = inv_m.DesechoDispositivo.objects.get(id=id_detalle)
            comentario_rechazar_detalle=inv_m.DesechoComentario(
                desecho= detalle.desecho,
                comentario = comentario,
                creado_por= self.request.user,
                dispositivo= detalle.dispositivo
            )
            comentario_rechazar_detalle.save()
            detalle.delete()
            return Response(
                    {
                        'mensaje': 'Dispositivo Rechazado'
                    },
                    status=status.HTTP_200_OK
                )

    @action(methods=['post'], detail=False)
    def finalizar_desecho(self, request, pk=None):
        """Metodo para finalizar  la salida de desecho
        """
        if "inv_bodega" in self.request.user.groups.values_list('name', flat=True):
            return Response(
                {'mensaje': 'No Tienes la Autorizacion para esta acción'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            id_desecho = request.data["id"]
            desecho = inv_m.DesechoSalida.objects.get(id=id_desecho)
            if desecho.revision_sub_jefe==True and desecho.revision_jefe==True:
                detalles = inv_m.DesechoDetalle.objects.filter(desecho=id_desecho).count()
                detalles_aprobados = inv_m.DesechoDetalle.objects.filter(desecho=id_desecho, aprobado=True).count()
                dispositivos = inv_m.DesechoDispositivo.objects.filter(desecho=id_desecho).count()
                dispositivos_aprobados = inv_m.DesechoDispositivo.objects.filter(desecho=id_desecho, aprobado=True).count()
                aprobar_dispositivos = inv_m.DesechoDispositivo.objects.filter(desecho=id_desecho)
                solicitudes = inv_m.DesechoSolicitud.objects.filter(desecho=id_desecho, rechazado=False).count()
                solicitudes_aprobadas = inv_m.DesechoSolicitud.objects.filter(desecho=id_desecho, aprobado=True).count()
                dispo_solicitud = inv_m.DesechoSolicitud.objects.filter(desecho=id_desecho, rechazado=False, aprobado=True)
                if detalles_aprobados == detalles:
                    if dispositivos_aprobados == dispositivos and solicitudes == solicitudes_aprobadas:
                        periodo_actual = conta_m.PeriodoFiscal.objects.get(actual=True)
                        for aprobar in aprobar_dispositivos:
                            precio = conta_m.PrecioDispositivo.objects.get(dispositivo = aprobar.dispositivo, activo= True)
                            aprobar.dispositivo.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.DS)
                            aprobar.dispositivo.valido = False
                            aprobar.dispositivo.creada_por = self.request.user
                            aprobar.dispositivo.save()

                            # Generar movimiento de salida
                            movimiento = conta_m.MovimientoDispositivo(
                                fecha=desecho.fecha,
                                dispositivo=aprobar.dispositivo,
                                periodo_fiscal=periodo_actual,
                                tipo_movimiento=conta_m.MovimientoDispositivo.BAJA,
                                referencia='Salida Desecho{}'.format(desecho.id),
                                precio=precio.precio,
                                creado_por = self.request.user)
                            movimiento.save()

                        for solicitud in dispo_solicitud:
                            precio = conta_m.PrecioDispositivo.objects.get(dispositivo = solicitud.dispositivo, activo= True)
                            solicitud.dispositivo.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.DS)
                            solicitud.dispositivo.valido = False
                            solicitud.dispositivo.save()

                            # Generar movimiento de salida
                            movimiento = conta_m.MovimientoDispositivo(
                                fecha=desecho.fecha,
                                dispositivo=solicitud.dispositivo,
                                periodo_fiscal=periodo_actual,
                                tipo_movimiento=conta_m.MovimientoDispositivo.BAJA,
                                referencia='Salida Desecho{}'.format(desecho.id),
                                precio=precio.precio,
                                creado_por = self.request.user)
                            movimiento.save()


                        desecho.en_creacion = False
                        desecho.save()
                        return Response(
                                {
                                    'mensaje': 'Salida de Desecho Finalizada'
                                },
                                status=status.HTTP_200_OK
                            )
                    else:
                        return Response(
                            {'mensaje': 'Faltan dispositivos por aprobar'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {'mensaje': 'Faltan detalles de desecho por aprobar'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'mensaje': 'No  puede cerrar aun el desecho falta que lo revise el supervisor de producción o  la administradora del  centro de reacondicionamiento comuníquese con alguno de los 2 para poder resolver el problema '},
                    status=status.HTTP_400_BAD_REQUEST
                )


class DesechoSolicitudViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar los detalles de la :class:`DesechoDetalle`
    """
    serializer_class = inv_s.DesechoSolicitudSerializer
    queryset = inv_m.DesechoSolicitud.objects.all()

    def get_queryset(self):
            queryset = super().get_queryset()
            desecho_id = self.request.query_params.get('desecho')
            if desecho_id:
                queryset = queryset.filter(desecho_id=desecho_id, rechazado= False)
            return queryset
    
    def create(self, request, *args, **kwargs):
        desecho_id = request.data.get('desecho')
        solicitud_id = request.data.get('solicitud')
        if not desecho_id or not solicitud_id:
            return Response({"error": "Debe enviar 'desecho' y 'solicitud'"}, status=400)

        try:
            solicitud = inv_m.SolicitudMovimiento.objects.get(pk=solicitud_id)
        except inv_m.SolicitudMovimiento.DoesNotExist:
            return Response({"error": "SolicitudMovimiento no encontrada"}, status=404)
        solicitud.etapa_final = inv_m.DispositivoEtapa.objects.get(pk=inv_m.DispositivoEtapa.DS)
        solicitud.save()

        dispositivos = inv_m.CambioEtapa.objects.filter(solicitud=solicitud)
        
        for cambio in dispositivos:
            obj = inv_m.DesechoSolicitud.objects.create(
                desecho_id=desecho_id,
                solicitud=solicitud,
                dispositivo=cambio.dispositivo,
                creada_por=request.user,
                aprobado=False,
                rechazado=False
            )
        dispositivos = inv_m.CambioEtapa.objects.filter(solicitud=solicitud)

        return Response({'mensaje': 'Dispositivos agregados con exito'},status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=False)
    def aprobar_dispositivo(self, request, pk=None):
        """Metodo para devolver los dispositivos que fueron prestados
        """
        if "inv_bodega" in self.request.user.groups.values_list('name', flat=True):
            return Response(
                {'mensaje': 'No Tienes la Autorizacion para esta accion'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            solicitud = request.data["solicitud"]
            solicitud_desecho = inv_m.DesechoSolicitud.objects.get(id=solicitud)
            solicitud_desecho.aprobado = True
            solicitud_desecho.save()
            return Response(
                    {
                        'mensaje': 'Dispositivo Aprobado'
                    },
                    status=status.HTTP_200_OK
                )

    @action(methods=['post'], detail=False)
    def rechazar_dispositivo(self, request, pk=None):
        """Metodo para devolver los dispositivos que fueron prestados
        """
        if "inv_bodega" in self.request.user.groups.values_list('name', flat=True):
            return Response(
                {'mensaje': 'No Tienes la Autorizacion para esta accion'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            solicitud = request.data["solicitud"]
            comentario = request.data["comentario"]
            solicitud_desecho = inv_m.DesechoSolicitud.objects.get(id=solicitud)
            solicitud_desecho.rechazado = False
            comentario_rechazar_detalle=inv_m.DesechoComentario(
                desecho= solicitud_desecho.desecho,
                comentario = comentario,
                creado_por= self.request.user,
                dispositivo= solicitud_desecho.dispositivo
            )
            comentario_rechazar_detalle.save()
            solicitud_desecho.rechazado = True
            solicitud_desecho.save()
            dispositivo = solicitud_desecho.dispositivo
            dispositivo.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.AB)
            dispositivo.save()

            return Response(
                    {
                        'mensaje': 'Dispositivo Rechazado'
                    },
                    status=status.HTTP_200_OK
                )

    

class DesechoSalidaFilter(filters.FilterSet):
    """ Filtros para generar informe de  Salida
    """
    id = django_filters.NumberFilter(name="id")
    en_creacion = django_filters.CharFilter(name='en_creacion')
    fecha_min = django_filters.DateFilter(name='fecha_min', method='filter_fecha')
    fecha_max = django_filters.DateFilter(name='fecha_max', method='filter_fecha')

    class Meta:
        model = inv_m.DesechoSalida
        fields = ['id', 'en_creacion', 'fecha_min', 'fecha_max']

    def filter_fecha(self, queryset, name, value):
        if value and name == 'fecha_min':
            queryset = queryset.filter(fecha__gte=value)
        if value and name == 'fecha_max':
            queryset = queryset.filter(fecha__lte=value)
        return queryset

class DesechoSalidaViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar los listado de la :class:`DesechoSalida`
    """
    serializer_class = inv_s.DesechoSalidaSerializer
    queryset = inv_m.DesechoSalida.objects.all()
    filter_class = DesechoSalidaFilter

class CambioEtapaAPIViewSet(viewsets.ModelViewSet):
    serializer_class = inv_s.CambioEtapaSerializer
    queryset = inv_m.CambioEtapa.objects.all()