import json
import qrcode
import requests
import shutil
import os
import datetime
import locale
import sys
from django.shortcuts import render
from apps.certificado import forms as certificado_f
from django.views.generic import TemplateView, FormView, DetailView, View
from django.middleware import csrf
from apps.cyd import models  as cyd_m
from apps.Evaluacion import models as eval_m
from django.conf import settings
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from django.core.urlresolvers import reverse_lazy
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Sum, Count
from io import BytesIO
from django.core import signing

class CertificadoMaestroView(FormView):
    """ Vista  encargada de obtener el dpi del participante por medio un  formulario y  muesta el listado de los
    cursos que se tienen asignados
    """
    template_name = 'certificado/certificado.html'
    form_class = certificado_f.DpiForm


class ListadoMaestroView(TemplateView):
     """ Vista  encargada de mostrar los cursos que  el  participante tiene asignado, muesta tambien cuales estan aprobados
     y cuales estan reprobados para asi poder imprimir los que  esta aprobados.
     tambien se conecta al suni de capacitacion para obtener todo esta informacion por medio de un metodo get y asi mostarar
     los datos del participante.
    """
     template_name = 'certificado/listadoMaestros.html'
     def get_context_data(self, **kwargs):
        context = super(ListadoMaestroView, self).get_context_data(**kwargs)
        #print("ACA ESTAMOS 2024")
        # Consumir Servicio PHP para obtener datos de suni capacitación por DPI
        url = settings.LEGACY_URL['certificado']        
        if url is not '':
             params = {'dpi': self.request.GET['dpi']}
             try:
                resp = requests.get(url=url, params= params)              
             except:
                print("en espera")
        else:
             print("el dpi esta vacio")
        try:
           #print(resp.json())           
           data= resp.json()                    
           #print("data:",data)
           if len(data) is 0:
               context['validacion'] = 0
           else:
               sedes = []
               sede_asignacion = []

               # Obtener Información General del Maestro              
               context['nombre'] = str(data[0]['nombre'])+" "+str(data[0]['apellido'])
               context['dpi']=self.request.GET['dpi']
               context['rol'] = data[0]['rol']
               context['escuela'] =data[0]['escuela']
               context['email'] =data[0]['email']     
               #print("email:",data[0]['email'])
               # Obtener Listado de Sedes
               for valor in data:                  
                  sede = valor['sede']
                  if sede not in sedes:                   
                    sedes.append(sede)

               # Recorrer Sedes del Maestro
               for sede in sedes:
                #print(sede.encode('utf-8'))                
                #print(sede)
                asignaciones = []
                cursos = []
                suma_curso = 0
                naat = False
                grupo_naat = 1
                year_cert = False
                year_const = False
                fecha_final = 0
                id_sede = 0
                combo_completo = False
                ka_lite = False
                grupo_combos = 0
                gano_tni = 0
                centro_comunitario = False
                solo_ka_lite = False
                # Obtener Promedio de Cursos por Sede
                for valor_data in data:               
                  if sede == valor_data['sede']:                    
                    validar_palabra = str(valor_data['descripcion'])                     
                    if validar_palabra.find("beneficiada") is not -1 or validar_palabra.find("BEQT") is not -1:                                                         
                        context['beneficiada'] = 1
                    else:
                        context['beneficiada'] = 0
                    #verificar si gano tni
                    validar_nombre_tni = str(valor_data['curso'])
                    #print("aca:",validar_nombre_tni)
                    if validar_nombre_tni.find("Tecnologia Nivel Intermedio") is not -1:
                       #print("si si entro")                      
                       if int(valor_data['nota']) < int(valor_data['nota_minima']):                                                    
                          gano_tni = 0
                       else:
                          #print("aca")                              
                          gano_tni= 1
                                                                 
                    id_sede = int(valor_data['id_sede'])
                    suma_curso += int(valor_data['nota'])
                    fecha_final = datetime.datetime.strptime(valor_data['fecha_final'], '%Y-%m-%d').date()
                    # Fecha válida para constancias (31 días)
                    fecha_valida_const = fecha_final + datetime.timedelta(days=90)

                    # Validar si recibió NAAT en la sede (18 o 22 semanas) o bien si recibió KaLite (Grupo 4)                   
                    if grupo_naat == 1 or grupo_naat == 2 and naat == False:                      
                      grupo = int(valor_data['grupo'])                          
                      if grupo == 1:
                        grupo_combos += 1
                      elif grupo == 2:
                        grupo_naat = 2
                      elif grupo == 3:
                        grupo_naat = 3
                        naat = True
                      elif grupo == 4:
                        grupo_combos += 1
                        ka_lite = True
                      elif grupo ==5:
                         centro_comunitario = True

                    # Validar si la capacitación fué durante el año actual y si no ha expirado el periodo de tiempo
                    if fecha_final.year <= datetime.date.today().year:
                      if datetime.date.today() <= fecha_valida_const:
                          year_const = True
                    valor_data['year_const'] = year_const

                    # Agregar asignación a la sede predeterminada
                    asignaciones.append(valor_data)

                # Cálculo de Promedio
                promedio = suma_curso / len(asignaciones)
                # Validar si la capacitación fué durante el año actual y si no ha expirado el periodo de tiempo
                fecha_valida_cert = fecha_final + datetime.timedelta(days=730)
                if fecha_final.year <= datetime.date.today().year:
                  if datetime.date.today() <= fecha_valida_cert:
                      year_cert = True

                # Validar si se ha dado el combo completo:
                #print(grupo_combos)
                if grupo_combos == 4 and ka_lite == True:
                  combo_completo = True  
                else: 
                  combo_completo = False
                
                if grupo_combos == 1 and ka_lite == True:
                   solo_ka_lite =  True
                  
                # Crear Objeto Asignacion por sede                           
                values = {"id": id_sede,"sede": sede, "asignaciones": asignaciones, "promedio": promedio, "grupo":grupo_naat, "year_cert":year_cert, "combo_completo":combo_completo,"gano_tni":gano_tni,"centro_comunitario":centro_comunitario,"solo_ka_lite":solo_ka_lite,"naat":naat}
                sede_asignacion.append(dict(values)) 
                #print(sede_asignacion)                            
               context['sedes'] = sede_asignacion
               context['validacion'] = 1
        except:
          #print(resp.json())
          print(sys.exc_info())
          print("Oops!", sys.exc_info()[0], "occurred.")         
          context['validacion'] = 0
        return context

