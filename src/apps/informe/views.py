import json
import qrcode
import requests
import shutil
import os
import datetime
import locale
import sys
from django.shortcuts import render
from django.views.generic import TemplateView, FormView, DetailView, View
from django.middleware import csrf
from django.conf import settings
from django.http import HttpResponse
from apps.informe import forms as informe_f
from rest_framework import views,status
from rest_framework.response import Response
from apps.escuela import models as escuela_m
from apps.inventario import models as inv_m
from apps.cyd import models as cyd_m
from django.db.models import Sum
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, FieldError
# Create your views here.
class InformeView(FormView):
    """ Vista  encargada de obtener los filtros necesarios para poder  obterner la informacion
    """
    template_name = 'informe/informe.html'
    form_class = informe_f.informeForm

class ConsultaEscuelaApi(views.APIView):
    """Apir para la creacion de cursos"""
    def get(self, request):
        print(self.request.GET)
        validar_fecha=0
        filtros= self.request.GET
        queryset=escuela_m.EscPoblacion.objects.distinct()
        queryset2=inv_m.SalidaInventario.objects.distinct()
        queryset3=cyd_m.Sede.objects.distinct()
        datos_enviar=[]
        total_hombre=0
        total_mujeres=0
        total_aprobados=0
        total_hombre1=0
        total_mujeres1=0
        total_aprobados1=0
        escuela=escuela_m.EscPoblacion.objects.filter(escuela__codigo="16-01-0063-43").last()
        filter_list = {
            'codigo': 'escuela__codigo',
            'nombre': 'escuela__nombre__icontains',
            'municipio': 'escuela__municipio',
            'departamento': 'escuela__municipio__departamento',
            'fecha_min': 'fecha__gte',
            'fecha_max': 'fecha__lte',
            'capacitador':'capacitador',
            'cooperante_tpe': 'cooperante',
            'proyecto_tpe': 'beneficiario',
            'fecha_min_capacitacion': 'fecha_creacion__gte',
            'fecha_max_capacitacion': 'fecha_creacion__lte',
        }
        filter_clauses = None
        for key, filtro in filter_list.items():
            if filtros.get(key):
                q = Q(**{"%s" % filtro: filtros.get(key)})
                if filter_clauses:
                    filter_clauses = filter_clauses & q
                else:
                    filter_clauses = q
        if filter_clauses:            
            try:
               queryset = queryset.filter(filter_clauses)
               for data1 in queryset:
                   salida1=inv_m.SalidaInventario.objects.filter(escuela__codigo=data1.escuela.codigo,tipo_salida__nombre="Entrega").last()
                   if salida1:
                       equipada1=True
                   else:
                       equipada1=False
                   total_equipo1 =inv_m.Paquete.objects.filter(salida=salida1).aggregate(total_paquetes=Sum('cantidad'))
                   sede_capacitada1= cyd_m.Sede.objects.filter(escuela_beneficiada__codigo=data1.escuela.codigo)
                   if sede_capacitada1:
                       capacitada1=True
                   else:
                       capacitada1=False
                   grupo=cyd_m.Grupo.objects.filter(sede=sede_capacitada1)
                   for datos1 in grupo:
                       total_hombre1 = total_hombre1 + datos1.get_hombres()
                       total_mujeres1 = total_mujeres1 + datos1.get_mujeres()
                       total_aprobados1= total_aprobados1 +datos1.count_aprobados()
                   maestros_desertores1=cyd_m.Asignacion.objects.filter(grupo__sede=sede_capacitada1,abandono=True).count()
                   datos_recolectar={}
                   datos_recolectar["Udi"]=data1.escuela.codigo
                   datos_recolectar["Nombre"]=data1.escuela.nombre
                   datos_recolectar["Direccion"]=data1.escuela.direccion
                   datos_recolectar["Departamento"]=data1.escuela.municipio.departamento.nombre
                   datos_recolectar["Municipio"]=data1.escuela.municipio.nombre
                   datos_recolectar["Ninos_beneficiados"]=data1.total_alumno
                   datos_recolectar["Docentes"]=data1.total_maestro
                   datos_recolectar["Equipada"]=equipada1
                   datos_recolectar["Fecha_equipamiento"]=0
                   datos_recolectar["No_equipamiento"]=str(salida1)
                   datos_recolectar["Proyecto"]= 0
                   datos_recolectar["Donante"]=0
                   datos_recolectar["Equipo_entregado"]=total_equipo1['total_paquetes']
                   datos_recolectar["Capacitada"]=capacitada1
                   datos_recolectar["Fecha_capacitacion"]=0
                   datos_recolectar["Capacitador"]=0
                   datos_recolectar["Maestros_capacitados"]= total_hombre1 + total_mujeres1
                   datos_recolectar["Maestros_promovidos"]=total_aprobados1
                   datos_recolectar["Maestros_no_promovidos"]=(total_mujeres1 + total_hombre1) - total_aprobados1
                   datos_recolectar["Maestros_desertores"]=maestros_desertores1
                   datos_enviar.append(datos_recolectar)
            except FieldError:
                try:
                    queryset2 = queryset2.filter(filter_clauses,tipo_salida__nombre="Entrega")
                    for data1 in queryset2:
                        salida1=inv_m.SalidaInventario.objects.filter(escuela__codigo=data1.escuela.codigo,tipo_salida__nombre="Entrega").last()
                        #print(salida1)
                        if salida1:
                            equipada1=True
                        else:
                            equipada1=False
                        sede_capacitada1= cyd_m.Sede.objects.filter(escuela_beneficiada__codigo=data1.escuela.codigo)
                        if sede_capacitada1:
                            capacitada1=True
                        else:
                            capacitada1=False
                        grupo=cyd_m.Grupo.objects.filter(sede=sede_capacitada1)
                        for datos1 in grupo:
                            total_hombre1 = total_hombre1 + datos1.get_hombres()
                            total_mujeres1 = total_mujeres1 + datos1.get_mujeres()
                            total_aprobados1= total_aprobados1 +datos1.count_aprobados()
                        total_equipo1 =inv_m.Paquete.objects.filter(salida=salida1).aggregate(total_paquetes=Sum('cantidad'))
                        maestros_desertores1=cyd_m.Asignacion.objects.filter(grupo__sede=sede_capacitada1,abandono=True).count()
                        datos_recolectar={}
                        datos_recolectar["Udi"]=data1.escuela.codigo
                        datos_recolectar["Nombre"]=data1.escuela.nombre
                        datos_recolectar["Direccion"]=data1.escuela.direccion
                        datos_recolectar["Departamento"]=data1.escuela.municipio.departamento.nombre
                        datos_recolectar["Municipio"]=data1.escuela.municipio.nombre
                        datos_recolectar["Ninos_beneficiados"]=escuela_m.EscPoblacion.objects.filter(escuela__codigo=data1.escuela.codigo).last().total_alumno
                        datos_recolectar["Docentes"]=escuela_m.EscPoblacion.objects.filter(escuela__codigo=data1.escuela.codigo).last().total_maestro
                        datos_recolectar["Equipada"]=equipada1
                        datos_recolectar["Fecha_equipamiento"]=0
                        datos_recolectar["No_equipamiento"]=str(salida1)
                        datos_recolectar["Proyecto"]= 0
                        datos_recolectar["Donante"]=0
                        datos_recolectar["Equipo_entregado"]=total_equipo1['total_paquetes']
                        datos_recolectar["Capacitada"]=capacitada1
                        datos_recolectar["Fecha_capacitacion"]=0
                        datos_recolectar["Capacitador"]=0
                        datos_recolectar["Maestros_capacitados"]= total_hombre1 + total_mujeres1
                        datos_recolectar["Maestros_promovidos"]=total_aprobados1
                        datos_recolectar["Maestros_no_promovidos"]=(total_mujeres1 + total_hombre1) - total_aprobados1
                        datos_recolectar["Maestros_desertores"]=maestros_desertores1
                        datos_enviar.append(datos_recolectar)
                except FieldError:
                    try:
                        queryset3 = queryset3.filter(filter_clauses,)
                        print(queryset3)
                        for data1 in queryset3:
                            salida1=inv_m.SalidaInventario.objects.filter(escuela__codigo=data1.escuela_beneficiada,tipo_salida__nombre="Entrega").last()
                            if salida1:
                                equipada1=True
                            else:
                                equipada1=False
                            sede_capacitada1= cyd_m.Sede.objects.filter(escuela_beneficiada__codigo=data1.escuela_beneficiada)
                            if data1:
                                capacitada1=True
                            else:
                                capacitada1=False
                            grupo=cyd_m.Grupo.objects.filter(sede=data1)
                            for datos1 in grupo:
                                total_hombre1 = total_hombre1 + datos1.get_hombres()
                                total_mujeres1 = total_mujeres1 + datos1.get_mujeres()
                                total_aprobados1= total_aprobados1 +datos1.count_aprobados()
                            total_equipo1 =inv_m.Paquete.objects.filter(salida=salida1).aggregate(total_paquetes=Sum('cantidad'))
                            maestros_desertores1=cyd_m.Asignacion.objects.filter(grupo__sede=sede_capacitada1,abandono=True).count()
                            datos_recolectar={}
                            datos_recolectar["Udi"]=data1.escuela_beneficiada.codigo
                            datos_recolectar["Nombre"]=data1.escuela_beneficiada.nombre
                            datos_recolectar["Direccion"]=data1.escuela_beneficiada.direccion
                            datos_recolectar["Departamento"]=data1.escuela_beneficiada.municipio.departamento.nombre
                            datos_recolectar["Municipio"]=data1.escuela_beneficiada.municipio.nombre
                            datos_recolectar["Ninos_beneficiados"]=escuela_m.EscPoblacion.objects.filter(escuela__codigo=data1.escuela_beneficiada.codigo).last().total_alumno
                            datos_recolectar["Docentes"]=escuela_m.EscPoblacion.objects.filter(escuela__codigo=data1.escuela_beneficiada.codigo).last().total_maestro
                            datos_recolectar["Equipada"]=equipada1
                            datos_recolectar["Fecha_equipamiento"]=0
                            datos_recolectar["No_equipamiento"]=str(salida1)
                            datos_recolectar["Proyecto"]= 0
                            datos_recolectar["Donante"]=0
                            datos_recolectar["Equipo_entregado"]=total_equipo1['total_paquetes']
                            datos_recolectar["Capacitada"]=capacitada1
                            datos_recolectar["Fecha_capacitacion"]=0
                            datos_recolectar["Capacitador"]=0
                            datos_recolectar["Maestros_capacitados"]= total_hombre1 + total_mujeres1
                            datos_recolectar["Maestros_promovidos"]=total_aprobados1
                            datos_recolectar["Maestros_no_promovidos"]=(total_mujeres1 + total_hombre1) - total_aprobados1
                            datos_recolectar["Maestros_desertores"]=maestros_desertores1
                            datos_enviar.append(datos_recolectar)
                    except FieldError:
                        print("No hay informacion disponible")
        return Response(
                datos_enviar,
            status=status.HTTP_200_OK
            )
