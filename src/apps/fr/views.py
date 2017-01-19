from django.shortcuts import get_object_or_404
from apps.fr.models import *
from apps.fr.forms import *
from django.views.generic.base import ContextMixin
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from braces.views import LoginRequiredMixin
from django.urls import reverse_lazy
from apps.fr.mixins import ContactoContextMixin
from django.http import HttpResponse
import json


class ListMixin(ContextMixin):
    querylist = None

    def get_context_data(self, **kwargs):
        context = super(ListMixin, self).get_context_data(**kwargs)
        if self.querylist is None:
            context['lista'] = self.model.objects.all()
        else:
            context['lista'] = self.querylist
            # querylist = model.objects.filter(id__gt = 3)

        return context


class ContactListMixin(ContextMixin):
    def get(self, request, **kwargs):
        query = self.get_object()
        contacto_list = query.contacto.all()
        lista_vacia = []

        for cont in contacto_list:
            telefono_list = []
            for telefono in cont.telefono.all():
                telefono_list.append(str(telefono))

            mail_list = []
            for correo in cont.mail.all():
                mail_list.append(str(correo))

            lista_vacia.append({
                'nombre': str(cont),
                'empresa': str(cont.empresa),
                'puesto': str(cont.puesto),
                'telefono': telefono_list,
                'mail': mail_list})
        return HttpResponse(json.dumps({
            "contact": lista_vacia}))


class CreateEmpresa(LoginRequiredMixin, ListMixin, CreateView):
    model = Empresa
    form_class = FormEmpresa
    template_name = "fr/empresa.html"
    success_url = reverse_lazy('contacto_empresa')


class EditEmpresa(LoginRequiredMixin, UpdateView):
    model = Empresa
    form_class = FormEmpresa
    pk_url_kwarg = 'empresa_pk'
    template_name = "fr/empresaedit.html"
    success_url= reverse_lazy('contacto_empresa')

class EmpresaDetail(LoginRequiredMixin, DetailView):
    model = Empresa
    template_name = "fr/empresadetail.html"
    pk_url_kwarg = 'empresa_pk'


class CreateEvento(LoginRequiredMixin, ListMixin, CreateView):
    model = Evento
    form_class = FormEvento
    template_name = "fr/evento.html"
    success_url= reverse_lazy('contacto_evento')


class CreateContacto(LoginRequiredMixin, ListMixin, CreateView):
    model = Contacto
    form_class = FormContacto
    template_name = "fr/contacto.html"
    success_url= reverse_lazy('contacto_contactos')


class ContactoEtiqueta(LoginRequiredMixin, ContactListMixin, DetailView):
    model = Etiqueta
    pk_url_kwarg = 'tag_pk'
    

class ContactoEvento(LoginRequiredMixin, ContactListMixin, DetailView):
    model = Evento
    pk_url_kwarg = 'tag_pk'


class CreateContactIntoEmpresa(LoginRequiredMixin, ListMixin, ContactoContextMixin, CreateView):
    model = Contacto
    form_class = FormContactoEmpresa
    pk_url_kwarg = 'contact_pk'
    template_name = "fr/contactempresa.html"
    success_url= reverse_lazy('contacto_empresa')
    def get_initial(self):
        empresa = get_object_or_404(Empresa, id=self.kwargs.get('empresa_pk'))
        return { 'empresa': empresa }
    
class EditContacto(LoginRequiredMixin, ListMixin, ContactoContextMixin, UpdateView):
    model = Contacto
    form_class = FormContactoEmpresa
    pk_url_kwarg = 'contact_pk'
    template_name = "fr/contactempresa.html"
    success_url= reverse_lazy('contacto_empresa')
