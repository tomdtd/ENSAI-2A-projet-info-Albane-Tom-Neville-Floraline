import pytest
from src.business_object.joueur import Joueur
from src.business_object.siege import Siege
from src.business_object.monnaie import Monnaie
from src.business_object.joueur_partie import JoueurPartie

# Mocks pour les dépendances
class MockJoueur:
    def __init__(self, id_joueur=1, pseudo="TestJoueur"):
        self.id_joueur = id_joueur
        self.pseudo = pseudo

class MockMain:
    def __init__(self):
        self.cartes = []

class TestJoueurPartie:
    
    @pytest.fixture
    def joueur(self):
        return MockJoueur()
    
    @pytest.fixture
    def siege(self):
        return Siege(id_siege=1, id_table=1)
    
    @pytest.fixture
    def joueur_partie(self, joueur, siege):
        return JoueurPartie(joueur=joueur, siege=siege, solde_partie=1000)
    
    def test_initialisation(self, joueur_partie, joueur, siege):
        """Test de l'initialisation de JoueurPartie"""
        assert joueur_partie.joueur == joueur
        assert joueur_partie.siege == siege
        assert joueur_partie.solde_partie.get() == 1000
        assert joueur_partie.statut == "en attente"
        assert joueur_partie.mise_tour.get() == 0
    
    def test_miser_montant_valide(self, joueur_partie):
        """Test de la méthode miser avec un montant valide"""
        solde_initial = joueur_partie.solde_partie.get()
        montant = 100
        
        joueur_partie.miser(montant)
        
        assert joueur_partie.solde_partie.get() == solde_initial - montant
        assert joueur_partie.mise_tour.get() == montant
    
    def test_miser_montant_zero(self, joueur_partie):
        """Test de la méthode miser avec un montant de 0"""
        solde_initial = joueur_partie.solde_partie.get()
        mise_initial = joueur_partie.mise_tour.get()
        
        joueur_partie.miser(0)
        
        # Rien ne doit changer
        assert joueur_partie.solde_partie.get() == solde_initial
        assert joueur_partie.mise_tour.get() == mise_initial
    
    def test_miser_montant_negatif(self, joueur_partie):
        """Test de la méthode miser avec un montant négatif"""
        solde_initial = joueur_partie.solde_partie.get()
        mise_initial = joueur_partie.mise_tour.get()
        
        joueur_partie.miser(-50)
        
        # Rien ne doit changer
        assert joueur_partie.solde_partie.get() == solde_initial
        assert joueur_partie.mise_tour.get() == mise_initial
    
    def test_se_coucher(self, joueur_partie):
        """Test de la méthode se_coucher"""
        joueur_partie.se_coucher()
        
        assert joueur_partie.statut == "couché"
    
    def test_plusieurs_mises(self, joueur_partie):
        """Test de plusieurs mises successives"""
        # Première mise
        joueur_partie.miser(100)
        assert joueur_partie.solde_partie.get() == 900
        assert joueur_partie.mise_tour.get() == 100
        
        # Deuxième mise
        joueur_partie.miser(50)
        assert joueur_partie.solde_partie.get() == 850
        assert joueur_partie.mise_tour.get() == 150
    
    def test_miser_solde_insuffisant(self, joueur_partie):
        """Test de mise avec solde insuffisant - ne doit pas lever d'erreur"""
        montant_trop_eleve = 1500
        
        # Ne doit pas lever d'erreur, mais miser le maximum possible
        joueur_partie.miser(montant_trop_eleve)
        
        assert joueur_partie.solde_partie.get() == 0
        assert joueur_partie.mise_tour.get() == 1000
    
    def test_miser_tout_solde(self, joueur_partie):
        """Test de mise de tout le solde"""
        joueur_partie.miser(1000)
        
        assert joueur_partie.solde_partie.get() == 0
        assert joueur_partie.mise_tour.get() == 1000
    
    def test_initialisation_solde_different(self, joueur, siege):
        """Test d'initialisation avec différents soldes"""
        for solde in [0, 500, 1000, 5000]:
            joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=solde)
            assert joueur_partie.solde_partie.get() == solde