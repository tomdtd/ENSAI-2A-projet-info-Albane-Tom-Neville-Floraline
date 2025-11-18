import pytest
from business_object.joueur_partie import JoueurPartie
from business_object.joueur import Joueur
from business_object.siege import Siege
from business_object.main import Main
from business_object.monnaie import Monnaie


class TestJoueurPartie:
    @pytest.fixture
    def joueur(self):
        return Joueur(
            pseudo="TestJoueur",
            mail="test@example.com", 
            mdp="password123",
            age=25
        )

    @pytest.fixture
    def siege(self):
        return Siege(id_siege=1)

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
        assert isinstance(joueur_partie.main, Main)

    def test_miser_montant_valide(self, joueur_partie, capsys):
        """Test de la méthode miser avec un montant valide"""
        solde_initial = joueur_partie.solde_partie.get()
        montant = 100
        
        joueur_partie.miser(montant)
        
        assert joueur_partie.solde_partie.get() == solde_initial - montant
        assert joueur_partie.mise_tour.get() == montant
        
        # Vérifier le message
        captured = capsys.readouterr()
        assert f"{joueur_partie.joueur.pseudo} mise {montant}." in captured.out

    def test_miser_montant_zero(self, joueur_partie):
        """Test de la méthode miser avec un montant de 0"""
        solde_initial = joueur_partie.solde_partie.get()
        mise_initial = joueur_partie.mise_tour.get()
        
        joueur_partie.miser(0)
        
        # Rien ne doit changer
        assert joueur_partie.solde_partie.get() == solde_initial
        assert joueur_partie.mise_tour.get() == mise_initial

    def test_miser_solde_insuffisant(self, joueur_partie, capsys):
        """Test de mise avec solde insuffisant"""
        montant_trop_eleve = 1500
        
        joueur_partie.miser(montant_trop_eleve)
        
        assert joueur_partie.solde_partie.get() == 0
        assert joueur_partie.mise_tour.get() == 1000
        
        # Vérifier le message
        captured = capsys.readouterr()
        assert f"{joueur_partie.joueur.pseudo} mise 1000." in captured.out

    def test_se_coucher(self, joueur_partie, capsys):
        """Test de la méthode se_coucher"""
        joueur_partie.se_coucher()
        
        assert joueur_partie.statut == "couché"
        
        # Vérifier le message
        captured = capsys.readouterr()
        assert f"{joueur_partie.joueur.pseudo} se couche." in captured.out

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