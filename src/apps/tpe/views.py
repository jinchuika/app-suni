from django.shortcuts import reverse
from django.views.generic.edit import CreateView, UpdateView
from apps.tpe.models import Equipamiento
from apps.tpe.forms import EquipamientoNuevoForm, EquipamientoForm


class EquipamientoCrearView(CreateView):
    model = Equipamiento
    form_class = EquipamientoNuevoForm

    def get_success_url(self):
        return reverse('escuela_equipamiento_update', kwargs={'pk': self.object.escuela.id, 'id_equipamiento': self.object.id})


class EquipamientoUpdateView(UpdateView):
    model = Equipamiento
    form_class = EquipamientoForm

    def get_success_url(self):
        return reverse('escuela_detail', kwargs={'pk': self.object.escuela.id})
