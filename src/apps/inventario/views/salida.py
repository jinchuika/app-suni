from django.shortcuts import reverse, render
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView, View
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin, JsonRequestResponseMixin, CsrfExemptMixin
)
from django.contrib import messages
from django.db.models import Sum

from apps.escuela import models as escuela_m
from apps.inventario import models as inv_m
from apps.inventario import forms as inv_f
from django import forms


class SalidaInventarioCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos de Salida mediante una :class:`SalidaInventario`
    Funciona  para recibir los datos de un  'SalidaInventarioForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.SalidaInventario
    form_class = inv_f.SalidaInventarioForm
    template_name = 'inventario/salida/salida_add.html'

    def get_success_url(self):
        return reverse_lazy('salidainventario_edit', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(SalidaInventarioCreateView, self).get_context_data(**kwargs)
        context['salidainventario_list'] = inv_m.SalidaInventario.objects.filter(en_creacion=True)
        return context

    def form_valid(self, form):
        form.instance.creada_por = self.request.user
        form.instance.estado = inv_m.SalidaEstado.objects.get(id=1)
        if form.instance.entrega:
            form.instance.beneficiario = None
            form.instance.escuela = escuela_m.Escuela.objects.get(codigo=form.cleaned_data['udi'])
        else:
            form.instance.escuela = None
        return super(SalidaInventarioCreateView, self).form_valid(form)


class SalidaInventarioUpdateView(LoginRequiredMixin, UpdateView):
    """ Vista   para obtener los datos de Salida mediante una :class:`SalidaInventario`
    Funciona  para recibir los datos de un  'SalidaInventarioForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.SalidaInventario
    form_class = inv_f.SalidaInventarioUpdateForm
    template_name = 'inventario/salida/salida_edit.html'
    permission_required = 'inventario.salidainventario_change'

    def get_context_data(self, *args, **kwargs):
        context = super(SalidaInventarioUpdateView, self).get_context_data(*args, **kwargs)
        if self.request.user.has_perm("inventario.salidainventario_change"):
            context['paquetes_form'] = inv_f.PaqueteCantidadForm()
        return context


class SalidaInventarioDetailView(LoginRequiredMixin, DetailView):
    """
    """
    model = inv_m.SalidaInventario
    template_name = 'inventario/salida/salida_detail.html'


class SalidaPaqueteUpdateView(LoginRequiredMixin, UpdateView):
    """ Vista   para obtener los datos de Paquete mediante una :class:`SalidaInventario`
    Funciona  para recibir los datos de un  'PaqueteCantidadForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.SalidaInventario
    form_class = inv_f.PaqueteCantidadForm
    template_name = 'inventario/salida/paquetes_add.html'

    def get_success_url(self):
        return reverse_lazy('salidainventario_edit', kwargs={'pk': self.object.id})

    def get_form(self, form_class=None):
        print(self.request.user)
        form = super(SalidaPaqueteUpdateView, self).get_form(form_class)
        form.fields['entrada'].widget = forms.SelectMultiple(attrs={
            'data-api-url': reverse_lazy('inventario_api:api_entrada-list')
        })
        form.fields['entrada'].queryset = inv_m.Entrada.objects.filter(
            tipo=3
        )
        return form

    def get_form_kwargs(self):
        kwargs = super(SalidaPaqueteUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        print(self.request.user.tipos_dispositivos.tipos.all())
        cantidad_disponible = form.cleaned_data['entrada']
        tipo = inv_m.PaqueteTipo.objects.get(id=self.request.POST['tipo_paquete'])
        cantidad = form.cleaned_data['cantidad']
        if (cantidad_disponible.count() > 0):
            cantidad_total = 0
            for disponibles in cantidad_disponible:
                try:
                    detalles = inv_m.EntradaDetalle.objects.filter(
                        entrada=disponibles,
                        tipo_dispositivo=tipo.tipo_dispositivo.id
                        ).aggregate(total_util=Sum('util'))
                    cantidad_total = cantidad_total + detalles['total_util']
                except TypeError as e:
                    messages.error(self.request, 'La entrada:'+str(disponibles)+" No tiene dispositivos de este tipo")
            if(cantidad < cantidad_total):
                form.instance.crear_paquetes(
                    cantidad=form.cleaned_data['cantidad'],
                    usuario=self.request.user,
                    tipo_paquete=form.cleaned_data['tipo_paquete'],
                    entrada=form.cleaned_data['entrada']
                    )
            else:
                messages.error(self.request, 'No Hay en existencia los dispositivos solicitados')
        else:
            form.instance.crear_paquetes(
                cantidad=form.cleaned_data['cantidad'],
                usuario=self.request.user,
                tipo_paquete=form.cleaned_data['tipo_paquete'],
                entrada=form.cleaned_data['entrada']
                )
        return super(SalidaPaqueteUpdateView, self).form_valid(form)


class SalidaPaqueteDetailView(LoginRequiredMixin, UpdateView):
    """Vista para detalle de :class:`Paquete`.
    """
    model = inv_m.Paquete
    template_name = 'inventario/salida/paquetes_detail.html'
    form_class = inv_f.PaqueteUpdateForm

    def get_form(self, form_class=None):
        form = super(SalidaPaqueteDetailView, self).get_form(form_class)
        form.fields['dispositivos'].widget = forms.SelectMultiple(
            attrs={
                'data-api-url': reverse_lazy('inventario_api:api_dispositivo-list'),
                'data-tipo-dispositivo': self.object.tipo_paquete.tipo_dispositivo.id,
                'data-slug': self.object.tipo_paquete.tipo_dispositivo.slug,
                'data-cantidad': self.object.cantidad,


            }
        )
        form.fields['dispositivos'].queryset = inv_m.Dispositivo.objects.filter(
            etapa=inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.TR),
            tipo=self.object.tipo_paquete.tipo_dispositivo
        )
        return form

    def form_valid(self, form):
        etapa_control = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.CC)
        form.instance.asignar_dispositivo(
            lista_dispositivos=form.cleaned_data['dispositivos'],
            usuario=self.request.user
        )
        print(form.cleaned_data['dispositivos'])
        for nuevosDispositivos in form.cleaned_data['dispositivos']:
            nuevosDispositivos.etapa = etapa_control
            nuevosDispositivos.save()
        return super(SalidaPaqueteDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SalidaPaqueteDetailView, self).get_context_data(**kwargs)
        context['dispositivos_paquetes'] = inv_m.DispositivoPaquete.objects.filter(paquete__id=self.object.id)
        context['dispositivos_no'] = inv_m.DispositivoPaquete.objects.filter(paquete__id=self.object.id).count()
        return context


