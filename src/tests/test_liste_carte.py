import pytest
from src.business_object.carte import Carte
from src.business_object.liste_cartes import ListeCartes

class TestListeCartes:
    """Tests unitaires pour la classe ListeCartes."""

    def test_creation_vide_genere_toutes_les_cartes(self):
        """Vérifie que la création sans argument génère 2 jeux complets de cartes."""
        liste = ListeCartes()
        # Un jeu = 52 cartes → *2 = 104 cartes
        assert len(liste) == 104

        # Vérifie qu'on a bien des objets Carte
        assert all(isinstance(c, Carte) for c in liste.get_cartes())

    def test_creation_avec_liste_valide(self):
        """Vérifie qu'on peut créer une ListeCartes avec une liste de cartes."""
        cartes = [Carte("As", "Pique"), Carte("Roi", "Cœur")]
        liste = ListeCartes(cartes)
        assert len(liste) == 2
        assert liste.get_cartes() == cartes

    def test_creation_avec_argument_non_liste_declenche_erreur(self):
        """Vérifie qu'une erreur est levée si l'argument n'est pas une liste."""
        with pytest.raises(ValueError):
            ListeCartes("pas une liste")

    def test_creation_avec_liste_contenant_autre_chose_que_des_cartes_declenche_erreur(self):
        """Vérifie qu'une erreur est levée si la liste contient autre chose que des Carte."""
        with pytest.raises(ValueError):
            ListeCartes([Carte("As", "Pique"), "Pas une carte"])

    def test_ajout_de_carte_valide(self):
        """Vérifie que l'ajout d'une carte valide fonctionne."""
        liste = ListeCartes([])
        carte = Carte("As", "Trèfle")
        liste.ajouter_carte(carte)
        assert carte in liste.get_cartes()

    def test_ajout_de_carte_invalide_declenche_erreur(self):
        """Vérifie qu'une erreur est levée si on ajoute autre chose qu'une Carte."""
        liste = ListeCartes([])
        with pytest.raises(ValueError):
            liste.ajouter_carte("Pas une carte")

    def test_str_affiche_correctement(self):
        """Vérifie que la représentation textuelle contient les cartes."""
        cartes = [Carte("As", "Carreau"), Carte("Roi", "Pique")]
        liste = ListeCartes(cartes)
        texte = str(liste)
        assert "As" in texte and "Roi" in texte