import factory
from apps.main import models as main_models
from apps.escuela import models


class EscAreaFactory(factory.django.DjangoModelFactory):
    """Fábrica para :class:'EscArea'"""
    class Meta:
        model = models.EscArea

    area = factory.Sequence(lambda n: "Área %03d" % n)


class EscJornadaFactory(factory.django.DjangoModelFactory):
    """Fábrica para :class:'EscJornada'"""
    class Meta:
        model = models.EscJornada

    jornada = factory.Sequence(lambda n: "Jornada %03d" % n)


class EscModalidadFactory(factory.django.DjangoModelFactory):
    """Fábrica para :class:'EscModalidad'"""
    class Meta:
        model = models.EscModalidad

    modalidad = factory.Sequence(lambda n: "Modalidad %03d" % n)


class EscNivelFactory(factory.django.DjangoModelFactory):
    """Fábrica para :class:'EscNivel'"""
    class Meta:
        model = models.EscNivel

    nivel = factory.Sequence(lambda n: "Nivel %03d" % n)


class EscPlanFactory(factory.django.DjangoModelFactory):
    """Fábrica para :class:'EscPlan'"""
    class Meta:
        model = models.EscPlan

    plan = factory.Sequence(lambda n: "Plan %03d" % n)


class EscSectorFactory(factory.django.DjangoModelFactory):
    """Fábrica para :class:'EscSector'"""
    class Meta:
        model = models.EscSector

    sector = factory.Sequence(lambda n: "Sector %03d" % n)


class EscStatusFactory(factory.django.DjangoModelFactory):
    """Fábrica para :class:'EscStatus'"""
    class Meta:
        model = models.EscStatus

    status = factory.Sequence(lambda n: "Status %03d" % n)


class EscuelaFactory(factory.django.DjangoModelFactory):
    """Fábrica para :class:'Escuela'"""
    class Meta:
        model = models.Escuela

    codigo = factory.Sequence(lambda n: '01-01-0000-{0}'.format(n))
    municipio = factory.Iterator(main_models.Municipio.objects.all())
    nombre = factory.Sequence(lambda n: 'Escuela {0}'.format(n))
    direccion = factory.Faker('address')
    nivel = factory.SubFactory(EscNivelFactory)
    sector = factory.SubFactory(EscSectorFactory)
    area = factory.SubFactory(EscAreaFactory)
    status = factory.SubFactory(EscStatusFactory)
    modalidad = factory.SubFactory(EscModalidadFactory)
    jornada = factory.SubFactory(EscJornadaFactory)
    plan = factory.SubFactory(EscPlanFactory)
