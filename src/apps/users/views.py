from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View, UpdateView, DetailView, ListView, TemplateView, RedirectView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from .mixins import PublicPerfilMixin, CurrentUserMixin
from braces.views import LoginRequiredMixin
from allauth.account.views import SignupView, LoginView
from dynamic_preferences.forms import user_preference_form_builder, UserPreferenceForm
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

# Para editar las preferencias desde el perfil
class PerfilPreferenciasUpdate(UserPreferenceFormView):
	success_url = reverse_lazy('profile')

	def get(self, request, *args, **kwargs):
		return redirect('profile')