class DiplomaPdfView(View):
   """ Vista  encargada de generar los diplomas que se entregaran a los participantes de los cursos, obteniendo el dpi
    para mostrar el resultado de que diploma se va a imprimir se puede  descargar el pdf del archivo tambien
   """
   def get( self, request, *args, **kwargs):
      # Obtener Parametros
      tipo_curso = self.request.GET['curso']     
      id_sede = self.request.GET['sede']      
      # Inicializar Variables
      curso_asignado = 0
      curso_aprobado = 0
      curso_naat = 0
      year_cert = False
      url_perfil = str("https://suni.funsepa.org/")+ str(reverse_lazy('listado')) + str("?dpi=")+str(self.request.GET['dpi'])
      url = settings.LEGACY_URL['certificado']
      locale.setlocale(locale.LC_ALL, 'es_GT.utf8')

      # Se hace la peticion al servidor de suni-capacitacion para mostrar los datos
      if url is not '':
             params = {'dpi': self.request.GET['dpi']}
             try:
                resp = requests.get(url=url, params= params)
             except:
                print("en espera")
      else:
             print("el dpi esta vacio")
      data= resp.json()

      # Se valida si se obtuvo información
      if len(data) is 0:
         return HttpResponse("El dpi ingresado no es valido")
      else:
         suma_curso = 0
         fecha_final = 0
         naat = False
         grupo_naat = 1
         combo_completo = False
         ka_lite = False
         grupo_combos = 0
         asignaciones = []
         centro_comunitario = False        
         for  nuevo in data:
            if int(nuevo['id_sede']) == int(id_sede):
              suma_curso += int(nuevo['nota'])
              fecha_final = datetime.datetime.strptime(nuevo['fecha_final'], '%Y-%m-%d').date()

              # Validar si recibió NAAT en la sede
              if grupo_naat == 1 or grupo_naat == 2 and naat == False:
                grupo = int(nuevo['grupo'])
                if grupo==1:
                  grupo_combos += 1
                elif grupo == 2:
                  grupo_naat = 2
                elif grupo == 3:
                  grupo_naat = 3
                  naat = True
                elif grupo == 4:
                  grupo_combos += 1
                  ka_lite = True
                elif grupo == 5:
                   centro_comunitario = True
              asignaciones.append(nuevo)

         # Validar si la capacitación fué durante el año actual y si no ha expirado el periodo de tiempo}
         #fecha_valida_cert = fecha_final + datetime.timedelta(days=30)
         fecha_valida_cert = fecha_final + datetime.timedelta(days=1095)
         if fecha_final.year <= datetime.date.today().year:
            if datetime.date.today() <= fecha_valida_cert:
              if fecha_final.year >= 2021:
                year_cert = True

         if year_cert == False:
            return HttpResponse("Curso No Válido")
         if centro_comunitario is not True:
            if grupo_naat == 1:
              if grupo_combos < 4 or ka_lite == False:
                return HttpResponse("Programa de capacitación no finalizado")
          

         if len(asignaciones) > 0:
            promedio = suma_curso / len(asignaciones)
            if promedio >= 75:
              #Creacion de codigos QR
              qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=6,
                border=1,)

              qr.add_data(url_perfil)
              qr.make(fit=True)
              filename = 'perfil-{}.png'.format(self.request.GET['dpi'])
              ruta_origin = str(os.getcwd()) +str("/")+ str(filename)
              ruta_qr = str(settings.MEDIA_ROOT) + str("qr_perfil/")+str(filename)

              #mover codigo QR a la carpeta correspondiente
              if not (os.path.isfile(ruta_qr)):
                img = qr.make_image()
                img.save(filename)
                shutil.move(ruta_origin,ruta_qr)

              #creacion de tipo de hoja y asignar imagen para colocar de fondo
              h=letter
              if int(tipo_curso) == 2 and grupo_naat == 2:
                ruta_diploma = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/CertificadoNaat22.png")
              elif int(tipo_curso) == 3 and grupo_naat == 3:
                #ruta_diploma = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/CertificadoNaat18.png")
                ruta_diploma = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/CertificadoNaat2023.jpg")
              elif int(tipo_curso) == 1 and centro_comunitario is True:
                 ruta_diploma = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/CertificadoCCT2023.jpg")
              else:                
                #ruta_diploma = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/CertificadoTB.png")
                ruta_diploma = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/CertificadoTNI2023.jpg")

              #obtener tipo de fuente que se le aplicara al nombre del diploma
              ruta_ttf = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/MyriadPro_BoldIt.ttf")
              registerFont(TTFont('MyriadPro_BoldIt',ruta_ttf))
              ruta_ttf = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/MyriadPro_Regular.ttf")
              registerFont(TTFont('MyriadPro_Regular',ruta_ttf))
              #obtener nuevas fuentes
              ruta_ttf = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/EdwardianScriptITC.ttf")
              registerFont(TTFont('Edwardian',ruta_ttf))
              response = HttpResponse(content_type='application/pdf')
              if int(tipo_curso) == 2 and grupo_naat == 2:
                response['Content-Disposition'] = 'filename="DiplomaFunsepaNaat22-{}.pdf"'.format(str(self.request.GET['dpi']))
              elif int(tipo_curso) == 3 and grupo_naat == 3:
                response['Content-Disposition'] = 'filename="DiplomaFunsepaNaat18-{}.pdf"'.format(str(self.request.GET['dpi']))
              else:
                response['Content-Disposition'] = 'filename="DiplomaFunsepaTB-{}.pdf"'.format(str(self.request.GET['dpi']))

              #Creacion de canvas con el programa reportlab para colocar todos los elementos del diploma
              buffer = BytesIO()
              c = canvas.Canvas(buffer, pagesize=(landscape(letter)))
              x = 400
              y = 220
              """if int(tipo_curso) == 2 and grupo_naat == 2 or int(tipo_curso) == 3 and grupo_naat == 3:
                y = 275
              else:
                y = 220"""
              w = 103
              h = 119

              #creacion  de la imagen que se colocora de fondo
              c.drawImage(ruta_diploma, 0,0,width=792,height=612,anchor='sw',anchorAtXY=True,showBoundary=False)
              c.drawImage(ruta_qr,35,45,width=75,height=75,anchor='sw',anchorAtXY=True,showBoundary=False)
              c.setFont("Edwardian",60,leading=None)
              #c.setFont("MyriadPro_Regular",30,leading=None)
              c.setFillColor((0,0,0))
              #c.drawCentredString(x+w*0.0,y+h*0.5, str(data[0]['nombre'].upper())+" "+str(data[0]['apellido'].upper()))
              c.drawCentredString(x+w*0.0,y+h*0.5, str(data[0]['nombre'])+" "+str(data[0]['apellido']))
              c.setFont("MyriadPro_BoldIt",18,leading=None)
              c.drawCentredString(x+w*0.0,60+h*0.5, "Guatemala, " + datetime.datetime.now().strftime("%d de %B del %Y"))
              
              """if int(tipo_curso) == 2 and grupo_naat == 2 or int(tipo_curso) == 3 and grupo_naat == 3:
                c.drawCentredString(x+w*0.0,y+h*0.5, str(data[0]['nombre'])+" "+str(data[0]['apellido']))
                c.setFont("MyriadProBold",15,leading=None)
                c.drawCentredString(x+w*0.0,75+h*0.5, "Guatemala, " + datetime.datetime.now().strftime("%d de %B del %Y"))
              else:
                c.drawCentredString(x+w*0.0,y+h*0.5, str(data[0]['nombre'])+" "+str(data[0]['apellido']))
                c.setFont("MyriadProBold",15,leading=None)
                c.drawCentredString(x+w*0.0,60+h*0.5, "Guatemala, " + datetime.datetime.now().strftime("%d de %B del %Y"))"""
              c.setTitle('Diploma Funsepa')
              c.showPage()
              c.save()
              pdf = buffer.getvalue()
              buffer.close()
              response.write(pdf)
              return response
            else:
              return HttpResponse("Tienes nota de reprobado")
         else:
            return HttpResponse("No tiene asignado este curso")

