import pytest
from src.business_object.monnaie import Monnaie
from src.business_object.joueur import Joueur


class TestJoueur:
    
    @pytest.fixture
    def joueur_test(self):
        """Fixture pour créer un joueur de test"""
        return Joueur(
            pseudo="TestPlayer",
            mail="test@example.com",
            mdp="password123",
            age=25,
            credit=Monnaie(100),
            id_joueur=1
        )
    
    @pytest.fixture
    def joueur_sans_id(self):
        """Fixture pour créer un joueur sans ID"""
        return Joueur(
            pseudo="NoID",
            mail="noid@test.com",
            mdp="mdp123",
            age=20
        )

    def test_initialisation_complete(self):
        """Test l'initialisation avec tous les paramètres"""
        joueur = Joueur(
            pseudo="John",
            mail="john@test.com",
            mdp="mdp123",
            age=30,
            credit=Monnaie(50),
            id_joueur=1
        )
        
        assert joueur.id_joueur == 1
        assert joueur.pseudo == "John"
        assert joueur.mail == "john@test.com"
        assert joueur.mdp == "mdp123"
        assert joueur.age == 30
        assert joueur.credit.get() == 50

    def test_initialisation_sans_id_et_credit(self, joueur_sans_id):
        """Test l'initialisation sans id_joueur et avec crédit par défaut"""
        assert joueur_sans_id.id_joueur is None
        assert joueur_sans_id.credit.get() == 0
        assert joueur_sans_id.pseudo == "NoID"
        assert joueur_sans_id.age == 20

    def test_crediter(self, joueur_test):
        """Test la méthode crediter"""
        solde_initial = joueur_test.credit.get()
        montant = 50
        
        joueur_test.crediter(montant)
        
        assert joueur_test.credit.get() == solde_initial + montant

    def test_debiter(self, joueur_test):
        """Test la méthode debiter"""
        solde_initial = joueur_test.credit.get()
        montant = 30
        
        joueur_test.debiter(montant)
        
        assert joueur_test.credit.get() == solde_initial - montant

    def test_debiter_solde_insuffisant(self, joueur_test):
        """Test debiter avec un montant supérieur au solde"""
        solde_initial = joueur_test.credit.get()
        montant = solde_initial + 100
        
        # On suppose que la méthode debiter de Monnaie gère les soldes insuffisants
        try:
            joueur_test.debiter(montant)
            # Si aucune exception n'est levée, vérifier le solde
            assert joueur_test.credit.get() == solde_initial - montant
        except Exception:
            # Vérifier que le solde n'a pas changé en cas d'erreur
            assert joueur_test.credit.get() == solde_initial

    def test_jouer_partie(self, joueur_test, capsys):
        """Test la méthode jouer_partie"""
        joueur_test.jouer_partie()
        
        captured = capsys.readouterr()
        assert f"Le joueur {joueur_test.pseudo} entre dans une partie." in captured.out

    def test_changer_mdp_success(self, joueur_test, capsys):
        """Test le changement de mot de passe avec l'ancien mot de passe correct"""
        ancien_mdp = "password123"
        nouveau_mdp = "newpassword456"
        
        joueur_test.changer_mdp(ancien_mdp, nouveau_mdp)
        
        assert joueur_test.mdp == nouveau_mdp
        
        captured = capsys.readouterr()
        # Correction : utiliser pseudo au lieu de name
        assert f"Le mot de passe de l'administrateur {joueur_test.pseudo} a été changé." in captured.out

    def test_changer_mdp_echec(self, joueur_test, capsys):
        """Test le changement de mot de passe avec l'ancien mot de passe incorrect"""
        ancien_mdp_incorrect = "wrongpassword"
        nouveau_mdp = "newpassword456"
        mdp_initial = joueur_test.mdp
        
        joueur_test.changer_mdp(ancien_mdp_incorrect, nouveau_mdp)
        
        # Le mot de passe ne devrait pas avoir changé
        assert joueur_test.mdp == mdp_initial
        
        captured = capsys.readouterr()
        assert "Mot de passe actuel incorrect." in captured.out

    def test_str(self, joueur_test):
        """Test la méthode __str__"""
        expected_str = "Joueur(TestPlayer, test@example.com ans)"
        assert str(joueur_test) == expected_str

    def test_repr(self, joueur_test):
        """Test la méthode __repr__"""
        expected_repr = "Joueur(id=1, pseudo='TestPlayer', credit=100)"
        assert repr(joueur_test) == expected_repr

    def test_repr_sans_id(self, joueur_sans_id):
        """Test la méthode __repr__ sans id_joueur"""
        expected_repr = "Joueur(id=None, pseudo='NoID', credit=0)"
        assert repr(joueur_sans_id) == expected_repr


