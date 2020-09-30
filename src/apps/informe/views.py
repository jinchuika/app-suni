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
from apps.tpe import models as tpe_m
from apps.cyd import models as cyd_m
from django.db.models import Sum
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.utils.datastructures import MultiValueDictKeyError

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
        try:
            print(self.request.GET['capacitada'])
            valor_capacitada =  self.request.GET['capacitada']
        except MultiValueDictKeyError:
            valor_capacitada =0
        try:
            print(self.request.GET['equipada'])
            valor_equipada = self.request.GET['equipada']
        except MultiValueDictKeyError:
            print("No tiene filtro de equipada")
            valor_equipada = 0
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
                if filtros.get(key)!="equipada":
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
                    print("aca entro en la segunda")
                    queryset2 = queryset2.filter(filter_clauses,tipo_salida__nombre="Entrega")
                    for data1 in queryset2:
                        if valor_equipada:
                            print("Entro aca")
                            salida1=inv_m.SalidaInventario.objects.filter(tipo_salida__nombre="Entrega").last()
                        else:
                            print("Entro aca 2")
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
                        if valor_equipada:
                            datos_recolectar["Equipada"]=True
                        else:
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
                        print("aca entro en la tercera")
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
        else:
            print("No viene en los filtros")
            queryset2 = queryset2.filter(tipo_salida__nombre="Entrega")
            nueva_escuela=[]
            for data1 in queryset2:
                try:
                    print(data1.escuela.codigo)
                    nueva_escuela.append(data1)
                except Exception as e:
                    print("No trae codigo")
            #print(nueva_escuela)
            for  new_data in  nueva_escuela:
                print(new_data.escuela.codigo)
        return Response(
                datos_enviar,
            status=status.HTTP_200_OK
            )

