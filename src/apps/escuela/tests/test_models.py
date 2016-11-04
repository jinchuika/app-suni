import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestEscuela:
    def test_model(self):
        obj = mixer.blend('escuela.Escuela')
        assert obj.pk == 1, "Debe crear una escuela"