class TestJoueurParametrized:
    """Tests paramétrés pour une meilleure couverture"""
    
    @pytest.fixture
    def joueur_base(self):
        """Fixture pour les tests paramétrés"""
        return Joueur(
            pseudo="Test",
            mail="test@test.com",
            mdp="mdp",
            age=25,
            credit=Monnaie(100),
            id_joueur=1
        )
    
    @pytest.mark.parametrize("pseudo, mail, mdp, age, credit, id_joueur", [
        ("player1", "p1@test.com", "mdp1", 18, 100, 1),
        ("player2", "p2@test.com", "mdp2", 35, 500, 2),
        ("player3", "p3@test.com", "mdp3", 65, 1000, 3),
        ("player4", "p4@test.com", "mdp4", 25, 0, 4),
        ("player5", "p5@test.com", "mdp5", 30, 200, None),
    ])
    def test_initialisation_parametres_variables(self, pseudo, mail, mdp, age, credit, id_joueur):
        """Test l'initialisation avec différents jeux de paramètres"""
        joueur = Joueur(
            pseudo=pseudo,
            mail=mail,
            mdp=mdp,
            age=age,
            credit=Monnaie(credit),
            id_joueur=id_joueur
        )
        
        assert joueur.pseudo == pseudo
        assert joueur.mail == mail
        assert joueur.mdp == mdp
        assert joueur.age == age
        assert joueur.credit.get() == credit
        assert joueur.id_joueur == id_joueur

    @pytest.mark.parametrize("montant, expected_solde", [
        (50, 150),   # crédit positif
        (0, 100),    # crédit nul
        (100, 200),  # crédit égal au solde initial
    ])
    def test_crediter_montants_variables(self, joueur_base, montant, expected_solde):
        """Test la méthode crediter avec différents montants"""
        joueur_base.crediter(montant)
        assert joueur_base.credit.get() == expected_solde

    @pytest.mark.parametrize("montant, expected_solde", [
        (30, 70),   # débit normal
        (100, 0),   # débit total
    ])
    def test_debiter_montants_variables(self, joueur_base, montant, expected_solde):
        """Test la méthode debiter avec différents montants"""
        joueur_base.debiter(montant)
        assert joueur_base.credit.get() == expected_solde


class TestJoueurEdgeCases:
    """Tests pour les cas limites"""
    
    @pytest.fixture
    def joueur_test(self):
        """Fixture pour créer un joueur de test - DOIT ÊTRE DÉFINIE DANS CHAQUE CLASSE"""
        return Joueur(
            pseudo="TestPlayer",
            mail="test@example.com",
            mdp="password123",
            age=25,
            credit=Monnaie(100),
            id_joueur=1
        )
    
    def test_initialisation_age_minimum(self):
        """Test avec l'âge minimum"""
        joueur = Joueur(
            pseudo="MinAge",
            mail="min@test.com",
            mdp="mdp",
            age=0,  # Âge minimum théorique
            credit=Monnaie(10)
        )
        
        assert joueur.age == 0
    
    def test_initialisation_pseudo_vide(self):
        """Test avec un pseudo vide"""
        joueur = Joueur(
            pseudo="",
            mail="empty@test.com",
            mdp="mdp",
            age=25
        )
        
        assert joueur.pseudo == ""
    
    def test_crediter_montant_negatif(self, joueur_test):
        """Test crediter avec un montant négatif"""
        solde_initial = joueur_test.credit.get()
        
        # Le comportement dépend de l'implémentation de Monnaie.crediter()
        try:
            joueur_test.crediter(-50)
            # Si aucune exception, vérifier le résultat
            assert joueur_test.credit.get() == solde_initial - 50
        except Exception:
            # Si une exception est levée, le solde ne devrait pas changer
            assert joueur_test.credit.get() == solde_initial
    
    def test_debiter_montant_negatif(self, joueur_test):
        """Test debiter avec un montant négatif"""
        solde_initial = joueur_test.credit.get()
        
        # Le comportement dépend de l'implémentation de Monnaie.debiter()
        try:
            joueur_test.debiter(-30)
            # Si aucune exception, vérifier le résultat
            assert joueur_test.credit.get() == solde_initial + 30
        except Exception:
            # Si une exception est levée, le solde ne devrait pas changer
            assert joueur_test.credit.get() == solde_initial