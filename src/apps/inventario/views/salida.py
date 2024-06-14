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
from apps.tpe import models as tpe_m
from django import forms
from dateutil.relativedelta import relativedelta
from apps.conta import models as cont_m

class SalidaInventarioCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    """Vista   para obtener los datos de Salida mediante una :class:`SalidaInventario`
    Funciona  para recibir los datos de un  'SalidaInventarioForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.SalidaInventario
    form_class = inv_f.SalidaInventarioForm
    template_name = 'inventario/salida/salida_add.html'
    group_required = [u"inv_cc", u"inv_admin"]

    def get_success_url(self):
        return reverse_lazy('salidainventario_edit', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(SalidaInventarioCreateView, self).get_context_data(**kwargs)
        context['salidainventario_list'] = inv_m.SalidaInventario.objects.filter(en_creacion=True)
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
    model = inv_m.SalidaInventario
    form_class = inv_f.SalidaInventarioUpdateForm
    template_name = 'inventario/salida/salida_edit.html'
    group_required = [u"inv_cc", u"inv_admin", u"inv_tecnico"]

    def get_context_data(self, *args, **kwargs):
        context = super(SalidaInventarioUpdateView, self).get_context_data(*args, **kwargs)
        context['paquetes_form'] = inv_f.PaqueteCantidadForm()
        Laptop = inv_m.PaqueteTipo.objects.get(nombre="Laptop")
        Tablet = inv_m.PaqueteTipo.objects.get(nombre="Tablet")
        cpu = inv_m.PaqueteTipo.objects.get(nombre="CPU")
        Total_Tablet = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=Tablet)
        Total_Laptop = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=Laptop)
        total_cpu = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=cpu,
            )
        comentarios_cc= inv_m.SalidaComentario.objects.filter(salida=self.object.id)
        comentarios_conta=inv_m.RevisionComentario.objects.filter(revision__salida=self.object.id)
        context['CPU'] = total_cpu.count()
        context['Laptops'] = Total_Laptop.count()
        context['Tablets'] = Total_Tablet.count()
        context['comentario_cc'] = comentarios_cc
        context['comentario_conta'] = comentarios_conta
        return context


class SalidaInventarioDetailView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Vista encargada de mostrar los detalles de la :class:`SalidaInventario`
    """
    model = inv_m.SalidaInventario
    template_name = 'inventario/salida/salida_detail.html'
    group_required = [u"inv_cc", u"inv_admin", u"inv_tecnico", u"inv_bodega", u"inv_conta"]

    def get_context_data(self, *args, **kwargs):
        context = super(SalidaInventarioDetailView, self).get_context_data(*args, **kwargs)
        Laptop = inv_m.PaqueteTipo.objects.get(nombre="Laptop")
        Tablet = inv_m.PaqueteTipo.objects.get(nombre="Tablet")
        cpu = inv_m.PaqueteTipo.objects.get(nombre="CPU")
        total_cpu = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=cpu,
            )
        context['CPU'] = total_cpu.count()
        Total_Tablet = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=Tablet)
        Total_Laptop = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=Laptop)
        context['Laptops'] = Total_Laptop.count()
        context['Tablets'] = Total_Tablet.count()
        
        
        salida = self.object.id
        precio_total = 0
        total_dispo = 0

        lista_paquete = inv_m.Paquete.objects.filter(salida = salida, aprobado_kardex = False)

        for paquete in lista_paquete: 
            dispositivos = inv_m.DispositivoPaquete.objects.filter(paquete = paquete.id)

            for dispositivo in dispositivos:
                precios = cont_m.MovimientoDispositivo.objects.filter(dispositivo = dispositivo.dispositivo, tipo_movimiento = -1)

                total_dispo += 1

                for precio in precios:
                    precio_total += precio.precio
            
        context['total_precio'] = precio_total
        context['total_dispositivos'] = total_dispo

        return context

