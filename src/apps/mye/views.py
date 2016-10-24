from django.http import JsonResponse
from django.shortcuts import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from .forms import CooperanteForm, ProyectoForm, SolicitudVersionForm, SolicitudForm, SolicitudNuevaForm
from .models import Cooperante, Proyecto, SolicitudVersion, Solicitud
from braces.views import LoginRequiredMixin, PermissionRequiredMixin


class CooperanteCrear(LoginRequiredMixin, CreateView):
    model = Cooperante
    template_name = 'mye/cooperante_form.html'
    form_class = CooperanteForm


class CooperanteDetalle(LoginRequiredMixin, DetailView):
    model = Cooperante
    template_name = 'mye/cooperante.html'


class CooperanteUpdate(LoginRequiredMixin, UpdateView):
    model = Cooperante
    template_name = 'mye/cooperante_form.html'
    form_class = CooperanteForm


class CooperanteList(LoginRequiredMixin, ListView):
    model = Cooperante
    template_name = 'mye/cooperante_list.html'


class ProyectoCrear(LoginRequiredMixin, CreateView):
    model = Proyecto
    template_name = 'mye/proyecto_form.html'
    form_class = ProyectoForm


class ProyectoDetalle(LoginRequiredMixin, DetailView):
    model = Proyecto
    template_name = 'mye/proyecto.html'


class ProyectoUpdate(LoginRequiredMixin, UpdateView):
    model = Proyecto
    template_name = 'mye/proyecto_form.html'
    form_class = ProyectoForm


class ProyectoList(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'mye/proyecto_list.html'


class SolicitudVersionCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SolicitudVersion
    template_name = 'mye/solicitud_version_form.html'
    form_class = SolicitudVersionForm
    permission_required = 'mye.add_solicitud_version'
    redirect_unauthenticated_users = True
    raise_exception = True


class SolicitudVersionDetalle(LoginRequiredMixin, DetailView):
    model = SolicitudVersion
    template_name = 'mye/solicitud_version.html'


class SolicitudCrearView(LoginRequiredMixin, CreateView):
    model = Solicitud
    form_class = SolicitudNuevaForm

    def form_valid(self, form):
        response = super(SolicitudCrearView, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super(SolicitudCrearView, self).form_valid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def get_success_url(self):
        return reverse('escuela_solicitud_update', kwargs={'pk': self.object.escuela.id, 'id_solicitud': self.object.id})


class SolicitudUpdate(LoginRequiredMixin, UpdateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'mye/solicitud_form.html'

    def get_success_url(self):
        return reverse('escuela_detail', kwargs={'pk': self.object.escuela.id})
