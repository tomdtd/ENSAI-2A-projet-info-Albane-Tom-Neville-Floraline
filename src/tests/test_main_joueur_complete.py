import pytest
from src.business_object.main_joueur_complete import MainJoueurComplete
from src.business_object.combinaison import Combinaison
from src.business_object.carte import Carte
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

    def test_combinaison_CarteHaute(self):
        # GIVEN
        liste_cartes = [
            pytest.roi_coeur,
            pytest.dame_pique,
            pytest.huit_trefle,
            pytest.six_coeur,
            pytest.quatre_pique,
            pytest.trois_trefle,
            pytest.deux_carreau
        ]
        # WHEN
        cartes = MainJoueurComplete(liste_cartes)
        # THEN
        assert cartes.combinaison() == Combinaison.CarteHaute

    def test_combinaison_Paire(self):
        # GIVEN
        liste_cartes = [
            pytest.as_coeur,
            pytest.as_pique,
            pytest.roi_coeur,
            pytest.dame_trefle,
            pytest.neuf_coeur,
            pytest.trois_trefle,
            pytest.deux_carreau
        ]
        #WHEN
        cartes = MainJoueurComplete(liste_cartes)
        #THEN
        assert cartes.combinaison() == Combinaison.Paire

    def test_combinaison_DoublePaire(self):
        # GIVEN
        liste_cartes = [
            pytest.as_coeur,
            pytest.as_carreau,
            pytest.roi_coeur,
            pytest.roi_pique,
            pytest.valet_trefle,
            pytest.deux_pique,
            pytest.trois_trefle
        ]
        #WHEN
        cartes = MainJoueurComplete(liste_cartes)
        #THEN
        assert cartes.combinaison() == Combinaison.DoublePaire

    def test_combinaison_Brelan(self):
        # GIVEN
        liste_cartes = [
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.dame_trefle,
            pytest.roi_coeur,
            pytest.valet_coeur,
            pytest.deux_pique,
            pytest.trois_trefle
        ]
        #WHEN
        cartes = MainJoueurComplete(liste_cartes)
        #THEN
        assert cartes.combinaison() == Combinaison.Brelan

    def test_combinaison_Quinte(self):
        # GIVEN
        liste_cartes = [
            pytest.cinq_coeur,
            pytest.six_pique,
            pytest.sept_trefle,
            pytest.huit_coeur,
            pytest.neuf_pique,
            pytest.as_carreau,
            pytest.deux_trefle
        ]
        #WHEN
        cartes = MainJoueurComplete(liste_cartes)
        #THEN
        assert cartes.combinaison() == Combinaison.Quinte

    def test_combinaison_Flush(self):
        # GIVEN
        liste_cartes = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.valet_coeur,
            pytest.six_coeur,
            pytest.deux_coeur,
            pytest.trois_trefle,
            pytest.quatre_pique
        ]
        #WHEN
        cartes = MainJoueurComplete(liste_cartes)
        #THEN
        assert cartes.combinaison() == Combinaison.Flush

    def test_combinaison_Full(self):
        # GIVEN
        liste_cartes = [
            pytest.as_coeur,
            pytest.as_carreau,
            pytest.as_pique,
            pytest.roi_coeur,
            pytest.roi_pique,
            pytest.valet_coeur,
            pytest.dix_coeur
        ]
        # WHEN
        cartes = MainJoueurComplete(liste_cartes)
        # THEN
        assert cartes.combinaison() == Combinaison.Full

    def test_combinaison_Carre(self):
        # GIVEN
        liste_cartes = [
            pytest.as_coeur,
            pytest.as_carreau,
            pytest.as_pique,
            pytest.as_trefle,
            pytest.roi_coeur,
            pytest.deux_pique,
            pytest.trois_trefle
        ]
        #WHEN
        cartes = MainJoueurComplete(liste_cartes)
        #THEN
        assert cartes.combinaison() == Combinaison.Carre

    def test_combinaison_QuinteFlush(self):
        # GIVEN
        liste_cartes = [
            pytest.cinq_coeur,
            pytest.six_coeur,
            pytest.sept_coeur,
            pytest.huit_coeur,
            pytest.neuf_coeur,
            pytest.as_pique,
            pytest.deux_trefle
        ]
        #WHEN
        cartes = MainJoueurComplete(liste_cartes)
        #THEN
        assert cartes.combinaison() == Combinaison.QuinteFlush

    def test_combinaison_QuinteRoyale(self):
        # GIVEN
        liste_cartes = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.dix_coeur,
            pytest.deux_pique,
            pytest.trois_trefle
        ]

        # WHEN
        main_complete = MainJoueurComplete(liste_cartes)

        # THEN
        assert main_complete.combinaison() == Combinaison.QuinteRoyale
