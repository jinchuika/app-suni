from django.db.utils import OperationalError

import django_filters
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from braces.views import LoginRequiredMixin
from django.db.models import Q
from apps.inventario import (
    serializers as inv_s,
    models as inv_m
)


class DetalleInformeFilter(filters.FilterSet):
    """ Filtro para generar los informes de Detalles de Entrada
    """
    tipo = django_filters.CharFilter(name='entrada')
    asignacion = filters.NumberFilter(name='asignacion', method='filter_asignacion')

    class Meta:
        model = inv_m.EntradaDetalle
        fields = ['entrada']

    def filter_asignacion(self, qs, name, value):
        tipo_dis = self.request.user.tipos_dispositivos.tipos.all()
        return qs.filter(entrada=value, tipo_dispositivo__in=tipo_dis)


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
        if "inv_tecnico" in self.request.user.groups.values_list('name', flat=True):
            return Response(
                {'mensaje': 'No Tienes la Autorizacion para esta accion'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
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
                {'mensaje': 'Dispositivos impresos'},
                status=status.HTTP_200_OK
            )

    @action(methods=['post'], detail=False)
    def cuadrar_salida(self, request, pk=None):
        """ Metodo para cuadrar los dispositivos de la :class:`EntradaDetalle`
        """

        if "inv_tecnico" in self.request.user.groups.values_list('name', flat=True):
            return Response(
                {'mensaje': 'No Tienes la Autorizacion para esta accion'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            mensaje_cuadrar = ""
            entrad_id = request.data['primary_key']
            dispositivos_utiles = inv_m.EntradaDetalle.objects.filter(Q(entrada=entrad_id),Q(util__gt = 0)).count()
            repuestos_utiles = inv_m.EntradaDetalle.objects.filter(Q(entrada=entrad_id),Q(repuesto__gt = 0)).count()
            validar_dispositivos = inv_m.EntradaDetalle.objects.filter(Q(entrada=entrad_id),Q(util__gt = 0) , dispositivos_creados=True).count()
            validar_repuestos = inv_m.EntradaDetalle.objects.filter(Q(entrada=entrad_id),Q(repuesto__gt = 0), repuestos_creados=True).count()

            tipo_dispositivo = inv_m.EntradaDetalle.objects.filter(entrada=entrad_id).values('tipo_dispositivo').distinct()
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
                    tipos_sin_cuadrar.append("<br><b>" + str(datos.tipo_dispositivo) + "</b>")

            if(len(tipos_sin_cuadrar) > 0):
                return Response(
                      {'mensaje': 'La entrada no esta cuadrada revisar:' + ', '.join(str(x) for x in tipos_sin_cuadrar)},
                      status=status.HTTP_400_BAD_REQUEST
                  )
            elif(dispositivos_utiles != validar_dispositivos or repuestos_utiles != validar_repuestos):
                return Response(
                    {'mensaje': 'Los dispositivos o repuestos no  han sido creados'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {'mensaje': 'Entrada Cuadrada'},
                    status=status.HTTP_200_OK
                )             
           
    @action(methods=['post'], detail=True)
    def crear_dispositivos(self, request, pk=None):
        """ Metodo para la Creacion de Dispositivos
        """
        if "inv_tecnico" in self.request.user.groups.values_list('name', flat=True):
            return Response(
                {'mensaje': 'No Tienes la Autorizacion para esta accion'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            entrada_detalle = self.get_object()
            try:
                entrada = entrada_detalle.entrada
                if not entrada.tipo.contenedor:
                    total = entrada_detalle.util + entrada_detalle.repuesto + entrada_detalle.desecho
                    if entrada_detalle.total != total:
                        return Response(
                            {'mensaje': 'La línea de detalle no cuadra, revisar'},
                            status=status.HTTP_400_BAD_REQUEST)

                creacion = entrada_detalle.crear_dispositivos()
                validar_dispositivos = inv_m.EntradaDetalle.objects.get(id=pk)
                validar_dispositivos.dispositivos_creados = True
                validar_dispositivos.save()
                return Response(
                    creacion,
                    status=status.HTTP_200_OK)
            except OperationalError as e:
                return Response(
                    {'mensaje': str(e)},
                    status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def crear_repuestos(self, request, pk=None):
        """ Metodo para la creacion de Repuestos
        """
        if "inv_tecnico" in self.request.user.groups.values_list('name', flat=True):
            return Response(
                {'mensaje': 'No Tienes la Autorizacion para esta accion'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            entrada_detalle = self.get_object()
            try:
                entrada = entrada_detalle.entrada
                if not entrada.tipo.contenedor:
                    total = entrada_detalle.util + entrada_detalle.repuesto + entrada_detalle.desecho
                    if entrada_detalle.total != total:
                        return Response(
                            {'mensaje': 'La línea de detalle no cuadra, revisar'},
                            status=status.HTTP_400_BAD_REQUEST)

                creacion = entrada_detalle.crear_repuestos()
                validar_dispositivos = inv_m.EntradaDetalle.objects.get(id=pk)
                validar_dispositivos.repuestos_creados = True
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


class EntradaFilter(filters.FilterSet):
    """ Filtros para generar informe de Entrada
    """

    proveedor = django_filters.CharFilter(name='proveedor')
    tipo = django_filters.CharFilter(name='tipo')
    recibida_por = django_filters.CharFilter(name='recibida_por')
    fecha_min = django_filters.DateFilter(name='fecha_min', method='filter_fecha')
    fecha_max = django_filters.DateFilter(name='fecha_max', method='filter_fecha')

    class Meta:
        model = inv_m.Entrada
        fields = ['proveedor', 'tipo', 'recibida_por', 'fecha_min', 'fecha_max']

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
