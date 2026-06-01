from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic import DetailView, ListView, View, TemplateView


from braces.views import GroupRequiredMixin

from apps.naat import models as naat_m
from apps.naat import forms as naat_f
from apps.cyd import models as cyd_m
from apps.escuela import models as escuela_m
from rest_framework import views,status
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import (LoginRequiredMixin, GroupRequiredMixin, JsonRequestResponseMixin, CsrfExemptMixin)
import requests


class BaseNaatPermission(GroupRequiredMixin):
    """Vista base para asignar los proteger las vistas de Naat y que solo puedan ser accedidas por usuarios
    de los grupos correspondientes.

    Todo:
        Definir si hay vistas que puedan ser informes generales para usuarios de `consulta`
    """
    group_required = ["naat", "naat_facilitador"]
    redirect_unauthenticated_users = False
    raise_exception = True


class ParticipanteNaatCreateView(BaseNaatPermission, CreateView):
    """Vista para crear un nuevo :class:`Participante` y una :class:`AsignacionNaat` asociada al mismo.
    La validación de que no exista un dato duplicado se realiza a nivel de base de datos.
    """
    model = cyd_m.Participante
    form_class = naat_f.AsignacionNaatForm
    template_name = 'naat/participante_add.html'

    def get_form(self, form_class=None):
        """
        Para filtra las opciones disponibles para elegir a `proceso` en el formulario
        """
        form = super(ParticipanteNaatCreateView, self).get_form(form_class)
        if self.request.user.groups.filter(name="naat_facilitador").exists():
            qs_proceso = form.fields['proceso'].queryset
            qs_proceso = qs_proceso.filter(capacitador=self.request.user)
            form.fields['proceso'].queryset = qs_proceso
        return form

    def form_valid(self, form):
        """Se debe validar que el UDI de la :class:`Escuela` exista para asignarla al :class:`Participante`
        que se está creando.
        """
        try:
            form.instance.escuela = escuela_m.Escuela.objects.get(codigo=form.cleaned_data['udi'])
        except ObjectDoesNotExist:
            form.add_error('udi', 'El UDI no es válido o no existe.')
            return self.form_invalid(form)
        return_value = super(ParticipanteNaatCreateView, self).form_valid(form)

        # Es necesario confirmar que el :class:`Participante` se creó correctamente en la base de datos
        if form.instance.pk:
            try:
                form.instance.asignaciones_naat.create(
                    proceso=form.cleaned_data['proceso'])
            except IntegrityError:
                # Valida en caso de que la :class:`AsignacionNaat` no pueda ser creada
                form.instance.delete()
                form.add_error('dpi', 'Error al asignar participante.')
                return self.form_invalid(form)
        return return_value


class AsignacionesActualesListView(BaseNaatPermission, ListView):
    """Esta vista es un acceso rápido a los :class:`Participante`s asignados actualmente al facilitador.
    """
    template_name = 'naat/asignaciones_actuales.html'

    def get_queryset(self):
        return naat_m.AsignacionNaat.objects.filter(
            proceso__capacitador=self.request.user,
            activa=True)


class SesionPresencialDetailView(BaseNaatPermission, DetailView):
    """Vista de detalle de una :class:`SesionPresencial`.
    """
    template_name = 'naat/sesionpresencial_detail.html'
    model = naat_m.SesionPresencial


class SesionPresencialCalendarView(BaseNaatPermission, FormView):
    """Calendario de las :class:`SesionPresencial` de Naat.
    Obtiene los datos de los eventos del calendario desdela url `naat_api:calendario_api_list`.
    """
    template_name = 'naat/calendario.html'
    form_class = naat_f.CalendarFilterForm

    def get_form(self, form_class=None):
        """
        Para filtrar el formulario si el usuario pertenece al grupo 'naat_facilitador`
        """
        form = super(SesionPresencialCalendarView, self).get_form(form_class)
        if self.request.user.groups.filter(name="naat_facilitador").exists():
            form.fields['capacitador'].queryset = form.fields['capacitador'].queryset.filter(id=self.request.user.id)
            form.fields['capacitador'].empty_label = None
        return form


class SesionPresencialCreateView(BaseNaatPermission, CreateView):
    """Creación de :class:`SesionPresencial` de Naat.
    Filtra los datos del campo `proceso` para que muestre solo los del usuario que consulta actualmente.
    """

    template_name = 'naat/sesionpresencial_add.html'
    form_class = naat_f.SesionPresencialCreateForm

    def get_form(self, form_class=None):
        """
        Para filtrar el formulario si el usuario pertenece al grupo 'naat_facilitador`
        """
        form = super(SesionPresencialCreateView, self).get_form(form_class)
        if self.request.user.groups.filter(name="naat_facilitador").exists():
            form.fields['proceso'].queryset = form.fields['proceso'].queryset.filter(capacitador=self.request.user.id)
            form.fields['proceso'].empty_label = None
        return form

    def form_valid(self, form):
        form.instance.creado_por_sesion = self.request.user
        return super( SesionPresencialCreateView, self).form_valid(form)


