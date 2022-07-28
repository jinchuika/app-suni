import django_filters
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from braces.views import LoginRequiredMixin
from datetime import datetime
from apps.recaudacionFondos import (
    serializers as rf_s,
    models as rf_m
)


class ProveedorViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informes de :class:`Proveedor`
    """
    serializer_class = rf_s.ProveedorSerializer
    queryset = rf_m.Proveedor.objects.all()
    filter_fields = ('id',)

    @action(methods=['post'], detail=False)
    def crear_proveedor(self, request, pk=None):
        """ Punto de acceso para poder crear proveedores desde el pop up
        """
        nombre = request.data["nombre"]
        email = request.data["email"]
        telefono = request.data["telefono"]
        direccion = request.data["direccion"]
        if nombre:
            nuevo_proveedor = rf_m.Proveedor(
             nombre = nombre,
             correo =  email,
             numero = telefono,
             direccion = direccion
            )
            nuevo_proveedor.save()
            return Response(
                    {
                        'mensaje': 'Proveedor ingresado correctamente'
                    },
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                    {
                        'mensaje': 'Ingrese el nombre de un proveedor'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )


class EntradaFilter(django_filters.FilterSet):
    fecha_inicio = django_filters.DateFilter(name='fecha', lookup_expr='gte')
    fecha_fin = django_filters.DateFilter(name='fecha', lookup_expr='lte')
    equipo = django_filters.NumberFilter(name='detalles__equipo')

    class Meta:
        model = rf_m.Entrada
        fields = ['fecha_inicio', 'fecha_fin', 'proveedor', 'equipo', 'id']

class EntradaViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informes de :class:`Entrada`
    """
    serializer_class = rf_s.EntradaSerializer
    queryset = rf_m.Entrada.objects.all()
    #filter_fields = ('id',)
    filter_class = EntradaFilter

    @action(methods=['post'], detail=False)
    def cerrar_entrada(self, request, pk=None):
        """ Punto de acceso para poder cerrar la entrada
        """
        id = request.data["id"]
        entrada = rf_m.Entrada.objects.get(id = id)
        fecha_actual =  datetime.today().strftime('%Y-%m-%d')
        fecha_entrada = datetime.strftime(entrada.fecha, '%Y-%m-%d')

        detalle_entrada = rf_m.DetalleEntrada.objects.filter(entrada = entrada).count()
        if fecha_actual >= fecha_entrada:
            if detalle_entrada != 0 :
                entrada.terminada = True
                entrada.save()
            else:
                return Response(
                        {
                            'mensaje': 'Falta el detalle de la entrada para poder finalizar la entrada'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

        else:
            return Response(
                    {
                        'mensaje': 'Faltan dias para poder cerrar la entrada'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
                    {
                        'mensaje': 'Entrada Finalizada correctamente '
                    },
                    status=status.HTTP_200_OK
                )

class ArticuloViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informes de :class:`Entrada`
    """
    serializer_class = rf_s.ArticuloSerializer
    queryset = rf_m.Articulo.objects.all()
    filter_fields = ('id',)


class DetalleEntradaViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informes de :class:`Proveedor`
    """
    serializer_class = rf_s.DetalleEntradaSerializer
    queryset = rf_m.DetalleEntrada.objects.all()
    filter_fields = ('id','entrada__id','articulo')

class SalidaFilter(django_filters.FilterSet):
    fecha_inicio_salida = django_filters.DateFilter(name='fecha', lookup_expr='gte')
    fecha_fin_salida = django_filters.DateFilter(name='fecha', lookup_expr='lte')


    class Meta:
        model = rf_m.Salida
        fields = ['fecha_inicio_salida', 'fecha_fin_salida', 'id']

class SalidaViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informes de :class:`Entrada`
    """
    serializer_class = rf_s.SalidaSerializer
    queryset = rf_m.Salida.objects.all()
    #filter_fields = ('id',)
    filter_class = SalidaFilter

    @action(methods=['post'], detail=False)
    def cerrar_salida(self, request, pk=None):
        """ Punto de acceso para poder cerrar la entrada
        """
        id = request.data["id"]
        salida = rf_m.Salida.objects.get(id = id)
        fecha_actual =  datetime.today().strftime('%Y-%m-%d')
        fecha_salida = datetime.strftime(salida.fecha, '%Y-%m-%d')

        detalle_salida = rf_m.DetalleSalida.objects.filter(salida = salida).count()
        if fecha_actual >= fecha_salida:            
            if detalle_salida != 0 :
                salida.terminada = True
                salida.save()
            else:
                return Response(
                        {
                            'mensaje': 'Falta el detalle de la salida para poder finalizar la entrada'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

        else:
            return Response(
                    {
                        'mensaje': 'Faltan dias para poder cerrar la salida'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
                    {
                        'mensaje': 'Salida Finalizada correctamente '
                    },
                    status=status.HTTP_200_OK
                )
class DetalleSalidaViewSet(viewsets.ModelViewSet):
    """ ViewSet para generar informes de :class:`Proveedor`
    """
    serializer_class = rf_s.DetalleSalidaSerializer
    queryset = rf_m.DetalleSalida.objects.all()
    filter_fields = ('id','salida__id','articulo')
