import pytest
from django.test import RequestFactory
from apps.escuela import views
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestEscuelaView:
    def test_abre(self):
        req = RequestFactory().get('/escuela/1')
        req.user = mixer.blend('auth.User', is_superuser=True)
        resp = views.EscuelaCrear.as_view()(req)
        assert resp.status_code == 200


class TestEscuelaDetail:
    def test_abre(self):
        req = RequestFactory().get('/escuela/1/')
        req.user = mixer.blend('auth.User', is_superuser=True)
        mixer.blend('escuela.Escuela', nombre='EORM')
        resp = views.EscuelaDetail.as_view()(req, pk=1)
        assert resp.status_code == 200, 'No se puede abrir el perfil de la escuela'

    def test_abre_solicitud(self):
        req = RequestFactory().get('/escuela/')

        req.user = mixer.blend('auth.User', is_superuser=True)
        eorm = mixer.blend('escuela.Escuela', nombre='EORM')
        mixer.blend('escuela.Escuela', nombre='EOUM')
        mixer.blend('mye.Solicitud', escuela=eorm)

        resp = views.EscuelaDetail.as_view()(req, pk=1, id_solicitud=1)
        assert 'solicitud_nueva_form' in resp.context_data

        resp = views.EscuelaDetail.as_view()(req, pk=2, id_solicitud=1)
        assert 'solicitud_nueva_form' not in resp.context_data, 'La solicitud debe ser de la escuela'