class SalidaInventarioListView(LoginRequiredMixin,  FormView):
    """ Vista creada para obtener el listado de las :class:`SalidaInventario`
    Funciona para recibir los datos de un 'SalidaInventarioListForm' mediante el metodo POST.
    y nos muestra el rempalte de la vista mediante le metodo get
    """
    model = inv_m.SalidaInventario
    form_class = inv_f.SalidaInventarioListForm
    template_name = 'inventario/salida/salida_add.html'

    def get_context_data(self, **kwargs):
        context = super(SalidaInventarioListView, self).get_context_data(**kwargs)
        context['lista'] = 1
        return context
    def get_success_url(self):
        return reverse_lazy('salidainventario_list')


class SalidaPaqueteUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """ Vista   para obtener los datos de Paquete mediante una :class:`SalidaInventario`
    Funciona  para recibir los datos de un  'PaqueteCantidadForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = inv_m.SalidaInventario
    form_class = inv_f.PaqueteCantidadForm
    template_name = 'inventario/salida/paquetes_add.html'
    group_required = [u"inv_cc", u"inv_admin"]

    def get_success_url(self):
        return reverse_lazy('salidainventario_edit', kwargs={'pk': self.object.id})

    def get_form(self, form_class=None):
        print('Get Form')
        form = super(SalidaPaqueteUpdateView, self).get_form(form_class)
        form.fields['entrada'].widget = forms.SelectMultiple(attrs={
            'data-api-url': reverse_lazy('inventario_api:api_entrada-list')
        })
        form.fields['entrada'].queryset = inv_m.Entrada.objects.filter(
            tipo=3
        )
        return form

    def form_valid(self, form):       
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


class SalidaPaqueteDetailView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """Vista para detalle de :class:`Paquete`.
    """
    model = inv_m.Paquete
    template_name = 'inventario/salida/paquetes_detail.html'
    form_class = inv_f.PaqueteUpdateForm
    group_required = [u"inv_tecnico", u"inv_cc", u"inv_admin", u"inv_bodega"]

    def get_form(self, form_class=None):
        form = super(SalidaPaqueteDetailView, self).get_form(form_class)
        etapa = inv_m.DispositivoEtapa.objects.get(id=inv_m.DispositivoEtapa.TR)
        estado = inv_m.DispositivoEstado.objects.get(id=inv_m.DispositivoEstado.PD)
        form.fields['dispositivos'].widget = forms.SelectMultiple(
            attrs={
                'data-api-url': reverse_lazy('inventario_api:api_dispositivo-list'),
                'data-tipo-dispositivo': self.object.tipo_paquete.tipo_dispositivo.id,
                'data-slug': self.object.tipo_paquete.tipo_dispositivo.slug,
                'data-cantidad': self.object.cantidad,
                'data-etapa_inicial': etapa.id,
                'data-estado_inicial': estado.id,
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
        for nuevosDispositivos in form.cleaned_data['dispositivos']:
            nuevosDispositivos.etapa = etapa_control
            nuevosDispositivos.save()
        return super(SalidaPaqueteDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SalidaPaqueteDetailView, self).get_context_data(**kwargs)
        nuevo_id = inv_m.Paquete.objects.get(id=self.object.id)
        context['dispositivos_paquetes'] = inv_m.DispositivoPaquete.objects.filter(paquete__id=self.object.id)
        context['dispositivos_no'] = inv_m.DispositivoPaquete.objects.filter(paquete__id=self.object.id).count()
        context['comentarios'] = inv_m.SalidaComentario.objects.filter(salida=nuevo_id.salida)
        
        return context


class RevisionSalidaCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    """Vista para creación de :class:`RevisionSalida`"""
    model = inv_m.RevisionSalida
    form_class = inv_f.RevisionSalidaCreateForm
    template_name = 'inventario/salida/revisionsalida_add.html'
    group_required = [u"inv_conta", u"inv_admin"]

    def get_success_url(self):
        return reverse_lazy('revisionsalida_update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {
            'fecha_revision': None
        }

    def form_valid(self, form):
        form.instance.revisado_por = self.request.user
        return super(RevisionSalidaCreateView, self).form_valid(form)


class RevisionSalidaUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """Vista para edición de :class:`RevisionSalida`"""
    model = inv_m.RevisionSalida
    form_class = inv_f.RevisionSalidaUpdateForm
    template_name = 'inventario/salida/revisionsalida_update.html'
    group_required = [u"inv_conta", u"inv_admin"]

    def get_context_data(self, *args, **kwargs):
        context = super(RevisionSalidaUpdateView, self).get_context_data(*args, **kwargs)
        comentarios_cc= inv_m.SalidaComentario.objects.filter(salida=self.object.salida.id)
        context['comentario_cc'] = comentarios_cc
        return context


class SalidaPaqueteView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Vista para detalle de :class:`SalidaInventario`.on sus respectivos filtros
    """
    model = inv_m.SalidaInventario
    template_name = 'inventario/salida/dispositivo_paquete.html'
    group_required = [u"inv_cc", u"inv_admin"]

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


class RevisionSalidaListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    """Vista para Los listados de :class:`RevisionSalida`. con sus respectivos datos
    """
    model = inv_m.RevisionSalida
    template_name = 'inventario/salida/revisionsalida_list.html'
    group_required = [u"inv_cc", u"inv_admin", u"inv_conta"]


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


class RevisionComentarioSalidaCreate(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """Vista Encargada de obtener las Revision de Comentario de las ofertas mediante el metodo
    POST y gurdarlos en la :class:`SalidaComentario`
    """

    require_json = True

    def post(self, request, *args, **kwargs):
        try:
            id_comentario = self.request_json["id_comentario"]
            revision_salida = inv_m.SalidaInventario.objects.filter(no_salida=id_comentario)
            comentario = self.request_json["comentario"]
            if not len(comentario) or len(revision_salida) == 0:
                raise KeyError
        except KeyError:
            error_dict = {u"message": u"Sin Comentario"}
            return self.render_bad_request_response(error_dict)
        comentario_revision = inv_m.SalidaComentario(
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
    model = inv_m.SalidaInventario
    template_name = 'inventario/salida/controlcalidad_list.html'
    group_required = [u"inv_cc", u"inv_admin", u"inv_tecnico", u"inv_conta"]

    def get_context_data(self, **kwargs):
        context = super(ControlCalidadListView, self).get_context_data(**kwargs)
        context['controlcalidad_list'] = inv_m.SalidaInventario.objects.filter(en_creacion=True)
        return context


class DispositivoAsignados(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Vista encargada de ver los dispositivos que se fueron asignados a los paquetes
    """
    model = inv_m.Paquete
    template_name = 'inventario/salida/dispositivos_salida.html'
    group_required = [u"inv_tecnico", u"inv_admin", u"inv_cc", u"inv_bodega"]

    def get_context_data(self, **kwargs):
        context = super(DispositivoAsignados, self).get_context_data(**kwargs)
        dispositivo_paquetes = inv_m.DispositivoPaquete.objects.filter(paquete__id=self.object.id)
        dispositivos_enviar=[]
        for data in dispositivo_paquetes:
            data_dipositivos ={}      
            data_dipositivos['dispositivo']=data.dispositivo
            data_dipositivos['paquete']=data.paquete
            data_dipositivos['fecha_creacion']=data.fecha_creacion
            data_dipositivos['asignado_por']=data.asignado_por
            data_dipositivos['fecha_aprobacion']=data.fecha_aprobacion
            data_dipositivos['aprobado']= data.aprobado
            data_dipositivos['tipo']= data.dispositivo.tipo
            data_dipositivos['tipo_salida']=data.paquete.salida.tipo_salida
            data_dipositivos['tipo_salida.id']=data.paquete.salida.tipo_salida.id
            data_dipositivos['precio']=data.paquete.salida.tipo_salida.id 
            movimiento_dispositivo = cont_m.MovimientoDispositivo.objects.filter(dispositivo=data.dispositivo,tipo_movimiento=-1)  
            if movimiento_dispositivo.count() == 1:                
                data_dipositivos['asignado']= 1
                data_dipositivos['precio']=movimiento_dispositivo[0].precio                  
            else:                
                data_dipositivos['asignado']= 0
                data_dipositivos['precio']=0                             
            dispositivos_enviar.append(data_dipositivos)        
        context['dispositivo_list'] = dispositivos_enviar          
        return context


class GarantiaPrintView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Vista encargada para imprimir las Garantias de las :class:`SalidaInventario`
    """
    model = inv_m.SalidaInventario
    template_name = 'inventario/salida/garantia_print.html'
    group_required = [u"inv_tecnico", u"inv_admin", u"inv_cc"]

    def get_context_data(self, **kwargs):
        context = super(GarantiaPrintView, self).get_context_data(**kwargs)
        cpu_servidor = 0
        CPU = inv_m.PaqueteTipo.objects.get(nombre="CPU")
        Laptop = inv_m.PaqueteTipo.objects.get(nombre="Laptop")
        Tablet = inv_m.PaqueteTipo.objects.get(nombre="Tablet")
        total_cpu = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=CPU,
            ) 
        laptops_server = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=Laptop,
            )
        Total_Cpu = inv_m.Paquete.objects.filter(
            salida__id=self.object.id,
            tipo_paquete=CPU).aggregate(total_cpu=Sum('cantidad'))
        Total_Laptop = inv_m.Paquete.objects.filter(
            salida__id=self.object.id,
            tipo_paquete=Laptop).aggregate(total_laptop=Sum('cantidad'))
        Total_Tablet = inv_m.Paquete.objects.filter(
            salida__id=self.object.id,
            tipo_paquete=Tablet).aggregate(total_tablet=Sum('cantidad'))
        for triage_cpu in total_cpu:
            nuevo_cpu = inv_m.Dispositivo.objects.get(triage=triage_cpu.dispositivo).cast()
            try:
                if nuevo_cpu.servidor is True:
                    cpu_servidor = cpu_servidor + 1
            except Exception as e:
                print(e)

        for servidor_laptop  in laptops_server:
            nueva_laptop = inv_m.Dispositivo.objects.get(triage=servidor_laptop.dispositivo).cast()
            try:
                if nueva_laptop.servidor is True:
                    cpu_servidor = cpu_servidor + 1
                    context['laptop'] = True
            except Exception as e:
                print(e)
        
        if Total_Cpu['total_cpu'] is None:
            Total_Cpu['total_cpu'] = 0
        if Total_Laptop['total_laptop'] is None:
            Total_Laptop['total_laptop'] = 0
        if Total_Tablet['total_tablet'] is None:
            Total_Tablet['total_tablet'] = 0
        Total_Entregado = (Total_Cpu['total_cpu']+Total_Laptop['total_laptop']+Total_Tablet['total_tablet']) - cpu_servidor
        if Total_Tablet['total_tablet'] > 1:
            context['cpu'] = 1
        else:
            context['cpu'] = 0
        Fecha = inv_m.SalidaInventario.objects.get(id=self.object.id)
        context['capacitada'] = Fecha.capacitada
        if Fecha.meses_garantia:
            context['fin_garantia'] = Fecha.fecha + relativedelta(months=6)
            context["tiempo"] = "6 meses"
        else:
            context['fin_garantia'] = Fecha.fecha + relativedelta(months=12)
            context["tiempo"] = " 1 año"
        context['dispositivo_total'] = Total_Entregado
        context['cpu_servidor'] = cpu_servidor


        Total_Cpu_num = Total_Cpu
        Total_Laptop_num = Total_Laptop
        context['Total_Cpu'] = Total_Cpu_num['total_cpu']
        context['Total_Laptop'] = Total_Laptop_num['total_laptop']
        return context
        

class LaptopPrintView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Vista encargada para imprimir las :class:`Laptop` de las salidas correspondiente
    """
    model = inv_m.SalidaInventario
    template_name = 'inventario/salida/laptop_print.html'
    group_required = [u"inv_tecnico", u"inv_admin", u"inv_cc"]

    def get_context_data(self, **kwargs):
        context = super(LaptopPrintView, self).get_context_data(**kwargs)
        nuevas_laptops = []
        cpu_servidor = ""
        Laptop = inv_m.PaqueteTipo.objects.get(nombre="Laptop")
        cpu = inv_m.PaqueteTipo.objects.get(nombre="CPU")
        Total_Laptop = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=Laptop)
        total_cpu = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=cpu,
            )
        cantidad_total = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=Laptop).count()
        for triage_cpu in total_cpu:
            nuevo_cpu = inv_m.Dispositivo.objects.get(triage=triage_cpu.dispositivo).cast()
            try:
                if nuevo_cpu.servidor is True:
                    cpu_servidor = str(nuevo_cpu.version_sistema)
            except Exception as e:
                print(e)
        for triage in Total_Laptop:
            nuevo_laptop = inv_m.Dispositivo.objects.get(triage=triage.dispositivo).cast()
            nuevas_laptops.append(nuevo_laptop)
        escuela = inv_m.SalidaInventario.objects.get(id=self.object.id)
        try:
            encargado = escuela_m.EscContacto.objects.get(escuela=escuela.escuela, rol=5)
            context['Encargado'] = str(encargado.nombre)+" "+str(encargado.apellido)
        except ObjectDoesNotExist as e:
            print(e)
            context['Encargado'] = "No Tiene Encargado"
        context['Laptos'] = nuevas_laptops
        context['Total'] = cantidad_total
        context['Servidor'] = cpu_servidor

        nuevos_mouse = []
        total_inalambricas_mostrar = 0
        
        mouse = inv_m.PaqueteTipo.objects.get(nombre="MOUSE")

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
        
        total_mouse = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=mouse,
            )
        total_cables_vga = inv_m.Paquete.objects.filter(
            salida=self.object.id,
            tipo_paquete=cables_vga,
            desactivado=False
            ).aggregate(total_cables_vga=Sum('cantidad'))
        
        for triage_mouse in total_mouse:
            nuevo_mouse = inv_m.Dispositivo.objects.get(triage=triage_mouse.dispositivo).cast()
            nuevos_mouse.append(nuevo_mouse)
        escuela = inv_m.SalidaInventario.objects.get(id=self.object.id)

        context['Mouses'] = nuevos_mouse
        context['total_mouse'] = total_mouse.count()
        #context['total_mouse'] = 0

        total_inalambricas_mostrar = int( total_inalambricas['total_inalambricas'] or 0) + int( total_inalambricas_usb['total_inalambricas_usb'] or 0)

        try:
            red = "Mixta"
            if total_inalambricas['total_inalambricas'] > 0 and total_alambricas['total_alambricas'] == 0:
                red = "Inalambrica"
            elif total_inalambricas['total_inalambricas'] == 0 and total_alambricas['total_alambricas'] > 0:
                red = "Alambrica"

            context['Red'] = red
        except TypeError as e:
            context['Red'] = 0
        
        context['Wifi'] = total_inalambricas_mostrar
        context['Ethernet'] = total_alambricas['total_alambricas']
        context['Access'] = total_access_point['total_access_point']
        context['Switch'] = total_switch['total_switch']        
        context['CablesPoder'] = total_cables_poder['total_cables_poder']
        context['CablesVga'] = total_cables_vga['total_cables_vga']


        return context


class TabletPrintView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Vista encargada para imprimir las :class:`Tablets` de las salidas correspondiente
    """
    model = inv_m.SalidaInventario
    template_name = 'inventario/salida/tablet_print.html'
    group_required = [u"inv_tecnico", u"inv_admin", u"inv_cc"]

    def get_context_data(self, **kwargs):
        context = super(TabletPrintView, self).get_context_data(**kwargs)
        nuevas_tablets = []
        total_cargadores_mostrar = 0
        Tablet = inv_m.PaqueteTipo.objects.get(nombre="Tablet")
        Cargador = inv_m.PaqueteTipo.objects.get(nombre="Cargadores")
        Cargador_cubo = inv_m.PaqueteTipo.objects.get(nombre="CUBO DE CARGA PARA TABLET")
        Cable_cargador = inv_m.PaqueteTipo.objects.get(nombre="CABLE DE DATOS PARA TABLET")
        Cargador_grande = inv_m.PaqueteTipo.objects.get(nombre="CARGADOR ENTRADA GRANDE PARA TABLET")
        Total_Tablet = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=Tablet)
        Total_Cargador = inv_m.Paquete.objects.filter(
            salida__id=self.object.id,
            tipo_paquete=Cargador).aggregate(cargadores=Sum('cantidad'))
        Total_Cargador_Cubo = inv_m.Paquete.objects.filter(
            salida__id=self.object.id,
            tipo_paquete=Cargador_cubo).aggregate(cargadores=Sum('cantidad'))
        Total_Cable_Cargador = inv_m.Paquete.objects.filter(
            salida__id=self.object.id,
            tipo_paquete=Cable_cargador).aggregate(cargadores=Sum('cantidad'))
        Total_Cargador_grande = inv_m.Paquete.objects.filter(
            salida__id=self.object.id,
            tipo_paquete=Cargador_grande).aggregate(cargadores=Sum('cantidad'))

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
        if Total_Cargador_Cubo['cargadores'] != None:
            total_cargadores_mostrar += Total_Cargador_Cubo['cargadores']
        if Total_Cargador_grande['cargadores'] != None:
            total_cargadores_mostrar += Total_Cargador_grande['cargadores']
        if Total_Cable_Cargador['cargadores'] != None:
            total_cargadores_mostrar += Total_Cable_Cargador['cargadores']
        context['Cargador'] = total_cargadores_mostrar
        context['Descripcion'] = "Cargadores"
        return context