class ConstanciaPdfView(View):
   """ Vista  encargada de generar los diplomas que se entregaran a los participantes de los cursos, obteniendo el dpi
    para mostrar el resultado de que diploma se va a imprimir se puede  descargar el pdf del archivo tambien
   """
   def get( self, request, *args, **kwargs):
      # Obtener Parametros
      id_asignacion = self.request.GET['asignacion']

      # Inicializar Variables
      curso_asignado = 0
      curso_aprobado = 0
      curso_naat = 0
      url_perfil = str("https://suni.funsepa.org/")+ str(reverse_lazy('listado')) + str("?dpi=")+str(self.request.GET['dpi'])
      url = settings.LEGACY_URL['certificado']
      locale.setlocale(locale.LC_ALL, 'es_GT.utf8')

      # Se hace la peticion al servidor de suni-capacitacion para mostrar los datos
      if url is not '':
             params = {'dpi': self.request.GET['dpi']}
             try:
                resp = requests.get(url=url, params= params)
             except:
                print("en espera")
      else:
             print("el dpi esta vacio")
      data= resp.json()    

      # Se valida si se obtuvo información
      if len(data) is 0:
         return HttpResponse("El dpi ingresado no es valido")
      else:
         nota_curso = 0
         nota_minima = 0
         fecha_final = 0
         url_constancia = ''
         year_const = False
         asignaciones = []

         for  registro in data:
            if int(registro['numero_asignacion']) == int(id_asignacion):
              nota_curso = int(registro['nota'])
              nota_minima = int(registro['nota_minima'])
              fecha_final = datetime.datetime.strptime(registro['fecha_final'], '%Y-%m-%d').date()
              url_constancia = str(registro['constancia'])
              asignaciones.append(registro)

         #fecha_valida_const = fecha_final + datetime.timedelta(days=90)
         fecha_valida_const = fecha_final + datetime.timedelta(days=365)
         # Validar si la capacitación fué durante el año actual y si no ha expirado el periodo de tiempo
         if fecha_final.year <= datetime.date.today().year:
            if datetime.date.today() <= fecha_valida_const:
                year_const = True

         if year_const == False:
            return HttpResponse("Curso No Válido") #Certificado

         if len(asignaciones) > 0:
            if nota_curso >= nota_minima:
              #Creacion de codigos QR
              qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=6,
                border=1,)

              qr.add_data(url_perfil)
              qr.make(fit=True)
              filename = 'perfil-{}.png'.format(self.request.GET['dpi'])
              ruta_origin = str(os.getcwd()) +str("/")+ str(filename)
              ruta_qr = str(settings.MEDIA_ROOT) + str("qr_perfil/")+str(filename)

              #mover codigo QR a la carpeta correspondiente
              if not (os.path.isfile(ruta_qr)):
                img = qr.make_image()
                img.save(filename)
                shutil.move(ruta_origin,ruta_qr)

              #creacion de tipo de hoja y asignar imagen para colocar de fondo
              h=letter
              ruta_diploma = str(settings.STATICFILES_DIRS[0] ) + str("/css/constancia/") + str(url_constancia)

              #obtener tipo de fuente que se le aplicara al nombre del diploma
              ruta_ttf = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/EdwardianScriptITC.ttf")
              registerFont(TTFont('Edwardian',ruta_ttf))
              response = HttpResponse(content_type='application/pdf')
              response['Content-Disposition'] = 'filename="ConstanciaFunsepaTB-{}.pdf"'.format(str(self.request.GET['dpi']))

              #Creacion de canvas con el programa reportlab para colocar todos los elementos del diploma
              buffer = BytesIO()
              c = canvas.Canvas(buffer, pagesize=(landscape(letter)))
              x = 400
              y = 230
              w = 103
              h = 119

              #creacion  de la imagen que se colocora de fondo
              c.drawImage(ruta_diploma, 0,0,width=792,height=612,anchor='sw',anchorAtXY=True,showBoundary=False)
              c.drawImage(ruta_qr,35,45,width=75,height=75,anchor='sw',anchorAtXY=True,showBoundary=False)
              c.setFont("Edwardian",50,leading=None)
              c.setFillColor((0,0,0))
              c.drawCentredString(x+w*0.0,y+h*0.5, str(data[0]['nombre'])+" "+str(data[0]['apellido']))
              c.setFont("Times-Bold",15,leading=None)
              c.drawCentredString(x+w*0.0,60+h*0.5, "Guatemala, " + datetime.datetime.now().strftime("%d de %B del %Y"))
              c.setTitle('Constancia Funsepa')
              c.showPage()
              c.save()
              pdf = buffer.getvalue()
              buffer.close()
              response.write(pdf)
              return response
            else:
              return HttpResponse("Tienes nota de reprobado")
         else:
            return HttpResponse("No tiene asignado este curso")
         
