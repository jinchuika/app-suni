from django.db import IntegrityError
from django.db.models.signals import pre_save, post_save
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User
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
        if instance.tipo_salida.equipamiento:
            tipo_salida = inventario_m.SalidaTipo.objects.get(equipamiento=True)
            entregas = inventario_m.SalidaInventario.objects.filter(entrega=True, tipo_salida__renovacion=False)
        elif instance.tipo_salida.especial:
            entregas = inventario_m.SalidaInventario.objects.filter(tipo_salida=instance.tipo_salida, entrega=False).exclude(no_salida__contains='GN')
        else:
            entregas = inventario_m.SalidaInventario.objects.filter(tipo_salida=instance.tipo_salida)

        if len(entregas) != 0:
            ultimo = entregas.only('id').latest('id')            
            indice = int(ultimo.no_salida.split('-')[1])            
        instance.no_salida = '{}-{}'.format(tipo_salida.slug, indice + 1)
       

pre_save.connect(calcular_salida, sender=inventario_m.SalidaInventario)

# def calcular_indice_paquete(sender, instance, **kwargs):
#     if not instance.pk:
#         if sender.objects.all().count() == 0:
#             instance.indice = 1
#         else:
#             ultimo = sender.objects.only('indice').latest('indice')
#             instance.indice = ultimo.indice + 1


# pre_save.connect(calcular_indice_paquete, sender=inventario_m.Paquete)

# Asignaciones de inventario
def calcular_inventario_interno(sender, instance, **kwargs):
    """ Se encarga de calcular el número de asignación para los registros de la :class: 'InventarioInterno'.
    El número sigue un correlativo de acuerdo al número de registro ingresado.
    """
    print('Inventario calcular_inventario_interno')
    if not instance.pk:
        indice = 0
        asignaciones = inventario_m.InventarioInterno.objects.all()
        if len(asignaciones) != 0:
            ultimo = asignaciones.only('id').latest('id')
            indice = int(ultimo.no_asignacion.split('-')[1])
        instance.no_asignacion = '{}-{}'.format('A', indice + 1)

pre_save.connect(calcular_inventario_interno, sender=inventario_m.InventarioInterno)

def crear_bitacora(sender, instance, created, **kwargs):
    """ Se encarga de crear los registros de la :class:`SolicitudBitacora`
    """
    if created:
        # Agregar a Bitácora nuevo registro
        nueva_bitacora = inventario_m.SolicitudBitacora(
            fecha_movimiento=datetime.now(),
            numero_solicitud=inventario_m.SolicitudMovimiento.objects.get(id=instance.id),
            accion=inventario_m.AccionBitacora.objects.get(id=1),
            usuario=instance.creada_por
        )
        nueva_bitacora.save()

        # Armar mensaje a enviar por correo electrónico
        usuario = User.objects.get(username=instance.creada_por)
        usuario_completo = str(usuario.first_name) +" "+ str(usuario.last_name)
        devolucion = False
        desecho = False

        if instance.devolucion:
            devolucion = True
            if instance.desecho:
                desecho = True

        html_message = loader.render_to_string(
            'inventario/email/email_solicitud.html',
            {
                'solicitud_id': str(instance.id),
                'fecha_movimiento': str(datetime.now()),
                'tipo_equipo': str(instance.tipo_dispositivo),
                'cantidad': str(instance.cantidad),
                'observaciones': instance.observaciones,
                'devolucion': str(devolucion),
                'desecho': str(desecho),
                'estado': 'Creada',
                'usuario': usuario_completo,
                'url': "https://suni.funsepa.org" + str(instance.get_absolute_url()),
            })

        usuarios_bodega = User.objects.filter(groups=21)
        lista_enviar_correos=[]
        for lista_correos  in usuarios_bodega:            
            lista_enviar_correos.append(lista_correos.email)

        motivo = "SUNI - Solicitud Creada: "+ str(instance.id)
        # Enviar Correo
        """send_mail(
            motivo,
            'mensaje',
            settings.EMAIL_HOST_USER,
            lista_enviar_correos,
            fail_silently=True,
            html_message = html_message
        )"""

    else:
        if instance.rechazar is  False:
            if instance.recibida is False:
                # Agregar a Bitácora el nuevo registro
                nueva_bitacora = inventario_m.SolicitudBitacora(
                    fecha_movimiento=datetime.now(),
                    numero_solicitud=inventario_m.SolicitudMovimiento.objects.get(id=instance.id),
                    accion=inventario_m.AccionBitacora.objects.get(id=2),
                    usuario=instance.creada_por
                )
                nueva_bitacora.save()

                # Armar información del correo

                # Obtener lista de Destinatarios
                lista_enviar_correos=[]
                usuario_completo = ''
                if instance.devolucion:
                    usuario = User.objects.get(username=instance.creada_por)
                    usuario_completo = str(usuario.first_name) +" "+ str(usuario.last_name)
                    usuarios_bodega = User.objects.filter(groups=21)
                    for lista_correos  in usuarios_bodega:            
                        lista_enviar_correos.append(lista_correos.email)
                else:
                    usuario = User.objects.get(username=instance.autorizada_por)
                    usuario_completo = str(usuario.first_name) +" "+ str(usuario.last_name)
                    lista_enviar_correos.append(instance.creada_por.email)
              
                dispositivos = inventario_m.CambioEtapa.objects.filter(solicitud=instance.id)
                lista_dispositivos=[]
                for nuevo_dipositivo in dispositivos:
                    lista_dispositivos.append(nuevo_dipositivo.dispositivo.triage)

                html_message = loader.render_to_string(
                    'inventario/email/email_solicitud.html',
                    {
                    'solicitud_id': str(instance.id),
                    'fecha_movimiento': str(datetime.now()),
                    'tipo_equipo': str(instance.tipo_dispositivo),
                    'dispositivos': lista_dispositivos,
                    'estado': 'Entregada',
                    'usuario': usuario_completo,
                    'url': "https://suni.funsepa.org" + str(instance.get_absolute_url()),
                    })

                motivo = "SUNI - Dispositivos Entregados: "+ str(instance.id)
                # Enviar Correo
                """send_mail(
                    motivo,
                    'mensaje',
                    settings.EMAIL_HOST_USER,
                    lista_enviar_correos,
                    fail_silently=True,
                    html_message = html_message
                )"""

post_save.connect(crear_bitacora, sender=inventario_m.SolicitudMovimiento)
