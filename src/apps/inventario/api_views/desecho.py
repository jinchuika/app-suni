import django_filters
from django_filters import rest_framework as filter
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
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
            detalles = inv_m.DesechoDetalle.objects.filter(desecho=id_desecho).count()
            detalles_aprobados = inv_m.DesechoDetalle.objects.filter(desecho=id_desecho, aprobado=True).count()
            dispositivos = inv_m.DesechoDispositivo.objects.filter(desecho=id_desecho).count()
            dispositivos_aprobados = inv_m.DesechoDispositivo.objects.filter(desecho=id_desecho, aprobado=True).count()
            aprobar_dispositivos = inv_m.DesechoDispositivo.objects.filter(desecho=id_desecho)
            if detalles_aprobados == detalles:
                if dispositivos_aprobados == dispositivos:
                    periodo_actual = conta_m.PeriodoFiscal.objects.get(actual=True)                    
                    for aprobar in aprobar_dispositivos:
                        precio = conta_m.PrecioDispositivo.objects.get(dispositivo = aprobar.dispositivo, activo= True)
                        aprobar.dispositivo.etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.DS)
                        aprobar.dispositivo.valido = False
                        aprobar.dispositivo.save()

                        # Generar movimiento de salida
                        movimiento = conta_m.MovimientoDispositivo(
                            fecha=desecho.fecha,
                            dispositivo=aprobar.dispositivo,
                            periodo_fiscal=periodo_actual,
                            tipo_movimiento=conta_m.MovimientoDispositivo.BAJA,
                            referencia='Salida Desecho{}'.format(desecho.id),
                            precio=precio.precio)
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