class CertificadoNuevoMaestroView(FormView):
    """ Vista  encargada de obtener el dpi del participante por medio un  formulario y  muesta el listado de los
    cursos que se tienen asignados
    """
    template_name = 'certificado/newcertificado.html'
    form_class = certificado_f.DpiForm
         
class NewListadoMaestroView(TemplateView):
     """ Vista  encargada de mostrar los cursos que  el  participante tiene asignado, muesta tambien cuales estan aprobados
     y cuales estan reprobados para asi poder imprimir los que  esta aprobados.
     tambien se conecta al suni de capacitacion para obtener todo esta informacion por medio de un metodo get y asi mostarar
     los datos del participante.
    """
     template_name = 'certificado/newlistadoMaestros.html'
     def get_context_data(self, **kwargs):
         context = super(NewListadoMaestroView, self).get_context_data(**kwargs)   
         sedes = []   
         data_certificado = {}
         data_participante = {}  
         info_participante = cyd_m.Participante.objects.get(dpi=self.request.GET['dpi'])
         encuesta = eval_m.AsignacionPregunta.objects.filter(evaluado=info_participante).last()         
         info_asignaciones = cyd_m.Asignacion.objects.filter(participante=info_participante)
         info_notas = 0
         sedes_mostrar = cyd_m.Asignacion.objects.values_list('grupo__sede',flat=True).order_by("-grupo__sede").filter(participante=info_participante).distinct()        
         listado_sedes = list(sedes_mostrar) 
         data_participante["nombre"]= info_participante.nombre +" "+info_participante.apellido
         data_participante["dpi"]=info_participante.dpi
         data_participante["codigo"]=signing.dumps(info_participante.dpi)
         data_participante["direccion"]=info_participante.direccion
         data_participante["email"]=info_participante.mail
         data_participante["etnia"]=info_participante.etnia.nombre
         data_participante["escuela"]=info_participante.escuela.nombre
         data_participante["rol"]=info_participante.rol.nombre
         data_participante["profesion"]=info_participante.profesion
         data_certificado["participante"]=data_participante         
         contador_curso = 0
         nota_naat =0              
         ultima_sede = listado_sedes[0]
         es_naat= False      
         while len(listado_sedes) != 0:
            id_cursos =[]  
            data_sedes = {}
            numero_sede = listado_sedes.pop()
            cursos = []
            #recorrido para obtener los cursos
            for  data_tni in info_asignaciones.filter(grupo__sede__id=numero_sede):               
               contador_curso = contador_curso +1
               #TNI2024
               if(data_tni.grupo.curso.id) in [66,67,68,69]:
                  id_cursos.append(data_tni.grupo.curso.id)
               #TNI2023 Y RESTO 2024
               if(data_tni.grupo.curso.id) in [66,67,68,53]:
                  id_cursos.append(data_tni.grupo.curso.id)
               #Kolibri-Khan Y RESTO 2024
               if(data_tni.grupo.curso.id) in [71,67,68,69]:
                  id_cursos.append(data_tni.grupo.curso.id)
                #TNI2023  
               elif (data_tni.grupo.curso.id) in [53,55,56,57]:
                  id_cursos.append(data_tni.grupo.curso.id)
                #NAAT 2024                  
               elif (data_tni.grupo.curso.id) in [62,63,64,65]:                  
                  es_naat =True
                  id_cursos.append(data_tni.grupo.curso.id)
                  nota_naat = nota_naat + data_tni.get_nota_promediada()["nota"]

            #recorrido para asignar el tipo de certificado o constancia que se entregara
            id_cursos = list(dict.fromkeys(id_cursos))
            for  data in info_asignaciones.filter(grupo__sede__id=numero_sede):               
               data_cursos = {}
               if ultima_sede == numero_sede:                
                if sum(id_cursos)== 270:                   
                    if data.grupo.numero==2:
                      if data.get_nota_final()>=70:
                        data_sedes["tipo"]=signing.dumps("constancia_tni")
                        data_sedes["constancia"]=True
                      else:
                         data_sedes["constancia"]=False                      
                    else:
                      if data.grupo.curso.id in [69]:                       
                         if data.get_nota_final()>=70:                          
                          data_sedes["tipo"]=signing.dumps("certificado_tni")
                          data_sedes["certificado"]=True
                         else:                            
                            data_sedes["certificado"]=False
                elif sum(id_cursos) == 221:
                   if data.grupo.sede.fecha_creacion.year ==2024:
                      data_sedes["tipo"]=signing.dumps("certificado_tni")
                      data_sedes["certificado"]=True
                elif sum(id_cursos) == 254 and es_naat==False:
                   if data.grupo.sede.fecha_creacion.year ==2024:
                      data_sedes["tipo"]=signing.dumps("certificado_tni")
                      data_sedes["certificado"]=True
                elif sum(id_cursos) ==135:                  
                    if data.grupo.curso.id in [69]:
                      if data.get_nota_final()>=70:                          
                          data_sedes["tipo"]=signing.dumps("certificado_tni_kalite")
                          data_sedes["certificado"]=True
                      else:
                         data_sedes["certificado"]=False
                elif sum(id_cursos) ==140:                  
                    if data.grupo.curso.id in [69]:
                      if data.get_nota_final()>=70:                          
                          data_sedes["tipo"]=signing.dumps("certificado_tni_kalite")
                          data_sedes["certificado"]=True
                      else:
                         data_sedes["certificado"]=False
                elif sum(id_cursos) ==275:                  
                    if data.grupo.curso.id in [69]:
                      if data.get_nota_final()>=70:                          
                          data_sedes["tipo"]=signing.dumps("certificado_combo_kalite")
                          data_sedes["certificado"]=True
                      else:
                         data_sedes["certificado"]=False
                elif(data.grupo.curso.id) in [48]:                   
                    if data.get_nota_final()>=70:
                       data_sedes["tipo"]=signing.dumps("certificado_cct")
                       data_sedes["certificado"]=True
                    else:
                       data_sedes["certificado"]=False                  
                elif(data.grupo.curso.id) in [70]:                   
                    if data.get_nota_final()>=70:
                       data_sedes["tipo"]=signing.dumps("certificado_tni_v")
                       data_sedes["certificado"]=True
                    else:
                       data_sedes["certificado"]=False                                         
                elif sum(id_cursos)== 254 and es_naat==True:                                      
                    if nota_naat>=61:                     
                      data_sedes["tipo"]=signing.dumps("certificado_naat")
                      data_sedes["certificado"]=True
                    else:                      
                      data_sedes["certificado"]=False
                elif sum(id_cursos)==69:
                   if (data.grupo.numero)==2:
                      if data.get_nota_final()>=70:
                        data_sedes["tipo"]=signing.dumps("constancia_tni")
                        data_sedes["constancia"]=True
                      else:
                         data_sedes["constancia"]=False
                      
                   
               data_cursos["asignacion"] =data.id
               data_cursos["curso"] =data.grupo.curso.nombre
               data_cursos["nota_aprobacion"] =data.grupo.curso.nota_aprobacion
               data_cursos["fecha_inicial"] =str(data.grupo.sede.fecha_creacion.date())
               try:
                  data_cursos["fecha_final"] = str(data.grupo.sede.fecha_finalizacion.date())
               except:
                  data_cursos["fecha_final"] = None                  
               data_cursos["nota"] = data.get_nota_final()
               data_cursos["aprobado"] = data.get_aprobado()                                         
               cursos.append(data_cursos)                
            data_sedes["numero_cursos"] = contador_curso
            contador_curso = 0
            if ultima_sede == numero_sede:               
               data_sedes["botones"] = True
            else:
               data_sedes["botones"] = False                         
            data_sedes["nombre"] = info_asignaciones.filter(grupo__sede__id=numero_sede).first().grupo.sede.nombre
            data_sedes["finalizada"] = info_asignaciones.filter(grupo__sede__id=numero_sede).first().grupo.sede.finalizada            
            data_sedes["cursos"] = cursos
            sedes.append(data_sedes)
         data_certificado["sedes"]=sedes
         #print(data_certificado)
         context['sedes'] = data_certificado
         return context


