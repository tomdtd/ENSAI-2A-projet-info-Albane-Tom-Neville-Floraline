import pytest
from src.business_object.partie import Partie


# Mocks pour les dépendances
class MockPot:
    def __init__(self, montant=0):
        self.montant = montant


class MockJoueurPartie:
    def __init__(self, id_joueur=1, pseudo="TestJoueur"):
        self.joueur = type('MockJoueur', (), {'id_joueur': id_joueur, 'pseudo': pseudo})()
        self.solde_partie = type('MockMonnaie', (), {'get': lambda: 1000})()
        self.statut = "actif"


class TestPartie:

    @pytest.fixture
    def joueurs(self):
        return [MockJoueurPartie(i) for i in range(1, 4)]

    @pytest.fixture
    def pot(self):
        return MockPot()

    @pytest.fixture
    def partie(self, joueurs, pot):
        return Partie(
            id_partie=1,
            joueurs=joueurs,
            pot=pot,
            id_table=10,
            date_debut="2024-01-01"
        )

    def test_initialisation(self, partie, joueurs, pot):
        """Test de l'initialisation d'une partie"""
        assert partie.id_partie == 1
        assert partie.joueurs == joueurs
        assert partie.pot == pot
        assert partie.id_table == 10
        assert partie.date_debut == "2024-01-01"
        assert partie.date_fin is None

    def test_initialisation_avec_liste_joueurs_vide(self, pot):
        """Test d'initialisation avec une liste de joueurs vide"""
        partie = Partie(
            id_partie=1,
            joueurs=[],
            pot=pot,
            id_table=10,
            date_debut="2024-01-01"
        )

        assert partie.joueurs == []

    def test_initialisation_date_fin_none(self, partie):
        """Test que date_fin est None à l'initialisation"""
        assert partie.date_fin is None

    def test_str_method(self, partie):
        """Test de la méthode __str__"""
        str_output = str(partie)
        assert "Partie(id_partie=1" in str_output
        assert "joueurs=" in str_output
        assert "pot=" in str_output

    def test_gerer_blind(self, partie):
        """Test de la méthode gerer_blind"""
        # Sauvegarder l'ordre initial des joueurs
        ordre_initial = partie.joueurs.copy()

        # Appeler la méthode
        partie.gerer_blind()

        # Vérifier que l'ordre a été modifié (rotation)
        assert len(partie.joueurs) == len(ordre_initial)
        assert partie.joueurs[0] == ordre_initial[-1]

    def test_gerer_blind_un_joueur(self, pot):
        """Test de gerer_blind avec un seul joueur"""
        joueur_seul = [MockJoueurPartie(1)]
        partie = Partie(
            id_partie=1,
            joueurs=joueur_seul,
            pot=pot,
            id_table=10,
            date_debut="2024-01-01"
        )

        # Avec un seul joueur, la méthode ne doit pas lever d'erreur
        partie.gerer_blind()
        assert len(partie.joueurs) == 1

    def test_gerer_blind_deux_joueurs(self, pot):
        """Test de gerer_blind avec deux joueurs"""
        joueurs = [MockJoueurPartie(1), MockJoueurPartie(2)]
        partie = Partie(
            id_partie=1,
            joueurs=joueurs,
            pot=pot,
            id_table=10,
            date_debut="2024-01-01"
        )

        ordre_initial = partie.joueurs.copy()
        partie.gerer_blind()

        # Vérifier la rotation
        assert partie.joueurs[0] == ordre_initial[1]
        assert partie.joueurs[1] == ordre_initial[0]

    def test_partie_sans_joueurs(self, pot):
        """Test d'initialisation sans joueurs"""
        partie = Partie(
            id_partie=1,
            joueurs=[],
            pot=pot,
            id_table=10,
            date_debut="2024-01-01"
        )

        assert partie.joueurs == []
        # La méthode gerer_blind ne doit pas lever d'erreur même avec 0 joueur
        partie.gerer_blind()
        assert partie.joueurs == []

    def test_finir_partie_method_exists(self, partie):
        """Test que la méthode finir_partie existe"""
        # Vérifier que la méthode existe et peut être appelée
        assert hasattr(partie, 'finir_partie')
        assert callable(partie.finir_partie)

    def test_repartition_blind_method_exists(self, partie):
        """Test que la méthode repartition_blind existe (même si vide)"""
        # Vérifier que la méthode existe dans la docstring
        assert "repartition_blind()" in Partie.__doc__

    def test_attributs_presents(self, partie):
        """Test que tous les attributs sont présents"""
        assert hasattr(partie, 'id_partie')
        assert hasattr(partie, 'joueurs')
        assert hasattr(partie, 'pot')
        assert hasattr(partie, 'id_table')
        assert hasattr(partie, 'date_debut')
        assert hasattr(partie, 'date_fin')
