#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Este archivo contiene transacciones generales para utilizar en los distintos inventarios
# el propósito principal de tener las transacciones separadas es poder garantizar que sean realizadas
# de forma atómica.
from django.db import transaction

from apps.conta import models as conta_m


def ingresar_dispositivo(entrada, modelo, tipo, entrada_detalle, precio=None):    
    with transaction.atomic():        
        nuevo_dispositivo = modelo(entrada=entrada, tipo=tipo, entrada_detalle=entrada_detalle,creada_por = entrada_detalle.creado_por)
        # Antes de ejecutar el save, se dispara la señal `calcular_triage`
        # Durante el `save` se genera el código QR
        nuevo_dispositivo.save()
        # Generar registros contables       
        movimiento = conta_m.MovimientoDispositivoBeqt(
            dispositivo=nuevo_dispositivo,           
            tipo_movimiento=conta_m.MovimientoDispositivoBeqt.ALTA,
            referencia='Entrada {}'.format(entrada),
            precio=precio,
            creado_por = entrada_detalle.creado_por)
        movimiento.save()