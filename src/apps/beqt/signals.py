from django.db import IntegrityError
from django.db.models.signals import pre_save, post_save
from datetime import datetime
from django.contrib.auth.models import User
from apps.beqt import models as beqt_m
from apps.inventario import models as inventario_m
from django.conf import settings
from django.template import loader

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


for dispositivo in beqt_m.DispositivoBeqt.__subclasses__():
    pre_save.connect(calcular_triage, sender=dispositivo)



def calcular_precio_unitario_beqt(sender, instance, **kwargs):
    """Calcula el `precio_unitario` para los :class:`EntradaDetalle` que tienen `precio_subtotal`.
    """  
    instance.precio_unitario = 1
    instance.precio_total = instance.total  * 1
pre_save.connect(calcular_precio_unitario_beqt, sender=beqt_m.EntradaDetalleBeqt)


# Para salidas de beqt

def calcular_salida(sender, instance, **kwargs):
    """Se encarga de calcular número de salida para los :class:`Salida`.
    El número sigue un correlativo de acuerdo del tipo de salida y si es una entra o no.
    """    
    if not instance.pk:    
        indice = 0
        tipo_salida = instance.tipo_salida
        if instance.tipo_salida.equipamiento:
            tipo_salida = beqt_m.SalidaTipoBeqt.objects.get(equipamiento=True)
            entregas = beqt_m.SalidaInventario.objects.filter(entrega=True, tipo_salida__renovacion=False)
        elif instance.tipo_salida.especial:
            entregas = beqt_m.SalidaInventario.objects.filter(tipo_salida=instance.tipo_salida, entrega=False).exclude(no_salida__contains='GN')
        else:
            entregas = beqt_m.SalidaInventario.objects.filter(tipo_salida=instance.tipo_salida)

        if len(entregas) != 0:
            ultimo = entregas.only('id').latest('id')            
            indice = int(ultimo.no_salida.split('-')[1])            
        instance.no_salida = '{}-{}'.format(tipo_salida.slug, indice + 1)
       

pre_save.connect(calcular_salida, sender=beqt_m.SalidaInventario)