# from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin, GroupRequiredMixin,
    CsrfExemptMixin, JsonRequestResponseMixin)
from django.views.generic import DetailView, ListView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from apps.crm import models as crm_m
from apps.crm import forms as crm_f


class DonanteCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos de los Donantes mediante una :class:`Donante`
    Funciona  para recibir los datos de un  'DonanteForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = crm_m.Donante
    template_name = 'crm/donante_add.html'
    form_class = crm_f.DonanteForm

    def get_success_url(self):
        return reverse_lazy('donante_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super(DonanteCreateView, self).form_valid(form)


class DonanteDetailView(LoginRequiredMixin, DetailView):
    """Vista para detalle de :class:`Donante`. con sus respectivos filtros
    """
    model = crm_m.Donante
    template_name = 'crm/donante_detail.html'


class DonanteUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para actualizar de :class:`Donante`. con sus respectivos campos
    """
    model = crm_m.Donante
    form_class = crm_f.DonanteForm
    template_name = 'crm/donante_add.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DonanteUpdateView, self).get_context_data(*args, **kwargs)
        context['TelefonoForm'] = crm_f.TelefonoForm(initial={'donante': self.object})
        context['CorreoForm'] = crm_f.CorreoForm(initial={'donante': self.object})
        context['ContactoForm'] = crm_f.ContactoForm(initial={'donante': self.object})
        context['OfertaForm'] = crm_f.OfertaForm()
        return context

    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super(DonanteUpdateView, self).form_valid(form)


class DonanteListView(LoginRequiredMixin, ListView):
    """Vista para Los listados de :class:`Donante`. con sus respectivos datos
    """
    model = crm_m.Donante
    template_name = 'crm/donante_list.html'


class OfertaCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos de los Donantes mediante una :class:`Oferta`
    Funciona  para recibir los datos de un  'OfertaForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = crm_m.Oferta
    template_name = 'crm/oferta_add.html'
    form_class = crm_f.OfertaForm

    def get_success_url(self):
        return reverse_lazy('oferta_detail', kwargs={'pk': self.object.id})


class OfertaDetailView(LoginRequiredMixin, DetailView):
    """Vista Encargada de Mostrar Los Detalles de  una oferta seleccionada
    """
    model = crm_m.Oferta
    template_name = 'crm/oferta_detail.html'


class OfertaUpdateView(LoginRequiredMixin, UpdateView):
    """Vista encargada de Actulizar de :class:'Oferta' con sus respectivos campos
    """
    model = crm_m.Oferta
    template_name = 'crm/oferta_add.html'
    form_class = crm_f.OfertaForm


class OfertaInformeView(LoginRequiredMixin, FormView):
    """Vista Encargada de crear los informes de  las ofertas obteniendo los datos
    desde el DRF
    """
    model = crm_m.Oferta
    template_name = 'crm/oferta_list.html'
    form_class = crm_f.OfertaInformeForm


class ContactoCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos del contacto  mediante una :class:`DonanteContacto`
    Funciona  para recibir los datos de un  'ContactoForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = crm_m.DonanteContacto
    template_name = 'crm/contacto_add.html'
    form_class = crm_f.ContactoForm

    def get_success_url(self):
        return reverse_lazy('donante_edit', kwargs={'pk': self.object.donante.id})


class ContactoDetailView(LoginRequiredMixin, DetailView):
    """Vista para detalle de :class:`DonanteContacto`. con sus respectivos filtros
    """
    model = crm_m.DonanteContacto
    template_name = 'crm/contacto_detail.html'
    form_class = crm_f.ContactoForm


class TelefonoCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos del contacto  mediante una :class:`TelefonoCrm`
    Funciona  para recibir los datos de un  'ContactoForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = crm_m.TelefonoCrm
    template_name = 'crm/telefono_contacto_add.html'
    form_class = crm_f.TelefonoForm

    def get_success_url(self):
        return reverse_lazy('donante_edit', kwargs={'pk': self.object.donante.id})


class CorreoCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos del contacto  mediante una :class:`CorreoCrm`
    Funciona  para recibir los datos de un  'CorreoForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = crm_m.MailCrm
    template_name = 'crm/correo_contacto_add.html'
    form_class = crm_f.CorreoForm

    def form_invalid(self, form):
        print(form.errors)
        return super(CorreoCreateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('donante_edit', kwargs={'pk': self.object.donante.id})


class HistoricoOfertaCrear(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """Vista Encargada de obtener los Historicos de las ofertas mediante el metodo
    POST y gurdarlos en la :class:`HistoricoOfertas`
    """
    require_json = True

    def post(self, request, *args, **kwargs):
        try:
            id_historico = self.request_json["id_historico"]
            oferta = crm_m.Oferta.objects.filter(id=id_historico)
            comentario = self.request_json["comentario"]
            if not len(comentario) or len(oferta) == 0:
                raise KeyError
        except KeyError:
            error_dict = {u"message": u"Sin Comentario"}
            return self.render_bad_request_response(error_dict)
        comentario_historico = crm_m.OfertaHistorico(
            oferta=oferta[0],
            usuario=self.request.user,
            comentario=comentario)
        comentario_historico.save()
        return self.render_json_response({
            "comentario": comentario_historico.comentario,
            "fecha": str(comentario_historico.fecha),
            "usuario": str(comentario_historico.usuario.perfil)
        })
