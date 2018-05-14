from django.db.models.signals import pre_save, post_save

from apps.inventario import models as inventario_m


def calcular_triage(sender, instance, **kwargs):
    """Se encarga de calcular el triage para los :class:`Dispositivo`.
    El triage sigue el formato SLUG-indice de cada modelo. Por ejemplo,
    el Monitor con `indice` 854 tiene un triage `M-854`.
    """
    if not instance.pk:
        if sender.objects.all().count() == 0:
            instance.indice = 1
        else:
            ultimo = sender.objects.only('indice').latest('indice')
            instance.indice = ultimo.indice + 1
        instance.triage = '{}-{}'.format(instance.tipo.slug, instance.indice)


for dispositivo in inventario_m.Dispositivo.__subclasses__():
    pre_save.connect(calcular_triage, sender=dispositivo)


def calcular_precio_unitario(sender, instance, **kwargs):
    """Calcula el `precio_unitario` para los :class:`EntradaDetalle` que tienen `precio_subtotal`.
    """
    if instance.precio_subtotal:
        instance.precio_unitario = instance.precio_subtotal / instance.total

        subtotal_entrada = instance.entrada.subtotal
        descontado_entrada = instance.entrada.descontado

        if not instance.pk:
            subtotal_entrada = subtotal_entrada + instance.precio_subtotal
            descontado_entrada = descontado_entrada + instance.precio_subtotal

        porcentaje_descuento = descontado_entrada / subtotal_entrada
        if porcentaje_descuento == 0:
            instance.precio_descontado = instance.precio_unitario
            instance.precio_total = instance.precio_subtotal
        else:
            instance.precio_descontado = porcentaje_descuento * instance.precio_unitario
            instance.precio_total = instance.precio_descontado * instance.total


pre_save.connect(calcular_precio_unitario, sender=inventario_m.EntradaDetalle)


def calcular_precio_descontado(sender, instance, **kwargs):
    """Actualiza el `precio_unitario` de todos los :class:`EntradaDetalle` despues de agregar un
    :class:`DescuentoEntrada` a la :class:`Entrada`.
    """
    for detalle in instance.entrada.detalles.all():
        detalle.save()


post_save.connect(calcular_precio_descontado, sender=inventario_m.DescuentoEntrada)


# def calcular_indice_paquete(sender, instance, **kwargs):
#     if not instance.pk:
#         if sender.objects.all().count() == 0:
#             instance.indice = 1
#         else:
#             ultimo = sender.objects.only('indice').latest('indice')
#             instance.indice = ultimo.indice + 1


# pre_save.connect(calcular_indice_paquete, sender=inventario_m.Paquete)