class TpePrintView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Vista encargada para imprimir las :class:`SalidaInventario` de las salidas correspondiente
    """
    model = inv_m.SalidaInventario
    template_name = 'inventario/salida/tpe_print.html'
    group_required = [u"inv_tecnico", u"inv_admin", u"inv_cc"]

    def get_context_data(self, **kwargs):
        context = super(TpePrintView, self).get_context_data(**kwargs)
        cpu_servidor = ""
        nuevos_cpus = []
        nuevos_teclados = []
        nuevos_monitores = []
        nuevos_mouse = []
        contador_all_in_one =0
        total_inalambricas_mostrar = 0
        cpu = inv_m.PaqueteTipo.objects.get(nombre="CPU")
        monitor = inv_m.PaqueteTipo.objects.get(nombre="MONITOR")
        mouse = inv_m.PaqueteTipo.objects.get(nombre="MOUSE")
        teclado = inv_m.PaqueteTipo.objects.get(nombre="TECLADO")
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
        total_cpu = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=cpu,
            )
        total_all_in_on = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=cpu,
            )
        total_monitor = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=monitor,
            )
        total_teclado = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=teclado,
            )
        total_mouse = inv_m.DispositivoPaquete.objects.filter(
            paquete__salida__id=self.object.id,
            paquete__tipo_paquete=mouse,
            )
        total_cables_vga = inv_m.Paquete.objects.filter(
            salida=self.object.id,
            tipo_paquete=cables_vga,
            desactivado=False
            ).aggregate(total_cables_vga=Sum('cantidad'))
        for triage in total_cpu:
            nueva_cpu = inv_m.Dispositivo.objects.get(triage=triage.dispositivo).cast()
            if nueva_cpu.all_in_one:
                contador_all_in_one += 1
            nuevos_cpus.append(nueva_cpu)
            try:
                if nueva_cpu.servidor is True:
                    cpu_servidor = str(nueva_cpu.version_sistema)
            except Exception as e:
                print(e)
        for triage_monitor in total_monitor:
            nuevo_monitor = inv_m.Dispositivo.objects.get(triage=triage_monitor.dispositivo).cast()
            nuevos_monitores.append(nuevo_monitor)
        for triage_teclado in total_teclado:
            nuevo_teclado = inv_m.Dispositivo.objects.get(triage=triage_teclado.dispositivo).cast()
            nuevos_teclados.append(nuevo_teclado)
        for triage_mouse in total_mouse:
            nuevo_mouse = inv_m.Dispositivo.objects.get(triage=triage_mouse.dispositivo).cast()
            nuevos_mouse.append(nuevo_mouse)
        escuela = inv_m.SalidaInventario.objects.get(id=self.object.id)
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
        total_inalambricas_mostrar = int( total_inalambricas['total_inalambricas'] or 0) + int( total_inalambricas_usb['total_inalambricas_usb'] or 0)
        context['CPUs'] = nuevos_cpus
        context['Monitores'] = nuevos_monitores
        context['Teclados'] = nuevos_teclados
        context['Mouses'] = nuevos_mouse
        context['Total'] = total_cpu.count()
        context['Servidor'] = cpu_servidor
        context['CablesVga'] = total_cables_vga['total_cables_vga']
        context['CablesPoder'] = total_cables_poder['total_cables_poder']
        context['Switch'] = total_switch['total_switch']
        context['Wifi'] = total_inalambricas_mostrar
        context['Ethernet'] = total_alambricas['total_alambricas']
        context['Access'] = total_access_point['total_access_point']
        context['AllInOne'] = contador_all_in_one
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
    template_name = 'inventario/salida/mineduc_print.html'
    group_required = [u"inv_tecnico", u"inv_admin", u"inv_cc"]

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
    template_name = 'inventario/salida/carta_prestamo_print.html'
    group_required = [u"inv_tecnico", u"inv_admin", u"inv_cc"]

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
    model = inv_m.DispositivoPaquete
    template_name = 'inventario/salida/dispositivos_grid_paquetes.html'
    group_required = [u"inv_bodega", u"inv_tecnico", u"inv_admin"]


class CajaRepuestosEntradaView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Vista encargada para imprimir la entrada de caja de repuesto
    """
    model = inv_m.SalidaInventario
    template_name = 'inventario/salida/entrada_caja_repuestos.html'
    group_required = [u"inv_tecnico", u"inv_admin", u"inv_cc"]

    def get_context_data(self, **kwargs):
        context = super(CajaRepuestosEntradaView, self).get_context_data(**kwargs)       
        caja = inv_m.SalidaInventario.objects.get(id = self.object.id) 
        paquetes = inv_m.Paquete.objects.filter(salida = caja)

        context['tecnico'] = caja.creada_por.get_full_name
        context['salidas_asignadas'] = self.object.caja_repuesto.all()
        context['fecha'] = caja.fecha
        context['paquetes'] = paquetes

        dispositivos = []
        for paquete in paquetes:
            dispo_paquete = inv_m.DispositivoPaquete.objects.filter(paquete=paquete)
            for dispositivo in dispo_paquete:
                dispositivos.append(dispositivo.dispositivo)
        context['dispositivos'] = dispositivos
        
        context['salida'] = caja
        dispo_salidos = inv_m.CajaRepuestos.objects.filter(salida_asignada = caja)
        
        dispo_malos = []
        for malos in dispo_salidos:
            dispo_malos.append(malos)
        context['dispo_malos'] = dispo_malos

        return context
    
class CajaRepuestosSalidaView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """Vista encargada para imprimir la entrada de caja de repuesto
    """
    model = inv_m.SalidaInventario
    template_name = 'inventario/salida/salida_caja_repuestos.html'
    group_required = [u"inv_tecnico", u"inv_admin", u"inv_cc"]

    def get_context_data(self, **kwargs):
        context = super(CajaRepuestosSalidaView, self).get_context_data(**kwargs)
        caja = inv_m.SalidaInventario.objects.get(id = self.object.id) 
        paquetes = inv_m.Paquete.objects.filter(salida = caja)

        context['tecnico'] = caja.creada_por.get_full_name
        context['salidas_asignadas'] = self.object.caja_repuesto.all()
        context['fecha'] = caja.fecha
        context['paquetes'] = paquetes

        dispositivos = []
        for paquete in paquetes:
            dispo_paquete = inv_m.DispositivoPaquete.objects.filter(paquete=paquete)
            for dispositivo in dispo_paquete:
                dispositivos.append(dispositivo.dispositivo)

        context['dispositivos'] = dispositivos
        context['salida'] = caja

        return context