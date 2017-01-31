from django import forms
from apps.users.models import *
from django.contrib.auth.forms import authenticate
from django.contrib.auth.models import Group


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


class PerfilCrearForm(forms.ModelForm):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    first_name = forms.CharField(label='Nombre', max_length=30)
    last_name = forms.CharField(label='Apellido', max_length=30)
    email = forms.EmailField(label='Correo electrónico', max_length=150)

    class Meta:
        model = Perfil
        fields = ['dpi', 'genero', 'fecha_nacimiento', 'direccion']


class PerfilForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombre', max_length=30)
    last_name = forms.CharField(label='Apellido', max_length=30)
    fecha_nacimiento = forms.CharField(widget=forms.TextInput(attrs={'class': 'datepicker'}))

    def __init__(self, *args, **kw):
        super(PerfilForm, self).__init__(*args, **kw)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

        self.fields.keyOrder = [
            'first_name',
            'last_name', ]

    def save(self, *args, **kwargs):
        obj = super(PerfilForm, self).save(*args, **kwargs)
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.save()
        return obj

    class Meta:
        model = Perfil
        fields = ['dpi', 'genero', 'fecha_nacimiento', 'direccion', 'foto']
