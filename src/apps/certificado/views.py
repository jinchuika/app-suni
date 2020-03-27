import json
import qrcode
import requests
import shutil
import os
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
               context['nombre'] = str(data[0]['nombre'])+" "+str(data[0]['apellido'])
               context['escuela'] =data[0]['escuela']
               context['asignacion'] = data[0]['numero_asignacion']
               context['dpi']=self.request.GET['dpi']
               context['maestros'] = resp.json()
        except:
           context['validacion'] = 0
        return context

class DiplomaPdfView(View):
   """ Vista  encargada de generar los diplomas que se entregaran a los participantes de los cursos, obteniendo el dpi
    para mostrar el resultado de que diploma se va a imprimir se puede  descargar el pdf del archivo tambien
   """
   def get( self, request, *args, **kwargs):
      curso_asignado = 0
      curso_aprobado = 0
      url_perfil = str("https://suni.funsepa.org/")+ str(reverse_lazy('listado')) + str("?dpi=")+str(self.request.GET['dpi'])
      url = settings.LEGACY_URL['certificado']
      tipo_curso = self.request.GET['curso']
      curso_naat = 0
      #se hace la peticion al servidor de suni-capacitacion para mostrar los datos
      if url is not '':
             params = {'dpi': self.request.GET['dpi']}
             try:
                resp = requests.get(url=url, params= params)
             except:
                print("en espera")
      else:
             print("el dpi esta vacio")
      data= resp.json()
      if len(data) is 0:
         return HttpResponse("El dpi ingresado no es valido")
      else:
         for  nuevo in data:
            if nuevo['curso'] == "NAAT":
               curso_naat = 2
            else:
               curso_naat = 1
            if nuevo['numero_asignacion'] == self.request.GET['asignacion']:
               if(nuevo['resultado']=="Aprobado"):
                  curso_aprobado = 1
               curso_asignado = 1
            if curso_asignado == 1:
               if curso_aprobado == 1:
                  #Creacion de codigos QR
                  qr = qrcode.QRCode(
                     version=1,
                     error_correction=qrcode.constants.ERROR_CORRECT_L,
                     box_size=6,
                     border=1,
                  )
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
                  if tipo_curso == str(2) and curso_naat == 2:
                     ruta_diploma = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/certificadoNaat.jpg")
                  else:
                     ruta_diploma = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/CertificadoTB.jpg")
                  #obtener tipo de fuente que se le aplicara al nombre del diploma
                  ruta_ttf = str(settings.STATICFILES_DIRS[0] ) + str("/css/diploma/EdwardianScriptITC.ttf")
                  registerFont(TTFont('Edwardian',ruta_ttf))
                  response = HttpResponse(content_type='application/pdf')
                  if tipo_curso == str(2) and curso_naat == 2:
                     response['Content-Disposition'] = 'filename="DiplomaFunsepaNaat-{}.pdf"'.format(str(self.request.GET['dpi']))
                  else:
                     response['Content-Disposition'] = 'filename="DiplomaFunsepaTB-{}.pdf"'.format(str(self.request.GET['dpi']))
                  #Creacion de canvas con el programa reportlab para colocar todos los elementos del diploma
                  buffer = BytesIO()
                  c = canvas.Canvas(buffer, pagesize=(landscape(letter)))
                  x = 350
                  if tipo_curso == str(2) and curso_naat==2:
                     y = 255
                  else:
                     y = 220
                  w = 103
                  h = 119
                  #creacion  de la imagen que se colocora de fondo
                  c.drawImage(ruta_diploma, 0,0,width=792,height=612,anchor='sw',anchorAtXY=True,showBoundary=False)
                  c.drawImage(ruta_qr,35,40,width=50,height=50,anchor='sw',anchorAtXY=True,showBoundary=False)
                  c.setFont("Edwardian",50,leading=None)
                  c.setFillColor((0,0,0))
                  if tipo_curso == str(2) and curso_naat==2:
                     c.drawCentredString(x+w*0.0,y+h*0.5, str(data[0]['nombre'])+" "+str(data[0]['apellido']))
                  else:
                     c.drawCentredString(x+w*0.0,y+h*0.5, str(data[0]['nombre'])+" "+str(data[0]['apellido']))
                  c.drawCentredString(x+w*0.0,y+h*0.5, str(data[0]['nombre'])+" "+str(data[0]['apellido']))
                  c.setTitle(f'Diploma Funsepa ')
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
