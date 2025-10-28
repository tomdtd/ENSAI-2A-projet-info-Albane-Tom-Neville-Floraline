import pytest
from src.business_object.carte import Carte
from src.business_object.main_joueur import MainJoueur


class TestMainJoueur:
    def test_main_joueur_valide_ok(self):
        # GIVEN
        cartes = (
            Carte("As", "Pique"),
            Carte("Roi", "Coeur")
        )

        # WHEN
        main_joueur = MainJoueur(cartes)

        # THEN
        assert isinstance(main_joueur, MainJoueur)
        # On vérifie que l'objet a bien deux cartes
        assert len(main_joueur._MainJoueur__cartes) == 2
        # On vérifie le contenu exact des cartes
        assert main_joueur._MainJoueur__cartes == cartes

    def test_main_joueur_non_tuple(self):
        # GIVEN
        cartes = [
            Carte("As", "Pique"),
            Carte("Roi", "Coeur")
        ]

        # WHEN / THEN
        with pytest.raises(ValueError) as excinfo:
            MainJoueur(cartes)
        assert "doit être un tuple" in str(excinfo.value)

    def test_main_joueur_taille_invalide(self):
        # GIVEN
        cartes = (Carte("As", "Pique"),)

        # WHEN / THEN
        with pytest.raises(ValueError) as excinfo:
            MainJoueur(cartes)
        assert "doit contenir deux cartes" in str(excinfo.value)

    def test_main_joueur_contenant_element_non_carte(self):
        # GIVEN
        cartes = (Carte("As", "Pique"), "Pas une carte")

        # WHEN / THEN
        with pytest.raises(ValueError) as excinfo:
            MainJoueur(cartes)
        assert "doivent être des cartes" in str(excinfo.value)
