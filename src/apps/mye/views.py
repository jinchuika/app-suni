from django.shortcuts import reverse

from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, UpdateView, FormView

from django.http import JsonResponse
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, CsrfExemptMixin, JsonRequestResponseMixin

from apps.mye import forms as mye_f
from apps.mye import models as mye_m

from apps.escuela.views import EscuelaDetail


class CooperanteCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Vista   para obtener los datos del cooperante mediante
       una :class:`Cooperante` Funciona  para recibir los datos
       de un  'CooperanteForm' mediante el metodo  POST.  y
       nos muestra el template de cooperante mediante el metodo GET.

    """
    model = mye_m.Cooperante
    template_name = 'mye/cooperante_form.html'
    form_class = mye_f.CooperanteForm
    permission_required = 'mye.add_cooperante'
    raise_exception = True


class CooperanteDetalle(LoginRequiredMixin, DetailView):
    """Esta vista es la encargada de  mostrar los detalles de :class:`Cooperante`
       y nos muestra el template
       de cooperante mediate el metodo GET.

    """
    model = mye_m.Cooperante
    template_name = 'mye/cooperante.html'


class CooperanteUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Vista encargada de  Actualizar la informacion de un Cooperante  mediante una
       :class:`Cooperante`. Funciona  para Actualizar los Datos  de un,
       'CooperanteForm' mediante el metodo POST  ye nos muestra el template de
        cooperante_form  mediante el  metodo GET.

    """
    model = mye_m.Cooperante
    template_name = 'mye/cooperante_form.html'
    form_class = mye_f.CooperanteForm
    permission_required = 'mye.change_cooperante'
    raise_exception = True


class CooperanteList(LoginRequiredMixin, FormView):
    """Vista encargada de mostrar la lista de la :class:`Cooperantes` , mediante el metodo GET nos muestrar
    el template de cooperante_list.

    """
    model = mye_m.Cooperante
    template_name = 'mye/cooperante_list.html'
    form_class = mye_f.CPFilterForm


class ProyectoCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Vista para obtener los datos del cooperante mediante un :class:`Proyecto`
    Funciona solo para recibir  los datos de un 'ProyectoForm' mediante el
    metodo POST,por medio del metodo GET nos  muestra el template de  proyecto .

    """
    model = mye_m.Proyecto
    template_name = 'mye/proyecto_form.html'
    form_class = mye_f.ProyectoForm
    permission_required = 'mye.add_proyecto'
    raise_exception = True


class ProyectoDetalle(LoginRequiredMixin, DetailView):
    """Vista encargada  de  mostrar los detalles de :class:`Proyecto` , por medio del metodo GET
    nos muestra el template de proyecto.

    """
    model = mye_m.Proyecto
    template_name = 'mye/proyecto.html'


class ProyectoUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Vista Encargada de Actualizar los datos de  proyecto mediante una :class:`Proyecto`
    Funciona solo para recibr los datos de un ''ProyectoForm' mediante el metodo POST, por Medio
    del metodo GET nos muestra el template de proyecto_form.

    """
    model = mye_m.Proyecto
    template_name = 'mye/proyecto_form.html'
    form_class = mye_f.ProyectoForm
    permission_required = 'mye.change_proyecto'
    raise_exception = True


class ProyectoList(LoginRequiredMixin, FormView):
    """Vista encarga de gestionar el listado de :class:`Proyecto`,obteniendo los datos necesarios
    por medio del metodo GET nos muestra el template proyecto_list.

    """
    model = mye_m.Proyecto
    form_class = mye_f.PYFilterForm
    template_name = 'mye/proyecto_list.html'


class SolicitudVersionCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Vista  para obtener los datos de la Solicitud mediante  una :class:`SolicitudVersion`
    Funciona solo para recibir los datos de un 'SolicitudVersionForm' mediante el metodo POST,
    el metodo GET nos muestra el template solicitud_version_form.

    """
    model = mye_m.SolicitudVersion
    template_name = 'mye/solicitud_version_form.html'
    form_class = mye_f.SolicitudVersionForm
    permission_required = 'mye.add_solicitud_version'
    redirect_unauthenticated_users = True
    raise_exception = True


class SolicitudVersionDetalle(LoginRequiredMixin, DetailView):
    """Vista Encargada de mostrar los detalles de :class:`SolicitudVersion`
    por  medio del metodo GET nos muestra el template solicitud_version.

    """
    model = mye_m.SolicitudVersion
    template_name = 'mye/solicitud_version.html'


class SolicitudCrearView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    TODO:
            refactorizar  esta vista
    """
    model = mye_m.Solicitud
    form_class = mye_f.SolicitudNuevaForm
    permission_required = 'mye.add_solicitud'
    raise_exception = True

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


class SolicitudUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Vista Encargada de Actualizar una :class:`Solicitud`, Solo funciona Para
    recibir un 'SolicitudForm' mediante POST y actualiza los datos , mediate el metodo GET
    nos muestra el template solicitud_form.

    """
    model = mye_m.Solicitud
    form_class = mye_f.SolicitudForm
    template_name = 'mye/solicitud_form.html'
    permission_required = 'mye.change_solicitud'
    raise_exception = True

    def get_success_url(self):
        return reverse('escuela_detail', kwargs={'pk': self.object.escuela.id})


class SolicitudComentarioCrear(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """ Vista encargada de  crear  el Historia  de Solicitudes
    """
    require_json = True

    def post(self, request, *args, **kwargs):
        try:
            id_comentario = self.request_json["id_solicitud"]
            solicitud = mye_m.Solicitud.objects.filter(id=id_comentario)
            comentario = self.request_json["comentario"]
            if not len(comentario) or len(solicitud) == 0:
                raise KeyError
        except KeyError:
            error_dict = {u"Sin Comentarios en Solicitud"}
            return self.render_bad_request_response(error_dict)
        comentario_solicitud = mye_m.SolicitudComentario(
            solicitud=solicitud[0],
            usuario=self.request.user,
            comentario=comentario
        )
        comentario_solicitud.save()
        return self.render_json_response({
            "comentario": comentario_solicitud.comentario,
            "fecha": str(comentario_solicitud.fecha),
            "usuario": str(comentario_solicitud.usuario.perfil)
        })


class ValidacionCrearView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = mye_m.Validacion
    form_class = mye_f.ValidacionNuevaForm
    permission_required = 'mye.add_validacion'
    raise_exception = True

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


class ValidacionUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """"Vista Encargada de Actualizar un :class:`Validacion`, solo funciona Para
    recibir un 'ValidacionForm', mediante el  metodo POST y actualiza los datos,
    mediante el metodo GET nos muestra el template solicitud_form.

    """
    model = mye_m.Validacion
    form_class = mye_f.ValidacionForm
    template_name = 'mye/solicitud_form.html'
    permission_required = 'mye.change_validacion'
    raise_exception = True

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
    """Vista Encargada de  mostrar el listado de :class:`Solicitud`, obteniendo los datos necesarios , mediante
    el metodo GET nos muestra el template de solicitud_list.

    """
    form_class = mye_f.SolicitudListForm
    template_name = 'mye/solicitud_list.html'


class ValidacionListView(LoginRequiredMixin, FormView):
    """Vista Encargada de mostrar el listado de :class:`Validacion`, obteniendo los datos necesarios, mediante
    el metodo GET nos muestra el  template validacion_list.

    """
    form_class = mye_f.ValidacionListForm
    template_name = 'mye/validacion_list.html'
