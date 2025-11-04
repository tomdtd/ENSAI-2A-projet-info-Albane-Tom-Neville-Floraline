import pytest
from src.business_object.carte import Carte
from src.business_object.liste_cartes import ListeCartes

@pytest.fixture
def carte_as_pique():
    return Carte("As", "Pique")

@pytest.fixture
def carte_roi_coeur():
    return Carte("Roi", "Coeur")

@pytest.fixture
def liste_2_cartes(carte_as_pique, carte_roi_coeur):
    return [carte_as_pique, carte_roi_coeur]


# ---------- TESTS ---------- #

class TestListeCartes:
    
    def test_creation_vide_genere_toutes_les_cartes(self):
        """Vérifie que la création sans argument génère 2 jeux complets de cartes."""
        liste = ListeCartes()
        cartes = liste.get_cartes()

        # Un jeu = 52 cartes → *2 = 104 cartes
        assert len(liste) == 104
        assert all(isinstance(c, Carte) for c in cartes)

        # Vérifie que chaque carte apparaît 2 fois
        for valeur in Carte.VALEURS():
            for couleur in Carte.COULEURS():
                assert cartes.count(Carte(valeur, couleur)) == 2

    def test_creation_avec_liste_valide(self, liste_2_cartes):
        liste = ListeCartes(liste_2_cartes)
        assert len(liste) == 2
        assert liste.get_cartes() == liste_2_cartes

    def test_creation_avec_argument_non_liste_declenche_erreur(self):
        with pytest.raises(ValueError):
            ListeCartes("pas une liste")

    def test_creation_avec_liste_contenant_autre_chose_que_des_cartes_declenche_erreur(self):
        with pytest.raises(ValueError):
            ListeCartes([Carte("As", "Pique"), "Pas une carte"])

    def test_ajout_de_carte_valide(self, carte_as_pique):
        liste = ListeCartes([])
        liste.ajouter_carte(carte_as_pique)
        assert carte_as_pique in liste.get_cartes()

    def test_ajout_de_carte_invalide_declenche_erreur(self):
        liste = ListeCartes([])
        with pytest.raises(ValueError):
            liste.ajouter_carte("Pas une carte")

    def test_str_affiche_correctement(self, liste_2_cartes):
        liste = ListeCartes(liste_2_cartes)
        texte = str(liste)
        assert "As" in texte or "Roi" in texte