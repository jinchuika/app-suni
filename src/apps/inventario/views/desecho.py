from django.shortcuts import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView
from braces.views import (
    LoginRequiredMixin, GroupRequiredMixin
)
from apps.inventario import models as inv_m
from apps.inventario import forms as inv_f
from django.db.models import Sum
from rest_framework import status, views
from rest_framework.response import Response
from django.db.models import Q
from apps.kardex import models as kax_m
from apps.conta import models as conta_m
class DesechoEmpresaCreateView(LoginRequiredMixin, CreateView, GroupRequiredMixin):
    """Vista   para obtener los datos de Entrada mediante una :class:`DesechoEmpresa`
    Funciona  para recibir los datos de un  'DesechoEmpresaForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.DesechoEmpresa
    form_class = inv_f.DesechoEmpresaForm
    template_name = 'inventario/desecho/desechoempresa_form.html'
    group_required = [u"inv_bodega", u"inv_admin", u"inv_monitoreo"]

    def get_success_url(self):
        return reverse('desechoempresa_list')

    def form_valid(self, form):
        form.instance.creada_por = self.request.user
        return super(DesechoEmpresaCreateView, self).form_valid(form)


class DesechoEmpresaUpdateView(LoginRequiredMixin, UpdateView, GroupRequiredMixin):
    """Vista   para obtener los datos de Entrada mediante una :class:`DesechoEmpresa`
    Funciona  para recibir los datos de un  'DesechoEmpresaForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.DesechoEmpresa
    form_class = inv_f.DesechoEmpresaForm
    template_name = 'inventario/desecho/desechoempresa_form.html'
    group_required = [u"inv_bodega", u"inv_admin", u"inv_monitoreo"]

    def get_success_url(self):
        return reverse('desechoempresa_list')


class DesechoEmpresaDetailView(LoginRequiredMixin, DetailView, GroupRequiredMixin):
    """Para generar detalles de la :class:`DesechoEmpresa`   con sus respectivos campos.
    """
    model = inv_m.DesechoEmpresa
    template_name = 'inventario/desecho/desechoempresa_detail.html'
    group_required = [u"inv_bodega", u"inv_admin", u"inv_monitoreo"]


class DesechoEmpresaListView(LoginRequiredMixin, ListView, GroupRequiredMixin):
    """Listado del :class:`DesechoEmpresa` con sus respectivos datos
    """
    model = inv_m.DesechoEmpresa
    template_name = 'inventario/desecho/desechoempresa_list.html'
    group_required = [u"inv_bodega", u"inv_admin", u"inv_monitoreo"]


