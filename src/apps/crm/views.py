# from django.shortcuts import render
from django.urls import reverse_lazy
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


class OfertaCreateView(LoginRequiredMixin, CreateView):
    model = crm_m.Oferta
    template_name = 'crm/oferta_add.html'
    form_class = crm_f.OfertaForm

    def get_success_url(self):
        return reverse_lazy('oferta_edit', kwargs={'pk': self.object.id})


class OfertaDetailView(LoginRequiredMixin, DetailView):
    model = crm_m.Oferta
    template_name = 'crm/oferta_detail.html'


class OfertaUpdateView(LoginRequiredMixin, UpdateView):
    """Vista encargada de Actulizar de :class:'Oferta' con sus respectivos campos
    """
    model = crm_m.Oferta
    template_name = 'crm/oferta_add.html'
    form_class = crm_f.OfertaForm


class OfertaInformeView(LoginRequiredMixin, FormView):
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
        return reverse_lazy('donante_update', kwargs={'pk': self.object.donante.id})


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


class CorreoCreateView(LoginRequiredMixin, CreateView):
    """Vista   para obtener los datos del contacto  mediante una :class:`CorreoCrm`
    Funciona  para recibir los datos de un  'CorreoForm' mediante el metodo  POST.  y
    nos muestra el template de visitas mediante el metodo GET.
    """
    model = crm_m.MailCrm
    template_name = 'crm/correo_contacto_add.html'
    form_class = crm_f.CorreoForm


class HistoricoOfertaCrear(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """"""
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
