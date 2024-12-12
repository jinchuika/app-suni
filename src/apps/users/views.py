from django.shortcuts import redirect
from django.views.generic import UpdateView, ListView, RedirectView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from braces.views import LoginRequiredMixin, GroupRequiredMixin
from allauth.account.views import LoginView
from dynamic_preferences.users.forms import user_preference_form_builder
from dynamic_preferences.users.views import UserPreferenceFormView

from apps.users.forms import *
from apps.users.mixins import PublicPerfilMixin

from rest_framework.authtoken.models import Token
import qrcode
import os
from django.conf import settings


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
        context['preferencias_form'] = user_preference_form_builder(instance=self.object.user, section='ui')

        if self.request.user.is_authenticated:
            try:
                user_token = Token.objects.get(user=self.request.user)
                token_valor = user_token.key
                context['token'] = user_token

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=3,
                )
                qr.add_data(token_valor)
                qr.make(fit=True)

                qr_dir = os.path.join(settings.MEDIA_ROOT, 'qr_tokens_perfil')
                os.makedirs(qr_dir, exist_ok=True)
                qr_path = os.path.join(qr_dir, str(self.request.user.id) + "_token.png")
                qr_img = qr.make_image(fill_color="black", back_color="white")
                qr_img.save(qr_path)

                qr_token_url = os.path.join(settings.MEDIA_URL, 'qr_tokens_perfil', str(self.request.user.id) + "_token.png")
                context['qr_code_url'] = qr_token_url

            except Token.DoesNotExist:
                user_token = None

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
