from django.shortcuts import redirect
from django.views.generic import UpdateView, ListView, RedirectView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy

from braces.views import LoginRequiredMixin, GroupRequiredMixin
from allauth.account.views import LoginView
from dynamic_preferences.forms import user_preference_form_builder
from dynamic_preferences.views import UserPreferenceFormView

from apps.users.forms import *
from apps.users.mixins import PublicPerfilMixin


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


class PerfilCrear(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = [u"admin", ]
    redirect_unauthenticated_users = True
    raise_exception = True
    model = Perfil
    template_name = 'users/user_add.html'
    form_class = PerfilCrearForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'])
        self.object.user = user
        self.object.user.first_name = form.cleaned_data['first_name']
        self.object.user.last_name = form.cleaned_data['last_name']
        self.object.user.save()
        self.object.save()
        return super(PerfilCrear, self).form_valid(form)
