from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View, UpdateView, DetailView, ListView, TemplateView, RedirectView
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from .mixins import PublicPerfilMixin, CurrentUserMixin
from braces.views import LoginRequiredMixin
from allauth.account.views import SignupView, LoginView
from django.core.urlresolvers import reverse_lazy

def index(request):
	return HttpResponse('hola users')

class UserLogin(LoginView):
    template_name = 'users/login.html'

class ProfileDetail(LoginRequiredMixin, DetailView):
	template_name = 'users/profile.html'
	model = Perfil

def current_profile_redirect(request):
	return redirect('perfil_detail', pk=request.user.perfil.id)	
		

class PerfilList(LoginRequiredMixin, PublicPerfilMixin, ListView):
	template_name = 'users/list.html'

class PerfilUpdate(LoginRequiredMixin, UpdateView):
	template_name = 'users/edit.html'
	form_class = PerfilForm
	success_url = reverse_lazy('profile')
	model = Perfil

	def get_context_data(self, **kwargs):
		context = super(PerfilUpdate, self).get_context_data(**kwargs)
		context['perfil'] = self.get_object()
		return context