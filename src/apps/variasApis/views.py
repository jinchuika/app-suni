from django.shortcuts import render
from apps.inventario import models as inv_m
from apps.cyd import models as cyd_m
import qrcode
import json
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import gettext_lazy as _
from openpyxl import load_workbook
import os
from django.conf import settings
from django.contrib.auth.models import User
from apps.escuela.models import *
import json
from apps.main.models import Municipio

# Create your views here.
from rest_framework import views, status
from rest_framework.response import Response  

class SubirTodo(views.APIView): 
    """  Clase encargada de Subir todos los datos de los archivos json a las tablas del modulo de cyd del SUNI
    """
    def get(self, request):
            ruta = "C:/Users/Edgar/Documents/TablasMigrarSuni/json/"
            file_escuela = open(str(ruta)+"cyd_escuela_new.json",encoding="utf-8")
            file_asesoria = open(str(ruta)+"cyd_asesoria.json",encoding="utf-8")
            file_asignacion = open(str(ruta)+"cyd_asignacion.json",encoding="utf-8")#1
            file_calendario = open(str(ruta)+"cyd_calendario.json",encoding="utf-8")#2
            file_crasistencia = open(str(ruta)+"cyd_crasistencia.json",encoding="utf-8")#3
            file_crhito = open(str(ruta)+"cyd_crhito.json",encoding="utf-8")#4
            file_curso = open(str(ruta)+"cyd_curso.json",encoding="utf-8")#5
            file_grupo = open( str(ruta)+"cyd_grupo.json",encoding="utf-8")#6
            file_notaasistencia = open( str(ruta)+"cyd_notaasistencia.json",encoding="utf-8")#7
            file_notahito = open(str(ruta)+"cyd_notahito.json",encoding="utf-8")#8
            file_parescolaridad =open(str(ruta)+"cyd_parescolaridad.json",encoding="utf-8")#9
            file_paretnia = open( str(ruta)+"cyd_paretnia.json",encoding="utf-8")#10
            file_pargenero = open( str(ruta)+"cyd_pargenero.json",encoding="utf-8")#11
            file_parrol = open( str(ruta)+"cyd_parrol.json",encoding="utf-8")#12         
            file_participante =open( str(ruta)+"cyd_participante.json",encoding="utf-8")#13
            file_sede = open( str(ruta)+"cyd_sede.json",encoding="utf-8")#14
            file = open(str(ruta)+"errores_finales2.txt", "w")
            data_file_escuela = json.load(file_escuela)#1
            data_file_asesoria = json.load(file_asesoria)#2
            data_file_asignacion = json.load(file_asignacion)#3
            data_file_calendario = json.load(file_calendario)#4
            data_file_crasistencia  = json.load(file_crasistencia)#5
            data_file_crhito = json.load(file_crhito)#6
            data_file_grupo = json.load(file_grupo)#7
            data_file_notaasistencia = json.load(file_notaasistencia)#8
            data_file_notahito = json.load(file_notahito)#9
            data_file_parescolaridad = json.load(file_parescolaridad)#10
            data_file_paretnia = json.load(file_paretnia)#11
            data_file_parrol = json.load( file_parrol)#12
            data_file_pargenero = json.load(file_pargenero)#13
            data_file_participante = json.load(file_participante)#14
            data_file_sede = json.load(file_sede)#15
            data_file_curso = json.load(file_curso)#16
            #data_ = json.load(f)
            for data_escuela in data_file_escuela:
                 print("escuela:",str(data_escuela['id']))
                 try:
                      escuela= Escuela.objects.get(codigo=data_escuela["codigo"])
                      #print(escuela)
                 except Exception as a:
                      escuela = Escuela(
                           codigo=data_escuela["codigo"],
                           distrito=data_escuela["distrito"],
                           municipio=Municipio.objects.get(id=data_escuela["municipio_id"]),
                           nombre=data_escuela["nombre"],
                           direccion=data_escuela["direccion"],
                           telefono=data_escuela["telefono"],
                           nivel=EscNivel.objects.get(id=data_escuela["nivel_id"]),
                           sector=EscSector.objects.get(id=data_escuela["sector_id"]),
                           area=EscArea.objects.get(id=data_escuela["area_id"]),
                           status=EscStatus.objects.get(id=data_escuela["status_id"]),
                           modalidad=EscModalidad.objects.get(id=data_escuela["modalidad_id"]),
                           jornada=EscJornada.objects.get(id=data_escuela["jornada_id"]),
                           plan=EscPlan.objects.get(id=data_escuela["plan_id"]),                         
                           
                           )
                      escuela.save()
                      
                      file.write(str(a)+str(data_escuela["codigo"])+'\n')
                      #print(a)
            file_escuela.close()
            print("---FIN ESCUELA---")
            for data_parrol  in data_file_parrol:
                 print("rol:",data_parrol["id"])
                 try:
                      rol = cyd_m.ParRol.objects.get(id=data_parrol["id"])
                 except Exception as b:
                      file.write(str(b)+str(data_parrol["id"])+'\n')
                      rol = cyd_m.ParRol(
                           id = data_parrol["id"],
		                 nombre = data_parrol["nombre"]
                           
                      )
                      rol.save()
            file_parrol.close()
            print("---FIN ROL---") 
            for data_participante  in data_file_participante:
                 print("participante",data_participante["id"])
                 try:
                      cyd_m.Participante.objects.id(id=data_participante["id"])
                 except Exception as c:
                    file.write(str(c)+str(data_participante["id"])+'\n')
                    nuevo_registro_participantes = cyd_m.Participante(
                            id = data_participante["id"],                            
                            nombre = data_participante["nombre"],                            
                            apellido= data_participante["apellido"],                            
                            genero = cyd_m.ParGenero.objects.get(id=data_participante["genero_id"]),                            
                            direccion = data_participante["direccion"],
                            mail = data_participante["mail"],                            
                            fecha_nac = data_participante["fecha_nac"],
                            escolaridad=cyd_m.ParEscolaridad.objects.get(id=data_participante["escolaridad_id"]),
                            escuela = Escuela.objects.get(id=data_participante["escuela_id"]),
                            etnia = cyd_m.ParEtnia.objects.get(id=data_participante["etnia_id"]),                            
                            rol = cyd_m.ParRol.objects.get(id=data_participante["rol_id"]),
                            slug= data_participante["slug"],
                            activo= data_participante["activo"],
                            dpi = data_participante["dpi"],  
                            tel_casa = data_participante["tel_casa"],
                            tel_movil = data_participante["tel_movil"]
                            
                              
                    )
                    nuevo_registro_participantes.save()
            file_participante.close()
            print("---FIN PARTICIPANTE---")
            for data_sede  in data_file_sede:
                 print("sede:",data_sede["id"])
                 try:
                     cyd_m.Sede.objects.get(id=data_sede["id"])
                 except Exception as d:
                      #print(datos["id_usr"])    
                      file.write(str(d)+str(data_sede["id"])+'\n')                  
                      sede=cyd_m.Sede(
                        id = data_sede["id"],
                        nombre = data_sede["nombre"],
                        capacitador = User.objects.get(id=data_sede["capacitador_id"]),
                        municipio = Municipio.objects.get(id=data_sede["municipio_id"]),
                        direccion = data_sede["direccion"],
                        observacion = data_sede["observacion"],
                        escuela_beneficiada = Escuela.objects.get(id=data_sede["escuela_beneficiada_id"]),
                        fecha_creacion  = data_sede["fecha_creacion"],
                        tipo_sede = data_sede["tipo_sede"],
                        activa = data_sede["activa"]                   
                        )
                      sede.save()
            file_sede.close()
            print("-- FIN SEDE----") 
            for data_curso  in data_file_curso:
                 print("curso",data_curso["id"])
                 try:
                      curso = cyd_m.Curso.objects.get(id=data_curso["id"])
                 except Exception as f:
                      file.write(str(f)+str(data_curso["id"])+'\n')
                      curso = cyd_m.Curso(
                           id=data_curso["id"],
                           nombre=data_curso["nombre"],
                           nota_aprobacion=data_curso["nota_aprobacion"],                           
                           activo=data_curso["activo"]
                      )
                      curso.save()
            file_curso.close() 
            print("---FIN CURSO---")
            for data_grupo  in data_file_grupo:
                 print("grupo:",data_grupo["id"])
                 try:
                       cyd_m.Grupo.objects.get(id=data_grupo["id"])
                 except Exception as e:
                      file.write(str(e)+str(data_grupo["id"])+'\n')
                      grupo=cyd_m.Grupo(
                            id = data_grupo["id"],
                            sede = cyd_m.Sede.objects.get(id=data_grupo["sede_id"]),
                            numero =data_grupo["numero"] ,
                            curso = cyd_m.Curso.objects.get(id=data_grupo["curso_id"]),
                            comentario = data_grupo["comentario"],
                            cyd_grupo_creado_por = User.objects.get(id=data_grupo["cyd_grupo_creado_por_id"]),
                            activo = data_grupo["activo"]                     
                        )
                      grupo.save()
                    
            file_grupo.close()
            print("---FIN GRUPO---")
                 
            for data_asignacion  in data_file_asignacion:
                 print("asignacion",data_asignacion["id"])
                 try:
                      cyd_m.Asignacion.objects.get(id=data_asignacion["id"])
                 except Exception as g:
                    asignacion=cyd_m.Asignacion(
                        id = data_asignacion["id"],
                        participante = cyd_m.Participante.objects.get(id=data_asignacion["participante_id"]),
                        grupo =cyd_m.Grupo.objects.get(id=data_asignacion["grupo_id"]),
                        abandono = data_asignacion["abandono"]                  
                    )
                    asignacion.save()
            file_asignacion.close()
            print("---FIN ASIGNACION---") 
            for data_crasistencia  in data_file_crasistencia:
                 print("crasitencia:",data_crasistencia["id"])
                 try:
                     cr_asi = cyd_m.CrAsistencia.objects.get(id=data_crasistencia["id"])
                 except Exception as h:
                      file.write(str(h)+str(data_crasistencia["id"])+'\n')
                      cr_asistecias=cyd_m.CrAsistencia(
                        id = data_crasistencia["id"],
                        curso=cyd_m.Curso.objects.get(id=data_crasistencia["curso_id"]),
                        modulo_num=data_crasistencia["modulo_num"],
                        punteo_max = data_crasistencia["punteo_max"]

                         )
                      cr_asistecias.save()            
            file_crasistencia.close()
            print("---FIN CRASISTENCIA---") 

            for data_crhito  in data_file_crhito:
                 print("cr_hito:",data_crhito["id"])
                 try:
                      cyd_m.CrHito.objects.get(id=data_crhito["id"])
                   
                 except Exception as i:
                     file.write(str(i)+str(data_crhito["id"])+'\n')
                     cr_hito=cyd_m.CrHito(
                        id = data_crhito["id"],
                        curso=cyd_m.Curso.objects.get(id=data_crhito["curso_id"]),
                        nombre=data_crhito["nombre"],
                        punteo_max=data_crhito["punteo_max"]
                     )
                     cr_hito.save()          
                 
            file_crhito.close()
            print("---FIN CRHITO---") 

            for data_calendario  in data_file_calendario:
                 print("calendario:",data_calendario["id"])
                 try:
                      cyd_m.Calendario.objects.get(id=data_calendario["id"])
                 except Exception as j:
                      file.write(str(j)+str(data_calendario["id"])+'\n')
                      calendario=cyd_m.Calendario(
                            id = data_calendario["id"],
                            cr_asistencia=cyd_m.CrAsistencia.objects.get(id=data_calendario["cr_asistencia_id"]),
                            grupo=cyd_m.Grupo.objects.get(id=data_calendario["grupo_id"]),
                            fecha=data_calendario["fecha"],
                            hora_inicio=data_calendario["hora_inicio"],
                            hora_fin=data_calendario["hora_fin"]

                            )
                      calendario.save()
                      
            file_calendario.close()
            print("---FIN CALENDARIO---")  
            for data_notaasistencia  in data_file_notaasistencia:
                 print("nota asistencia:",data_notaasistencia["id"])
                 try:
                     asistencia=  cyd_m.NotaAsistencia.objects.get(id=data_notaasistencia ["id"])                     
                 except Exception as k:
                    file.write(str(k)+str(data_notaasistencia["id"])+'\n')
                    notas_asistencias=cyd_m.NotaAsistencia(
                            id = data_notaasistencia ["id"],
                            asignacion=cyd_m.Asignacion.objects.get(id=data_notaasistencia ["asignacion_id"]),
                            gr_calendario=cyd_m.Calendario.objects.get(id=data_notaasistencia ["gr_calendario_id"]),
                            nota=data_notaasistencia ["nota"]

                         )
                    notas_asistencias.save()
                         
            file_notaasistencia.close()
            print("---FIN NOTA ASISTENCIA---")      
            for data_notahito  in data_file_notahito:
                 print("notahito",data_notahito["id"])
                 
                 try:
                       nota = cyd_m.NotaHito.objects.get(id=data_notahito["id"])                       
                 except Exception as l:
                        file.write(str(l)+str(data_notahito["id"])+'\n')
                        nota_hito=cyd_m.NotaHito(
                            id = data_notahito["id"],
                            asignacion=cyd_m.Asignacion.objects.get(id=data_notahito["asignacion_id"]),
                            cr_hito = cyd_m.CrHito.objects.get(id=data_notahito["cr_hito_id"]),
                            nota=data_notahito["nota"]

                        )
                        nota_hito.save()
            file_notahito.close()
            print("---FIN HITO---")

            

            for data_asesoria  in data_file_asesoria:
                 print("asesoria:",data_asesoria["id"])
                 try:
                      aseso = cyd_m.Asesoria.objects.get(id=data_asesoria["id"])
                 except Exception as m:
                    file.write(str(m)+str(data_asesoria["id"])+'\n')
                    asesorias=cyd_m.Asesoria(
                        id = data_asesoria["id"],
                        sede=cyd_m.Sede.objects.get(id=data_asesoria["sede_id"]),
                        fecha=data_asesoria["fecha"],
                        hora_inicio=data_asesoria["hora_inicio"],
                        hora_fin=data_asesoria["hora_fin"],
                        observacion=data_asesoria["observacion"]

                    )
                    asesorias.save()
            file_asesoria.close()
            print("---FIN ASESORIA---") 

                
                
                
                       
           
                
                  
            """ for data_parescolaridad  in data_file_parescolaridad:
                 print(data_parescolaridad["id"])
            file_parescolaridad.close()
            print("---FIN ESCOLARIDAD---")      
            for data_paretnia  in data_file_paretnia:
                 print(data_paretnia["id"])
            file_paretnia.close()
            print("--FIN ESCOLARIDAD----")      
            for data_pargenero  in data_file_pargenero:
                 print(data_pargenero["id"])
            file_pargenero.close()
            print("--PAR GENERO----")      
             """    
                  
                 
            file.close()
                            
            return Response(
                            "Datos ingresados Correctamente Carlitos Ya podes ir a descanzar",
                            status=status.HTTP_200_OK
                        ) 
class RevionErrores(views.APIView):
        """ Importar registros de excel con DjangoRestFramework para Bienestar
        """
        def get(self, request):
            ruta = "C:/Users/Edgar/Documents/TablasMigrarSuni/json/" 
            file = open(str(ruta)+"errores_finales2.txt", "rb")
            lineas = file.readlines()
                               
            return Response(
                            lineas,
                            status=status.HTTP_200_OK
                        ) 