class SesionPresencialUpdateView(BaseNaatPermission, UpdateView):
    """Vista para edición de :class:`SesionPresencial` de Naat.
    Filtra el campo de `asistentes` para que muestre únicamente los de la :class:`Escuela`.
    """
    template_name = 'naat/sesionpresencial_edit.html'
    form_class = naat_f.SesionPresencialForm
    model = naat_m.SesionPresencial

    def get_form(self, form_class=None):
        form = super(SesionPresencialUpdateView, self).get_form(form_class)
        form.fields['asistentes'].queryset = naat_m.AsignacionNaat.objects.filter(proceso=form.instance.proceso)
        return form

    def form_valid(self, form):
        form.instance.creado_por_sesion = self.request.user
        return super( SesionPresencialUpdateView, self).form_valid(form)


class ProcesoNaatCreateView(BaseNaatPermission, CreateView):
    """Vista para la creación de :class:`ProcesoNaat`.
    """
    template_name = 'naat/proceso_add.html'
    form_class = naat_f.ProcesoNaatForm
    model = naat_m.ProcesoNaat

    def get_context_data(self, **kwargs):
        """Crea un listado de :class:`ProcesoNaat` asignados al usuario actual.
        """
        context = super(ProcesoNaatCreateView, self).get_context_data(**kwargs)
        context['proceso_list'] = naat_m.ProcesoNaat.objects.filter(capacitador=self.request.user)
        return context

    def form_valid(self, form):
        """
        Asigna al usuario actual como `capacitador` del objeto.
        """
        try:
            form.instance.escuela = escuela_m.Escuela.objects.get(codigo=form.cleaned_data['udi'])
        except ObjectDoesNotExist:
            form.add_error('udi', 'El UDI no es válido o no existe.')
            return self.form_invalid(form)
        form.instance.capacitador = self.request.user
        return super(ProcesoNaatCreateView, self).form_valid(form)


class ProcesoNaatDetailView(BaseNaatPermission, DetailView):
    """Vista de detalle de un :class:`ProcesoNaat`"""
    model = naat_m.ProcesoNaat
    template_name = 'naat/proceso_detail.html'


class ProcesoNaatListView(BaseNaatPermission, ListView):
    """Vista para mostrar un listado de :class:`ProcesosNaat`.
    Eventualmente puede que esta vista cambie para generar un informe completo
    utilizando DRF."""
    model = naat_m.ProcesoNaat
    template_name = 'naat/proceso_list.html'

class TareasNaat(LoginRequiredMixin, GroupRequiredMixin, FormView):
    template_name = "naat/tareas_naat.html"    
    form_class = naat_f.ParticipanteNaatTareasForm 
    group_required = [u"cyd", u"cyd_capacitador", u"cyd_admin", ]
        

class TareasNaatApi(views.APIView):
    def get(self, request, *args, **kwargs):
        sede = request.GET.get('sede', '').strip()
        if not sede:
            return JsonResponse({'error': 'Debes proporcionar un código UDI.'}, status=400)
        try:
            sede_obj = cyd_m.Sede.objects.get(id=sede)
            escuelas = sede_obj.get_escuelas()
            udis_escuela = [escuela.codigo for escuela in escuelas]
            udis_listado = ",".join(udis_escuela)

        except cyd_m.Sede.DoesNotExist:
            return JsonResponse({'error': 'Sede no encontrada.'}, status=404)

        url = getattr(settings, 'NAAT_URL_APIS')
        url_base_naat = getattr(settings, 'NAAT_URL_BASE')
        token = getattr(settings, 'NAAT_TOKEN', '')
        endpoint = 'get_maestros_tareas'
        url = "{}{}".format(url, endpoint)
        headers= {
            'API-KEY': token
        }
        try:
            response = requests.get(url, params={'udi': udis_listado}, headers=headers)
            participantes_naat = response.json()
            maestros_agrupados = {}

            for item in participantes_naat:
                dpi = item.get('usuario_dpi')
                
                if dpi not in maestros_agrupados:
                    try:
                        maestro = cyd_m.Participante.objects.get(dpi=dpi, activo=True)
                    except cyd_m.Participante.DoesNotExist:
                        maestro = None

                    maestros_agrupados[dpi] = {
                        'nombre': maestro.nombre if maestro else item.get('usuario_nombre', ''),
                        'apellido': maestro.apellido if maestro else item.get('usuario_apellido', ''),
                        'url_participante': maestro.get_absolute_url() if maestro else "#",
                        'registrado': True if maestro else False,
                        'tareas': {} 
                    }
                nombre_tarea = item.get('nombre')
                ruta_completa = url_base_naat + item.get('ruta', '') 
                maestros_agrupados[dpi]['tareas'][nombre_tarea] = ruta_completa

            datos_finales = list(maestros_agrupados.values())

            return JsonResponse(datos_finales, safe=False, status=200)

        except requests.exceptions.Timeout:
            return JsonResponse({'error': 'El servidor tardo demasiado en responder.'}, status=504)
        except requests.exceptions.ConnectionError:
            return JsonResponse({'error': 'No se pudo conectar con el servidor Naat.'}, status=502)
        except ValueError:
            return JsonResponse({'error': 'El servidor de Naat devolvió una respuesta inválida.'}, status=500)
        except Exception as e:
            return JsonResponse({'error': 'Error desconocido: {}'.format(str(e))}, status=500)



