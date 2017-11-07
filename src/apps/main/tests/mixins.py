from django.urls import reverse
from django.test import Client, TestCase
from apps.users.tests.factories import UserFactory


class PermissionTest(object):
    client = None
    view_url = None
    permissions = None

    def build_user_auth(self):
        return UserFactory(permissions=self.permissions)

    def build_user_unauth(self):
        return UserFactory()

    def test_permiso_falla(self):
        user = self.build_user_unauth()
        self.client.login(username=user.username, password='hola1234.')
        response = self.client.get(reverse(self.view_url))
        self.assertEqual(response.status_code, 403)

    def test_permiso_sirve(self):
        if self.permissions:
            user = self.build_user_auth()
            self.client.login(username=user.username, password='hola1234.')

            response = self.client.get(reverse('escuela_crear'))
            self.assertEqual(response.status_code, 200)
