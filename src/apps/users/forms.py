from django import forms
from apps.users.models import *
from django.forms import ModelForm, ModelChoiceField, formset_factory, modelformset_factory
from django.contrib.auth.forms import authenticate
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
	username = forms.CharField(max_length=255, required=True)
	password = forms.CharField(widget=forms.PasswordInput, required=True)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if not user or not user.is_active:
			raise forms.ValidationError('No se encuentran datos que coincidan')
		return self.cleaned_data

	def login(self, request):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		return user


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Nombre')
    last_name = forms.CharField(max_length=30, label='Apellido')
    groups = forms.ModelMultipleChoiceField(
    	widget=forms.CheckboxSelectMultiple,
    	queryset=Group.objects.all()
    	)
    public = forms.BooleanField()
    foto = forms.ImageField(required=False, widget=forms.FileInput(), label='Foto')

    def signup(self, request, user):
        new_user = Perfil(
            user=user,
            public=self.cleaned_data['public'],
            foto=self.cleaned_data['foto'],
        )
        for g in self.cleaned_data['groups']:
        	user.groups.add(g)
        user.save()
        new_user.save()

class CustomSignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Nombre')
    last_name = forms.CharField(max_length=30, label='Apellido')
    groups = forms.ModelMultipleChoiceField(
    	widget=forms.CheckboxSelectMultiple,
    	queryset=Group.objects.all()
    	)
    public = forms.BooleanField()
    foto = forms.ImageField(required=False, widget=forms.FileInput(), label='Foto')

    def signup(self, request, user):
        new_user = Perfil(
            user=user,
            public=self.cleaned_data['public'],
            foto=self.cleaned_data['foto'],
        )
        for g in self.cleaned_data['groups']:
        	user.groups.add(g)
        user.save()
        new_user.save()

class PerfilForm(forms.ModelForm):
	class Meta:
		model = Perfil
		fields = ['dpi', 'genero', 'fecha_nacimiento', 'direccion', 'foto']