class InformeNaatParticipanteView(LoginRequiredMixin, GroupRequiredMixin, FormView):
    template_name = "naat/informeUsuariosNaat.html"    
    form_class = naat_f.InformeNaatParticipanteForm 
    group_required = [u"cyd", u"cyd_capacitador", u"cyd_admin", ]


class InformeNaatParticipanteAPI(View):
    """
    Vista para importar participantes desde NAAT Mobile. Recibe un código UDI de escuela como parámetro GET, 
    consulta la API de NAAT, y devuelve un JSON con la información de los maestros asociados a esa escuela.
    """
    def get(self, request, *args, **kwargs):
        sede = request.GET.get('sede').strip()
        fecha_inicio = request.GET.get('fecha_inicio', '')
        fecha_fin = request.GET.get('fecha_fin', '')
        if not (sede or fecha_inicio or fecha_fin):
            return JsonResponse({'error': 'Debes proporcionar almenos un campo para filtrar.'}, status=400)
        try:
            sede_obj = cyd_m.Sede.objects.get(id=sede)
            escuelas = sede_obj.get_escuelas()
            udis_escuela = [escuela.codigo for escuela in escuelas]
            udis_listado = ",".join(udis_escuela)
        except:
            udis_listado = ""


        url = getattr(settings, 'NAAT_URL_APIS')
        token = getattr(settings, 'NAAT_TOKEN', '')
        endpoint = 'get_estadisticas_api'
        url = "{}{}".format(url, endpoint)

        headers= {
            'API-KEY': token
        }
        parametros = {
            'udi': udis_listado,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin
        }

        try:
            response = requests.get(url, params=parametros, headers=headers)
            participantes_naat = response.json()
            listado = []

            for par in participantes_naat.get('data', []):
                dpi = par.get('dpi', {})
                try:
                    participante = cyd_m.Participante.objects.get(dpi=dpi, activo=True)
                except Exception as e:
                    participante = None

                calif_lista = par.get('calificaciones', [])
                mundos_data = { c.get('mundo_numero'): c for c in calif_lista }

                data = {
                    "nombre": participante.nombre if participante else par.get('nombre'),
                    'apellido': participante.apellido if participante else par.get('apellido'),
                    'url_participante': participante.get_absolute_url() if participante else None,
                    'udi': par.get('udi', {}),
                    'municipio': par.get('municipio_nombre', {}),
                    'departamento': par.get('departamento_nombre', {}),
                    'puesto': par.get('puesto_nombre', {}),
                    'genero': par.get('genero', {}),

                    "mundo1": mundos_data.get(1, {}).get('porcentaje_total', 0),
                    "mundo2": mundos_data.get(2, {}).get('porcentaje_total', 0),
                    "mundo3": mundos_data.get(3, {}).get('porcentaje_total', 0),
                    "mundo4": mundos_data.get(4, {}).get('porcentaje_total', 0),
                    "mundo5": mundos_data.get(5, {}).get('porcentaje_total', 0),
                    "mundo6": mundos_data.get(6, {}).get('porcentaje_total', 0),
                    "mundo7": mundos_data.get(7, {}).get('porcentaje_total', 0),
                    "mundo8": mundos_data.get(8, {}).get('porcentaje_total', 0),

                    #PC = prueba de conocimiento
                    "mundo1_pc_nota_inicial": mundos_data.get(1, {}).get('datos_prueba', {}).get('resultado', "-"),
                    "mundo1_pc_nota_final": mundos_data.get(1, {}).get('datos_prueba', {}).get('resultado_final', "-"),
                    "mundo2_pc_nota_inicial": mundos_data.get(2, {}).get('datos_prueba', {}).get('resultado', "-"),
                    "mundo2_pc_nota_final": mundos_data.get(2, {}).get('datos_prueba', {}).get('resultado_final', "-"),
                    "mundo3_pc_nota_inicial": mundos_data.get(3, {}).get('datos_prueba', {}).get('resultado', "-"),
                    "mundo3_pc_nota_final": mundos_data.get(3, {}).get('datos_prueba', {}).get('resultado_final', "-"),
                    "mundo4_pc_nota_inicial": mundos_data.get(4, {}).get('datos_prueba', {}).get('resultado', "-"),
                    "mundo4_pc_nota_final": mundos_data.get(4, {}).get('datos_prueba', {}).get('resultado_final', "-"),
                }
                listado.append(data)

            return JsonResponse(listado, safe=False, status=200)

        except requests.exceptions.Timeout:
            return JsonResponse({'error': 'El servidor tardó demasiado en responder.'}, status=504)
        except requests.exceptions.ConnectionError:
            return JsonResponse({'error': 'No se pudo conectar con el servidor Naat.'}, status=502)
        except ValueError:
            return JsonResponse({'error': 'El servidor de Naat devolvió una respuesta inválida.'}, status=500)
        except Exception as e:
            return JsonResponse({'error': 'Error con la conexión', 'details': str(e)}, status=500)
        