class DesechoSalidaCreateView(LoginRequiredMixin, CreateView, GroupRequiredMixin):
    """Vista   para obtener los datos de Entrada mediante una :class:`DesechoSalida`
    Funciona  para recibir los datos de un  'DesechoSalidaForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.DesechoSalida
    form_class = inv_f.DesechoSalidaForm
    template_name = 'inventario/desecho/desechosalida_add.html'
    group_required = [u"inv_bodega", u"inv_admin", u"inv_monitoreo"]

    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super(DesechoSalidaCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DesechoSalidaCreateView, self).get_context_data(**kwargs)
        context['desechosalida'] = inv_m.DesechoSalida.objects.all()
        return context


class DesechoSalidaDetailView(LoginRequiredMixin, DetailView, GroupRequiredMixin):
    """Vista encargada de mostrar los detalles de la :class:`SalidaInventario`
    """
    model = inv_m.DesechoSalida
    template_name = 'inventario/desecho/desechosalida_detail.html'
    group_required = [u"inv_bodega", u"inv_admin", u"inv_monitoreo"]

    def get_context_data(self, **kwargs):
        context = super(DesechoSalidaDetailView, self).get_context_data(**kwargs)


        desecho_solicitud = []
        dispositivo_solicitud = inv_m.DesechoSolicitud.objects.filter(desecho=self.object.id, aprobado=True)
        for solicitud in dispositivo_solicitud:
            motivo = inv_m.CambioEtapa.objects.filter(dispositivo=solicitud.dispositivo).first()
            desecho_solicitud.append({
                'dispositivo': solicitud.dispositivo,
                'motivo': motivo.motivo,
            })

        context['desechodetalles'] = inv_m.DesechoDetalle.objects.filter(desecho=self.object.id)
        context['desechodispositivo'] = inv_m.DesechoDispositivo.objects.filter(desecho=self.object.id)
        context['desechosolicitud'] = desecho_solicitud
        return context


class DesechoSalidaUpdateView(LoginRequiredMixin, UpdateView, GroupRequiredMixin):
    """Vista para actualizar la :class:`DesechoSalida`. con sus respectios Campos
    """
    model = inv_m.DesechoSalida
    form_class = inv_f.DesechoSalidaUpdateForm
    template_name = 'inventario/desecho/desechosalida_form.html'
    group_required = [u"inv_bodega", u"inv_admin", u"inv_monitoreo"]

    def get_context_data(self, **kwargs):
        context = super(DesechoSalidaUpdateView, self).get_context_data(**kwargs)
        context['DesechoDetalleForm'] = inv_f.DesechoDetalleForm(initial={'desecho': self.object})
        context['DesechoDispositivoForm'] = inv_f.DesechoDispositivoForm(initial={'desecho': self.object})
        context['DesechoSolicitudForm'] = inv_f.DesechoSolicitudForm(initial={'desecho': self.object})
        return context

    def get_success_url(self):
        return reverse('desechosalida_update', kwargs={'pk': self.object.id})


class DesechoSalidaPrintView(LoginRequiredMixin, DetailView, GroupRequiredMixin):
    """Vista encargada de mostrar los detalles de la :class:`SalidaInventario`
    """
    model = inv_m.DesechoSalida
    template_name = 'inventario/desecho/desecho_print.html'
    group_required = [u"inv_bodega", u"inv_admin", u"inv_monitoreo"]

    def get_context_data(self, **kwargs):
        context = super(DesechoSalidaPrintView, self).get_context_data(**kwargs)
        context['desechodetalles'] = inv_m.DesechoDetalle.objects.filter(desecho=self.object.id)
        context['desechodispositivo'] = inv_m.DesechoDispositivo.objects.filter(desecho=self.object.id)
        context['desechosolicitud'] = inv_m.DesechoSolicitud.objects.filter(desecho=self.object.id, aprobado=True)
        total_detalles = inv_m.DesechoDetalle.objects.filter(
                desecho=self.object.id).aggregate(total_util=Sum('cantidad'))        
        if total_detalles['total_util'] is None:
            total_detalles['total_util'] = 0
        total_dispositivo = inv_m.DesechoDispositivo.objects.filter(desecho=self.object.id).count()
        total_dispo_solicitudes =  + inv_m.DesechoSolicitud.objects.filter(desecho=self.object.id, aprobado=True).count()
        cantidad_total = total_dispositivo + total_dispo_solicitudes + total_detalles['total_util']
        context['cantidad_total'] = cantidad_total
        return context

class DesechoSalidaListView(LoginRequiredMixin,  FormView, GroupRequiredMixin):
    """Vista encargada de mostrar los listados de la :class:`DesechoSalida`
    """
    model = inv_m.DesechoSalida
    template_name = 'inventario/desecho/desechosalida_list.html'
    form_class = inv_f.DesechoInventarioListForm
    group_required = [u"inv_bodega", u"inv_admin", u"inv_monitoreo"]


class ValidacionesDesechoJson(views.APIView):
    def get(self, request):
         jefe = self.request.GET['jefe']
         aprobado = self.request.GET['aprobado']
         numero_desecho = self.request.GET['id']
         if jefe=='true' and aprobado== 'true':
             desecho = inv_m.DesechoSalida.objects.get(id=numero_desecho)
             if desecho.revision_sub_jefe == True:
                 desecho.revision_jefe = True
                 desecho.save()
             else:
                return Response(
                        {
                            'mensaje': 'El sub jefe de produccion aun no a autorizado el detalle'
                        },
                        status=status.HTTP_401_UNAUTHORIZED
                    )
         elif jefe=='true' and aprobado == 'false':
             desecho = inv_m.DesechoSalida.objects.get(id=numero_desecho)
             desecho.revision_sub_jefe = False
             desecho.save()
         elif jefe=='false' and aprobado == 'true':
             desecho = inv_m.DesechoSalida.objects.get(id=numero_desecho)
             desecho.revision_sub_jefe = True
             desecho.save()
         else:
             desecho = inv_m.DesechoSalida.objects.get(id=numero_desecho)
             desecho.revision_bodega  = False
             desecho.save()
         return Response(
                {
                    'mensaje': 'Detalle Aprobado'
                },
                status=status.HTTP_200_OK
            )


class SolicitudMovimientoDesechoCreateView(LoginRequiredMixin, CreateView):
    """ Crea la solicitud de movimiento de dispositivos que pasan de util a desecho.
    Funciona  para recibir los datos de un  'SolicitudMovimientoCreateForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.SolicitudMovimiento
    template_name = 'inventario/desecho/solicitudmovimientodesecho_add.html'
    form_class = inv_f.SolicitudMovimientoDesechoCreateForm
    group_required = [u"inv_cc", u"inv_admin", u"inv_tecnico", u"inv_bodega"]

    def form_valid(self, form):
        tipo_dispositivo = form.cleaned_data['tipo_dispositivo']
        form.instance.creada_por = self.request.user

        return super(SolicitudMovimientoDesechoCreateView, self).form_valid(form)

    def get_initial(self):
        return {
            'fecha_creacion': None
        }

    def get_form(self, form_class=None):
        form = super(SolicitudMovimientoDesechoCreateView, self).get_form(form_class)
        form.fields['tipo_dispositivo'].queryset = self.request.user.tipos_dispositivos.tipos.filter(Q(usa_triage=True) | Q(kardex=True))
        return form