class ConsultaEscuelaApiDos(views.APIView):
    def get(self, request):
        print("Esto es nuevo")
        total_hombre=0
        total_mujeres=0
        total_aprobados=0
        total_hombre1=0
        total_mujeres1=0
        total_aprobados1=0
        datos_enviar=[]
        totales={}
        acumulador_ninos_beneficiados=0
        acumulador_docentes=0
        acumulador_equipo_entregado=0
        acumulador_maestros_capacitados=0
        acumulador_promovidos=0
        acumulador_no_promovidos=0
        acumulador_inconclusos=0
        try:
            validar_filtro = self.request.GET['equipada']
            bandera_filtro = 0
        except Exception as e:
            try:
                validar_filtro = self.request.GET['capacitada']
                bandera_filtro =1
            except Exception as e:
                bandera_filtro=2
        if bandera_filtro==0:
            print("Biene filtro equipamiento")
            queryset=tpe_m.Equipamiento.objects.all().distinct()
            for data in queryset:
                if data.cantidad_equipo >= 1:
                    datos_recolectar={}
                    datos_recolectar["Udi"]=data.escuela.codigo
                    datos_recolectar["Nombre"]=data.escuela.nombre
                    datos_recolectar["Direccion"]=data.escuela.direccion
                    datos_recolectar["Departamento"]=data.escuela.municipio.departamento.nombre
                    datos_recolectar["Municipio"]=data.escuela.municipio.nombre
                    datos_recolectar["escuela_url"]=data.escuela.get_absolute_url()
                    try:
                        poblacion =  escuela_m.EscPoblacion.objects.filter(escuela__codigo=data.escuela.codigo).last()
                        datos_recolectar["Ninos_beneficiados"]=poblacion.total_alumno
                        #print(acumulador_ninos_beneficiados)
                        datos_recolectar["Docentes"]=poblacion.total_maestro
                    except Exception as e:
                        print("No tiene poblacion")
                        datos_recolectar["Ninos_beneficiados"]=0
                        datos_recolectar["Docentes"]=0
                    if data.cantidad_equipo >=1:
                        print("Si esta equipada")
                        datos_recolectar["Equipada"]=True
                    else:
                        print("No esta capacitada")
                        datos_recolectar["Equipada"]=False
                    datos_recolectar["Fecha_equipamiento"]=data.fecha
                    datos_recolectar["No_equipamiento"]=str(data.id)
                    datos_recolectar["Donante"]=str(data.cooperante.all().last())
                    datos_recolectar["Proyecto"]=str(data.proyecto.all().last())
                    datos_recolectar["Equipo_entregado"]=data.cantidad_equipo
                    sede_capacitada= cyd_m.Sede.objects.filter(escuela_beneficiada__codigo=data.escuela.codigo).last()
                    if cyd_m.Sede.objects.filter(escuela_beneficiada__codigo=data.escuela.codigo).count() >=1:
                        print("Si esta capacitada")
                        datos_recolectar["Capacitada"]=True
                    else:
                        datos_recolectar["Capacitada"]=False
                    grupo=cyd_m.Grupo.objects.filter(sede=sede_capacitada)
                    for datos in grupo:
                        total_hombre = total_hombre + datos.get_hombres()
                        total_mujeres = total_mujeres + datos.get_mujeres()
                        total_aprobados= total_aprobados +datos.count_aprobados()
                    maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede=sede_capacitada,abandono=True).count()
                    try:
                        datos_recolectar["Fecha_capacitacion"]=str(sede_capacitada.fecha_creacion.date())
                        datos_recolectar["Capacitador"]=str(sede_capacitada.capacitador.get_full_name())
                    except Exception as e:
                        datos_recolectar["Fecha_capacitacion"]="No"
                        datos_recolectar["Capacitador"]="No"
                    datos_recolectar["Maestros_capacitados"]= total_hombre + total_mujeres
                    datos_recolectar["Maestros_promovidos"]=total_aprobados
                    datos_recolectar["Maestros_no_promovidos"]=(total_mujeres + total_hombre) - total_aprobados
                    datos_recolectar["Maestros_desertores"]=maestros_desertores
                    datos_enviar.append(datos_recolectar)
            totales["acumulador_equipo_entregado"]=acumulador_equipo_entregado
            #datos_enviar.append(totales)
        elif bandera_filtro==1:
            print("Viene filtro de capacitacion")
            queryset2=cyd_m.Sede.objects.all().distinct()
            for data1 in queryset2:
                datos_recolectar={}
                datos_recolectar["Udi"]=data1.escuela_beneficiada.codigo
                datos_recolectar["Nombre"]=data1.escuela_beneficiada.nombre
                datos_recolectar["Direccion"]=data1.escuela_beneficiada.direccion
                datos_recolectar["Departamento"]=data1.escuela_beneficiada.municipio.departamento.nombre
                datos_recolectar["Municipio"]=data1.escuela_beneficiada.municipio.nombre
                datos_recolectar["escuela_url"]=data.escuela.get_absolute_url()
                try:
                    poblacion =  escuela_m.EscPoblacion.objects.filter(escuela__codigo=data.escuela_beneficiada.codigo).last()
                    datos_recolectar["Ninos_beneficiados"]=poblacion.total_alumno
                    datos_recolectar["Docentes"]=poblacion.total_maestro
                except Exception as e:
                    print("No tiene poblacion")
                    datos_recolectar["Ninos_beneficiados"]=0
                    datos_recolectar["Docentes"]=0
                data_equipamiento=tpe_m.Equipamiento.objects.filter(escuela__codigo=data1.escuela_beneficiada.codigo).last()
                if data_equipamiento.cantidad_equipo >=1:
                    print("Si esta equipada")
                    datos_recolectar["Equipada"]=True
                else:
                    print("No esta capacitada")
                    datos_recolectar["Equipada"]=False
                datos_recolectar["Fecha_equipamiento"]=data_equipamiento.fecha
                datos_recolectar["No_equipamiento"]=str(data_equipamiento.id)
                datos_recolectar["Donante"]=str(data_equipamiento.cooperante.all().last())
                datos_recolectar["Proyecto"]=str(data_equipamiento.proyecto.all().last())
                datos_recolectar["Equipo_entregado"]=data_equipamiento.cantidad_equipo
                if queryset2.count() >=1:
                    print("Si esta capacitada")
                    datos_recolectar["Capacitada"]=True
                else:
                    datos_recolectar["Capacitada"]=False
                grupo=cyd_m.Grupo.objects.filter(sede=data1)
                for datos in grupo:
                    total_hombre = total_hombre + datos.get_hombres()
                    total_mujeres = total_mujeres + datos.get_mujeres()
                    total_aprobados= total_aprobados +datos.count_aprobados()
                maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede=data1,abandono=True).count()
                try:
                    datos_recolectar["Fecha_capacitacion"]=str(sede_capacitada.fecha_creacion.date())
                    datos_recolectar["Capacitador"]=str(sede_capacitada.capacitador.get_full_name())
                except Exception as e:
                    datos_recolectar["Fecha_capacitacion"]="No"
                    datos_recolectar["Capacitador"]="No"
                datos_recolectar["Maestros_capacitados"]= total_hombre + total_mujeres
                datos_recolectar["Maestros_promovidos"]=total_aprobados
                datos_recolectar["Maestros_no_promovidos"]=(total_mujeres + total_hombre) - total_aprobados
                datos_recolectar["Maestros_desertores"]=maestros_desertores
                datos_enviar.append(datos_recolectar)
        else:
            filtros= self.request.GET
            queryset=tpe_m.Equipamiento.objects.distinct()
            queryset2=cyd_m.Sede.objects.distinct()
            filter_list = {
                'codigo': 'escuela__codigo',
                'nombre': 'escuela__nombre__icontains',
                'municipio': 'escuela__municipio',
                'departamento': 'escuela__municipio__departamento',
                'fecha_min': 'fecha__gte',
                'fecha_max': 'fecha__lte',
                'capacitador':'capacitador',
                'cooperante_tpe': 'cooperante',
                'proyecto_tpe': 'proyecto',
                'fecha_min_capacitacion': 'fecha_creacion__gte',
                'fecha_max_capacitacion': 'fecha_creacion__lte',
                'equipada':'equipada'

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
                print(filter_clauses)
            #queryset=tpe_m.Equipamien1to.objects.distinct()
            try:
                #print(queryset.filter(filter_clauses))
                for data in queryset.filter(filter_clauses):
                    datos_recolectar={}
                    datos_recolectar["Udi"]=data.escuela.codigo
                    datos_recolectar["Nombre"]=data.escuela.nombre
                    datos_recolectar["Direccion"]=data.escuela.direccion
                    datos_recolectar["Departamento"]=data.escuela.municipio.departamento.nombre
                    datos_recolectar["Municipio"]=data.escuela.municipio.nombre
                    datos_recolectar["escuela_url"]=data.escuela.get_absolute_url()
                    #print("Ninos Beneficiados: "+str(data.poblacion))
                    #print("Docentes: ")+str(data.poblacion)
                    try:
                        poblacion =  escuela_m.EscPoblacion.objects.filter(escuela__codigo=data.escuela.codigo).last()
                        datos_recolectar["Ninos_beneficiados"]=poblacion.total_alumno
                        datos_recolectar["Docentes"]=poblacion.total_maestro
                    except Exception as e:
                        print("No tiene poblacion")
                        datos_recolectar["Ninos_beneficiados"]=0
                        datos_recolectar["Docentes"]=0
                    if data.cantidad_equipo >=1:
                        print("Si esta equipada")
                        datos_recolectar["Equipada"]=True
                    else:
                        print("No esta capacitada")
                        datos_recolectar["Equipada"]=False
                    datos_recolectar["Fecha_equipamiento"]=data.fecha
                    datos_recolectar["No_equipamiento"]=str(data.id)
                    datos_recolectar["Donante"]=str(data.cooperante.all().last())
                    datos_recolectar["Proyecto"]=str(data.proyecto.all().last())
                    datos_recolectar["Equipo_entregado"]=data.cantidad_equipo
                    sede_capacitada= cyd_m.Sede.objects.filter(escuela_beneficiada__codigo=data.escuela.codigo).last()
                    if cyd_m.Sede.objects.filter(escuela_beneficiada__codigo=data.escuela.codigo).count() >=1:
                        print("Si esta capacitada")
                        datos_recolectar["Capacitada"]=True
                    else:
                        datos_recolectar["Capacitada"]=False
                    grupo=cyd_m.Grupo.objects.filter(sede=sede_capacitada)
                    for datos in grupo:
                        total_hombre = total_hombre + datos.get_hombres()
                        total_mujeres = total_mujeres + datos.get_mujeres()
                        total_aprobados= total_aprobados +datos.count_aprobados()
                    maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede=sede_capacitada,abandono=True).count()
                    try:
                        datos_recolectar["Fecha_capacitacion"]=str(sede_capacitada.fecha_creacion.date())
                        datos_recolectar["Capacitador"]=str(sede_capacitada.capacitador.get_full_name())
                    except Exception as e:
                        datos_recolectar["Fecha_capacitacion"]="No"
                        datos_recolectar["Capacitador"]="No"
                    datos_recolectar["Maestros_capacitados"]= total_hombre + total_mujeres
                    datos_recolectar["Maestros_promovidos"]=total_aprobados
                    datos_recolectar["Maestros_no_promovidos"]=(total_mujeres + total_hombre) - total_aprobados
                    datos_recolectar["Maestros_desertores"]=maestros_desertores
                    datos_enviar.append(datos_recolectar)
            except Exception as e:
                #cyd_m.Sede.objects.distinct()
                print("Sede")
                for data1 in queryset2.filter(filter_clauses):
                    datos_recolectar={}
                    datos_recolectar["Udi"]=data1.escuela_beneficiada.codigo
                    datos_recolectar["Nombre"]=data1.escuela_beneficiada.nombre
                    datos_recolectar["Direccion"]=data1.escuela_beneficiada.direccion
                    datos_recolectar["Departamento"]=data1.escuela_beneficiada.municipio.departamento.nombre
                    datos_recolectar["Municipio"]=data1.escuela_beneficiada.municipio.nombre
                    datos_recolectar["escuela_url"]=data1.escuela_beneficiada.get_absolute_url()
                    try:
                        poblacion =  escuela_m.EscPoblacion.objects.filter(escuela__codigo=data.escuela_beneficiada.codigo).last()
                        datos_recolectar["Ninos_beneficiados"]=poblacion.total_alumno
                        datos_recolectar["Docentes"]=poblacion.total_maestro
                    except Exception as e:
                        print("No tiene poblacion")
                        datos_recolectar["Ninos_beneficiados"]=0
                        datos_recolectar["Docentes"]=0
                    data_equipamiento=tpe_m.Equipamiento.objects.filter(escuela__codigo=data1.escuela_beneficiada.codigo).last()
                    if data_equipamiento.cantidad_equipo >=1:
                        print("Si esta equipada")
                        datos_recolectar["Equipada"]=True
                    else:
                        print("No esta capacitada")
                        datos_recolectar["Equipada"]=False
                    datos_recolectar["Fecha_equipamiento"]=data_equipamiento.fecha
                    datos_recolectar["No_equipamiento"]=str(data_equipamiento.id)
                    datos_recolectar["Donante"]=str(data_equipamiento.cooperante.all().last())
                    datos_recolectar["Proyecto"]=str(data_equipamiento.proyecto.all().last())
                    datos_recolectar["Equipo_entregado"]=data_equipamiento.cantidad_equipo
                    if queryset2.filter(filter_clauses).count() >=1:
                        print("Si esta capacitada")
                        datos_recolectar["Capacitada"]=True
                    else:
                        datos_recolectar["Capacitada"]=False
                    grupo=cyd_m.Grupo.objects.filter(sede=data1)
                    for datos in grupo:
                        total_hombre = total_hombre + datos.get_hombres()
                        total_mujeres = total_mujeres + datos.get_mujeres()
                        total_aprobados= total_aprobados +datos.count_aprobados()
                    maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede=data1,abandono=True).count()
                    try:
                        datos_recolectar["Fecha_capacitacion"]=str(sede_capacitada.fecha_creacion.date())
                        datos_recolectar["Capacitador"]=str(sede_capacitada.capacitador.get_full_name())
                    except Exception as e:
                        datos_recolectar["Fecha_capacitacion"]="No"
                        datos_recolectar["Capacitador"]="No"
                    datos_recolectar["Maestros_capacitados"]= total_hombre + total_mujeres
                    datos_recolectar["Maestros_promovidos"]=total_aprobados
                    datos_recolectar["Maestros_no_promovidos"]=(total_mujeres + total_hombre) - total_aprobados
                    datos_recolectar["Maestros_desertores"]=maestros_desertores
                    datos_enviar.append(datos_recolectar)
        return Response(
            datos_enviar,
        status=status.HTTP_200_OK
        )
