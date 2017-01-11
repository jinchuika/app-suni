from django.shortcuts import redirect
from django.views.generic import UpdateView, ListView, RedirectView
from django.core.urlresolvers import reverse_lazy
from apps.users.forms import *
from apps.users.mixins import PublicPerfilMixin
from braces.views import LoginRequiredMixin
from allauth.account.views import LoginView
from dynamic_preferences.forms import user_preference_form_builder
from dynamic_preferences.views import UserPreferenceFormView


class UserLogin(LoginView):
    template_name = 'users/login.html'


class PerfilList(LoginRequiredMixin, PublicPerfilMixin, ListView):
    template_name = 'users/list.html'


class CurrentPerfilDetail(LoginRequiredMixin, RedirectView):
    pattern_name = 'perfil_detail'

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('perfil_detail', kwargs={'pk': self.request.user.perfil.id})


class PerfilUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'users/perfil.html'
    form_class = PerfilForm
    model = Perfil

    def get_context_data(self, **kwargs):
        context = super(PerfilUpdate, self).get_context_data(**kwargs)
        context['preferencias_form'] = user_preference_form_builder(instance=self.object.user)
        return context


class PerfilPreferenciasUpdate(UserPreferenceFormView):
    success_url = reverse_lazy('perfil')

    def get(self, request, *args, **kwargs):
        return redirect('perfil')
