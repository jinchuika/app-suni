from django.shortcuts import reverse

from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, UpdateView, FormView

from django.http import JsonResponse
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, CsrfExemptMixin, JsonRequestResponseMixin

from apps.mye import forms as mye_f
from apps.mye import models as mye_m

from apps.escuela.views import EscuelaDetail


class CooperanteCrear(LoginRequiredMixin, CreateView):
    model = mye_m.Cooperante
    template_name = 'mye/cooperante_form.html'
    form_class = mye_f.CooperanteForm


class CooperanteDetalle(LoginRequiredMixin, DetailView):
    model = mye_m.Cooperante
    template_name = 'mye/cooperante.html'


class CooperanteUpdate(LoginRequiredMixin, UpdateView):
    model = mye_m.Cooperante
    template_name = 'mye/cooperante_form.html'
    form_class = mye_f.CooperanteForm


class CooperanteList(LoginRequiredMixin, FormView):
    model = mye_m.Cooperante
    template_name = 'mye/cooperante_list.html'
    form_class = mye_f.CPFilterForm


class ProyectoCrear(LoginRequiredMixin, CreateView):
    model = mye_m.Proyecto
    template_name = 'mye/proyecto_form.html'
    form_class = mye_f.ProyectoForm


class ProyectoDetalle(LoginRequiredMixin, DetailView):
    model = mye_m.Proyecto
    template_name = 'mye/proyecto.html'


class ProyectoUpdate(LoginRequiredMixin, UpdateView):
    model = mye_m.Proyecto
    template_name = 'mye/proyecto_form.html'
    form_class = mye_f.ProyectoForm


class ProyectoList(LoginRequiredMixin, ListView):
    model = mye_m.Proyecto
    template_name = 'mye/proyecto_list.html'


class SolicitudVersionCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = mye_m.SolicitudVersion
    template_name = 'mye/solicitud_version_form.html'
    form_class = mye_f.SolicitudVersionForm
    permission_required = 'mye.add_solicitud_version'
    redirect_unauthenticated_users = True
    raise_exception = True


class SolicitudVersionDetalle(LoginRequiredMixin, DetailView):
    model = mye_m.SolicitudVersion
    template_name = 'mye/solicitud_version.html'


class SolicitudCrearView(LoginRequiredMixin, CreateView):
    model = mye_m.Solicitud
    form_class = mye_f.SolicitudNuevaForm

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
        return reverse(
            'escuela_solicitud_update',
            kwargs={'pk': self.object.escuela.id, 'id_solicitud': self.object.id})


class SolicitudUpdate(LoginRequiredMixin, UpdateView):
    model = mye_m.Solicitud
    form_class = mye_f.SolicitudForm
    template_name = 'mye/solicitud_form.html'

    def get_success_url(self):
        return reverse('escuela_detail', kwargs={'pk': self.object.escuela.id})


class ValidacionCrearView(LoginRequiredMixin, CreateView):
    model = mye_m.Validacion
    form_class = mye_f.ValidacionNuevaForm

    def form_valid(self, form):
        response = super(ValidacionCrearView, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super(ValidacionCrearView, self).form_valid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def get_success_url(self):
        return reverse(
            'escuela_validacion_update',
            kwargs={'pk': self.object.escuela.id, 'id_validacion': self.object.id})


class ValidacionUpdate(LoginRequiredMixin, UpdateView):
    model = mye_m.Validacion
    form_class = mye_f.ValidacionForm
    template_name = 'mye/solicitud_form.html'

    def get_success_url(self):
        return reverse('escuela_detail', kwargs={'pk': self.object.escuela.id})


class ValidacionComentarioCrear(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """
    Todo:
        Se debe cambiar esta vista para utilizar DRF
    """
    require_json = True

    def post(self, request, *args, **kwargs):
        try:
            id_validacion = self.request_json["id_validacion"]
            validacion = mye_m.Validacion.objects.filter(id=id_validacion)
            comentario = self.request_json["comentario"]
            if not len(comentario) or len(validacion) == 0:
                raise KeyError
        except KeyError:
            error_dict = {u"message": u"Sin comentario"}
            return self.render_bad_request_response(error_dict)
        comentario_validacion = mye_m.ValidacionComentario(
            validacion=validacion[0],
            usuario=self.request.user,
            comentario=comentario)
        comentario_validacion.save()
        return self.render_json_response({
            "comentario": comentario_validacion.comentario,
            "fecha": str(comentario_validacion.fecha),
            "usuario": str(comentario_validacion.usuario.perfil)
        })


class ValidacionDetailView(EscuelaDetail):

    def get_context_data(self, **kwargs):
        id_validacion = self.kwargs.pop('id_validacion')
        context = super(ValidacionDetailView, self).get_context_data(**kwargs)
        context['validacion_detail'] = id_validacion
        return context


class SolicitudListView(LoginRequiredMixin, FormView):
    form_class = mye_f.SolicitudListForm
    template_name = 'mye/solicitud_list.html'


class ValidacionListView(LoginRequiredMixin, FormView):
    form_class = mye_f.ValidacionListForm
    template_name = 'mye/validacion_list.html'
