from django.shortcuts import reverse, render
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView, View
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin, JsonRequestResponseMixin, CsrfExemptMixin, GroupRequiredMixin
)
from django.contrib import messages
from django.db.models import Sum

from apps.escuela import models as escuela_m
from apps.inventario import models as inv_m
from apps.inventario import forms as inv_f
from apps.beqt import models as beqt_m
from apps.beqt import forms as beqt_f
from apps.tpe import models as tpe_m
from django import forms
from dateutil.relativedelta import relativedelta


class SalidaInventarioCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    """Vista   para obtener los datos de Salida mediante una :class:`SalidaInventario`
    Funciona  para recibir los datos de un  'SalidaInventarioForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = beqt_m.SalidaInventario
    form_class = beqt_f.SalidaInventarioForm
    template_name = 'beqt/salida/salida_add.html'
    group_required = []

    def get_success_url(self):
        return reverse_lazy('salidainventario_beqt_edit', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(SalidaInventarioCreateView, self).get_context_data(**kwargs)
        context['salidainventario_list'] = beqt_m.SalidaInventario.objects.filter(en_creacion=True)
        return context

    def form_valid(self, form):
        form.instance.creada_por = self.request.user
        form.instance.estado = inv_m.SalidaEstado.objects.get(id=1)
        su_udi = form.cleaned_data['udi']
        if form.instance.entrega:
            if su_udi == "":
                form.instance.udi = None
            else:
                try:
                    form.instance.escuela = escuela_m.Escuela.objects.get(codigo=form.cleaned_data['udi'])
                except ObjectDoesNotExist:
                    form.add_error('udi', 'El UDI no es válido o no existe.')
                    return self.form_invalid(form)

        else:
            form.instance.escuela = None
            if form.instance.garantia is not None:
                escuela = tpe_m.TicketSoporte.objects.get(id=str(form.instance.garantia))
                nueva_escuela = escuela.garantia.equipamiento.escuela.codigo
                form.instance.escuela = escuela_m.Escuela.objects.get(codigo=nueva_escuela)
            else:
                form.instance.escuela = None
        return super(SalidaInventarioCreateView, self).form_valid(form)


class SalidaInventarioUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """ Vista   para obtener los datos de Salida mediante una :class:`SalidaInventario`
    Funciona  para recibir los datos de un  'SalidaInventarioForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = beqt_m.SalidaInventario
    form_class = beqt_f.SalidaInventarioUpdateForm
    template_name = 'beqt/salida/salida_edit.html'
    group_required = [u"inv_cc", u"inv_admin"]

    def get_context_data(self, *args, **kwargs):
        context = super(SalidaInventarioUpdateView, self).get_context_data(*args, **kwargs)
        context['paquetes_form'] = beqt_f.PaqueteCantidadForm()
        Laptop = beqt_m.PaqueteTipoBeqt.objects.get(nombre="Laptop")
        Tablet = beqt_m.PaqueteTipoBeqt.objects.get(nombre="Tablet")       
        Total_Tablet = beqt_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=Tablet)
        Total_Laptop = beqt_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=Laptop)
       
        comentarios_cc= beqt_m.SalidaComentarioBeqt.objects.filter(salida=self.object.id)
        comentarios_conta=beqt_m.RevisionComentarioBeqt.objects.filter(revision__salida=self.object.id)
        
        context['Laptops'] = Total_Laptop.count()
        context['Tablets'] = Total_Tablet.count()
        context['comentario_cc'] = comentarios_cc
        context['comentario_conta'] = comentarios_conta
        return context


class SalidaInventarioDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Vista encargada de mostrar los detalles de la :class:`SalidaInventario`
    """
    model = beqt_m.SalidaInventario
    template_name = 'beqt/salida/salida_detail.html'
    group_required = []

    def get_context_data(self, *args, **kwargs):
        context = super(SalidaInventarioDetailView, self).get_context_data(*args, **kwargs)
        Laptop = beqt_m.PaqueteTipoBeqt.objects.get(nombre="Laptop")
        Tablet = beqt_m.PaqueteTipoBeqt.objects.get(nombre="Tablet")     
        Total_Tablet = beqt_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=Tablet)
        Total_Laptop = beqt_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=Laptop)
        context['Laptops'] = Total_Laptop.count()
        context['Tablets'] = Total_Tablet.count()
        return context

class SalidaInventarioListView(LoginRequiredMixin,  FormView):
    """ Vista creada para obtener el listado de las :class:`SalidaInventario`
    Funciona para recibir los datos de un 'SalidaInventarioListForm' mediante el metodo POST.
    y nos muestra el rempalte de la vista mediante le metodo get
    """
    model = beqt_m.SalidaInventario
    form_class = beqt_f.SalidaInventarioListForm
    template_name = 'beqt/salida/salida_add.html'

    def get_context_data(self, **kwargs):
        context = super(SalidaInventarioListView, self).get_context_data(**kwargs)
        context['lista'] = 1
        return context


class SalidaPaqueteUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """ Vista   para obtener los datos de Paquete mediante una :class:`SalidaInventario`
    Funciona  para recibir los datos de un  'PaqueteCantidadForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = beqt_m.SalidaInventario
    form_class = beqt_f.PaqueteCantidadForm
    template_name = 'beqt/salida/paquetes_add.html'
    group_required = []

    def get_success_url(self):
        return reverse_lazy('salidainventario_beqt_edit', kwargs={'pk': self.object.id})

    def get_form(self, form_class=None):
        print('Get Form')
        form = super(SalidaPaqueteUpdateView, self).get_form(form_class)
        form.fields['entrada'].widget = forms.SelectMultiple(attrs={
            'data-api-url': reverse_lazy('beqt_api:api_entrada_beqt-list')
        })
        form.fields['entrada'].queryset = beqt_m.Entrada.objects.filter(
            tipo=5
        )        
        return form

    def form_valid(self, form):
        cantidad_disponible = form.cleaned_data['entrada']
        tipo = beqt_m.PaqueteTipoBeqt.objects.get(id=self.request.POST['tipo_paquete'])
        cantidad = form.cleaned_data['cantidad']        
        if (cantidad_disponible.count() > 0):            
            cantidad_total = 0
            for disponibles in cantidad_disponible:              
                try:
                    detalles = beqt_m.EntradaDetalleBeqt.objects.filter(
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


class SalidaPaqueteDetailView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """Vista para detalle de :class:`Paquete`.
    """
    model = beqt_m.PaqueteBeqt
    template_name = 'beqt/salida/paquetes_detail.html'
    form_class = beqt_f.PaqueteUpdateForm
    group_required = []

    def get_form(self, form_class=None):
        form = super(SalidaPaqueteDetailView, self).get_form(form_class)
        etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.TR)
        estado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.PD)
        form.fields['dispositivos'].widget = forms.SelectMultiple(
            attrs={
                'data-api-url': reverse_lazy('beqt_api:api_dispositivo-list'),
                'data-tipo-dispositivo': self.object.tipo_paquete.tipo_dispositivo.id,
                'data-slug': self.object.tipo_paquete.tipo_dispositivo.slug,
                'data-cantidad': self.object.cantidad,
                'data-etapa_inicial': etapa.id,
                'data-estado_inicial': estado.id,
            }
        )
        form.fields['dispositivos'].queryset = beqt_m.DispositivoBeqt.objects.filter(
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
        for nuevosDispositivos in form.cleaned_data['dispositivos']:
            nuevosDispositivos.etapa = etapa_control
            nuevosDispositivos.save()
        return super(SalidaPaqueteDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SalidaPaqueteDetailView, self).get_context_data(**kwargs)
        nuevo_id = beqt_m.PaqueteBeqt.objects.get(id=self.object.id)
        context['dispositivos_paquetes'] = beqt_m.DispositivoPaquete.objects.filter(paquete__id=self.object.id)
        context['dispositivos_no'] = beqt_m.DispositivoPaquete.objects.filter(paquete__id=self.object.id).count()
        context['comentarios'] = beqt_m.SalidaComentarioBeqt.objects.filter(salida=nuevo_id.salida)
        return context


class RevisionSalidaCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    """Vista para creación de :class:`RevisionSalida`"""
    model = beqt_m.RevisionSalidaBeqt
    form_class = beqt_f.RevisionSalidaCreateForm
    template_name = 'beqt/salida/revisionsalida_add.html'
    group_required = []

    def get_success_url(self):
        return reverse_lazy('revisionsalida_beqt_update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {
            'fecha_revision': None
        }

    def form_valid(self, form):
        form.instance.revisado_por = self.request.user
        return super(RevisionSalidaCreateView, self).form_valid(form)


class RevisionSalidaUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """Vista para edición de :class:`RevisionSalida`"""
    model = beqt_m.RevisionSalidaBeqt
    form_class = beqt_f.RevisionSalidaUpdateForm
    template_name = 'beqt/salida/revisionsalida_update.html'
    group_required = []

    def get_context_data(self, *args, **kwargs):
        context = super(RevisionSalidaUpdateView, self).get_context_data(*args, **kwargs)
        comentarios_cc= beqt_m.SalidaComentarioBeqt.objects.filter(salida=self.object.salida.id)
        context['comentario_cc'] = comentarios_cc
        return context


class SalidaPaqueteView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Vista para detalle de :class:`SalidaInventario`.on sus respectivos filtros
    """
    model = beqt_m.SalidaInventario
    template_name = 'beqt/salida/dispositivo_paquete.html'
    group_required = []

    def get_context_data(self, **kwargs):
        context = super(SalidaPaqueteView, self).get_context_data(**kwargs)
        paquete_form = beqt_f.DispositivoPaqueteCreateForm()
        paquete_form.fields['tipo'].queryset = inv_m.DispositivoTipo.objects.filter(
            id__in=self.request.user.tipos_dispositivos.tipos.all()
        )
        paquete_form.fields['paquete'].queryset = beqt_m.PaqueteBeqt.objects.filter(salida=self.object,
                                                                               aprobado=False)

        context['paquete_form'] = paquete_form
        context['paquete_id'] = self.object.id
        return context


class RevisionSalidaListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    """Vista para Los listados de :class:`RevisionSalida`. con sus respectivos datos
    """
    model = beqt_m.RevisionSalidaBeqt
    template_name = 'beqt/salida/revisionsalida_list.html'
    group_required = []


class RevisionComentarioCreate(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """Vista Encargada de obtener las Revision de Comentario de las ofertas mediante el metodo
    POST y gurdarlos en la :class:`RevisionComentario`
    """

    require_json = True

    def post(self, request, *args, **kwargs):
        try:
            id_comentario = self.request_json["id_comentario"]
            revision_salida = beqt_m.RevisionSalidaBeqt.objects.filter(salida=id_comentario)
            comentario = self.request_json["comentario"]
            if not len(comentario) or len(revision_salida) == 0:
                raise KeyError
        except KeyError:
            error_dict = {u"message": u"Sin Comentario"}
            return self.render_bad_request_response(error_dict)
        comentario_revision = beqt_m.RevisionComentarioBeqt(
            revision=revision_salida[0],
            comentario=comentario,
            creado_por=self.request.user)
        comentario_revision.save()
        return self.render_json_response({
            "comentario": comentario_revision.comentario,
            "fecha": str(comentario_revision.fecha_revision),
            "usuario": str(comentario_revision.creado_por.perfil)
            })


class RevisionComentarioSalidaCreate(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """Vista Encargada de obtener las Revision de Comentario de las ofertas mediante el metodo
    POST y gurdarlos en la :class:`SalidaComentario`
    """

    require_json = True

    def post(self, request, *args, **kwargs):
        try:
            id_comentario = self.request_json["id_comentario"]
            revision_salida = beqt_m.SalidaInventario.objects.filter(no_salida=id_comentario)
            comentario = self.request_json["comentario"]
            if not len(comentario) or len(revision_salida) == 0:
                raise KeyError
        except KeyError:
            error_dict = {u"message": u"Sin Comentario"}
            return self.render_bad_request_response(error_dict)
        comentario_revision = beqt_m.SalidaComentarioBeqt(
            salida=revision_salida[0],
            comentario=comentario,
            creado_por=self.request.user)
        comentario_revision.save()
        return self.render_json_response({
            "comentario": comentario_revision.comentario,
            "fecha": str(comentario_revision.fecha_revision),
            "usuario": str(comentario_revision.creado_por.perfil)
            })


class ControlCalidadListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    """Vista para Los listados de :class:`SalidaInventario`. con sus respectivos datos
    """
    model = beqt_m.SalidaInventario
    template_name = 'beqt/salida/controlcalidad_list.html'
    group_required = []

    def get_context_data(self, **kwargs):
        context = super(ControlCalidadListView, self).get_context_data(**kwargs)
        context['controlcalidad_list'] = beqt_m.SalidaInventario.objects.filter(en_creacion=True)
        return context


class DispositivoAsignados(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Vista encargada de ver los dispositivos que se fueron asignados a los paquetes
    """
    model = beqt_m.PaqueteBeqt
    template_name = 'beqt/salida/dispositivos_salida.html'
    group_required = []

    def get_context_data(self, **kwargs):
        context = super(DispositivoAsignados, self).get_context_data(**kwargs)
        context['dispositivo_list'] = beqt_m.DispositivoPaquete.objects.filter(paquete__id=self.object.id)
        return context


class GarantiaPrintView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Vista encargada para imprimir las Garantias de las :class:`SalidaInventario`
    """
    model = beqt_m.SalidaInventario
    template_name = 'beqt/salida/garantia_print.html'
    group_required = []

    def get_context_data(self, **kwargs):
        context = super(GarantiaPrintView, self).get_context_data(**kwargs)
        cpu_servidor = 0       
        Laptop = beqt_m.PaqueteTipoBeqt.objects.get(nombre="Laptop")
        Tablet = beqt_m.PaqueteTipoBeqt.objects.get(nombre="Tablet")       
        
        laptops_server = beqt_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=Laptop,
            )        
        Total_Laptop = beqt_m.PaqueteBeqt.objects.filter(
            salida__id=self.object.id,
            tipo_paquete=Laptop).aggregate(total_laptop=Sum('cantidad'))
        Total_Tablet = beqt_m.PaqueteBeqt.objects.filter(
            salida__id=self.object.id,
            tipo_paquete=Tablet).aggregate(total_tablet=Sum('cantidad'))       

        for servidor_laptop  in laptops_server:
            nueva_laptop = beqt_m.DispositivoBeqt.objects.get(triage=servidor_laptop.dispositivo).cast()
            try:
                if nueva_laptop.servidor is True:
                    cpu_servidor = cpu_servidor + 1
                    context['laptop'] = True
            except Exception as e:
                print(e)       
        if Total_Laptop['total_laptop'] is None:
            Total_Laptop['total_laptop'] = 0
        if Total_Tablet['total_tablet'] is None:
            Total_Tablet['total_tablet'] = 0
        Total_Entregado = (Total_Laptop['total_laptop']+Total_Tablet['total_tablet']) - cpu_servidor
        if Total_Tablet['total_tablet'] > 1:
            context['cpu'] = 1
        else:
            context['cpu'] = 0
        Fecha = beqt_m.SalidaInventario.objects.get(id=self.object.id)
        context['capacitada'] = Fecha.capacitada
        if Fecha.meses_garantia:
            context['fin_garantia'] = Fecha.fecha + relativedelta(months=6)
            context["tiempo"] = "6 meses"
        else:
            context['fin_garantia'] = Fecha.fecha + relativedelta(months=12)
            context["tiempo"] = " 1 año"
        context['dispositivo_total'] = Total_Entregado
        context['cpu_servidor'] = cpu_servidor
        return context


class LaptopPrintView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Vista encargada para imprimir las :class:`Laptop` de las salidas correspondiente
    """
    model = beqt_m.SalidaInventario
    template_name = 'beqt/salida/laptop_print.html'
    group_required = []

    def get_context_data(self, **kwargs):
        context = super(LaptopPrintView, self).get_context_data(**kwargs)
        nuevas_laptops = []
        cpu_servidor = ""
        Laptop = beqt_m.PaqueteTipoBeqt.objects.get(nombre="Laptop")      
        Total_Laptop = beqt_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=Laptop)        
        cantidad_total = beqt_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=Laptop).count()        
        for triage in Total_Laptop:
            nuevo_laptop = beqt_m.DispositivoBeqt.objects.get(triage=triage.dispositivo).cast()
            nuevas_laptops.append(nuevo_laptop)
        escuela = beqt_m.SalidaInventario.objects.get(id=self.object.id)
        try:
            encargado = escuela_m.EscContacto.objects.get(escuela=escuela.escuela, rol=5)
            context['Encargado'] = str(encargado.nombre)+" "+str(encargado.apellido)
        except ObjectDoesNotExist as e:
            print(e)
            context['Encargado'] = "No Tiene Encargado"
        context['Laptos'] = nuevas_laptops
        context['Total'] = cantidad_total
        context['Servidor'] = cpu_servidor
        return context


