#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Este archivo contiene transacciones generales para utilizar en los distintos inventarios
# el propósito principal de tener las transacciones separadas es poder garantizar que sean realizadas
# de forma atómica.
from django.db import transaction

from apps.conta import models as conta_m


def ingresar_dispositivo(entrada, modelo, tipo, entrada_detalle, precio=None):   
    with transaction.atomic():
        periodo_actual = conta_m.PeriodoFiscal.objects.get(actual=True)
        if not precio or precio == 0.0:
            precio_estandar = conta_m.PrecioEstandar.objects.get(
                tipo_dispositivo=tipo,
                periodo=periodo_actual,
                inventario=conta_m.PrecioEstandar.DISPOSITIVO)
            precio = precio_estandar.precio
        nuevo_dispositivo = modelo(entrada=entrada, tipo=tipo, entrada_detalle=entrada_detalle,creada_por = entrada_detalle.creado_por)
        # Antes de ejecutar el save, se dispara la señal `calcular_triage`
        # Durante el `save` se genera el código QR
        nuevo_dispositivo.save() #este guarda los dispositivo
        # Generar registros contables
        nuevo_precio = conta_m.PrecioDispositivo(
            dispositivo=nuevo_dispositivo,
            periodo=periodo_actual,
            precio=precio,
            creado_por = entrada_detalle.creado_por)
        nuevo_precio.save()
        movimiento = conta_m.MovimientoDispositivo(
            dispositivo=nuevo_dispositivo,
            periodo_fiscal=periodo_actual,
            tipo_movimiento=conta_m.MovimientoDispositivo.ALTA,
            referencia='Entrada {}'.format(entrada),
            precio=precio,
            creado_por = entrada_detalle.creado_por)
        movimiento.save()
        


def ingresar_repuesto(entrada, modelo_repuesto, estado, tipo, entrada_detalle, precio=None):
    with transaction.atomic():
        periodo_actual = conta_m.PeriodoFiscal.objects.get(actual=True)
        if not precio or precio == 0.0:
            precio_estandar = conta_m.PrecioEstandar.objects.get(
                tipo_dispositivo=tipo,
                periodo=periodo_actual,
                inventario=conta_m.PrecioEstandar.REPUESTO)
            precio = precio_estandar.precio
        nuevo_repuesto = modelo_repuesto(
            entrada=entrada,
            tipo=tipo,
            entrada_detalle=entrada_detalle,
            disponible=True,
            estado=estado,
            creada_por = entrada_detalle.creado_por
        )
        nuevo_repuesto.save()
        nuevo_precio = conta_m.PrecioRepuesto(
            repuesto=nuevo_repuesto,
            precio=precio,
            periodo=periodo_actual,
            creado_por = entrada_detalle.creado_por
        )
        nuevo_precio.save()
        # Crear el registro del movimiento
        movimiento = conta_m.MovimientoRepuesto(
            repuesto=nuevo_repuesto,
            precio=precio,
            periodo_fiscal=periodo_actual,
            tipo_movimiento=conta_m.MovimientoRepuesto.ALTA,
            referencia='Entrada {}'.format(entrada),
            creado_por = entrada_detalle.creado_por
        )
        movimiento.save()
