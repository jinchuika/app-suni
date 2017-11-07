from django.urls import reverse
from django.core.management import call_command
from django.test import Client, TestCase

from apps.main.tests.mixins import PermissionTest
from apps.escuela.tests import factories


class EscuelaCrearTest(PermissionTest, TestCase):
    """Test para la vista de creación de escuelas"""
    view_url = 'escuela_crear'
    permissions = ['escuela.add_escuela']

    def setUp(self):
        call_command('loaddata', 'src/fix/test_data.json', verbosity=0)
        self.client = Client()

    def test_crea(self):
        escuela = factories.EscuelaFactory()
        self.client.get(reverse(self.view_url))
        self.client.form['codigo'] = escuela.codigo
        self.client.form['municipio'] = escuela.municipio
        self.client.form['nombre'] = escuela.nombre
        self.client.form['direccion'] = escuela.direccion
        self.client.form['nivel'] = escuela.nivel
        self.client.form['sector'] = escuela.sector
        self.client.form['area'] = escuela.area
        self.client.form['status'] = escuela.status
        self.client.form['modalidad'] = escuela.modalidad
        self.client.form['jornada'] = escuela.jornada
        self.client.form['plan'] = escuela.plan
        page = self.client.form.submit()
        self.assertRedirects(page, escuela.get_absolute_url())