class TabletPrintView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Vista encargada para imprimir las :class:`Tablets` de las salidas correspondiente
    """
    model = beqt_m.SalidaInventario
    template_name = 'beqt/salida/tablet_print.html'
    group_required = []

    def get_context_data(self, **kwargs):
        context = super(TabletPrintView, self).get_context_data(**kwargs)
        nuevas_tablets = []
        total_cargadores_mostrar = 0
        Tablet = beqt_m.PaqueteTipoBeqt.objects.get(nombre="Tablet")
        Cargador = beqt_m.PaqueteTipoBeqt.objects.get(nombre="Cargadores")
        Total_Tablet = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=Tablet)
        Total_Cargador = inv_m.Paquete.objects.filter(
            salida__id=self.object.id,
            tipo_paquete=Cargador).aggregate(cargadores=Sum('cantidad'))       

        for triage in Total_Tablet:
            nueva_tablet = inv_m.Dispositivo.objects.get(triage=triage.dispositivo).cast()
            nuevas_tablets.append(nueva_tablet)
        escuela = inv_m.SalidaInventario.objects.get(id=self.object.id)
        try:
            encargado = escuela_m.EscContacto.objects.get(escuela=escuela.escuela, rol=5)
            context['Encargado'] = str(encargado.nombre)+" "+str(encargado.apellido)
            context['Jornada'] = encargado.escuela.jornada
        except ObjectDoesNotExist as e:
            print(e)
            context['Jornada'] = "No tiene Jornada"
            context['Encargado'] = "No Tiene Encargado"
        context['Tablets'] = nuevas_tablets
        context['Total'] = Total_Tablet.count()
        if Total_Cargador['cargadores'] != None:
            total_cargadores_mostrar += Total_Cargador['cargadores']       
        context['Cargador'] = total_cargadores_mostrar
        context['Descripcion'] = "Cargadores"
        return context


class TpePrintView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Vista encargada para imprimir las :class:`SalidaInventario` de las salidas correspondiente
    """
    model = beqt_m.SalidaInventario
    template_name = 'beqt/salida/tpe_print.html'
    group_required = []

    def get_context_data(self, **kwargs):
        context = super(TpePrintView, self).get_context_data(**kwargs)
        cpu_servidor = ""
            
        try:
            cables_vga = inv_m.PaqueteTipo.objects.get(nombre="CABLE VGA")
        except ObjectDoesNotExist as e:
            cables_vga = 0
        try:
            cables_poder = inv_m.PaqueteTipo.objects.get(nombre="CABLE DE PODER")
        except ObjectDoesNotExist as e:
            cables_poder = 0
        try:
            access_point = inv_m.PaqueteTipo.objects.get(nombre="ACCESS POINT")
        except ObjectDoesNotExist as e:
            access_point = 0
        try:
            switch = inv_m.PaqueteTipo.objects.get(nombre="SWITCH")
        except ObjectDoesNotExist as e:
            switch = 0
        try:
            alambricas = inv_m.PaqueteTipo.objects.get(nombre="TARJETA DE RED ALAMBRICA")
        except ObjectDoesNotExist as e:
            alambricas = 0
        try:
            inalambricas = inv_m.PaqueteTipo.objects.get(nombre="TARJETA DE RED INALAMBRICA")
        except ObjectDoesNotExist as e:
            inalambricas = 0
        try:
            inalambricas_usb = inv_m.PaqueteTipo.objects.get(nombre="Adaptadores de WIFI USB")
        except ObjectDoesNotExist as e:
            inalambricas_usb = 0
        total_inalambricas = inv_m.Paquete.objects.filter(
            salida=self.object.id,
            tipo_paquete=inalambricas,
            desactivado=False
            ).aggregate(total_inalambricas=Sum('cantidad'))
        total_inalambricas_usb = inv_m.Paquete.objects.filter(
            salida=self.object.id,
            tipo_paquete=inalambricas_usb,
            desactivado=False
            ).aggregate(total_inalambricas_usb=Sum('cantidad'))
        total_alambricas = inv_m.Paquete.objects.filter(
            salida=self.object.id,
            tipo_paquete=alambricas,
            desactivado=False
            ).aggregate(total_alambricas=Sum('cantidad'))
        total_switch = inv_m.Paquete.objects.filter(
            salida=self.object.id,
            tipo_paquete=switch,
            desactivado=False
            ).aggregate(total_switch=Sum('cantidad'))
        total_access_point = inv_m.Paquete.objects.filter(
            salida=self.object.id,
            tipo_paquete=access_point,
            desactivado=False
            ).aggregate(total_access_point=Sum('cantidad'))
        total_cables_poder = inv_m.Paquete.objects.filter(
            salida=self.object.id,
            tipo_paquete=cables_poder,
            desactivado=False
            ).aggregate(total_cables_poder=Sum('cantidad'))
        escuela = beqt_m.SalidaInventario.objects.get(id=self.object.id)
         
        try:
            encargado = escuela_m.EscContacto.objects.filter(escuela=escuela.escuela, rol=5).reverse()[0]
            telefono = escuela_m.EscContactoTelefono.objects.get(contacto=encargado)
            context['Encargado'] = str(encargado.nombre)+" "+str(encargado.apellido)
            context['Telefono'] = str(telefono.telefono)
            context['Jornada'] = encargado.escuela.jornada
        except ObjectDoesNotExist as e:
            print(e)
            context['Jornada'] = "No tiene Jornada"
            context['Encargado'] = "No Tiene Encargado"
        except IndexError as e:
            print(e)
            context['Jornada'] = "No tiene Jornada"
            context['Encargado'] = "No Tiene Encargado"     
        
        try:
            red = "Mixta"
            if total_inalambricas['total_inalambricas'] > 0 and total_alambricas['total_alambricas'] == 0:
                red = "Inalambrica"
            elif total_inalambricas['total_inalambricas'] == 0 and total_alambricas['total_alambricas'] > 0:
                red = "Alambrica"

            context['Red'] = red
        except TypeError as e:
            context['Red'] = 0
        return context


