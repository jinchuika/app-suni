from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import UpdateView, ListView
from django.core.urlresolvers import reverse_lazy
from apps.users.forms import *
from apps.users.mixins import PublicPerfilMixin
from braces.views import LoginRequiredMixin
from allauth.account.views import LoginView
from dynamic_preferences.forms import user_preference_form_builder
from dynamic_preferences.views import UserPreferenceFormView

def index(request):
    return HttpResponse('hola users')


class UserLogin(LoginView):
    template_name = 'users/login.html'


# Para redirigir al usuario actual a su perfil
def current_profile_redirect(request):
    return redirect('perfil_detail', pk=request.user.perfil.id) 


class PerfilList(LoginRequiredMixin, PublicPerfilMixin, ListView):
    template_name = 'users/list.html'


class PerfilUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'users/perfil.html'
    form_class = PerfilForm
    model = Perfil

    def get_context_data(self, **kwargs):
        context = super(PerfilUpdate, self).get_context_data(**kwargs)
        context['preferencias_form'] = user_preference_form_builder(instance=self.object.user)
        return context


class PerfilPreferenciasUpdate(UserPreferenceFormView):
    success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        return redirect('profile')
