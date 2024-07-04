import django_filters
from braces.views import CsrfExemptMixin
from rest_framework import generics, viewsets, status
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, timedelta
import json
import datetime as dt

from apps.main.mixins import APIFilterMixin
from apps.cyd.serializers import (
    SedeSerializer, GrupoSerializer, CalendarioSerializer,
    AsignacionSerializer, ParticipanteSerializer,
    NotaAsistenciaSerializer, NotaHitoSerializer, AsesoriaSerializer,
    AsesoriaCalendarSerializer, EscuelaCalendarioSerializer, RecordatorioSerializer)
from apps.cyd.models import (
    Sede, Grupo, Calendario, Asignacion, Participante,
    NotaAsistencia, NotaHito, Asesoria,Curso, RecordatorioCalendario, ParGenero)


def crear_calendario(grupo):
    for asistencia in grupo.curso.asistencias.all():
        nueva_asistencia = Calendario(
            cr_asistencia=asistencia,
            grupo=grupo,
            fecha=datetime.now(),
            hora_inicio=dt.time(0,0,0),
            hora_fin=dt.time(0,0,0),
            observacion='',
            cyd_calendario_creado_por=grupo.cyd_grupo_creado_por
        )
        nueva_asistencia.save()

class GrupoViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    serializer_class = GrupoSerializer
    queryset = Grupo.objects.all()
    filter_fields = ('sede', 'curso', 'activo','numero', 'cyd_grupo_creado_por')

    def get_queryset(self):
        queryset = Grupo.objects.all()
        if "cyd_capacitador" in self.request.user.groups.values_list('name', flat=True):
            queryset = Grupo.objects.filter(sede__in=self.request.user.sedes.filter(activa=True))
        return queryset

    @action(methods=['post'], detail=False)
    def desactivar_grupo(self,request, pk=None):
        """ Metodo  que cambia la disponibilidad del grupo
        """
        id_grupo= request.data['primary_key']        
        try:
            eliminar_grupo= request.data['eliminar']
        except Exception:
            eliminar_grupo=0
        if eliminar_grupo==0:
            grupo = Grupo.objects.get(id=id_grupo)
            grupo.activo = False
            grupo.save()
        else:
            grupo = Grupo.objects.get(id=id_grupo)
            grupo.delete()
        return Response(
            {'mensaje': 'Cambio Aceptado'},
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False)
    def desactivar_curso(self,request, pk=None):
        """ Metodo  que cambia la disponibilidad del curso
        """
        id_curso= request.data['primary_key']
        curso = Curso.objects.get(id=id_curso)
        curso.activo = False
        curso.save()
        return Response(
            {'mensaje': 'Cambio Aceptado'},
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False)
    def crear_grupos(self,request, pk=None):
        """ Metodo  que crea mas grupos
        """
        sede=Sede.objects.get(id=request.data['sede'])
        curso=Curso.objects.get(id=request.data['curso'])
        cantidad= request.data['numero']
        comentario=request.data['comentario'] if ('comentario' in request.data) else ''
        ultimo_grupo=Grupo.objects.filter(sede=sede,curso=curso).last()
        if ultimo_grupo:
            for x in range(ultimo_grupo.numero+1, (ultimo_grupo.numero + int(cantidad))+1):
                nuevo_grupo= Grupo(
                sede=sede,
                numero=x,
                curso=curso,
                comentario=comentario,
                activo=True,
                cyd_grupo_creado_por = request.user
                )
                nuevo_grupo.save()
                crear_calendario(nuevo_grupo)
        else:
            for x in range(int(cantidad)):
                nuevo_grupo= Grupo(
                sede=sede,
                numero=str(x+1),
                curso=curso,
                comentario=comentario,
                activo=True,
                cyd_grupo_creado_por = request.user
                )
                nuevo_grupo.save()
                crear_calendario(nuevo_grupo)
        return Response(
            {'mensaje': 'Grupos creados correctamente'},
            status=status.HTTP_200_OK
        )

class CalendarioViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    serializer_class = CalendarioSerializer
    queryset = Calendario.objects.all()
    filter_fields = ('grupo','grupo__sede')



class SedeViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    serializer_class = SedeSerializer
    queryset = Sede.objects.filter(activa=True)
    filter_fields = ('capacitador',)

    @action(methods=['post'], detail=False)
    def desactivar_sede(self,request, pk=None):
        """ Metodo  que cambia la disponibilidad de la sede
        """
        id_sede= request.data['primary_key']
        sede = Sede.objects.get(id=id_sede)
        if len(sede.grupos.filter(activo=True)) > 0:
            return Response(
                {'mensaje': 'La sede contiene grupos activos'},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        else:
            sede.activa = False
            sede.save()
            return Response(
                {'mensaje': 'Cambio Aceptado'},
                status=status.HTTP_200_OK
            )

    @action(methods=['post'], detail=False)
    def desactivar_participante(self,request, pk=None):
        """ Metodo  que cambia la disponibilidad del participante
        """
        id_participante= request.data['primary_key']
        participante = Participante.objects.get(id=id_participante)
        participante.activo = False
        participante.save()
        return Response(
            {'mensaje': 'Cambio Aceptado'},
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False)
    def actualizar_control_academico(self,request, pk=None):
        """ Metodo  que cambia la disponibilidad del participante
        """
        contado = 0
        contado_hitos  = 0
        dato =  json.loads(request.data['datos'])      
        for numero in dato:
            try:
                asignacion = Asignacion.objects.get(id=numero['Asignacion'])
                if asignacion.participante.genero.genero != numero['Genero']:
                    if ParGenero.objects.filter(genero=numero['Genero']):
                        asignacion.participante.genero.genero=genero=numero['Genero']
                        asignacion.participante.genero.save()
                notas_hitos = NotaHito.objects.filter(asignacion=asignacion)                
                notas_asistencia = NotaAsistencia.objects.filter(asignacion=asignacion)            
                for hitos in notas_hitos:
                    contado_hitos = contado_hitos +1
                    #if(int(numero[hitos.cr_hito.nombre]) > hitos.cr_hito.punteo_max):
                    if(int(numero[str("Hito"+str(contado_hitos))]) > hitos.cr_hito.punteo_max):
                        return Response(
                                {'mensaje': 'La nota del'+ str(hitos.cr_hito.nombre)+"No es permitida"},
                                status=status.HTTP_406_NOT_ACCEPTABLE
                                )
                    else:
                        #hitos.nota=numero[hitos.cr_hito.nombre]
                        hitos.nota = numero[str("Hito"+str(contado_hitos))]
                        hitos.save()
                        if (contado_hitos==notas_hitos.count()):
                            contado_hitos=0
                for notas in notas_asistencia:
                    contado = contado +1
                    #if(int(numero[str("Asistencia "+str(contado))]) > notas.gr_calendario.cr_asistencia.punteo_max ):
                    if(int(numero[str("A "+str(contado))]) > notas.gr_calendario.cr_asistencia.punteo_max ):
                        return Response(
                                {'mensaje': 'La nota de la '+ str("Asistencia "+str(contado))+" No es permitida"},
                                status=status.HTTP_406_NOT_ACCEPTABLE
                                )
                    else:                    
                        notas.nota = numero[str("A "+str(contado))]
                        #notas.nota = numero[str("Asistencia "+str(contado))]
                        notas.save()
                        if(contado==notas_asistencia.count()):
                            contado=0                
            except Exception as e:
                print(e)
        return Response(
                            {'mensaje': 'Cambio Aceptado'},
                            status=status.HTTP_200_OK
                        )
    @action(methods=['post'], detail=False)
    def finalizar_capacitacion_sede(self, request,pk=None):
        """ Metodo  que cambia la disponibilidad de la capacitacion de una sede dando por 
        concluido la capacitacion
        """
        id_sede= request.data['sede']
        sede = Sede.objects.get(id=id_sede,activa=True)
        sede.fecha_finalizacion =datetime.now()
        sede.finalizada = True
        sede.save()
        return Response(
                            {'mensaje': 'Se ha terminado la capacitacion de la sede'},
                            status=status.HTTP_200_OK
                        )
            



class SedeViewSetInforme(CsrfExemptMixin, viewsets.ModelViewSet):
    serializer_class = SedeSerializer
    queryset = Sede.objects.filter(activa=True)
    filter_fields = ('capacitador','id','activa')
    ordering = ('id')

    def get_queryset(self):
        queryset = Sede.objects.filter(activa=True)
        if "cyd_capacitador" in self.request.user.groups.values_list('name', flat=True):
            queryset = self.request.user.sedes.filter(activa=True)

        return queryset
class AsignacionViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    serializer_class = AsignacionSerializer
    queryset = Asignacion.objects.all()
    filter_fields = ('grupo__curso','grupo__sede')
    #filter_fields = ('grupo',)

    @action(methods=['post'], detail=False)
    def desactivar_asignacion(self, request, pk=None):
        """ Método que elimina una asignación
        """
        id_asignacion = request.data['primary_key']
        asignacion = Asignacion.objects.get(id=id_asignacion)
        asignacion.delete()
        return Response(
            {'mensaje': 'Cambio Aceptado'},
            status=status.HTTP_200_OK
        )
    
    @action(methods=['post'], detail=False)
    def verificar_duplicidad(self, request,pk=None):
        """ Metodo para ver si el participante esta asignado en otro grupo 
        """        
        participante_id = request.data['participante']
        grupo_id = request.data['grupo']        
        grupos = Grupo.objects.get(id=grupo_id)            
        buscar_grupos = Grupo.objects.filter(curso=grupos.curso).last()              
        buscar_asignacion = Asignacion.objects.filter(grupo__curso=buscar_grupos.curso,participante__id=participante_id,grupo__sede=buscar_grupos.sede)        
        if buscar_asignacion.count() >0:
            return Response(
                {'Ya esta asignado en los grupos de: '+ str(buscar_asignacion[0].grupo)},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        else:
            return Response(
                {'mensaje': 'Libre'},
                status=status.HTTP_200_OK
            )

        

class ParticipanteViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    """Consulta de participantes usando el DPI como primary key.
    """
    class ParticipanteFilter(django_filters.FilterSet):
        """Define los filtros estándares para el ViewSet.
        Esta clase se define para poder usar SearchFilter y DjangoFilterBackend
        en el mismo ViewSet.
        """
        class Meta:
            model = Participante
            fields = [
                'dpi', 'escuela', 'asignaciones__grupo', 'asignaciones__grupo__sede',
                'asignaciones__grupo__sede__capacitador', 'escuela__codigo',
                'escuela__municipio', 'escuela__municipio__departamento','activo','etnia','escolaridad']
    serializer_class = ParticipanteSerializer
    queryset = Participante.objects.all()
    filter_class = ParticipanteFilter
    filter_backends = (SearchFilter, filters.DjangoFilterBackend)
    search_fields = ('nombre', 'apellido','dpi')
    lookup_field = 'pk'



class ParticipanteAPIViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    """La diferencia con ParticipanteViewSet es que este ViewSet se basa en el ID
    """
    serializer_class = ParticipanteSerializer
    queryset = Participante.objects.all()
    filter_fields = ('escuela', 'asignaciones__grupo', 'dpi','activo')
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    search_fields = ('nombre')


class CalendarioListAPIView(APIFilterMixin, generics.ListAPIView):
    serializer_class = CalendarioSerializer
    queryset = Calendario.objects.all()
    filter_fields = ('fecha',)
    filter_list = {
        'fecha_inicio': 'fecha__gte',
        'fecha_fin': 'fecha__lte'
    }

    def get_queryset(self):
        queryset = super(CalendarioListAPIView, self).get_queryset()
        return self.filter_queryset(queryset)



class NotaAsistenciaViewSet(viewsets.ModelViewSet):
    serializer_class = NotaAsistenciaSerializer
    queryset = NotaAsistencia.objects.all()
    filter_fields = ('asignacion',)


class NotaHitoViewSet(viewsets.ModelViewSet):
    serializer_class = NotaHitoSerializer
    queryset = NotaHito.objects.all()
    filter_fields = ('asignacion',)


class AsesoriaViewSet(viewsets.ModelViewSet):
    serializer_class = AsesoriaSerializer
    queryset = Asesoria.objects.all()
    filter_fields = ('sede', 'sede__capacitador',)


class CalendarioFilter(filters.FilterSet):
    start = django_filters.DateFilter(name='fecha', lookup_expr='gte')
    end = django_filters.DateFilter(name='fecha', lookup_expr='lte')

    class Meta:
        model = Asesoria
        fields = ['sede__capacitador', 'sede', 'fecha', 'start', 'end']


class AsesoriaCalendarViewSet(viewsets.ModelViewSet):
    queryset = Asesoria.objects.all()
    serializer_class = AsesoriaCalendarSerializer
    filter_class = CalendarioFilter

    def get_queryset(self):
        queryset = Asesoria.objects.all()
        if "cyd_capacitador" in self.request.user.groups.values_list('name', flat=True):
            queryset = Asesoria.objects.filter(sede__capacitador=self.request.user)
        return queryset

class CalendarioFilter2(filters.FilterSet):
    start = django_filters.DateFilter(name='fecha', lookup_expr='gte')
    end = django_filters.DateFilter(name='fecha', lookup_expr='lte')

    class Meta:
        model = Calendario
        fields = '__all__'

class EscuelaCalendarioViewSet(CsrfExemptMixin, viewsets.ModelViewSet):
    serializer_class = EscuelaCalendarioSerializer
    queryset = Calendario.objects.all()
    filter_fields = ('grupo',)
    filter_class=CalendarioFilter2

class RecordatorioViewSet(viewsets.ModelViewSet):
    serializer_class=RecordatorioSerializer
    queryset = RecordatorioCalendario.objects.all()
    filter_fields=('capacitador',)
