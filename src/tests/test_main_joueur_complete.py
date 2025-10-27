import pytest
from src.business_object.main_joueur_complete import MainJoueurComplete
from src.business_object.combinaison import Combinaison
import re

class TestMainJoueurComplete():
    def test_creation_main_joueur_complete_ok(self):
        # GIVEN
        liste_cartes = [pytest.as_coeur, pytest.as_pique, pytest.trois_pique, pytest.dix_carreau,
                        pytest.dame_carreau, pytest.cinq_coeur, pytest.quatre_trefle]

        # WHEN
        cartes = MainJoueurComplete(liste_cartes)

        # THEN
        assert cartes.get_cartes() == liste_cartes

    def test_creation_main_joueur_complete_echec(self):
        # GIVEN
        liste_cartes = [pytest.as_coeur, pytest.as_pique, pytest.trois_pique, pytest.dix_carreau,
                pytest.dame_carreau, pytest.cinq_coeur, pytest.quatre_trefle, pytest.valet_trefle]

        message_attendu = "La main complète doit contenir entre 2 et 7 cartes."

        # THEN
        with pytest.raises(ValueError, match=re.escape(message_attendu)):
            # WHEN
            MainJoueurComplete(liste_cartes)

    def test_combinaison_QuinteRoyale(self):
        # GIVEN
        liste_cartes =  [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.dix_coeur,
            pytest.deux_pique,
            pytest.trois_trefle
        ]

        # WHEN
        cartes = MainJoueurComplete(liste_cartes)

        # THEN
        assert cartes.combinaison() == Combinaison.QuinteRoyale
