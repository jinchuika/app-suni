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
        total_hombre=0
        total_mujeres=0
        total_aprobados=0
        filtros= self.request.GET
        queryset=escuela_m.Escuela.objects.distinct()
        queryset2=tpe_m.Equipamiento.objects.distinct()
        queryset3=cyd_m.Sede.objects.distinct()
        datos_enviar=[]
        bandera_filtro_equipada=0
        bandera_filtro_capacitada =0
        bandera_filtro =0
        bandera_filtro_prueba=0
        valor_filtro_equipada=0
        valor_filtro_capacitada=0
        valor_filtro_combinado=0
        valor_filtro=0
        try:
            validar_filtro_equipada = self.request.GET['equipada']
            bandera_filtro_equipada = 1
            bandera_filtro_prueba = bandera_filtro_prueba +1
        except Exception as e:
            try:
                validar_filtro_capacitada = self.request.GET['capacitada']
                bandera_filtro_capacitada =2
                bandera_filtro_prueba = bandera_filtro_prueba +2
            except Exception as e:
                bandera_filtro = 3
                bandera_filtro_prueba = bandera_filtro + 3
        filter_list = {
            'codigo': 'codigo',
            'nombre': 'nombre__icontains',
            'municipio': 'municipio',
            'departamento': 'municipio__departamento',
            'fecha_min': 'fecha__gte',
            'fecha_max': 'fecha__lte',
            'capacitador':'capacitador',
            'cooperante_tpe': 'cooperante',
            'proyecto_tpe': 'proyecto',
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
            #validaciones de filtros
            if(filtros.get("capacitada")):
                if(filtros.get("equipada")):
                    valor_filtro_combinado=1
                else:
                    valor_filtro_capacitada=1
            elif(filtros.get("equipada")):
                valor_filtro_equipada=1
            #seleccion de query
            if valor_filtro_equipada == 1:
                if filtros.get("equipada")=='True':                    
                    try:
                        for data in queryset.filter(filter_clauses):
                            if not data.datos_equipamiento() is None:
                                datos_recolectar={}
                                datos_recolectar["Equipada"]=True
                                datos_recolectar["Udi"]=data.codigo
                                datos_recolectar["Nombre"]=data.nombre
                                datos_recolectar["Direccion"]=data.direccion
                                datos_recolectar["Departamento"]=data.municipio.departamento.nombre
                                datos_recolectar["Municipio"]=data.municipio.nombre
                                datos_recolectar["escuela_url"]=data.get_absolute_url()
                                datos_recolectar["Ninos_beneficiados"]=data.poblacion
                                datos_recolectar["Docentes"]=data.maestros
                                datos_recolectar["Fecha_equipamiento"]=data.datos_equipamiento().fecha
                                datos_recolectar["No_equipamiento"]=str(data.datos_equipamiento().id)
                                datos_recolectar["Donante"]=str(data.datos_equipamiento().cooperante.all().last())
                                datos_recolectar["Proyecto"]=str(data.datos_equipamiento().proyecto.all().last())
                                datos_recolectar["Equipo_entregado"]=data.datos_equipamiento().cantidad_equipo
                                if data.capacitacion["capacitada"]== True:
                                    for  data_sede in data.get_sedes():
                                        capacitador = data_sede.capacitador.get_full_name()
                                        fecha_creacion =data_sede.fecha_creacion.date()
                                    datos_recolectar["Capacitada"]=True
                                    grupo=cyd_m.Grupo.objects.filter(sede=data.get_sedes())
                                    for datos in grupo:
                                        total_hombre = total_hombre + datos.get_hombres()
                                        total_mujeres = total_mujeres + datos.get_mujeres()
                                        total_aprobados= total_aprobados +datos.count_aprobados()
                                    maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede=data.get_sedes(),abandono=True).count()
                                    datos_recolectar["Capacitador"]=capacitador
                                    datos_recolectar["Fecha_capacitacion"]=fecha_creacion
                                    datos_recolectar["Capacitador"]=capacitador
                                    datos_recolectar["Maestros_capacitados"]= total_hombre + total_mujeres
                                    datos_recolectar["Maestros_promovidos"]=total_aprobados
                                    datos_recolectar["Maestros_no_promovidos"]=(total_mujeres + total_hombre) - total_aprobados
                                    datos_recolectar["Maestros_desertores"]=maestros_desertores
                                else:
                                    datos_recolectar["Capacitada"]=False
                                    datos_recolectar["Fecha_capacitacion"]="No tiene"
                                    datos_recolectar["Capacitador"]="No tiene"
                                    datos_recolectar["Maestros_capacitados"]= 0
                                    datos_recolectar["Maestros_promovidos"]=0
                                    datos_recolectar["Maestros_no_promovidos"]=0
                                    datos_recolectar["Maestros_desertores"]=0
                                datos_enviar.append(datos_recolectar)
                    except Exception as e:
                        for data in queryset2.filter(filter_clauses):
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
                                datos_recolectar["Docentes"]=poblacion.total_maestro
                            except Exception as e:
                                datos_recolectar["Ninos_beneficiados"]=0
                                datos_recolectar["Docentes"]=0
                            if data.cantidad_equipo >=1:
                                datos_recolectar["Equipada"]=True
                            else:
                                datos_recolectar["Equipada"]=False
                            datos_recolectar["Fecha_equipamiento"]=data.fecha
                            datos_recolectar["No_equipamiento"]=str(data.id)
                            datos_recolectar["Donante"]=str(data.cooperante.all().last())
                            datos_recolectar["Proyecto"]=str(data.proyecto.all().last())
                            datos_recolectar["Equipo_entregado"]=data.cantidad_equipo
                            sede_capacitada= cyd_m.Sede.objects.filter(escuela_beneficiada__codigo=data.escuela.codigo).last()
                            if cyd_m.Sede.objects.filter(escuela_beneficiada__codigo=data.escuela.codigo).count() >=1:
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
                else:
                    try:
                        for data in queryset.filter(filter_clauses):
                            if not data.datos_equipamiento():
                                datos_recolectar={}
                                datos_recolectar["Udi"]=data.codigo
                                datos_recolectar["Nombre"]=data.nombre
                                datos_recolectar["Direccion"]=data.direccion
                                datos_recolectar["Departamento"]=data.municipio.departamento.nombre
                                datos_recolectar["Municipio"]=data.municipio.nombre
                                datos_recolectar["escuela_url"]=data.get_absolute_url()
                                datos_recolectar["Ninos_beneficiados"]=data.poblacion
                                datos_recolectar["Docentes"]=data.maestros
                                datos_recolectar["Fecha_equipamiento"]="No tiene"
                                datos_recolectar["No_equipamiento"]=0
                                datos_recolectar["Donante"]=0
                                datos_recolectar["Proyecto"]=0
                                datos_recolectar["Equipo_entregado"]=0
                                datos_recolectar["Equipada"]=False
                                if data.capacitacion["capacitada"]== True:
                                    for  data_sede in data.get_sedes():
                                        capacitador = data_sede.capacitador.get_full_name()
                                        fecha_creacion =data_sede.fecha_creacion.date()
                                    datos_recolectar["Capacitada"]=True
                                    grupo=cyd_m.Grupo.objects.filter(sede=data.get_sedes())
                                    for datos in grupo:
                                        total_hombre = total_hombre + datos.get_hombres()
                                        total_mujeres = total_mujeres + datos.get_mujeres()
                                        total_aprobados= total_aprobados +datos.count_aprobados()
                                    maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede=data.get_sedes(),abandono=True).count()
                                    datos_recolectar["Capacitador"]=capacitador
                                    datos_recolectar["Maestros_capacitados"]= total_hombre + total_mujeres
                                    datos_recolectar["Maestros_promovidos"]=total_aprobados
                                    datos_recolectar["Maestros_no_promovidos"]=(total_mujeres + total_hombre) - total_aprobados
                                    datos_recolectar["Maestros_desertores"]=maestros_desertores
                                else:
                                    datos_recolectar["Capacitada"]=False
                                    datos_recolectar["Fecha_capacitacion"]="No tiene"
                                    datos_recolectar["Capacitador"]="No tiene"
                                    datos_recolectar["Maestros_capacitados"]= 0
                                    datos_recolectar["Maestros_promovidos"]=0
                                    datos_recolectar["Maestros_no_promovidos"]=0
                                    datos_recolectar["Maestros_desertores"]=0
                                datos_enviar.append(datos_recolectar)
                    except Exception as e:
                        print("Esto es nuevo")
            elif valor_filtro_capacitada==1:
                print("Trae capacitacion1")
                try:
                    for data in queryset.filter(filter_clauses):
                        if data.capacitacion["capacitada"] is True:
                            datos_recolectar={}
                            datos_recolectar["Udi"]=data.codigo
                            datos_recolectar["Nombre"]=data.nombre
                            datos_recolectar["Direccion"]=data.direccion
                            datos_recolectar["Departamento"]=data.municipio.departamento.nombre
                            datos_recolectar["Municipio"]=data.municipio.nombre
                            datos_recolectar["escuela_url"]=data.get_absolute_url()
                            datos_recolectar["Ninos_beneficiados"]=data.poblacion
                            datos_recolectar["Docentes"]=data.maestros
                            datos_recolectar["Fecha_equipamiento"]=data.datos_equipamiento().fecha
                            datos_recolectar["No_equipamiento"]=str(data.datos_equipamiento().id)
                            datos_recolectar["Donante"]=str(data.datos_equipamiento().cooperante.all().last())
                            datos_recolectar["Proyecto"]=str(data.datos_equipamiento().proyecto.all().last())
                            datos_recolectar["Equipo_entregado"]=data.datos_equipamiento().cantidad_equipo
                            if str(data.datos_equipamiento().proyecto.all().last()) == 'NA´AT':
                                datos_recolectar["Capacitador"]="No tiene"
                                datos_recolectar["Maestros_capacitados"]= 0
                                datos_recolectar["Maestros_promovidos"]=0
                                datos_recolectar["Maestros_no_promovidos"]=0
                                datos_recolectar["Maestros_desertores"]=0
                                datos_recolectar["Fecha_capacitacion"]="No tiene"
                                datos_enviar.append(datos_recolectar)
                            else:
                                for  data_sede in data.get_sedes():
                                    capacitador = data_sede.capacitador.get_full_name()
                                    fecha_creacion =data_sede.fecha_creacion.date()
                                    datos_recolectar["Fecha_capacitacion"]= fecha_creacion
                                datos_recolectar["Capacitada"]=True
                                grupo=cyd_m.Grupo.objects.filter(sede=data.get_sedes())
                                for datos in grupo:
                                    total_hombre = total_hombre + datos.get_hombres()
                                    total_mujeres = total_mujeres + datos.get_mujeres()
                                    total_aprobados= total_aprobados +datos.count_aprobados()
                                maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede=data.get_sedes(),abandono=True).count()
                                datos_recolectar["Capacitador"]=capacitador
                                datos_recolectar["Maestros_capacitados"]= total_hombre + total_mujeres
                                datos_recolectar["Maestros_promovidos"]=total_aprobados
                                datos_recolectar["Maestros_no_promovidos"]=(total_mujeres + total_hombre) - total_aprobados
                                datos_recolectar["Maestros_desertores"]=maestros_desertores
                                datos_enviar.append(datos_recolectar)
                except Exception as e:
                    for data in queryset2.filter(filter_clauses):
                        if filtros.get("capacitada")=='True':
                            if data.escuela.capacitacion["capacitada"] is  True:
                                datos_recolectar={}
                                datos_recolectar["Udi"]=data.escuela.codigo
                                datos_recolectar["Nombre"]=data.escuela.nombre
                                datos_recolectar["Direccion"]=data.escuela.direccion
                                datos_recolectar["Departamento"]=data.escuela.municipio.departamento.nombre
                                datos_recolectar["Municipio"]=data.escuela.municipio.nombre
                                datos_recolectar["escuela_url"]=data.escuela.get_absolute_url()
                                datos_recolectar["Ninos_beneficiados"]=data.escuela.poblacion
                                datos_recolectar["Docentes"]=data.escuela.maestros
                                datos_recolectar["Fecha_equipamiento"]=data.escuela.datos_equipamiento().fecha
                                datos_recolectar["No_equipamiento"]=str(data.escuela.datos_equipamiento().id)
                                datos_recolectar["Donante"]=str(data.escuela.datos_equipamiento().cooperante.all().last())
                                datos_recolectar["Proyecto"]=str(data.escuela.datos_equipamiento().proyecto.all().last())
                                datos_recolectar["Equipo_entregado"]=data.escuela.datos_equipamiento().cantidad_equipo
                                if str(data.escuela.datos_equipamiento().proyecto.all().last()) == 'NA´AT':
                                    datos_recolectar["Capacitador"]="No tiene"
                                    datos_recolectar["Maestros_capacitados"]= 0
                                    datos_recolectar["Maestros_promovidos"]=0
                                    datos_recolectar["Maestros_no_promovidos"]=0
                                    datos_recolectar["Maestros_desertores"]=0
                                    datos_enviar.append(datos_recolectar)
                                else:
                                    for  data_sede in data.escuela.get_sedes():
                                        capacitador = data_sede.capacitador.get_full_name()
                                        fecha_creacion =data_sede.fecha_creacion.date()
                                    datos_recolectar["Capacitada"]=True
                                    grupo=cyd_m.Grupo.objects.filter(sede=data.escuela.get_sedes())
                                    for datos in grupo:
                                        total_hombre = total_hombre + datos.get_hombres()
                                        total_mujeres = total_mujeres + datos.get_mujeres()
                                        total_aprobados= total_aprobados +datos.count_aprobados()
                                    maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede=data.escuela.get_sedes(),abandono=True).count()
                                    datos_recolectar["Capacitador"]=capacitador
                                    datos_recolectar["Maestros_capacitados"]= total_hombre + total_mujeres
                                    datos_recolectar["Maestros_promovidos"]=total_aprobados
                                    datos_recolectar["Maestros_no_promovidos"]=(total_mujeres + total_hombre) - total_aprobados
                                    datos_recolectar["Maestros_desertores"]=maestros_desertores
                                    datos_enviar.append(datos_recolectar)
                        #End filtros.get("capacitada")=='True'
                        else:
                            if data.escuela.capacitacion["capacitada"] is  False:
                                datos_recolectar={}
                                datos_recolectar["Udi"]=data.escuela.codigo
                                datos_recolectar["Nombre"]=data.escuela.nombre
                                datos_recolectar["Direccion"]=data.escuela.direccion
                                datos_recolectar["Departamento"]=data.escuela.municipio.departamento.nombre
                                datos_recolectar["Municipio"]=data.escuela.municipio.nombre
                                datos_recolectar["escuela_url"]=data.escuela.get_absolute_url()
                                datos_recolectar["Ninos_beneficiados"]=data.escuela.poblacion
                                datos_recolectar["Docentes"]=data.escuela.maestros
                                datos_recolectar["Fecha_equipamiento"]=data.escuela.datos_equipamiento().fecha
                                datos_recolectar["No_equipamiento"]=str(data.escuela.datos_equipamiento().id)
                                datos_recolectar["Donante"]=str(data.escuela.datos_equipamiento().cooperante.all().last())
                                datos_recolectar["Proyecto"]=str(data.escuela.datos_equipamiento().proyecto.all().last())
                                datos_recolectar["Equipo_entregado"]=data.escuela.datos_equipamiento().cantidad_equipo
                                datos_recolectar["Capacitada"]=False
                                datos_recolectar["Capacitador"]="No tiene"
                                datos_recolectar["Maestros_capacitados"]= 0
                                datos_recolectar["Maestros_promovidos"]=0
                                datos_recolectar["Maestros_no_promovidos"]=0
                                datos_recolectar["Maestros_desertores"]=0
                                datos_enviar.append(datos_recolectar)
            elif valor_filtro_combinado==1:
                print("Trae los 2 filtros")
                if filtros.get("capacitada")=='True' and filtros.get("equipada")=='True' :
                    print("Viene 2 verdaderos")
                    try:
                        for data in queryset.filter(filter_clauses):
                            if (data.es_equipada() is True  and data.capacitacion["capacitada"] is True):
                                datos_recolectar={}
                                datos_recolectar["Udi"]=data.codigo
                                datos_recolectar["Nombre"]=data.nombre
                                datos_recolectar["Direccion"]=data.direccion
                                datos_recolectar["Departamento"]=data.municipio.departamento.nombre
                                datos_recolectar["Municipio"]=data.municipio.nombre
                                datos_recolectar["escuela_url"]=data.get_absolute_url()
                                datos_recolectar["Ninos_beneficiados"]=data.poblacion
                                datos_recolectar["Docentes"]=data.maestros
                                datos_recolectar["Fecha_equipamiento"]=data.datos_equipamiento().fecha
                                datos_recolectar["No_equipamiento"]=str(data.datos_equipamiento().id)
                                datos_recolectar["Donante"]=str(data.datos_equipamiento().cooperante.all().last())
                                datos_recolectar["Proyecto"]=str(data.datos_equipamiento().proyecto.all().last())
                                datos_recolectar["Equipo_entregado"]=data.datos_equipamiento().cantidad_equipo
                                if str(data.datos_equipamiento().proyecto.all().last()) == 'NA´AT':
                                    datos_recolectar["Capacitador"]="No tiene"
                                    datos_recolectar["Maestros_capacitados"]= 0
                                    datos_recolectar["Maestros_promovidos"]=0
                                    datos_recolectar["Maestros_no_promovidos"]=0
                                    datos_recolectar["Maestros_desertores"]=0
                                    datos_recolectar["Fecha_capacitacion"]="No tiene"
                                    datos_enviar.append(datos_recolectar)
                                else:
                                    for  data_sede in data.get_sedes():
                                        capacitador = data_sede.capacitador.get_full_name()
                                        fecha_creacion =data_sede.fecha_creacion.date()
                                        datos_recolectar["Fecha_capacitacion"]= fecha_creacion
                                    datos_recolectar["Capacitada"]=True
                                    grupo=cyd_m.Grupo.objects.filter(sede=data.get_sedes())
                                    for datos in grupo:
                                        total_hombre = total_hombre + datos.get_hombres()
                                        total_mujeres = total_mujeres + datos.get_mujeres()
                                        total_aprobados= total_aprobados +datos.count_aprobados()
                                    maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede=data.get_sedes(),abandono=True).count()
                                    datos_recolectar["Capacitador"]=capacitador
                                    datos_recolectar["Maestros_capacitados"]= total_hombre + total_mujeres
                                    datos_recolectar["Maestros_promovidos"]=total_aprobados
                                    datos_recolectar["Maestros_no_promovidos"]=(total_mujeres + total_hombre) - total_aprobados
                                    datos_recolectar["Maestros_desertores"]=maestros_desertores
                                    datos_enviar.append(datos_recolectar)
                    except Exception as e:
                        print("Viene True, True  Equipamiento")
                        try:
                            for data in queryset2.filter(filter_clauses):
                                if (data.escuela.es_equipada() is True  and data.escuela.capacitacion["capacitada"] is True):
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
                                        datos_recolectar["Docentes"]=poblacion.total_maestro
                                    except Exception as e:
                                        datos_recolectar["Ninos_beneficiados"]=0
                                        datos_recolectar["Docentes"]=0
                                    if data.cantidad_equipo >=1:
                                        datos_recolectar["Equipada"]=True
                                    else:
                                        datos_recolectar["Equipada"]=False
                                    datos_recolectar["Fecha_equipamiento"]=data.fecha
                                    datos_recolectar["No_equipamiento"]=str(data.id)
                                    datos_recolectar["Donante"]=str(data.cooperante.all().last())
                                    datos_recolectar["Proyecto"]=str(data.proyecto.all().last())
                                    datos_recolectar["Equipo_entregado"]=data.cantidad_equipo
                                    sede_capacitada= cyd_m.Sede.objects.filter(escuela_beneficiada__codigo=data.escuela.codigo).last()
                                    datos_recolectar["Capacitada"]= data.escuela.capacitacion["capacitada"]
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
                            for data1 in queryset3.filter(filter_clauses):
                                if (data1.escuela_beneficiada.es_equipada() is True  and data1.escuela_beneficiada.capacitacion["capacitada"] is True):
                                    datos_recolectar={}
                                    datos_recolectar["Udi"]=data1.escuela_beneficiada.codigo
                                    datos_recolectar["Nombre"]=data1.escuela_beneficiada.nombre
                                    datos_recolectar["Direccion"]=data1.escuela_beneficiada.direccion
                                    datos_recolectar["Departamento"]=data1.escuela_beneficiada.municipio.departamento.nombre
                                    datos_recolectar["Municipio"]=data1.escuela_beneficiada.municipio.nombre
                                    datos_recolectar["escuela_url"]=data1.escuela_beneficiada.get_absolute_url()
                                    datos_recolectar["Ninos_beneficiados"]=data1.escuela_beneficiada.poblacion
                                    datos_recolectar["Docentes"]=data1.escuela_beneficiada.maestros
                                    datos_recolectar["Fecha_equipamiento"]=data1.escuela_beneficiada.datos_equipamiento().fecha
                                    datos_recolectar["No_equipamiento"]=str(data1.escuela_beneficiada.datos_equipamiento().id)
                                    datos_recolectar["Donante"]=str(data1.escuela_beneficiada.datos_equipamiento().cooperante.all().last())
                                    datos_recolectar["Proyecto"]=str(data1.escuela_beneficiada.datos_equipamiento().proyecto.all().last())
                                    datos_recolectar["Equipo_entregado"]=data1.escuela_beneficiada.datos_equipamiento().cantidad_equipo
                                    datos_recolectar["Equipada"]= data1.escuela_beneficiada.es_equipada()
                                    if str(data1.escuela_beneficiada.datos_equipamiento().proyecto.all().last()) == 'NA´AT':
                                        print("Si tengo un proyecto NAAT")
                                        datos_recolectar["Capacitador"]="No tiene"
                                        datos_recolectar["Maestros_capacitados"]= 0
                                        datos_recolectar["Maestros_promovidos"]=0
                                        datos_recolectar["Maestros_no_promovidos"]=0
                                        datos_recolectar["Maestros_desertores"]=0
                                        datos_recolectar["Fecha_capacitacion"]="No tiene"
                                        datos_enviar.append(datos_recolectar)
                                    else:
                                        print("No es NA`AT")
                                        for  data_sede in data1.escuela_beneficiada.get_sedes():
                                            capacitador = data_sede.capacitador.get_full_name()
                                            fecha_creacion =data_sede.fecha_creacion.date()
                                            datos_recolectar["Fecha_capacitacion"]= fecha_creacion
                                        datos_recolectar["Capacitada"]=True
                                        grupo=cyd_m.Grupo.objects.filter(sede__in=data1.escuela_beneficiada.get_sedes())
                                        for datos in grupo:
                                            total_hombre = total_hombre + datos.get_hombres()
                                            total_mujeres = total_mujeres + datos.get_mujeres()
                                            total_aprobados= total_aprobados +datos.count_aprobados()
                                        maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede__in=data1.escuela_beneficiada.get_sedes(),abandono=True).count()
                                        datos_recolectar["Capacitador"]=capacitador
                                        datos_recolectar["Maestros_capacitados"]= total_hombre + total_mujeres
                                        datos_recolectar["Maestros_promovidos"]=total_aprobados
                                        datos_recolectar["Maestros_no_promovidos"]=(total_mujeres + total_hombre) - total_aprobados
                                        datos_recolectar["Maestros_desertores"]=maestros_desertores
                                        datos_enviar.append(datos_recolectar)
                elif filtros.get("capacitada")=='False' and filtros.get("equipada")=='False' :
                    print("Viene 2 Falsos")
                    try:
                        for data in queryset.filter(filter_clauses):
                            if (data.es_equipada() is False  and data.capacitacion["capacitada"] is False):
                                datos_recolectar={}
                                datos_recolectar["Udi"]=data.codigo
                                datos_recolectar["Nombre"]=data.nombre
                                datos_recolectar["Direccion"]=data.direccion
                                datos_recolectar["Departamento"]=data.municipio.departamento.nombre
                                datos_recolectar["Municipio"]=data.municipio.nombre
                                datos_recolectar["escuela_url"]=data.get_absolute_url()
                                datos_recolectar["Ninos_beneficiados"]=data.poblacion
                                datos_recolectar["Docentes"]=data.maestros
                                datos_recolectar["Fecha_equipamiento"]="No tiene"
                                datos_recolectar["No_equipamiento"]=0
                                datos_recolectar["Donante"]="No tiene"
                                datos_recolectar["Proyecto"]="No tiene"
                                datos_recolectar["Equipo_entregado"]=0
                                datos_recolectar["Capacitador"]="No tiene"
                                datos_recolectar["Maestros_capacitados"]= 0
                                datos_recolectar["Maestros_promovidos"]=0
                                datos_recolectar["Maestros_no_promovidos"]=0
                                datos_recolectar["Maestros_desertores"]=0
                                datos_recolectar["Fecha_capacitacion"]="No tiene"
                                datos_enviar.append(datos_recolectar)
                    except Exception as e:
                        print("Viene False, False  Equipamiento")
                        try:
                            #print(queryset.filter(filter_clauses))
                            for data in queryset2.filter(filter_clauses):
                                if (data.escuela.es_equipada() is False  and data.escuela.capacitacion["capacitada"] is False):
                                    datos_recolectar={}
                                    datos_recolectar["Udi"]=data.escuela.codigo
                                    datos_recolectar["Nombre"]=data.escuela.nombre
                                    datos_recolectar["Direccion"]=data.escuela.direccion
                                    datos_recolectar["Departamento"]=data.escuela.municipio.departamento.nombre
                                    datos_recolectar["Municipio"]=data.escuela.municipio.nombre
                                    datos_recolectar["escuela_url"]=data.escuela.get_absolute_url()
                                    datos_recolectar["Fecha_equipamiento"]="No tiene"
                                    datos_recolectar["No_equipamiento"]="No tiene"
                                    datos_recolectar["Donante"]="No tiene"
                                    datos_recolectar["Proyecto"]="No tiene"
                                    datos_recolectar["Equipo_entregado"]=data.cantidad_equipo
                                    datos_recolectar["Maestros_capacitados"]= 0
                                    datos_recolectar["Maestros_promovidos"]=0
                                    datos_recolectar["Maestros_no_promovidos"]=0
                                    datos_recolectar["Maestros_desertores"]=0
                                    datos_enviar.append(datos_recolectar)
                        except Exception as e:
                            #cyd_m.Sede.objects.distinct()
                            for data1 in queryset3.filter(filter_clauses):
                                if (data1.escuela_beneficiada.es_equipada() is False  and data1.escuela_beneficiada.capacitacion["capacitada"] is False):
                                    datos_recolectar={}
                                    datos_recolectar["Udi"]=data1.escuela_beneficiada.codigo
                                    datos_recolectar["Nombre"]=data1.escuela_beneficiada.nombre
                                    datos_recolectar["Direccion"]=data1.escuela_beneficiada.direccion
                                    datos_recolectar["Departamento"]=data1.escuela_beneficiada.municipio.departamento.nombre
                                    datos_recolectar["Municipio"]=data1.escuela_beneficiada.municipio.nombre
                                    datos_recolectar["escuela_url"]=data1.escuela_beneficiada.get_absolute_url()
                                    datos_recolectar["Ninos_beneficiados"]=data1.escuela_beneficiada.poblacion
                                    datos_recolectar["Docentes"]=data1.escuela_beneficiada.maestros
                                    datos_recolectar["Fecha_equipamiento"]=data1.escuela_beneficiada.datos_equipamiento().fecha
                                    datos_recolectar["No_equipamiento"]=str(data1.escuela_beneficiada.datos_equipamiento().id)
                                    datos_recolectar["Donante"]=str(data1.escuela_beneficiada.datos_equipamiento().cooperante.all().last())
                                    datos_recolectar["Proyecto"]=str(data1.escuela_beneficiada.datos_equipamiento().proyecto.all().last())
                                    datos_recolectar["Equipo_entregado"]=data1.escuela_beneficiada.datos_equipamiento().cantidad_equipo
                                    datos_recolectar["Capacitador"]="No tiene"
                                    datos_recolectar["Maestros_capacitados"]= 0
                                    datos_recolectar["Maestros_promovidos"]=0
                                    datos_recolectar["Maestros_no_promovidos"]=0
                                    datos_recolectar["Maestros_desertores"]=0
                                    datos_enviar.append(datos_recolectar)
                elif filtros.get("capacitada")=='True' and filtros.get("equipada")=='False' :
                    print("Viene capacitada  y no equipada")
                else:
                    print("Viene equipa y no cacitada")
                    try:
                        for data in queryset.filter(filter_clauses):
                            if (data.es_equipada() is True  and data.capacitacion["capacitada"] is False):
                                datos_recolectar={}
                                datos_recolectar["Udi"]=data.codigo
                                datos_recolectar["Nombre"]=data.nombre
                                datos_recolectar["Direccion"]=data.direccion
                                datos_recolectar["Departamento"]=data.municipio.departamento.nombre
                                datos_recolectar["Municipio"]=data.municipio.nombre
                                datos_recolectar["escuela_url"]=data.get_absolute_url()
                                datos_recolectar["Ninos_beneficiados"]=data.poblacion
                                datos_recolectar["Docentes"]=data.maestros
                                datos_recolectar["Fecha_equipamiento"]=data.datos_equipamiento().fecha
                                datos_recolectar["No_equipamiento"]=str(data.datos_equipamiento().id)
                                datos_recolectar["Donante"]=str(data.datos_equipamiento().cooperante.all().last())
                                datos_recolectar["Proyecto"]=str(data.datos_equipamiento().proyecto.all().last())
                                datos_recolectar["Equipo_entregado"]=data.datos_equipamiento().cantidad_equipo
                                if str(data.datos_equipamiento().proyecto.all().last()) == 'NA´AT':
                                    print("Si tengo un proyecto NAAT")
                                    datos_recolectar["Capacitador"]="No tiene"
                                    datos_recolectar["Maestros_capacitados"]= 0
                                    datos_recolectar["Maestros_promovidos"]=0
                                    datos_recolectar["Maestros_no_promovidos"]=0
                                    datos_recolectar["Maestros_desertores"]=0
                                    datos_recolectar["Fecha_capacitacion"]="No tiene"
                                    datos_enviar.append(datos_recolectar)
                                else:
                                    print("No es NA`AT")
                                    for  data_sede in data.get_sedes():
                                        capacitador = data_sede.capacitador.get_full_name()
                                        fecha_creacion =data_sede.fecha_creacion.date()
                                        datos_recolectar["Fecha_capacitacion"]= fecha_creacion
                                    datos_recolectar["Capacitada"]=True
                                    grupo=cyd_m.Grupo.objects.filter(sede=data.get_sedes())
                                    for datos in grupo:
                                        total_hombre = total_hombre + datos.get_hombres()
                                        total_mujeres = total_mujeres + datos.get_mujeres()
                                        total_aprobados= total_aprobados +datos.count_aprobados()
                                    maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede=data.get_sedes(),abandono=True).count()
                                    datos_recolectar["Capacitador"]=capacitador
                                    datos_recolectar["Maestros_capacitados"]= total_hombre + total_mujeres
                                    datos_recolectar["Maestros_promovidos"]=total_aprobados
                                    datos_recolectar["Maestros_no_promovidos"]=(total_mujeres + total_hombre) - total_aprobados
                                    datos_recolectar["Maestros_desertores"]=maestros_desertores
                                    datos_enviar.append(datos_recolectar)
                    except Exception as e:
                        print("Viene True, False  Equipamiento")
                        try:
                            #print(queryset.filter(filter_clauses))
                            for data in queryset2.filter(filter_clauses):
                                if (data.escuela.es_equipada() is True  and data.escuela.capacitacion["capacitada"] is False):
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
                                        datos_recolectar["Docentes"]=poblacion.total_maestro
                                    except Exception as e:
                                        datos_recolectar["Ninos_beneficiados"]=0
                                        datos_recolectar["Docentes"]=0
                                    if data.cantidad_equipo >=1:
                                        datos_recolectar["Equipada"]=True
                                    else:
                                        datos_recolectar["Equipada"]=False
                                    datos_recolectar["Fecha_equipamiento"]=data.fecha
                                    datos_recolectar["No_equipamiento"]=str(data.id)
                                    datos_recolectar["Donante"]=str(data.cooperante.all().last())
                                    datos_recolectar["Proyecto"]=str(data.proyecto.all().last())
                                    datos_recolectar["Equipo_entregado"]=data.cantidad_equipo
                                    sede_capacitada= cyd_m.Sede.objects.filter(escuela_beneficiada__codigo=data.escuela.codigo).last()
                                    if cyd_m.Sede.objects.filter(escuela_beneficiada__codigo=data.escuela.codigo).count() >=1:
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
                            for data1 in queryset3.filter(filter_clauses):
                                if (data1.escuela_beneficiada.es_equipada() is True  and data1.escuela_beneficiada.capacitacion["capacitada"] is False):
                                    datos_recolectar={}
                                    datos_recolectar["Udi"]=data1.escuela_beneficiada.codigo
                                    datos_recolectar["Nombre"]=data1.escuela_beneficiada.nombre
                                    datos_recolectar["Direccion"]=data1.escuela_beneficiada.direccion
                                    datos_recolectar["Departamento"]=data1.escuela_beneficiada.municipio.departamento.nombre
                                    datos_recolectar["Municipio"]=data1.escuela_beneficiada.municipio.nombre
                                    datos_recolectar["escuela_url"]=data1.escuela_beneficiada.get_absolute_url()
                                    datos_recolectar["Ninos_beneficiados"]=data1.escuela_beneficiada.poblacion
                                    datos_recolectar["Docentes"]=data1.escuela_beneficiada.maestros
                                    datos_recolectar["Fecha_equipamiento"]=data1.escuela_beneficiada.datos_equipamiento().fecha
                                    datos_recolectar["No_equipamiento"]=str(data1.escuela_beneficiada.datos_equipamiento().id)
                                    datos_recolectar["Donante"]=str(data1.escuela_beneficiada.datos_equipamiento().cooperante.all().last())
                                    datos_recolectar["Proyecto"]=str(data1.escuela_beneficiada.datos_equipamiento().proyecto.all().last())
                                    datos_recolectar["Equipo_entregado"]=data1.escuela_beneficiada.datos_equipamiento().cantidad_equipo
                                    if str(data1.escuela_beneficiada.datos_equipamiento().proyecto.all().last()) == 'NA´AT':
                                        datos_recolectar["Capacitador"]="No tiene"
                                        datos_recolectar["Maestros_capacitados"]= 0
                                        datos_recolectar["Maestros_promovidos"]=0
                                        datos_recolectar["Maestros_no_promovidos"]=0
                                        datos_recolectar["Maestros_desertores"]=0
                                        datos_recolectar["Fecha_capacitacion"]="No tiene"
                                        datos_enviar.append(datos_recolectar)
                                    else:
                                        for  data_sede in data1.escuela_beneficiada.get_sedes():
                                            capacitador = data_sede.capacitador.get_full_name()
                                            fecha_creacion =data_sede.fecha_creacion.date()
                                            datos_recolectar["Fecha_capacitacion"]= fecha_creacion
                                        datos_recolectar["Capacitada"]=True
                                        grupo=cyd_m.Grupo.objects.filter(sede=data1.escuela_beneficiada.get_sedes())
                                        for datos in grupo:
                                            total_hombre = total_hombre + datos.get_hombres()
                                            total_mujeres = total_mujeres + datos.get_mujeres()
                                            total_aprobados= total_aprobados +datos.count_aprobados()
                                        maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede=data1.escuela_beneficiada.get_sedes(),abandono=True).count()
                                        datos_recolectar["Capacitador"]=capacitador
                                        datos_recolectar["Maestros_capacitados"]= total_hombre + total_mujeres
                                        datos_recolectar["Maestros_promovidos"]=total_aprobados
                                        datos_recolectar["Maestros_no_promovidos"]=(total_mujeres + total_hombre) - total_aprobados
                                        datos_recolectar["Maestros_desertores"]=maestros_desertores
                                        datos_enviar.append(datos_recolectar)
                #endIF
            else:
                print("No trae los  dos filtros")
                try:
                    for data in queryset.filter(filter_clauses)[:1000]:
                        datos_recolectar={}
                        datos_recolectar["Udi"]=data.codigo
                        datos_recolectar["Nombre"]=data.nombre
                        datos_recolectar["Direccion"]=data.direccion
                        datos_recolectar["Departamento"]=data.municipio.departamento.nombre
                        datos_recolectar["Municipio"]=data.municipio.nombre
                        datos_recolectar["escuela_url"]=data.get_absolute_url()
                        datos_recolectar["Ninos_beneficiados"]=data.poblacion
                        datos_recolectar["Docentes"]=data.maestros
                        if data.datos_equipamiento():
                            datos_recolectar["Fecha_equipamiento"]=data.datos_equipamiento().fecha
                            datos_recolectar["No_equipamiento"]=str(data.datos_equipamiento().id)
                            if data.datos_equipamiento().cooperante.all().last() is None:
                                datos_recolectar["Donante"]="No tiene"
                            else:
                                datos_recolectar["Donante"]=str(data.datos_equipamiento().cooperante.all().last())
                            if  data.datos_equipamiento().proyecto.all().last() is None:
                                datos_recolectar["Proyecto"]="No tiene"
                            else:
                                datos_recolectar["Proyecto"]=str(data.datos_equipamiento().proyecto.all().last())
                            datos_recolectar["Equipo_entregado"]=data.datos_equipamiento().cantidad_equipo
                        else:
                            datos_recolectar["Fecha_equipamiento"]=0
                            datos_recolectar["No_equipamiento"]=0
                            datos_recolectar["Donante"]="No tiene"
                            datos_recolectar["Proyecto"]="No tiene"
                            datos_recolectar["Equipo_entregado"]=0
                        if data.capacitacion["capacitada"]== True:
                            for  data_sede in data.get_sedes():
                                capacitador = data_sede.capacitador.get_full_name()
                                fecha_creacion =data_sede.fecha_creacion.date()
                            datos_recolectar["Capacitada"]=True
                            grupo=cyd_m.Grupo.objects.filter(sede=data.get_sedes())
                            for datos in grupo:
                                total_hombre = total_hombre + datos.get_hombres()
                                total_mujeres = total_mujeres + datos.get_mujeres()
                                total_aprobados= total_aprobados +datos.count_aprobados()
                            maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede=data.get_sedes(),abandono=True).count()
                            try:
                                datos_recolectar["Capacitador"]=capacitador
                                datos_recolectar["Maestros_capacitados"]= total_hombre + total_mujeres
                                datos_recolectar["Maestros_promovidos"]=total_aprobados
                                datos_recolectar["Maestros_no_promovidos"]=(total_mujeres + total_hombre) - total_aprobados
                                datos_recolectar["Maestros_desertores"]=maestros_desertores
                                datos_recolectar["Fecha_capacitacion"]=fecha_creacion
                            except Exception as e:
                                datos_recolectar["Capacitador"]="No tiene"
                                datos_recolectar["Maestros_capacitados"]= 0
                                datos_recolectar["Maestros_promovidos"]=0
                                datos_recolectar["Maestros_no_promovidos"]=0
                                datos_recolectar["Maestros_desertores"]=0
                                datos_recolectar["Fecha_capacitacion"]="No tiene"
                        else:
                            datos_recolectar["Capacitada"]=False
                            datos_recolectar["Fecha_capacitacion"]=0
                            datos_recolectar["Capacitador"]="No tiene"
                            datos_recolectar["Maestros_capacitados"]= 0
                            datos_recolectar["Maestros_promovidos"]=0
                            datos_recolectar["Maestros_no_promovidos"]=0
                            datos_recolectar["Maestros_desertores"]=0
                        datos_enviar.append(datos_recolectar)
                except Exception as e:
                    print("Carretera")
                    try:
                        for data in queryset2.filter(filter_clauses):
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
                                datos_recolectar["Docentes"]=poblacion.total_maestro
                            except Exception as e:
                                datos_recolectar["Ninos_beneficiados"]=0
                                datos_recolectar["Docentes"]=0
                            if data.cantidad_equipo >=1:
                                datos_recolectar["Equipada"]=True
                            else:
                                datos_recolectar["Equipada"]=False
                            datos_recolectar["Fecha_equipamiento"]=data.fecha
                            datos_recolectar["No_equipamiento"]=str(data.id)
                            datos_recolectar["Donante"]=str(data.cooperante.all().last())
                            datos_recolectar["Proyecto"]=str(data.proyecto.all().last())
                            datos_recolectar["Equipo_entregado"]=data.cantidad_equipo
                            sede_capacitada= cyd_m.Sede.objects.filter(escuela_beneficiada__codigo=data.escuela.codigo).last()
                            if cyd_m.Sede.objects.filter(escuela_beneficiada__codigo=data.escuela.codigo).count() >=1:
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
                        for data1 in queryset3.filter(filter_clauses):
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
                                datos_recolectar["Ninos_beneficiados"]=0
                                datos_recolectar["Docentes"]=0
                            data_equipamiento=tpe_m.Equipamiento.objects.filter(escuela__codigo=data1.escuela_beneficiada.codigo).last()
                            try:
                                 cantidad = data_equipamiento.cantidad_equipo
                            except Exception as e:
                                cantidad = 0
                            if cantidad >=1:
                                datos_recolectar["Equipada"]=True
                                datos_recolectar["Fecha_equipamiento"]=data_equipamiento.fecha
                                datos_recolectar["No_equipamiento"]=str(data_equipamiento.id)
                                datos_recolectar["Donante"]=str(data_equipamiento.cooperante.all().last())
                                datos_recolectar["Proyecto"]=str(data_equipamiento.proyecto.all().last())
                                datos_recolectar["Equipo_entregado"]=data_equipamiento.cantidad_equipo
                            else:
                                datos_recolectar["Equipada"]=False
                                datos_recolectar["Fecha_equipamiento"]=0
                                datos_recolectar["No_equipamiento"]=0
                                datos_recolectar["Donante"]=0
                                datos_recolectar["Proyecto"]=0
                                datos_recolectar["Equipo_entregado"]=0

                            if queryset3.filter(filter_clauses).count() >=1:
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
            print("No trae filtros")
            if filtros.get("capacitada")=='True' and filtros.get("equipada")=='True' :
                print("Viene 2 verdaderos")
                for data in tpe_m.Equipamiento.objects.distinct():
                    if(data.cantidad_equipo >0  and data.escuela.capacitacion["capacitada"] is True and data.escuela.get_sedes().count()>0):
                        datos_recolectar={}
                        datos_recolectar["Udi"]=data.escuela.codigo
                        datos_recolectar["Nombre"]=data.escuela.nombre
                        datos_recolectar["Direccion"]=data.escuela.direccion
                        datos_recolectar["Departamento"]=data.escuela.municipio.departamento.nombre
                        datos_recolectar["Municipio"]=data.escuela.municipio.nombre
                        datos_recolectar["escuela_url"]=data.escuela.get_absolute_url()
                        datos_recolectar["Ninos_beneficiados"]=data.escuela.poblacion
                        datos_recolectar["Docentes"]=data.escuela.maestros
                        datos_recolectar["Fecha_equipamiento"]=data.escuela.datos_equipamiento().fecha
                        datos_recolectar["No_equipamiento"]=str(data.escuela.datos_equipamiento().id)
                        datos_recolectar["Equipada"]=True
                        datos_recolectar["Donante"]=str(data.escuela.datos_equipamiento().cooperante.all().last())
                        datos_recolectar["Proyecto"]=str(data.escuela.datos_equipamiento().proyecto.all().last())
                        datos_recolectar["Equipo_entregado"]=data.escuela.datos_equipamiento().cantidad_equipo
                        for  data_sede in data.escuela.get_sedes():
                            capacitador = data_sede.capacitador.get_full_name()
                            fecha_creacion =data_sede.fecha_creacion.date()
                            datos_recolectar["Capacitada"]=True
                            datos_recolectar["Capacitador"]=capacitador
                            datos_recolectar["Fecha_capacitacion"]=fecha_creacion
                        grupo=cyd_m.Grupo.objects.filter(sede__in=data.escuela.get_sedes())
                        for datos in grupo:
                            total_hombre = total_hombre + datos.get_hombres()
                            total_mujeres = total_mujeres + datos.get_mujeres()
                            total_aprobados= total_aprobados +datos.count_aprobados()
                        maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede__in=data.escuela.get_sedes(),abandono=True).count()
                        datos_recolectar["Maestros_capacitados"]= total_hombre + total_mujeres
                        datos_recolectar["Maestros_promovidos"]=total_aprobados
                        datos_recolectar["Maestros_no_promovidos"]=(total_mujeres + total_hombre) - total_aprobados
                        datos_recolectar["Maestros_desertores"]=maestros_desertores
                        datos_enviar.append(datos_recolectar)
            elif filtros.get("capacitada")=='False' and filtros.get("equipada")=='False' :
                for data in escuela_m.Escuela.objects.distinct()[:1000]:
                     if (data.equipada is False and data.capacitacion["capacitada"] is False):
                         datos_recolectar={}
                         datos_recolectar["Udi"]=data.codigo
                         datos_recolectar["Nombre"]=data.nombre
                         datos_recolectar["Direccion"]=data.direccion
                         datos_recolectar["Departamento"]=data.municipio.departamento.nombre
                         datos_recolectar["Municipio"]=data.municipio.nombre
                         datos_recolectar["escuela_url"]=data.get_absolute_url()
                         datos_recolectar["Ninos_beneficiados"]=data.poblacion
                         datos_recolectar["Docentes"]=data.maestros
                         datos_recolectar["Fecha_equipamiento"]="No tiene"
                         datos_recolectar["No_equipamiento"]="No tiene"
                         datos_recolectar["Equipada"]=False
                         datos_recolectar["Donante"]="No tiene"
                         datos_recolectar["Proyecto"]="No tiene"
                         datos_recolectar["Equipo_entregado"]=0
                         datos_recolectar["Capacitada"]=False
                         datos_recolectar["Capacitador"]="No tiene"
                         datos_recolectar["Fecha_capacitacion"]="No tiene"
                         datos_recolectar["Maestros_capacitados"]=0
                         datos_recolectar["Maestros_promovidos"]=0
                         datos_recolectar["Maestros_no_promovidos"]=0
                         datos_recolectar["Maestros_desertores"]=0
                         datos_enviar.append(datos_recolectar)
            elif filtros.get("capacitada")=='True' and filtros.get("equipada")=='False' :
                print("Viene capacitada  y no equipada")
            elif filtros.get("capacitada")=='True':
                for data in tpe_m.Equipamiento.objects.distinct():
                    if(data.escuela.capacitacion["capacitada"] is True):
                        if(data.escuela.get_sedes().count()>0):
                            datos_recolectar={}
                            datos_recolectar["Udi"]=data.escuela.codigo
                            datos_recolectar["Nombre"]=data.escuela.nombre
                            datos_recolectar["Direccion"]=data.escuela.direccion
                            datos_recolectar["Departamento"]=data.escuela.municipio.departamento.nombre
                            datos_recolectar["Municipio"]=data.escuela.municipio.nombre
                            datos_recolectar["escuela_url"]=data.escuela.get_absolute_url()
                            datos_recolectar["Ninos_beneficiados"]=data.escuela.poblacion
                            datos_recolectar["Docentes"]=data.escuela.maestros
                            datos_recolectar["Fecha_equipamiento"]=data.escuela.datos_equipamiento().fecha
                            datos_recolectar["No_equipamiento"]=str(data.escuela.datos_equipamiento().id)
                            datos_recolectar["Equipada"]=True
                            datos_recolectar["Donante"]=str(data.escuela.datos_equipamiento().cooperante.all().last())
                            datos_recolectar["Proyecto"]=str(data.escuela.datos_equipamiento().proyecto.all().last())
                            datos_recolectar["Equipo_entregado"]=data.escuela.datos_equipamiento().cantidad_equipo
                            for data_sede in data.escuela.get_sedes():
                                capacitador = data_sede.capacitador.get_full_name()
                                fecha_creacion =data_sede.fecha_creacion.date()
                                datos_recolectar["Capacitada"]=True
                                datos_recolectar["Capacitador"]=capacitador
                                datos_recolectar["Fecha_capacitacion"]=fecha_creacion
                            grupo=cyd_m.Grupo.objects.filter(sede__in=data.escuela.get_sedes())
                            for datos in grupo:
                                total_hombre = total_hombre + datos.get_hombres()
                                total_mujeres = total_mujeres + datos.get_mujeres()
                                total_aprobados= total_aprobados +datos.count_aprobados()
                            maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede__in=data.escuela.get_sedes(),abandono=True).count()
                            datos_recolectar["Maestros_capacitados"]= total_hombre + total_mujeres
                            datos_recolectar["Maestros_promovidos"]=total_aprobados
                            datos_recolectar["Maestros_no_promovidos"]=(total_mujeres + total_hombre) - total_aprobados
                            datos_recolectar["Maestros_desertores"]=maestros_desertores
                            datos_enviar.append(datos_recolectar)
            elif filtros.get("equipada")=='True':
                print("Solo viene equipada")
                for data in tpe_m.Equipamiento.objects.distinct():
                    if(data.cantidad_equipo >0 ):
                        datos_recolectar={}
                        datos_recolectar["Udi"]=data.escuela.codigo
                        datos_recolectar["Nombre"]=data.escuela.nombre
                        datos_recolectar["Direccion"]=data.escuela.direccion
                        datos_recolectar["Departamento"]=data.escuela.municipio.departamento.nombre
                        datos_recolectar["Municipio"]=data.escuela.municipio.nombre
                        datos_recolectar["escuela_url"]=data.escuela.get_absolute_url()
                        datos_recolectar["Ninos_beneficiados"]=data.escuela.poblacion
                        datos_recolectar["Docentes"]=data.escuela.maestros
                        datos_recolectar["Fecha_equipamiento"]=data.escuela.datos_equipamiento().fecha
                        datos_recolectar["No_equipamiento"]=str(data.escuela.datos_equipamiento().id)
                        datos_recolectar["Equipada"]=True
                        datos_recolectar["Donante"]=str(data.escuela.datos_equipamiento().cooperante.all().last())
                        datos_recolectar["Proyecto"]=str(data.escuela.datos_equipamiento().proyecto.all().last())
                        datos_recolectar["Equipo_entregado"]=data.escuela.datos_equipamiento().cantidad_equipo
                        if data.escuela.get_sedes().count()>0:
                            for  data_sede in data.escuela.get_sedes():
                                capacitador = data_sede.capacitador.get_full_name()
                                fecha_creacion =data_sede.fecha_creacion.date()
                                datos_recolectar["Capacitada"]=True
                                datos_recolectar["Capacitador"]=capacitador
                                datos_recolectar["Fecha_capacitacion"]=fecha_creacion
                        else:
                            datos_recolectar["Capacitada"]=False
                            datos_recolectar["Capacitador"]="No tiene"
                            datos_recolectar["Fecha_capacitacion"]="No tiene fecha"
                        grupo=cyd_m.Grupo.objects.filter(sede__in=data.escuela.get_sedes())
                        for datos in grupo:
                            total_hombre = total_hombre + datos.get_hombres()
                            total_mujeres = total_mujeres + datos.get_mujeres()
                            total_aprobados= total_aprobados +datos.count_aprobados()
                        maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede__in=data.escuela.get_sedes(),abandono=True).count()
                        datos_recolectar["Maestros_capacitados"]= total_hombre + total_mujeres
                        datos_recolectar["Maestros_promovidos"]=total_aprobados
                        datos_recolectar["Maestros_no_promovidos"]=(total_mujeres + total_hombre) - total_aprobados
                        datos_recolectar["Maestros_desertores"]=maestros_desertores
                        datos_enviar.append(datos_recolectar)
            elif filtros.get("equipada")=='False':
                for data in queryset.filter()[:1000]:
                    if(data.equipada is False):
                        datos_recolectar={}
                        datos_recolectar["Udi"]=data.codigo
                        datos_recolectar["Nombre"]=data.nombre
                        datos_recolectar["Direccion"]=data.direccion
                        datos_recolectar["Departamento"]=data.municipio.departamento.nombre
                        datos_recolectar["Municipio"]=data.municipio.nombre
                        datos_recolectar["escuela_url"]=data.get_absolute_url()
                        datos_recolectar["Ninos_beneficiados"]=data.poblacion
                        datos_recolectar["Docentes"]=data.maestros
                        datos_recolectar["Fecha_equipamiento"]="No tiene"
                        datos_recolectar["No_equipamiento"]=0
                        datos_recolectar["Equipada"]=False
                        datos_recolectar["Donante"]="No tiene"
                        datos_recolectar["Proyecto"]="No tiene"
                        datos_recolectar["Equipo_entregado"]=0
                        if data.get_sedes().count()>0:
                            for  data_sede in data.get_sedes():
                                capacitador = data_sede.capacitador.get_full_name()
                                fecha_creacion =data_sede.fecha_creacion.date()
                                datos_recolectar["Capacitada"]=True
                                datos_recolectar["Capacitador"]=capacitador
                                datos_recolectar["Fecha_capacitacion"]=fecha_creacion
                        else:
                            datos_recolectar["Capacitada"]=False
                            datos_recolectar["Capacitador"]="No tiene"
                            datos_recolectar["Fecha_capacitacion"]="No tiene fecha"

                        grupo=cyd_m.Grupo.objects.filter(sede__in=data.get_sedes())
                        for datos in grupo:
                            total_hombre = total_hombre + datos.get_hombres()
                            total_mujeres = total_mujeres + datos.get_mujeres()
                            total_aprobados= total_aprobados +datos.count_aprobados()
                        maestros_desertores=cyd_m.Asignacion.objects.filter(grupo__sede__in=data.get_sedes(),abandono=True).count()
                        datos_recolectar["Maestros_capacitados"]= total_hombre + total_mujeres
                        datos_recolectar["Maestros_promovidos"]=total_aprobados
                        datos_recolectar["Maestros_no_promovidos"]=(total_mujeres + total_hombre) - total_aprobados
                        datos_recolectar["Maestros_desertores"]=maestros_desertores
                        datos_enviar.append(datos_recolectar)
            else:
                print("Viene equipa y no capacitada")
                for data in tpe_m.Equipamiento.objects.distinct():
                    if(data.cantidad_equipo >0  and data.escuela.capacitacion["capacitada"] is False):
                        datos_recolectar={}
                        datos_recolectar["Udi"]=data.escuela.codigo
                        datos_recolectar["Nombre"]=data.escuela.nombre
                        datos_recolectar["Direccion"]=data.escuela.direccion
                        datos_recolectar["Departamento"]=data.escuela.municipio.departamento.nombre
                        datos_recolectar["Municipio"]=data.escuela.municipio.nombre
                        datos_recolectar["escuela_url"]=data.escuela.get_absolute_url()
                        datos_recolectar["Ninos_beneficiados"]=data.escuela.poblacion
                        datos_recolectar["Docentes"]=data.escuela.maestros
                        datos_recolectar["Fecha_equipamiento"]=data.escuela.datos_equipamiento().fecha
                        datos_recolectar["No_equipamiento"]=str(data.escuela.datos_equipamiento().id)
                        datos_recolectar["Equipada"]=True
                        datos_recolectar["Donante"]="No tiene"
                        datos_recolectar["Proyecto"]="No tiene"
                        datos_recolectar["Equipo_entregado"]=data.escuela.datos_equipamiento().cantidad_equipo
                        datos_recolectar["Capacitada"]=False
                        datos_recolectar["Capacitador"]="No tiene"
                        datos_recolectar["Fecha_capacitacion"]="No tiene"
                        datos_recolectar["Maestros_capacitados"]=0
                        datos_recolectar["Maestros_promovidos"]=0
                        datos_recolectar["Maestros_no_promovidos"]=0
                        datos_recolectar["Maestros_desertores"]=0
                        datos_enviar.append(datos_recolectar)
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
