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
from django.db.models import Count
# Create your views here.
class InformeView(FormView):
    """ Vista  encargada de obtener los filtros necesarios para poder  obterner la informacion
    """
    template_name = 'informe/informe.html'
    form_class = informe_f.informeForm

class ConsultaEscuelaApi(views.APIView):
    """Api para la creacion del informe general mediante un metodo get"""
    def get(self, request):        
        datos_enviar = []
        municipios_digitales =[]
        elegir_filtros = {}
        filtros_usar = {}
        contador_filtros = 0
        filtros_aplicar =""
        data = json.loads(self.request.GET["myData"]) 
        data_escuela = json.loads(data.get("escuela"))
        data_equipamiento = json.loads(data.get("equipada"))
        data_capacitada = json.loads(data.get("capacitacion"))
        elegir_filtros["escuela"] = len(data_escuela)
        elegir_filtros["equipamiento"] = len(data_equipamiento)
        elegir_filtros["capacitada"] = len(data_capacitada)
        viene_equipada = 0       
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
        for key,value in elegir_filtros.items():
            if value != 1:
                contador_filtros = contador_filtros + 1
                filtros_aplicar = key 
        if contador_filtros ==1:           
            if filtros_aplicar == "escuela":                
                for dataEscuela in data_escuela:
                    if dataEscuela["value"] !="":                                         
                        for new_key, filtro in filter_list.items():
                            if new_key == dataEscuela["name"]:
                                filtros_usar[filtro] = dataEscuela["value"]                
                query = escuela_m.Escuela.objects.filter(**filtros_usar)                     
            elif filtros_aplicar =="equipamiento":               
                for dataEquipamiento in data_equipamiento:
                    if dataEquipamiento["value"] !="":                       
                        if dataEquipamiento["name"] == "equipada":                                                                       
                            if dataEquipamiento["value"] is "0":                               
                                viene_equipada = 0
                            elif dataEquipamiento["value"] is "1":                               
                                viene_equipada = 1
                            elif dataEquipamiento["value"] is "2":                               
                                viene_equipada = 2
                        for new_key, filtro in filter_list.items():                            
                            if new_key == dataEquipamiento["name"]:
                                filtros_usar[filtro] = dataEquipamiento["value"]               
                query = tpe_m.Equipamiento.objects.filter(**filtros_usar)
            elif filtros_aplicar == "capacitada":                
                viene_capacitada = 0
                for dataCapacitacion in data_capacitada:                    
                    if dataCapacitacion["value"] !="":
                        if dataCapacitacion["name"] =="capacitada":                             
                            if dataCapacitacion["value"] is "0":
                                viene_capacitada = 0
                            elif dataCapacitacion["value"] is "1":
                                viene_capacitada = 1
                            elif dataCapacitacion["value"] is "2":
                                viene_capacitada = 2    
                        for new_key, filtro in filter_list.items():
                            if new_key == dataCapacitacion["name"]:
                                filtros_usar[filtro] = dataCapacitacion["value"]
                query = cyd_m.Sede.objects.filter(**filtros_usar)
        else:
            if int(data_capacitada[0]["value"]) == 0 and int(data_equipamiento[0]["value"]) ==0:
                    return Response(
                        {str("Por favor estos filtros tiene que acompañado de otro campo")},
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                if int(data_equipamiento[0]["value"]) ==1:                    
                    viene_equipada = 1
                    query=tpe_m.Equipamiento.objects.all()                    
                elif int(data_equipamiento[0]["value"]) ==2:                   
                    viene_equipada = 2
                    equipamientos =tpe_m.Equipamiento.objects.all().values('escuela')
                    query = escuela_m.Escuela.objects.exclude(id__in=equipamientos)
                elif int(data_capacitada[0]["value"]) ==1:                    
                    viene_capacitada = 1
                    query = cyd_m.Sede.objects.all()  
                elif int(data_capacitada[0]["value"]) ==2:                    
                    viene_capacitada = 2
                    sedes = cyd_m.Sede.objects.all().values('escuela_beneficiada')    
                    query = escuela_m.Escuela.objects.exclude(id__in=sedes)

        if isinstance(query.first(), cyd_m.Sede):            
            if viene_capacitada == 0:
                for data_final in query:  
                    datos_recolectar ={}
                    datos_recolectar["Udi"]= data_final.escuela_beneficiada.codigo
                    datos_recolectar["Nombre"]= data_final.escuela_beneficiada.nombre
                    datos_recolectar["escuela_url"]= data_final.escuela_beneficiada.get_absolute_url()
                    datos_recolectar["Direccion"]= data_final.escuela_beneficiada.direccion
                    datos_recolectar["Departamento"]= data_final.escuela_beneficiada.municipio.departamento.nombre
                    datos_recolectar["Municipio"]= data_final.escuela_beneficiada.municipio.nombre
                    datos_recolectar["Ninos_beneficiados"]= data_final.escuela_beneficiada.get_poblacion()
                    datos_recolectar["Docentes"]= data_final.escuela_beneficiada.get_maestros()
                    datos_recolectar["Equipada"]= data_final.escuela_beneficiada.es_equipada()
                    datos_recolectar["Cct"]= data_final.escuela_beneficiada.get_es_cct()
                    if data_final.escuela_beneficiada.get_es_muni_digi()==1:
                        municipios_digitales.append(data_final.escuela_beneficiada.municipio.id)                                            
                    if data_final.escuela_beneficiada.es_equipada():
                        datos_recolectar["Fecha_equipamiento"]= data_final.escuela_beneficiada.datos_equipamiento().fecha
                        datos_recolectar["No_equipamiento"]= data_final.escuela_beneficiada.datos_equipamiento().no_referencia
                        datos_recolectar["Proyecto"]= [x.nombre for x in data_final.escuela_beneficiada.datos_equipamiento().proyecto.all()]  
                        datos_recolectar["Donante"]= [x.nombre for x in data_final.escuela_beneficiada.datos_equipamiento().cooperante.all()]                       
                        datos_recolectar["Equipo_entregado"]= data_final.escuela_beneficiada.datos_equipamiento().cantidad_equipo
                    else:
                        datos_recolectar["Fecha_equipamiento"]= "No tiene"
                        datos_recolectar["No_equipamiento"]= "No tiene"
                        datos_recolectar["Proyecto"]= "No tiene"  
                        datos_recolectar["Donante"]= "No tiene"          
                        datos_recolectar["Equipo_entregado"]= 0
                    if data_final.escuela_beneficiada.fue_capacitada():
                        datos_recolectar["Capacitada"]= data_final.escuela_beneficiada.fue_capacitada()
                        datos_recolectar["Fecha_capacitacion"]=data_final.fecha_creacion.date()
                        datos_recolectar["Capacitador"]= data_final.capacitador.get_full_name()
                        datos_recolectar["Maestros_capacitados"]= data_final.escuela_beneficiada.get_escuelas_sedes("",data_final.escuela_beneficiada.codigo,data_final.id)["total_maestros"]
                        datos_recolectar["Maestros_promovidos"]= data_final.escuela_beneficiada.get_escuelas_sedes("",data_final.escuela_beneficiada.codigo,data_final.id)["aprobados"]
                        datos_recolectar["Maestros_no_promovidos"]=data_final.escuela_beneficiada.get_escuelas_sedes("",data_final.escuela_beneficiada.codigo,data_final.id)["reprobados"]
                        datos_recolectar["Maestros_desertores"]= data_final.escuela_beneficiada.get_escuelas_sedes("",data_final.escuela_beneficiada.codigo,data_final.id)["nivelar"]
                    else:
                        datos_recolectar["Capacitada"]= data_final.escuela_beneficiada.fue_capacitada()
                        datos_recolectar["Fecha_capacitacion"]="No tiene"
                        datos_recolectar["Capacitador"]= "No tiene"
                        datos_recolectar["Maestros_capacitados"]= 0
                        datos_recolectar["Maestros_promovidos"]= 0
                        datos_recolectar["Maestros_no_promovidos"]= 0
                        datos_recolectar["Maestros_desertores"]= 0
                    datos_recolectar["Municipios_digitales"]=len(set(municipios_digitales))    
                    datos_enviar.append(datos_recolectar)
            elif viene_capacitada == 1:
                for data_final in query:
                    if data_final.escuela_beneficiada.get_es_muni_digi()==1:
                        municipios_digitales.append(data_final.escuela_beneficiada.municipio.id)                        
                    if data_final.escuela_beneficiada.fue_capacitada():                        
                        datos_recolectar ={}
                        datos_recolectar["Udi"]= data_final.escuela_beneficiada.codigo
                        datos_recolectar["Nombre"]= data_final.escuela_beneficiada.nombre
                        datos_recolectar["escuela_url"]= data_final.escuela_beneficiada.get_absolute_url()
                        datos_recolectar["Direccion"]= data_final.escuela_beneficiada.direccion
                        datos_recolectar["Departamento"]= data_final.escuela_beneficiada.municipio.departamento.nombre
                        datos_recolectar["Municipio"]= data_final.escuela_beneficiada.municipio.nombre
                        datos_recolectar["Ninos_beneficiados"]= data_final.escuela_beneficiada.get_poblacion()
                        datos_recolectar["Docentes"]= data_final.escuela_beneficiada.get_maestros()
                        datos_recolectar["Equipada"]= data_final.escuela_beneficiada.es_equipada()
                        datos_recolectar["Capacitada"]= data_final.escuela_beneficiada.fue_capacitada()
                        datos_recolectar["Fecha_capacitacion"]=data_final.fecha_creacion.date()
                        datos_recolectar["Capacitador"]= data_final.capacitador.get_full_name()
                        datos_recolectar["Maestros_capacitados"]= data_final.escuela_beneficiada.get_escuelas_sedes("",data_final.escuela_beneficiada.codigo,data_final.id)["total_maestros"]
                        datos_recolectar["Maestros_promovidos"]= data_final.escuela_beneficiada.get_escuelas_sedes("",data_final.escuela_beneficiada.codigo,data_final.id)["aprobados"]
                        datos_recolectar["Maestros_no_promovidos"]=data_final.escuela_beneficiada.get_escuelas_sedes("",data_final.escuela_beneficiada.codigo,data_final.id)["reprobados"]
                        datos_recolectar["Maestros_desertores"]= data_final.escuela_beneficiada.get_escuelas_sedes("",data_final.escuela_beneficiada.codigo,data_final.id)["nivelar"]
                        datos_recolectar["Cct"]= data_final.escuela_beneficiada.get_es_cct()
                        if data_final.escuela_beneficiada.es_equipada():
                            datos_recolectar["Fecha_equipamiento"]= data_final.escuela_beneficiada.datos_equipamiento().fecha
                            datos_recolectar["No_equipamiento"]= data_final.escuela_beneficiada.datos_equipamiento().no_referencia
                            datos_recolectar["Proyecto"]= [x.nombre for x in data_final.escuela_beneficiada.datos_equipamiento().proyecto.all()]  
                            datos_recolectar["Donante"]= [x.nombre for x in data_final.escuela_beneficiada.datos_equipamiento().cooperante.all()]                       
                            datos_recolectar["Equipo_entregado"]= data_final.escuela_beneficiada.datos_equipamiento().cantidad_equipo
                        else:
                            datos_recolectar["Fecha_equipamiento"]= "No tiene"
                            datos_recolectar["No_equipamiento"]= "No tiene"
                            datos_recolectar["Proyecto"]= "No tiene"  
                            datos_recolectar["Donante"]= "No tiene"          
                            datos_recolectar["Equipo_entregado"]= 0
                    datos_recolectar["Municipios_digitales"]=len(set(municipios_digitales)) 
                    datos_enviar.append(datos_recolectar)     
            elif viene_capacitada == 2:
                print("No hay capacitadas")
                return Response(
                        {str("No hay escuelas capacitadas")},
                        status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(query.first(), tpe_m.Equipamiento):
            if viene_equipada ==0:                             
                for data_final in query:                  
                    datos_recolectar ={}
                    datos_recolectar["Udi"]= data_final.escuela.codigo
                    datos_recolectar["Nombre"]= data_final.escuela.nombre
                    datos_recolectar["escuela_url"]= data_final.escuela.get_absolute_url()
                    datos_recolectar["Direccion"]= data_final.escuela.direccion
                    datos_recolectar["Departamento"]= data_final.escuela.municipio.departamento.nombre
                    datos_recolectar["Municipio"]= data_final.escuela.municipio.nombre
                    datos_recolectar["Ninos_beneficiados"]= data_final.escuela.get_poblacion()
                    datos_recolectar["Docentes"]= data_final.escuela.get_maestros()
                    datos_recolectar["Equipada"]= data_final.escuela.es_equipada()
                    datos_recolectar["Cct"]= data_final.escuela.get_es_cct()
                    if data_final.escuela.get_es_muni_digi()==1:
                        municipios_digitales.append(data_final.escuela.municipio.id) 
                    if data_final.escuela.es_equipada():
                        datos_recolectar["Fecha_equipamiento"]= data_final.escuela.datos_equipamiento().fecha
                        datos_recolectar["No_equipamiento"]= data_final.escuela.datos_equipamiento().no_referencia
                        datos_recolectar["Proyecto"]= [x.nombre for x in data_final.escuela.datos_equipamiento().proyecto.all()]  
                        datos_recolectar["Donante"]= [x.nombre for x in data_final.escuela.datos_equipamiento().cooperante.all()]                       
                        datos_recolectar["Equipo_entregado"]= data_final.escuela.datos_equipamiento().cantidad_equipo
                    else:
                        datos_recolectar["Fecha_equipamiento"]= "No tiene"
                        datos_recolectar["No_equipamiento"]= "No tiene"
                        datos_recolectar["Proyecto"]= "No tiene"  
                        datos_recolectar["Donante"]= "No tiene"          
                        datos_recolectar["Equipo_entregado"]= 0
                    if data_final.escuela.fue_capacitada():
                        sede_capacitada = data_final.escuela.escuela_beneficiada.all().order_by('fecha_creacion').last()                       
                        total = sede_capacitada.get_participantes()['resumen']["estado"]["aprobado"]["cantidad"] + sede_capacitada.get_participantes()['resumen']["estado"]["reprobado"]["cantidad"] + sede_capacitada.get_participantes()['resumen']["estado"]["nivelar"]["cantidad"]                        
                        datos_recolectar["Capacitada"]= data_final.escuela.fue_capacitada()
                        datos_recolectar["Fecha_capacitacion"]=sede_capacitada.fecha_creacion.date()
                        datos_recolectar["Capacitador"]= sede_capacitada.capacitador.get_full_name()
                        datos_recolectar["Maestros_capacitados"]= total
                        datos_recolectar["Maestros_promovidos"]= sede_capacitada.get_participantes()['resumen']["estado"]["aprobado"]["cantidad"]
                        datos_recolectar["Maestros_no_promovidos"]=sede_capacitada.get_participantes()['resumen']["estado"]["reprobado"]["cantidad"]
                        datos_recolectar["Maestros_desertores"]= sede_capacitada.get_participantes()['resumen']["estado"]["nivelar"]["cantidad"]
                    else:
                        datos_recolectar["Capacitada"]= data_final.escuela.fue_capacitada()
                        datos_recolectar["Fecha_capacitacion"]="No tiene"
                        datos_recolectar["Capacitador"]= "No tiene"
                        datos_recolectar["Maestros_capacitados"]= 0
                        datos_recolectar["Maestros_promovidos"]= 0
                        datos_recolectar["Maestros_no_promovidos"]= 0
                        datos_recolectar["Maestros_desertores"]= 0
                    datos_recolectar["Municipios_digitales"]=len(set(municipios_digitales))    
                    datos_enviar.append(datos_recolectar)
            elif viene_equipada ==1:               
                for data_final in query:
                    datos_recolectar ={}
                    datos_recolectar["Udi"]= data_final.escuela.codigo
                    datos_recolectar["Nombre"]= data_final.escuela.nombre
                    datos_recolectar["escuela_url"]= data_final.escuela.get_absolute_url()
                    datos_recolectar["Direccion"]= data_final.escuela.direccion
                    datos_recolectar["Departamento"]= data_final.escuela.municipio.departamento.nombre
                    datos_recolectar["Municipio"]= data_final.escuela.municipio.nombre
                    datos_recolectar["Ninos_beneficiados"]= data_final.escuela.get_poblacion()
                    datos_recolectar["Docentes"]= data_final.escuela.get_maestros()
                    datos_recolectar["Equipada"]= data_final.escuela.es_equipada()
                    datos_recolectar["Cct"]= data_final.escuela.get_es_cct()
                    if data_final.escuela.get_es_muni_digi()==1:
                        municipios_digitales.append(data_final.escuela_beneficiada.municipio.id) 
                    if data_final.escuela.es_equipada():
                        datos_recolectar["Fecha_equipamiento"]= data_final.escuela.datos_equipamiento().fecha
                        datos_recolectar["No_equipamiento"]= data_final.escuela.datos_equipamiento().no_referencia
                        datos_recolectar["Proyecto"]= [x.nombre for x in data_final.escuela.datos_equipamiento().proyecto.all()]  
                        datos_recolectar["Donante"]= [x.nombre for x in data_final.escuela.datos_equipamiento().cooperante.all()]                       
                        datos_recolectar["Equipo_entregado"]= data_final.escuela.datos_equipamiento().cantidad_equipo
                    else:
                        datos_recolectar["Fecha_equipamiento"]= "No tiene"
                        datos_recolectar["No_equipamiento"]= "No tiene"
                        datos_recolectar["Proyecto"]= "No tiene"  
                        datos_recolectar["Donante"]= "No tiene"          
                        datos_recolectar["Equipo_entregado"]= 0
                    if data_final.escuela.fue_capacitada():
                        sede_capacitada = data_final.escuela.escuela_beneficiada.all().order_by('fecha_creacion').last()                       
                        total = sede_capacitada.get_participantes()['resumen']["estado"]["aprobado"]["cantidad"] + sede_capacitada.get_participantes()['resumen']["estado"]["reprobado"]["cantidad"] + sede_capacitada.get_participantes()['resumen']["estado"]["nivelar"]["cantidad"]                        
                        datos_recolectar["Capacitada"]= data_final.escuela.fue_capacitada()
                        datos_recolectar["Fecha_capacitacion"]=sede_capacitada.fecha_creacion.date()
                        datos_recolectar["Capacitador"]= sede_capacitada.capacitador.get_full_name()
                        datos_recolectar["Maestros_capacitados"]= total
                        datos_recolectar["Maestros_promovidos"]= sede_capacitada.get_participantes()['resumen']["estado"]["aprobado"]["cantidad"]
                        datos_recolectar["Maestros_no_promovidos"]=sede_capacitada.get_participantes()['resumen']["estado"]["reprobado"]["cantidad"]
                        datos_recolectar["Maestros_desertores"]= sede_capacitada.get_participantes()['resumen']["estado"]["nivelar"]["cantidad"]
                    else:
                        datos_recolectar["Capacitada"]= data_final.escuela.fue_capacitada()
                        datos_recolectar["Fecha_capacitacion"]="No tiene"
                        datos_recolectar["Capacitador"]= "No tiene"
                        datos_recolectar["Maestros_capacitados"]= 0
                        datos_recolectar["Maestros_promovidos"]= 0
                        datos_recolectar["Maestros_no_promovidos"]= 0
                        datos_recolectar["Maestros_desertores"]= 0
                    datos_recolectar["Municipios_digitales"]=len(set(municipios_digitales))
                    datos_enviar.append(datos_recolectar)
            elif viene_equipada ==2:
                for data_final in query:
                    datos_recolectar ={}
                    datos_recolectar["Udi"]= data_final.escuela.codigo
                    datos_recolectar["Nombre"]= data_final.escuela.nombre
                    datos_recolectar["escuela_url"]= data_final.escuela.get_absolute_url()
                    datos_recolectar["Direccion"]= data_final.escuela.direccion
                    datos_recolectar["Departamento"]= data_final.escuela.municipio.departamento.nombre
                    datos_recolectar["Municipio"]= data_final.escuela.municipio.nombre
                    datos_recolectar["Ninos_beneficiados"]= data_final.escuela.get_poblacion()
                    datos_recolectar["Docentes"]= data_final.escuela.get_maestros()
                    datos_recolectar["Equipada"]= data_final.escuela.es_equipada()
                    datos_recolectar["Cct"]= data_final.escuela.get_es_cct()
                    if data_final.escuela.get_es_muni_digi()==1:
                        municipios_digitales.append(data_final.escuela_beneficiada.municipio.id) 
                    if data_final.escuela.es_equipada() is not True:
                        datos_recolectar["Fecha_equipamiento"]= data_final.escuela.datos_equipamiento().fecha
                        datos_recolectar["No_equipamiento"]= data_final.escuela.datos_equipamiento().no_referencia
                        datos_recolectar["Proyecto"]= [x.nombre for x in data_final.escuela.datos_equipamiento().proyecto.all()]  
                        datos_recolectar["Donante"]= [x.nombre for x in data_final.escuela.datos_equipamiento().cooperante.all()]                       
                        datos_recolectar["Equipo_entregado"]= data_final.escuela.datos_equipamiento().cantidad_equipo
                    else:
                        datos_recolectar["Fecha_equipamiento"]= "No tiene"
                        datos_recolectar["No_equipamiento"]= "No tiene"
                        datos_recolectar["Proyecto"]= "No tiene"  
                        datos_recolectar["Donante"]= "No tiene"          
                        datos_recolectar["Equipo_entregado"]= 0
                    if data_final.escuela.fue_capacitada():
                        sede_capacitada = data_final.escuela.escuela_beneficiada.all().order_by('fecha_creacion').last()                       
                        total = sede_capacitada.get_participantes()['resumen']["estado"]["aprobado"]["cantidad"] + sede_capacitada.get_participantes()['resumen']["estado"]["reprobado"]["cantidad"] + sede_capacitada.get_participantes()['resumen']["estado"]["nivelar"]["cantidad"]                        
                        datos_recolectar["Capacitada"]= data_final.escuela.fue_capacitada()
                        datos_recolectar["Fecha_capacitacion"]=sede_capacitada.fecha_creacion.date()
                        datos_recolectar["Capacitador"]= sede_capacitada.capacitador.get_full_name()
                        datos_recolectar["Maestros_capacitados"]= total
                        datos_recolectar["Maestros_promovidos"]= sede_capacitada.get_participantes()['resumen']["estado"]["aprobado"]["cantidad"]
                        datos_recolectar["Maestros_no_promovidos"]=sede_capacitada.get_participantes()['resumen']["estado"]["reprobado"]["cantidad"]
                        datos_recolectar["Maestros_desertores"]= sede_capacitada.get_participantes()['resumen']["estado"]["nivelar"]["cantidad"]
                    else:
                        datos_recolectar["Capacitada"]= data_final.escuela.fue_capacitada()
                        datos_recolectar["Fecha_capacitacion"]="No tiene"
                        datos_recolectar["Capacitador"]= "No tiene"
                        datos_recolectar["Maestros_capacitados"]= 0
                        datos_recolectar["Maestros_promovidos"]= 0
                        datos_recolectar["Maestros_no_promovidos"]= 0
                        datos_recolectar["Maestros_desertores"]= 0
                    datos_recolectar["Municipios_digitales"]=len(set(municipios_digitales))
                    datos_enviar.append(datos_recolectar)                    
        elif isinstance(query.first(), escuela_m.Escuela):            
            for data_final in query:
                datos_recolectar ={}                               
                datos_recolectar["Udi"]= data_final.codigo
                datos_recolectar["Nombre"]= data_final.nombre
                datos_recolectar["escuela_url"]= data_final.get_absolute_url()
                datos_recolectar["Direccion"]= data_final.direccion
                datos_recolectar["Departamento"]= data_final.municipio.departamento.nombre
                datos_recolectar["Municipio"]= data_final.municipio.nombre
                datos_recolectar["Ninos_beneficiados"]= data_final.get_poblacion()
                datos_recolectar["Docentes"]= data_final.get_maestros()
                datos_recolectar["Equipada"]= data_final.es_equipada()
                datos_recolectar["Cct"]= data_final.get_es_cct()
                if data_final.get_es_muni_digi()==1:
                        municipios_digitales.append(data_final.municipio.id) 
                if data_final.es_equipada():
                        datos_recolectar["Fecha_equipamiento"]= data_final.datos_equipamiento().fecha
                        datos_recolectar["No_equipamiento"]= data_final.datos_equipamiento().no_referencia
                        datos_recolectar["Proyecto"]= [x.nombre for x in data_final.datos_equipamiento().proyecto.all()]
                        datos_recolectar["Donante"]= [x.nombre for x in data_final.datos_equipamiento().cooperante.all()]
                        datos_recolectar["Equipo_entregado"]= data_final.datos_equipamiento().cantidad_equipo                        
                else:
                    datos_recolectar["Fecha_equipamiento"]= "No tiene"
                    datos_recolectar["No_equipamiento"]= "No tiene"
                    datos_recolectar["Proyecto"]= "No tiene"
                    datos_recolectar["Donante"]= "No tiene"
                    datos_recolectar["Equipo_entregado"]= 0
                if data_final.fue_capacitada():
                        sede_capacitada = data_final.escuela_beneficiada.all().order_by('fecha_creacion').last()                       
                        total = sede_capacitada.get_participantes()['resumen']["estado"]["aprobado"]["cantidad"] + sede_capacitada.get_participantes()['resumen']["estado"]["reprobado"]["cantidad"] + sede_capacitada.get_participantes()['resumen']["estado"]["nivelar"]["cantidad"]                        
                        datos_recolectar["Capacitada"]= data_final.fue_capacitada()
                        datos_recolectar["Fecha_capacitacion"]=sede_capacitada.fecha_creacion.date()
                        datos_recolectar["Capacitador"]= sede_capacitada.capacitador.get_full_name()
                        datos_recolectar["Maestros_capacitados"]= total
                        datos_recolectar["Maestros_promovidos"]= sede_capacitada.get_participantes()['resumen']["estado"]["aprobado"]["cantidad"]
                        datos_recolectar["Maestros_no_promovidos"]=sede_capacitada.get_participantes()['resumen']["estado"]["reprobado"]["cantidad"]
                        datos_recolectar["Maestros_desertores"]= sede_capacitada.get_participantes()['resumen']["estado"]["nivelar"]["cantidad"]
                else:
                    datos_recolectar["Capacitada"]= data_final.fue_capacitada()
                    datos_recolectar["Fecha_capacitacion"]="No tiene"
                    datos_recolectar["Capacitador"]= "No tiene"
                    datos_recolectar["Maestros_capacitados"]= 0
                    datos_recolectar["Maestros_promovidos"]= 0
                    datos_recolectar["Maestros_no_promovidos"]= 0
                    datos_recolectar["Maestros_desertores"]= 0
                datos_recolectar["Municipios_digitales"]=len(set(municipios_digitales))
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
class InformeFinalView(TemplateView):
    """ Vista  encargada de obtener los filtros necesarios para poder  obterner la informacion
    """
    template_name = 'informe/informeFinal.html'

    def get_context_data(self, **kwargs):
        context = super(InformeFinalView, self).get_context_data(**kwargs)
        context['form_escuela'] = informe_f.informeEscuelaForm        
        context['form_equipada'] = informe_f.informeEquipamientoForm
        context['form_capacitada'] = informe_f.informeCapacitadaForm
        return context