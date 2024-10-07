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
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from datetime import datetime
from django.db.models import F
from itertools import groupby
from operator import attrgetter
from django.db.models import Count

# Create your views here.
class FormularioAdd(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = eva_models.Formulario
    template_name = 'Evaluacion/formulario_add.html'
    form_class = eva_forms.FormularioAdd
    group_required = [u"eva_admin", u"eva_tpe", u"eva_capacitacion"]

    def form_valid(self, form):
        sede = form.cleaned_data['sede']
        if sede != "":
            try:
                form.instance.escuela = sede.escuela_beneficiada
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

 
class FormularioListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    """Listado de formularios"""
    model = eva_models.Formulario
    template_name = 'Evaluacion/formulario_list.html'
    context_object_name = 'formularios'
    group_required = [u"eva_admin", u"eva_tpe", u"eva_capacitacion"]


    def get_queryset(self):
        return eva_models.Formulario.objects.all().order_by('-fecha_inicio_formulario')
    

class FormularioDetail(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = eva_models.Formulario
    template_name = 'Evaluacion/formulario_detail.html'
    group_required = [u"eva_admin", u"eva_tpe", u"eva_capacitacion"]

    def get_context_data(self, **kwargs):
        context = super(FormularioDetail, self).get_context_data(**kwargs)
        formulario = self.object

        secciones = eva_models.SeccionPregunta.objects.filter(area_evaluada=formulario.area_evaluada)
        context['secciones'] = secciones

        preguntas = eva_models.Pregunta.objects.filter(area_evaluada=formulario.area_evaluada, estado=True, evaluacion=formulario.evaluacion)
        context['preguntas'] = preguntas

        estado_formulario = eva_models.estadoFormulario.objects.filter(preguntas__formulario=formulario).distinct()

        respondidos = estado_formulario.filter(estado=True).count()
        no_respondidos = estado_formulario.filter(estado=False).count()

        context['no_participantes_respondidos'] = respondidos
        context['no_participantes_no_respondidos'] = no_respondidos

        total_participantes = cyd_models.Participante.objects.filter(
            asignaciones__grupo__sede=formulario.sede
        ).distinct().count()

        context['total_participantes'] = total_participantes
        context['no_participantes_no_respondidos'] = total_participantes - respondidos

        return context

class FormularioUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = eva_models.Formulario
    template_name = 'Evaluacion/formulario_edit.html'
    form_class = eva_forms.FormularioForm
    group_required = [u"eva_admin", u"eva_tpe", u"eva_capacitacion"]

    def form_valid(self, form):
        sede = form.cleaned_data['sede']
        if sede != "":
            try:
                form.instance.escuela = sede.escuela_beneficiada
                form.instance.sede = sede
                form.instance.formulario_creado_por = self.request.user
                self.object = form.save()

            except ObjectDoesNotExist:
                form.add_error('sede', 'La sede no es correcta.')
                return self.form_invalid(form)
                    
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('formulario_list')

class ingresoDPIView(TemplateView):
    template_name = 'Evaluacion/acceso.html'
    model = cyd_models.Participante

    def post(self, request, *args, **kwargs):
            dpi = request.POST.get('dpi', None)
            dpi = dpi.replace('-', '')

            if dpi is not None:
                try:
                    participante = cyd_models.Participante.objects.get(dpi=dpi, activo = True)                   
                    try:
                        sede = cyd_models.Asignacion.objects.filter(participante__dpi=participante.dpi).last()
                        
                        try:
                            formulario = eva_models.Formulario.objects.filter(escuela = sede.grupo.sede.escuela_beneficiada, usuario = sede.grupo.sede.capacitador).last()
                            fecha_actual = timezone.localtime(timezone.now())
                            fechaActualUTC = fecha_actual.astimezone(timezone.utc)

                            if formulario.fecha_inicio_formulario <= fechaActualUTC <= formulario.fecha_fin_formulario:
                                Preguntas = eva_models.Pregunta.objects.filter(evaluacion= formulario.evaluacion, area_evaluada__area_evaluada = formulario.area_evaluada, estado = True, seccion_pregunta__activo = True)

                                for pregunta in Preguntas:
                                    asignacion = eva_models.AsignacionPregunta.objects.filter(formulario = formulario, evaluado = participante, pregunta = pregunta)
                                    
                                    estado = eva_models.estadoFormulario.objects.filter(preguntas__evaluado=participante).last()

                                    if(estado is None):
                                        if not asignacion.exists():  
                                            AsignacionPregunta = eva_models.AsignacionPregunta(
                                                formulario = formulario,
                                                evaluado = participante,
                                                pregunta = pregunta
                                            )
                                            AsignacionPregunta.save()
                                        else:
                                            fechaUpdate = eva_models.AsignacionPregunta.objects.filter(formulario = formulario, evaluado = participante, pregunta = pregunta).last()
                                            fechaUpdate.fecha_incio_evaluacion = timezone.now()
                                            fechaUpdate.save()

                                    else: 
                                        if estado.estado == False:
                                            if not asignacion.exists():  
                                                AsignacionPregunta = eva_models.AsignacionPregunta(
                                                formulario = formulario,
                                                evaluado = participante,
                                                pregunta = pregunta
                                                )
                                                AsignacionPregunta.save()
                                            else:
                                                fechaUpdate = eva_models.AsignacionPregunta.objects.filter(formulario = formulario, evaluado = participante, pregunta = pregunta).last()
                                                fechaUpdate.fecha_incio_evaluacion = timezone.now()
                                                fechaUpdate.save()
                                        else: 
                                            return redirect("acceso")

                                request.session['dpi'] = dpi

                                url = reverse('preguntas', kwargs={'formulario_id': formulario.id})
                                return HttpResponseRedirect(url)
                            else:
                                return redirect('acceso')

                        except:
                            print("El participante con DPI {} no tiene un formulario por contestar.".format(dpi))
                            return redirect('acceso')

                    except ObjectDoesNotExist:
                        print("El participante con DPI {} no esta inscrito en nunguna sede.".format(dpi))
                        return redirect('acceso')

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

        formulario_id = self.kwargs.get('formulario_id', None)
        dpi = self.request.session.get('dpi', None)
        formulario = eva_models.Formulario.objects.get( id = formulario_id)

        context['formulario_id'] = formulario_id
        context['participante'] = dpi 
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
            estado = eva_models.estadoFormulario.objects.filter(preguntas__evaluado=participante).first()

            if estado is not None: 
                if estado.estado == False: 
                    if asigancionUpdate.respondido == False:
                        preguntas_respuestas = []
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

                            preguntas_respuestas.append(asignacionAdd)
                        
                        try: 
                            estado_formulario = eva_models.estadoFormulario.objects.filter(preguntas__in=preguntas_respuestas, preguntas__evaluado=participante).distinct().last()
                            estado_formulario.estado = True
                            estado_formulario.save()

                        except Exception as e:
                            print(e)
                            formularioAdd = eva_models.estadoFormulario.objects.create()
                            formularioAdd.preguntas.set(preguntas_respuestas)
                                
                            cant_preguntas = eva_models.Pregunta.objects.filter(evaluacion = formularioNo.evaluacion).count()
                            if cant_preguntas == len(preguntas_respuestas):
                                formularioAdd.estado = True
                                formularioAdd.save()

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

                if estado.estado == True:
                    return redirect("acceso")
                
            if estado is None: 
                if asigancionUpdate.respondido == False:
                    preguntas_respuestas = []
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

                        preguntas_respuestas.append(asignacionAdd)
                    
                    try: 
                        estado_formulario = eva_models.estadoFormulario.objects.filter(preguntas__in=preguntas_respuestas, preguntas__evaluado=participante).distinct().last()
                        estado_formulario.estado = True
                        estado_formulario.save()

                    except Exception as e:
                        formularioAdd = eva_models.estadoFormulario.objects.create()
                        formularioAdd.preguntas.set(preguntas_respuestas)
                            
                        cant_preguntas = eva_models.Pregunta.objects.filter(evaluacion = formularioNo.evaluacion).count()
                        if cant_preguntas == len(preguntas_respuestas):
                            formularioAdd.estado = True
                            formularioAdd.save()

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


class InformeEvalaucionesView(LoginRequiredMixin, FormView):
    """Vista para mostrar las estadistias del modulo de Evaluacion """
    template_name = 'Evaluacion/informe_evaluaciones.html'
    form_class = eva_forms.InformeEstadisticasForm

    def get_context_data(self, **kwargs):
        context = super(InformeEvalaucionesView, self).get_context_data(**kwargs)
        return context

class participantesApi(APIView):
    """API para mostrar la información de formularios, participantes y su estado de completitud"""

    def get(self, request):
        try:
            sedes_info = {}
            completados_info = {}
            faltantes_info = {}
            porcentaje_completado_info = {}
            total_participantes_global = 0
            total_completados_global = 0
            total_faltantes_global = 0
            formularios = eva_models.Formulario.objects.all()
            data = []

            estados_formularios = eva_models.estadoFormulario.objects.filter(estado=True)
            for estado_formulario in estados_formularios:
                for asignacion_pregunta in estado_formulario.preguntas.all():
                    evaluado = asignacion_pregunta.evaluado

            for formulario in formularios:
                capacitador = formulario.usuario
                sede = formulario.sede

                if not sede:
                    continue

                participantes = cyd_models.Participante.objects.filter(
                    asignaciones__grupo__sede__id=sede.id, activo=True).annotate(
                    cursos_sede=Count('asignaciones'))
                total_participantes = participantes.count()

                sedes_info[sede.escuela_beneficiada.codigo] = total_participantes
                completados = eva_models.estadoFormulario.objects.filter(
                    preguntas__evaluado__asignaciones__grupo__sede__id=sede.id,
                    preguntas__respondido=True,
                    estado=True
                ).distinct()

                participantes_completados = [estado_formulario.get_participante() for estado_formulario in completados]
                participantes_faltantes = list(participantes.exclude(id__in=[p.id for p in participantes_completados]))
                faltantes_info[sede.escuela_beneficiada.codigo] = participantes_faltantes

                total_completados = len(participantes_completados)
                if total_participantes > 0:
                    porcentaje_completado = int((total_completados / total_participantes) * 100)
                else:
                    porcentaje_completado = 0

                porcentaje_completado_info[sede.escuela_beneficiada.codigo] = porcentaje_completado
                total_participantes_global += total_participantes
                total_completados_global += total_completados
                total_faltantes_global += len(participantes_faltantes)

                data.append({
                    'escuela_codigo': sede.escuela_beneficiada.codigo,
                    'sede': sede.id,
                    'total_participantes': total_participantes,
                    'participantes_completados': total_completados,
                    'porcentaje_completado': porcentaje_completado,
                    'capacitador': {
                        'id': capacitador.id,
                        'username': capacitador.username,
                        'first_name': capacitador.first_name,
                        'last_name': capacitador.last_name,
                        'email': capacitador.email,
                    },
                    'lista_participantes_faltantes': [str(p) for p in participantes_faltantes],  
                    'lista_participantes_completados': [str(p) for p in participantes_completados]
                })

            response_data = {
                'formularios': data,
                'total_participantes': total_participantes_global,
                'total_completados': total_completados_global,
                'total_faltantes': total_faltantes_global
            }

            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response(
                {'mensaje': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class EstadisticasJson(views.APIView):
    """API para mostrar las preguntas con su tipo de respuesta y conteo"""

    def get(self, request):
        try:
            formulario_id = request.GET.get('id')

            if formulario_id is not None:
                formulario = eva_models.Formulario.objects.get(id=formulario_id)

                preguntas_unicas_ids = eva_models.AsignacionPregunta.objects.filter(
                    formulario=formulario,
                    respondido=True
                ).values_list('pregunta', flat=True).distinct()

                preguntas_unicas = eva_models.Pregunta.objects.filter(id__in=preguntas_unicas_ids)
                response_data = {
                    'preguntas': [],
                    'pregunta_texto': []
                }

                for pregunta in preguntas_unicas:
                    asignaciones_ids = eva_models.estadoFormulario.objects.filter(
                        estado=True,
                        preguntas__pregunta=pregunta 
                    ).values_list('preguntas', flat=True)

                    respuestas_conteo = eva_models.AsignacionPregunta.objects.filter(
                        id__in=asignaciones_ids,
                        pregunta=pregunta,
                        formulario=formulario,
                        respondido=True
                    ).values('respuesta__respuesta').annotate(conteo=Count('respuesta__respuesta'))

                    if pregunta.tipo_respuesta.id == 4:
                        respuestas = [r['respuesta__respuesta'] for r in respuestas_conteo]
                        pregunta_data = {
                            'pregunta': pregunta.pregunta,
                            'tipo_respuesta': pregunta.tipo_respuesta.tipo_respuesta,
                            'respuestas': respuestas 
                        }
                        response_data['pregunta_texto'].append(pregunta_data)
                    else:
                        posibles_respuestas = eva_models.Respuesta.objects.filter(
                            tipo_respuesta=pregunta.tipo_respuesta
                        ).values_list('respuesta', flat=True)
                        conteo_dict = {r['respuesta__respuesta']: r['conteo'] for r in respuestas_conteo}
                        respuestas = [{'respuesta': r, 'conteo': conteo_dict.get(r, 0)} for r in posibles_respuestas]

                        pregunta_data = {
                            'pregunta': pregunta.pregunta,
                            'tipo_respuesta': pregunta.tipo_respuesta.tipo_respuesta,
                            'respuestas': respuestas
                        }
                        response_data['preguntas'].append(pregunta_data)

                return Response({
                    'datos': response_data
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'mensaje': 'ID no proporcionado'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            print(e)
            return Response(
                {'mensaje': 'No se pudo procesar la solicitud'},
                status=status.HTTP_400_BAD_REQUEST
            )


class EstadisticasInformeApi(views.APIView):
    """API para mostrar las preguntas con su tipo de respuesta, conteo y secciones, filtradas por los parámetros dados."""

    def get(self, request):
        try:
            departamento_ids = request.GET.getlist('departamento') or []
            municipio_ids = request.GET.getlist('municipio')  or []
            usuario_ids = request.GET.getlist('usuario')  or []
            sede_id = request.GET.get('sede') or None
            evaluacion_id = request.GET.get('evaluacion') or None
            fecha_inicio = request.GET.get('fecha_inicio_formulario') or None
            fecha_fin = request.GET.get('fecha_fin_formulario') or None

            filter_params = {}
            if sede_id is not None:
                filter_params['formulario__sede_id'] = sede_id
            if len(municipio_ids) != 0:
                filter_params['formulario__sede__municipio_id__in'] = municipio_ids
            if len(departamento_ids) != 0:
                filter_params['formulario__sede__municipio__departamento_id__in'] = departamento_ids
            if len(usuario_ids) != 0:
                filter_params['formulario__usuario_id__in'] = usuario_ids
            if evaluacion_id is not None:
                filter_params['formulario__evaluacion_id'] = evaluacion_id
            if fecha_inicio is not None:
                filter_params['formulario__fecha_inicio_formulario__gte'] = fecha_inicio
            if fecha_fin is not None:
                filter_params['formulario__fecha_inicio_formulario__lte'] = fecha_fin

            if len(filter_params) == 0:
                return Response(
                    {'mensaje': 'No se pudo obtener información, consulte los filtros de búsqueda'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            asignaciones = eva_models.AsignacionPregunta.objects.filter(**filter_params)
            asignaciones_con_estado_true = [
                asigna for asigna in asignaciones
                if eva_models.estadoFormulario.objects.filter(preguntas=asigna, estado=True).exists()
            ]

            preguntas_unicas_ids = eva_models.AsignacionPregunta.objects.filter(
                id__in=[a.id for a in asignaciones_con_estado_true]
            ).values_list('pregunta', flat=True).distinct()

            preguntas_unicas = eva_models.Pregunta.objects.filter(id__in=preguntas_unicas_ids)

            response_data = {
                'preguntas': [],
                'pregunta_texto': [],
                'secciones': []
            }

            secciones_unicas_ids = preguntas_unicas.values_list('seccion_pregunta', flat=True).distinct()
            secciones_unicas = eva_models.SeccionPregunta.objects.filter(id__in=secciones_unicas_ids)
            response_data['secciones'] = [seccion.seccion_pregunta for seccion in secciones_unicas]

            for pregunta in preguntas_unicas:
                respuestas_conteo = eva_models.AsignacionPregunta.objects.filter(
                    id__in=[a.id for a in asignaciones_con_estado_true],
                    pregunta=pregunta,
                    respondido=True
                ).values('respuesta__respuesta').annotate(conteo=Count('respuesta__respuesta'))

                if pregunta.tipo_respuesta.id == 4:
                    respuestas = [r['respuesta__respuesta'] for r in respuestas_conteo]
                    pregunta_data = {
                        'pregunta': pregunta.pregunta,
                        'tipo_respuesta': pregunta.tipo_respuesta.tipo_respuesta,
                        'respuestas': respuestas, 
                        'seccion_pregunta': pregunta.seccion_pregunta.seccion_pregunta
                    }
                    response_data['pregunta_texto'].append(pregunta_data)
                else:
                    posibles_respuestas = eva_models.Respuesta.objects.filter(
                        tipo_respuesta=pregunta.tipo_respuesta
                    ).values_list('respuesta', flat=True)
                    conteo_dict = {r['respuesta__respuesta']: r['conteo'] for r in respuestas_conteo}
                    respuestas = [{'respuesta': r, 'conteo': conteo_dict.get(r, 0)} for r in posibles_respuestas]

                    pregunta_data = {
                        'pregunta': pregunta.pregunta,
                        'tipo_respuesta': pregunta.tipo_respuesta.tipo_respuesta,
                        'respuestas': respuestas,
                        'seccion_pregunta': pregunta.seccion_pregunta.seccion_pregunta
                    }
                    response_data['preguntas'].append(pregunta_data)

            return Response({
                'datos': response_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {'mensaje': 'No se pudo procesar la solicitud'},
                status=status.HTTP_400_BAD_REQUEST
            )