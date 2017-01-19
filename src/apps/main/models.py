from django.db import models


class Departamento(models.Model):
    """
    Description: Departamento de Guatemala
    """
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre


class Municipio(models.Model):
    """
    Description: Municipio de Guatemala
    """
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre + " (" + str(self.departamento) + ")"


class Coordenada(models.Model):
    lat = models.CharField(max_length=25)
    lng = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=70, null=True, blank=True)

    def __str__(self):
        if self.descripcion:
            return self.descripcion
        else:
            return self.lat + ", " + self.lng
