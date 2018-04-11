# from django.shortcuts import render
from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin, GroupRequiredMixin,
    CsrfExemptMixin, JsonRequestResponseMixin)
from django.views.generic import DetailView, ListView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView


class DonanteListView(LoginRequiredMixin, TemplateView):
    template_name = 'tpe/equipamiento_list.html'
