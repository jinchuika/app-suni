from django.db import IntegrityError
from django.db.models.signals import pre_save, post_save
from datetime import datetime

from apps.inventario import models as inventario_m


# Para dispositivos

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
        try:
            instance.triage = '{}-{}'.format(instance.tipo.slug, instance.indice)
        except IntegrityError:
            instance.triage = '{}-{}'.format(instance.tipo.slug, instance.indice + 1)


for dispositivo in inventario_m.Dispositivo.__subclasses__():
    pre_save.connect(calcular_triage, sender=dispositivo)


# Para entradas

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


# Para salidas

def calcular_salida(sender, instance, **kwargs):
    """Se encarga de calcular número de salida para los :class:`Salida`.
    El número sigue un correlativo de acuerdo del tipo de salida y si es una entra o no.
    """
    if not instance.pk:
        indice = 0
        tipo_salida = instance.tipo_salida
        if instance.tipo_salida.equipamiento or (instance.tipo_salida.especial and instance.entrega):
            tipo_salida = inventario_m.SalidaTipo.objects.get(equipamiento=True)
            entregas = inventario_m.SalidaInventario.objects.filter(entrega=True, tipo_salida__renovacion=False)
        elif instance.tipo_salida.especial and not instance.entrega:
            entregas = inventario_m.SalidaInventario.objects.filter(tipo_salida=instance.tipo_salida, entrega=False).exclude(no_salida__contains='GN')
        else:
            entregas = inventario_m.SalidaInventario.objects.filter(tipo_salida=instance.tipo_salida)

        if len(entregas) != 0:
            ultimo = entregas.only('id').latest('id')
            print(ultimo)
            indice = int(ultimo.no_salida.split('-')[1])
            print(indice)
        instance.no_salida = '{}-{}'.format(tipo_salida.slug, indice + 1)
        print(instance.no_salida)

pre_save.connect(calcular_salida, sender=inventario_m.SalidaInventario)

# def calcular_indice_paquete(sender, instance, **kwargs):
#     if not instance.pk:
#         if sender.objects.all().count() == 0:
#             instance.indice = 1
#         else:
#             ultimo = sender.objects.only('indice').latest('indice')
#             instance.indice = ultimo.indice + 1


# pre_save.connect(calcular_indice_paquete, sender=inventario_m.Paquete)
def crear_bitacora(sender, instance, created, **kwargs):
    """ Se encarga de crear los registros de la :class:`SolicitudBitacora`
    """
    if created:
        nueva_bitacora = inventario_m.SolicitudBitacora(
            fecha_movimiento=datetime.now(),
            numero_solicitud=inventario_m.SolicitudMovimiento.objects.get(id=instance.id),
            accion=inventario_m.AccionBitacora.objects.get(id=1),
            usuario=instance.creada_por
        )
        nueva_bitacora.save()
    else:
        if instance.rechazar is  False:
            if instance.recibida is False:
                nueva_bitacora = inventario_m.SolicitudBitacora(
                    fecha_movimiento=datetime.now(),
                    numero_solicitud=inventario_m.SolicitudMovimiento.objects.get(id=instance.id),
                    accion=inventario_m.AccionBitacora.objects.get(id=2),
                    usuario=instance.creada_por
                )
                nueva_bitacora.save()




post_save.connect(crear_bitacora, sender=inventario_m.SolicitudMovimiento)