class MineducPrintView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Vista encargada para imprimir las :class:`CPU` y la :class:`HDD` de las salidas correspondiente
    """
    model = inv_m.SalidaInventario
    template_name = 'beqt/salida/mineduc_print.html'
    group_required = []

    def get_context_data(self, **kwargs):
        context = super(MineducPrintView, self).get_context_data(**kwargs)
        nuevos_cpus = []
        cpu_servidor = ""
        cpu = inv_m.PaqueteTipo.objects.get(nombre="CPU")
        total_cpu = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=cpu,
            )
        for triage in total_cpu:
            nueva_cpu = inv_m.Dispositivo.objects.get(triage=triage.dispositivo).cast()
            nuevos_cpus.append(nueva_cpu)
            try:
                if nueva_cpu.servidor is True:
                    cpu_servidor = str(nueva_cpu.version_sistema)
            except Exception as e:
                print(e)
        escuela = inv_m.SalidaInventario.objects.get(id=self.object.id)
        try:
            encargado = escuela_m.EscContacto.objects.get(escuela=escuela.escuela, rol=5)
            context['Encargado'] = str(encargado.nombre)+" "+str(encargado.apellido)
            context['Jornada'] = encargado.escuela.jornada
        except ObjectDoesNotExist as e:
            print(e)
            context['Jornada'] = "No tiene Jornada"
            context['Encargado'] = "No Tiene Encargado"
        context['CPUs'] = nuevos_cpus
        context['Total'] = total_cpu.count()
        context['Servidor'] = cpu_servidor
        return context


class PrestamoCartaPrintView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Vista encargada para imprimir las Carta de Prestamo de las :class:`SalidaInventario`
    """
    model = inv_m.SalidaInventario
    template_name = 'beqt/salida/carta_prestamo_print.html'
    group_required = []

    def get_context_data(self, **kwargs):
        cpu_servidor = 0
        context = super(PrestamoCartaPrintView, self).get_context_data(**kwargs)
        CPU = inv_m.PaqueteTipo.objects.get(nombre="CPU")
        CPU2 = inv_m.DispositivoTipo.objects.get(tipo="CPU")
        Laptop = inv_m.PaqueteTipo.objects.get(nombre="Laptop")
        Tablet = inv_m.PaqueteTipo.objects.get(nombre="Tablet")
        Total_Servidor = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            dispositivo__tipo=CPU2)
        for nuevos in Total_Servidor:
            if nuevos.dispositivo.cast().servidor is True:
                cpu_servidor = cpu_servidor + 1
        Total_Cpu = inv_m.Paquete.objects.filter(
            salida__id=self.object.id,
            tipo_paquete=CPU).aggregate(total_cpu=Sum('cantidad'))
        Total_Laptop = inv_m.Paquete.objects.filter(
            salida__id=self.object.id,
            tipo_paquete=Laptop).aggregate(total_laptop=Sum('cantidad'))
        Total_Tablet = inv_m.Paquete.objects.filter(
            salida__id=self.object.id,
            tipo_paquete=Tablet).aggregate(total_tablet=Sum('cantidad'))
        if Total_Cpu['total_cpu'] is None:
            Total_Cpu['total_cpu'] = 0
        if Total_Laptop['total_laptop'] is None:
            Total_Laptop['total_laptop'] = 0
        if Total_Tablet['total_tablet'] is None:
            Total_Tablet['total_tablet'] = 0
        Total_Entregado = (Total_Cpu['total_cpu'] + Total_Laptop['total_laptop'] + Total_Tablet['total_tablet']) - cpu_servidor
        if Total_Tablet['total_tablet'] > 1:
            context['cpu'] = 1
        else:
            context['cpu'] = 0
        context['cpu_servidor'] = cpu_servidor
        context['dispositivo_total'] = Total_Entregado + cpu_servidor
        escuela = inv_m.SalidaInventario.objects.get(id=self.object.id)
        try:
            encargado = escuela_m.EscContacto.objects.get(escuela=escuela.escuela, rol=5)
            context['Encargado'] = str(encargado.nombre)+" "+str(encargado.apellido)
            context['Jornada'] = encargado.escuela.jornada
        except ObjectDoesNotExist as e:
            print(e)
            context['Jornada'] = "No tiene Jornada"
            context['Encargado'] = "No Tiene Encargado"
        return context


class PaquetesDetalleGrid(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """ Muestra los QR por Detalle de Entrada Creados
    """
    model = beqt_m.DispositivoPaquete
    template_name = 'beqt/salida/dispositivos_grid_paquetes.html'
    group_required = []
