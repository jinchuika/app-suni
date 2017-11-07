from django.test import TestCase
from apps.mye.tests import factories


class CooperanteProyectoTestCase(TestCase):
    def setUp(self):
        self.codisa = factories.CooperanteFactory(nombre="CODISA")
        self.combo = factories.ProyectoFactory(nombre="Combo")


class SolicitudVersionTestCase(TestCase):
    def setUp(self):
        self.req1 = factories.RequisitoFactory()
        self.req2 = factories.RequisitoFactory()
        self.req3 = factories.RequisitoFactory()

        self.medio = factories.MedioFactory()

    def test_crea_version(self):
        """Prueba que se puedan crear Proyectos.
        """
        self.version1 = factories.SolicitudVersionFactory.create(
            requisito=(self.req1, self.req2))
        self.assertEqual(self.version1.requisito.count(), 2)

        self.version2 = factories.SolicitudVersionFactory.create(
            requisito=(self.req3,))
        self.assertEqual(self.version2.requisito.count(), 1)

    def test_crea_solicitud(self):
        solicitud = factories.SolicitudFactory(
            requisito=(self.req1),
            medio=self.medio)
        self.assertEqual(solicitud.requisito.count(), 1)
