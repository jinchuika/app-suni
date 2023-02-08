from django.test import TestCase
from apps.beqt import models as beqt_m
# Create your tests here.

class DispositivosTestCase(TestCase):
    def setUp(self) -> None:
        beqt_m.Entrada.objects.create(
            tipo = 1,
            fecha = "2014-01-01",
            fecha_cierre = "2014-01-01",
            en_creacion = True,
            recibida_por = 49,
            proveedor =446,
            factura = 0,
            observaciones = "Equipo listo para su uso"

        )
