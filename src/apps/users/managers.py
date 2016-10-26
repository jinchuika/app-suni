from django.db import models


class TelefonoManager(models.Manager):

    def add_telefono(self, request, perfil, telefono):
        try:
            telefono = self.get(perfil=perfil, telefono__iexact=telefono)
        except self.model.DoesNotExist:
            telefono = self.create(perfil=perfil, telefono=telefono)
        return telefono

    def get_principal(self, perfil):
        try:
            return self.get(perfil=perfil, principal=True)
        except self.model.DoesNotExist:
            return None
