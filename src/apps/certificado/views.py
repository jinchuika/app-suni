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
from apps.cyd.models import Participante
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

from io import BytesIO

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
           data= resp.json()                    
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
               
               # Obtener Listado de Sedes
               for valor in data:
                  sede = valor['sede']
                  if sede not in sedes:                   
                    sedes.append(sede)

               # Recorrer Sedes del Maestro
               for sede in sedes:
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
                    if validar_nombre_tni.find("Tecnologia Nivel Intermedio") is not -1:                      
                       if int(valor_data['nota']) < int(valor_data['nota_minima']):                                                    
                          gano_tni = 0
                       else:                              
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
                if grupo_combos == 4 and ka_lite == True:
                  combo_completo = True  
                else: 
                  combo_completo = False
                
                if grupo_combos == 1 and ka_lite == True:
                   solo_ka_lite =  True
                  
                # Crear Objeto Asignacion por sede                           
                values = {"id": id_sede,"sede": sede, "asignaciones": asignaciones, "promedio": promedio, "grupo":grupo_naat, "year_cert":year_cert, "combo_completo":combo_completo,"gano_tni":gano_tni,"centro_comunitario":centro_comunitario,"solo_ka_lite":solo_ka_lite,"naat":naat}
                sede_asignacion.append(dict(values))                             
               context['sedes'] = sede_asignacion
               context['validacion'] = 1
        except:
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
                ruta_diploma = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/CertificadoNaat18.png")
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