class RevisionSalidaCreateView(LoginRequiredMixin, CreateView):
    """Vista para creación de :class:`RevisionSalida`"""
    model = inv_m.RevisionSalida
    form_class = inv_f.RevisionSalidaCreateForm
    template_name = 'inventario/salida/revisionsalida_add.html'

    def get_success_url(self):
        return reverse_lazy('revisionsalida_list')

    def get_initial(self):
        return {
            'fecha_revision': None
        }

    def form_valid(self, form):
        form.instance.revisado_por = self.request.user
        return super(RevisionSalidaCreateView, self).form_valid(form)


class RevisionSalidaUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para edición de :class:`RevisionSalida`"""
    model = inv_m.RevisionSalida
    form_class = inv_f.RevisionSalidaUpdateForm
    template_name = 'inventario/salida/revisionsalida_update.html'


class SalidaPaqueteView(LoginRequiredMixin, DetailView):
    """Vista para detalle de :class:`SalidaInventario`.on sus respectivos filtros
    """
    model = inv_m.SalidaInventario
    template_name = 'inventario/salida/dispositivo_paquete.html'

    def get_context_data(self, **kwargs):
        context = super(SalidaPaqueteView, self).get_context_data(**kwargs)
        paquete_form = inv_f.DispositivoPaqueteCreateForm()
        paquete_form.fields['tipo'].queryset = inv_m.DispositivoTipo.objects.filter(
            id__in=self.request.user.tipos_dispositivos.tipos.all()
        )
        paquete_form.fields['paquete'].queryset = inv_m.Paquete.objects.filter(salida=self.object,
                                                                               aprobado=False)

        context['paquete_form'] = paquete_form
        context['paquete_id'] = self.object.id
        return context


class RevisionSalidaListView(LoginRequiredMixin, ListView):
    """Vista para Los listados de :class:`RevisionSalida`. con sus respectivos datos
    """
    model = inv_m.RevisionSalida
    template_name = 'inventario/salida/revisionsalida_list.html'


class RevisionComentarioCreate(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """Vista Encargada de obtener las Revision de Comentario de las ofertas mediante el metodo
    POST y gurdarlos en la :class:`RevisionComentario`
    """

    require_json = True

    def post(self, request, *args, **kwargs):
        try:
            id_comentario = self.request_json["id_comentario"]
            revision_salida = inv_m.RevisionSalida.objects.filter(salida=id_comentario)
            comentario = self.request_json["comentario"]
            print()
            if not len(comentario) or len(revision_salida) == 0:
                raise KeyError
        except KeyError:
            error_dict = {u"message": u"Sin Comentario"}
            return self.render_bad_request_response(error_dict)
        comentario_revision = inv_m.RevisionComentario(
            revision=revision_salida[0],
            comentario=comentario,
            creado_por=self.request.user)
        comentario_revision.save()
        return self.render_json_response({
            "comentario": comentario_revision.comentario,
            "fecha": str(comentario_revision.fecha_revision),
            "usuario": str(comentario_revision.creado_por.perfil)
            })


class ControlCalidadListView(LoginRequiredMixin, ListView):
    """Vista para Los listados de :class:`SalidaInventario`. con sus respectivos datos
    """
    model = inv_m.SalidaInventario
    template_name = 'inventario/salida/controlcalidad_list.html'

    def get_context_data(self, **kwargs):
        context = super(ControlCalidadListView, self).get_context_data(**kwargs)
        context['controlcalidad_list'] = inv_m.SalidaInventario.objects.filter(en_creacion=True)
        return context


class DispositivoAsignados(LoginRequiredMixin, DetailView):
    """
    """
    model = inv_m.Paquete
    template_name = 'inventario/salida/dispositivos_salida.html'

    def get_context_data(self, **kwargs):
        context = super(DispositivoAsignados, self).get_context_data(**kwargs)
        context['dispositivo_list'] = inv_m.DispositivoPaquete.objects.filter(paquete__id=self.object.id)
        return context
