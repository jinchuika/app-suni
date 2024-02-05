from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, DetailView, View, CreateView, ListView, UpdateView
from django.shortcuts import render
from apps.Evaluacion import models as eva_models
from apps.cyd import models as cyd_models
from apps.users import models as users_models 
from apps.escuela import models as esc_models
from apps.Evaluacion import forms as eva_forms
from rest_framework import views, status
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect
import json
from django.shortcuts import get_object_or_404
from django.utils import timezone
from braces.views import (LoginRequiredMixin, GroupRequiredMixin) 
from django.contrib.auth.mixins import LoginRequiredMixin
from django_user_agents.utils import get_user_agent



class FormularioAdd(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = eva_models.Formulario
    template_name = 'Evaluacion/formulario_add.html'
    form_class = eva_forms.FormularioAdd
    group_required = [u"eva_admin", u"eva_tpe", u"eva_capacitacion"]

    def form_valid(self, form):
        udi = form.cleaned_data['udi']
        codigo = esc_models.Escuela.objects.get(codigo=str(udi)) 

        if udi != "":
            try:
                codigo = esc_models.Escuela.objects.get(codigo=str(udi)) 
                form.instance.escuela = codigo
                form.instance.formulario_creado_por = self.request.user

                user_groups = [group.name for group in self.request.user.groups.all()]
                if any("cyd" in group for group in user_groups):
                    form.instance.area_evaluada = eva_models.AreaEvaluada.objects.get(area_evaluada = "Capacitacion")
                elif any("tpe" in group for group in user_groups):
                    form.instance.area_evaluada = eva_models.AreaEvaluada.objects.get(area_evaluada = "TPE")
                else: 
                    form.instance.area_evaluada = eva_models.AreaEvaluada.objects.get(area_evaluada = "Administracion")

                self.object = form.save()

            except ObjectDoesNotExist:
                form.add_error('udi', 'El UDI no es válido o no existe.')
                return self.form_invalid(form)
            
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('formulario_list')
    

class FormularioListView(ListView):
    """Listado de formularios"""
    model = eva_models.Formulario
    template_name = 'Evaluacion/formulario_list.html' 
    context_object_name = 'formularios' 

    
    def get_queryset(self):
        return eva_models.Formulario.objects.all().order_by('-fecha_inicio_formulario')
    

class FormularioUpdateView(UpdateView):
    model = eva_models.Formulario
    template_name = 'Evaluacion/formulario_edit.html'
    form_class = eva_forms.FormularioForm

    def get_success_url(self):
        return reverse('formulario_list')


# Create your views here.
class ingresoDPIView(TemplateView):
    template_name = 'Evaluacion/acceso.html'
    model = cyd_models.Participante

    def post(self, request, *args, **kwargs):
            dpi = request.POST.get('dpi', None)
            dpi = dpi.replace('-', '')

            if dpi is not None:

                try:
                    participante = cyd_models.Participante.objects.get(dpi=dpi)

                    try:
                        sede = cyd_models.Asignacion.objects.filter(participante__dpi=participante.dpi).last()
                        
                        try:
                            formulario = eva_models.Formulario.objects.filter(escuela = sede.grupo.sede.escuela_beneficiada, usuario = sede.grupo.sede.capacitador).last()

                            fecha_actual = timezone.localtime(timezone.now())
                            fechaActualUTC = fecha_actual.astimezone(timezone.utc)

                            # Información
                            if formulario.fecha_inicio_formulario <= fechaActualUTC <= formulario.fecha_fin_formulario:
         
                                Preguntas = eva_models.Pregunta.objects.filter(evaluacion= formulario.evaluacion, area_evaluada__area_evaluada = formulario.area_evaluada, estado = True, seccion_pregunta__activo = True)
                                
                                for pregunta in Preguntas:
                                    asignacion = eva_models.AsignacionPregunta.objects.filter(formulario = formulario, evaluado = participante, pregunta = pregunta)
                            
                                    if not asignacion.exists():  
                                        AsignacionPregunta = eva_models.AsignacionPregunta(
                                        formulario = formulario,
                                        evaluado = participante,
                                        pregunta = pregunta
                                        )
                                        AsignacionPregunta.save()
                                    else:
                                        if asignacion.last().respondido:
                                            return redirect("acceso")
                                        fechaUpdate = eva_models.AsignacionPregunta.objects.filter(formulario = formulario, evaluado = participante, pregunta = pregunta).last()
                                        fechaUpdate.fecha_incio_evaluacion = timezone.now()
                                        fechaUpdate.save()

                                # Almacenar el DPI en la sesión
                                request.session['dpi'] = dpi

                                url = reverse('preguntas', kwargs={'formulario_id': formulario.id})
                                return HttpResponseRedirect(url)
                            else:
                                return redirect('acceso')
                                #retornar a un template de mal horario 

                        except:
                            print("El participante con DPI {} no tiene un formulario por contestar.".format(dpi))
                            return redirect('acceso')

                    except ObjectDoesNotExist:
                        print("El participante con DPI {} no esta inscrito en nunguna sede.".format(dpi))
                        return redirect('acceso')
                        #Enviar alerta (puede estar inscrito, pero no tiene formulario

                except ObjectDoesNotExist:
                    print("El participante con DPI {} no existe.".format(dpi))
                    return redirect('acceso')
            else: 
                print("No se ingreso DPI")

            return HttpResponse("Solicitud POST exitosa")
    

class asignacionPreguntaView(TemplateView):
    """Vista para mostrar las preguntas del :class: Preguntas """
    template_name = 'Evaluacion/formulario.html'
    model = eva_models.AsignacionPregunta


    def get_context_data(self, **kwargs):
        context = super(asignacionPreguntaView, self).get_context_data(**kwargs)

        # Obtener el formulario_id de los parámetros de la URL
        formulario_id = self.kwargs.get('formulario_id', None)
        dpi = self.request.session.get('dpi', None)
        formulario = eva_models.Formulario.objects.get( id = formulario_id)


        # Añadir formulario_id al contexto
        context['formulario_id'] = formulario_id
        context['participante'] = dpi 

        #Contexto de tipos de respuestas
        context['respuesta_booleana'] = eva_models.Respuesta.objects.filter(respuesta__in=["Si", "No"])
        context['respuesta_opinion'] = eva_models.Respuesta.objects.filter(respuesta__in=["De acuerdo", "En desacuerdo"])
        context['respuesta_calidad'] = eva_models.Respuesta.objects.filter(respuesta__in=["Bueno", "Regular", "Malo"])


        secciones = eva_models.SeccionPregunta.objects.filter(area_evaluada__area_evaluada=formulario.area_evaluada, activo=True).order_by('id')
        preguntas = []

        for seccion in secciones:
            preguntas.append((seccion.seccion_pregunta, seccion.instrucciones,eva_models.Pregunta.objects.filter(area_evaluada__area_evaluada=formulario.area_evaluada, seccion_pregunta=seccion, evaluacion=formulario.evaluacion, estado=True)))

        context['preguntas'] = preguntas
        
        return context
        
class guardarPreguntas(APIView):
    """ View para poder guardar las preguntas y sus respuestas
    """
    def post(self, request, *args, **kwargs):
        data = request.data
        
        try:
            formulario_id = request.data.get('formulario_id')
            formularioNo = eva_models.Formulario.objects.get(id=formulario_id)
            dpi = request.data.get('dpi_participante')
            participante =  cyd_models.Participante.objects.get(dpi = dpi)

            asigancionUpdate = eva_models.AsignacionPregunta.objects.filter(formulario = formularioNo , evaluado = participante).last()

            if asigancionUpdate is None:
                return redirect("acceso")
            else: 
                if asigancionUpdate.respondido == False:
                    for item in data.items():
                        try:
                            Pregunta = eva_models.Pregunta.objects.get(pregunta=item[0])
                        except eva_models.Pregunta.DoesNotExist:
                            continue
                        
                        try:
                            respuesta = eva_models.Respuesta.objects.get(respuesta=item[1])
                        except eva_models.Respuesta.DoesNotExist:
                            respuestaAdd = eva_models.Respuesta(
                                tipo_respuesta = eva_models.TipoRespuesta.objects.get(tipo_respuesta="Texto"), 
                                respuesta = item[1]
                            )
                            respuestaAdd.save()
                            respuesta = eva_models.Respuesta.objects.get(respuesta=item[1])
                        
                        asignacionAdd = eva_models.AsignacionPregunta.objects.get(formulario = formularioNo, evaluado = participante, pregunta = Pregunta) 

                        asignacionAdd.respuesta = respuesta
                        asignacionAdd.respondido = True
                        asignacionAdd.fecha_fin_evaluacion = timezone.now()
                        
                        asignacionAdd.save()
                    
                    user_agent = get_user_agent(request)
                    tipoDispositivo = user_agent.device.family if user_agent.device.family else "Desconocido"
                    tipoSO = user_agent.os.family if user_agent.os.family else "Desconocido"


                    dispositivo_info = eva_models.DispositivoParticipantes.objects.create(
                        dispositivo=tipoDispositivo,
                        os=tipoSO,
                        participante_info=participante
                    )
                    dispositivo_info.save()
                    
                else: 
                    return HttpResponse("Formulario ya contestado, gracias")
        except eva_models.Formulario.DoesNotExist:
            return HttpResponse("No existe el formulario")
        
        return redirect('finalizado')


class FinalizadoView(TemplateView):
    """View para mostrar al finalizar la evaluacion"""
    template_name = 'Evaluacion/finalizado.html'


class baseView(TemplateView):
    """Vista para mostrar las preguntas del :class: Preguntas """
    template_name = 'Evaluacion/base_evaluacion.html'
    model = eva_models.AsignacionPregunta
