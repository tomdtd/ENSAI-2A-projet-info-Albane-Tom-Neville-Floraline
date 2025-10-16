import pytest
from src.business_object.liste_cartes import ListeCartes

class TestListeCartes():
    def test_creation_liste_cartes_ok(self):
        # GIVEN
        liste_cartes = [pytest.as_coeur]

        # WHEN
        cartes = ListeCartes(liste_cartes)

        # THEN
        assert cartes.get_cartes() == [pytest.as_coeur]