class NuevoDiplomaPdfView(View):
   """ Vista  encargada de generar los diplomas que se entregaran a los participantes de los cursos, obteniendo el dpi
    para mostrar el resultado de que diploma se va a imprimir se puede  descargar el pdf del archivo tambien
   """
   def get( self, request, *args, **kwargs):
      codigo = self.request.GET['codigo'] 
      tipo = self.request.GET['tipo']
      dpi =signing.loads(codigo)      
      nombre_archivo =""            
      url_perfil = str('https://suni.funsepa.org')+str(reverse_lazy('new_listado'))+str('?dpi=')+str(dpi)
      nuevo_url_perfil = "https://suni.funsepa.org/certificado/nuevo/maestros/"+str('?dpi=')+str(dpi)
      locale.setlocale(locale.LC_ALL,'es_GT.utf8')               
      participante = cyd_m.Participante.objects.get(dpi=dpi,activo=True)      
      contador_nombre = participante.nombre.split(" ")
      contador_apellido = participante.apellido.split(" ")
      numero_palabras = len(contador_nombre) + len(contador_apellido)         
      encuesta = eval_m.AsignacionPregunta.objects.filter(evaluado=participante).last()     
      asignacion = cyd_m.Asignacion.objects.filter(participante=participante).last() 
      fecha_finalizacion = asignacion.grupo.sede.fecha_finalizacion    
      tipo_decifrada = signing.loads(tipo)       
      #Creacion de codigos QR
      qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=1,)

      #qr.add_data(url_perfil)
      qr.add_data(nuevo_url_perfil)
      qr.make(fit=True)
      filename = 'perfil-{}.png'.format(dpi)
      ruta_origin = str(os.getcwd()) +str("/")+ str(filename)
      ruta_qr = str(settings.MEDIA_ROOT) + str("qr_perfil/")+str(filename)

      #mover codigo QR a la carpeta correspondiente
      if not (os.path.isfile(ruta_qr)):
        img = qr.make_image()
        img.save(filename)
        shutil.move(ruta_origin,ruta_qr)

      #creacion de tipo de hoja y asignar imagen para colocar de fondo
      h=letter
      if tipo_decifrada == "certificado_tni":
         nombre_archivo = "certificado-tni-"+str(dpi)
         ruta_diploma = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/2024/certificado-TNI-24.jpg")
      elif tipo_decifrada == "certificado_tni_v":
         nombre_archivo = "certificado-tni-virtual"+str(dpi)
         ruta_diploma = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/2024/certificado-TNI-Virtual-24.jpg")
      elif tipo_decifrada == "certificado_naat":
         nombre_archivo = "certificado-naat-"+str(dpi)
         ruta_diploma = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/2024/certificado-naat-24.jpg")
      elif tipo_decifrada == "certificado_cct":
         nombre_archivo = "certificado-cct-"+str(dpi)
         ruta_diploma = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/2024/certificado-cct-24.jpg")
      elif tipo_decifrada =="certificado_tni_kalite":
         nombre_archivo = "certificado-tni-kalite-"+str(dpi)
         ruta_diploma = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/2024/certificado-Kolibri-Khan-Academy-TNI-24.jpg")
      elif tipo_decifrada =="certificado_combo_kalite":
         nombre_archivo = "certificado-combo-kalite-"+str(dpi)
         ruta_diploma = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/2024/certificado-Kolibri-Khan-Academy-Mantenimiento preventivo-LE-TNI-24.jpg")
      elif tipo_decifrada =="constancia_tni":
         nombre_archivo = "constancia_tni-"+str(dpi)
         ruta_diploma = str(settings.STATICFILES_DIRS[0] ) + str("/css/constancia/2024/constancia-TNI-24.jpg")

      
      #ruta_diploma = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/TNIVirtual2024.jpg") 
      #obtener tipo de fuente que se le aplicara al nombre del diploma
      ruta_ttf = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/MyriadPro_BoldIt.ttf")
      registerFont(TTFont('MyriadPro_BoldIt',ruta_ttf))
      ruta_ttf = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/MyriadPro_Regular.ttf")
      registerFont(TTFont('MyriadPro_Regular',ruta_ttf))
      #obtener nuevas fuentes
      ruta_ttf = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/EdwardianScriptITC.ttf")
      registerFont(TTFont('Edwardian',ruta_ttf))
      response = HttpResponse(content_type='application/pdf')
      #response['Content-Disposition'] = 'attachment;filename="{}"'.format(nombre_archivo)
     

      #Creacion de canvas con el programa reportlab para colocar todos los elementos del diploma
      buffer = BytesIO()
      c = canvas.Canvas(buffer, pagesize=(landscape(letter)))
      x = 400
      y = 220
      """if int(tipo_curso) == 2 and grupo_naat == 2 or int(tipo_curso) == 3 and grupo_naat == 3:
        y = 275
      else:
        y = 220"""
      w = 103
      h = 119

      #creacion  de la imagen que se colocora de fondo
      c.drawImage(ruta_diploma, 0,0,width=792,height=612,anchor='sw',anchorAtXY=True,showBoundary=False)
      c.drawImage(ruta_qr,35,45,width=75,height=75,anchor='sw',anchorAtXY=True,showBoundary=False)
      if numero_palabras <=4: 
        c.setFont("Edwardian",60,leading=None)
      else:
         c.setFont("Edwardian",45,leading=None)
      #c.setFont("MyriadPro_Regular",30,leading=None)
      c.setFillColor((0,0,0))
      #c.drawCentredString(x+w*0.0,y+h*0.5, str(data[0]['nombre'].upper())+" "+str(data[0]['apellido'].upper()))
      c.drawCentredString(x+w*0.0,y+h*0.5, str(participante.nombre)+" "+str(participante.apellido))
      c.setFont("MyriadPro_BoldIt",18,leading=None)
      #c.drawCentredString(x+w*0.0,60+h*0.5, "Guatemala, " + datetime.datetime.now().strftime("%d de %B del %Y"))         
      c.drawCentredString(x+w*0.0,60+h*0.3, "Guatemala, " + fecha_finalizacion.date().strftime("%d de %B del %Y")) 
      c.setTitle('Diploma Funsepa')
      c.showPage()
      c.save()
      pdf = buffer.getvalue()      
      buffer.close()
      response.write(pdf)     
      return response
      
