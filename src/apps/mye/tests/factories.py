import factory
from apps.mye import models
from django.utils import timezone


class CooperanteFactory(factory.django.DjangoModelFactory):
    """Fábrica para crear cooperantes"""
    class Meta:
        model = models.Cooperante

    nombre = factory.Sequence(lambda n: "Cooperante %03d" % n)


class ProyectoFactory(factory.django.DjangoModelFactory):
    """Fábrica para crear proyecto"""
    class Meta:
        model = models.Proyecto

    nombre = factory.Sequence(lambda n: "Proyecto %03d" % n)


class RequisitoFactory(factory.django.DjangoModelFactory):
    """Fábrica para Requisitos"""
    class Meta:
        model = models.Requisito

    nombre = factory.Sequence(lambda n: "Requisito %03d" % n)


class MedioFactory(factory.django.DjangoModelFactory):
    """Fábrica para Medios"""
    class Meta:
        model = models.Medio

    medio = factory.Sequence(lambda n: "Medio %03d" % n)


class SolicitudVersionFactory(factory.django.DjangoModelFactory):
    """Fábrica para SolicitudVersions"""
    class Meta:
        model = models.SolicitudVersion

    nombre = factory.Sequence(lambda n: "Versión %03d" % n)

    @factory.post_generation
    def requisito(self, create, nuevos, **kwargs):
        if not create:
            return
        if nuevos:
            for req in nuevos:
                self.requisito.add(req)


class SolicitudFactory(factory.django.DjangoModelFactory):
    """Fábrica para :class:'Solicitud'"""
    class Meta():
        model = models.Solicitud
    fecha = factory.LazyFunction(timezone.now)

    @factory.post_generation
    def requisito(self, create, nuevos, **kwargs):
        if not create:
            return
        if nuevos:
            for req in nuevos:
                self.requisito.add(req)

    @factory.post_generation
    def medio(self, create, nuevos, **kwargs):
        if not create:
            return
        if nuevos:
            for req in nuevos:
                self.medio.add(req)
