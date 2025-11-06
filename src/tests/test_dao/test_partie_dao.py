import pytest
from src.dao.partie_dao import PartieDao
from src.business_object.partie import Partie, JoueurPartie
from src.business_object.pot import Pot
from src.business_object.joueur import Joueur
from src.business_object.siege import Siege
from src.business_object.monnaie import Monnaie


class TestPartieDao:
    
    @pytest.fixture
    def dao(self):
        return PartieDao()
    
    @pytest.fixture
    def joueur_test(self):
        return Joueur(id_joueur=1, pseudo="TestJoueur", mail="test@test.com", mdp="password", age=25)
    
    @pytest.fixture
    def siege_test(self):
        return Siege(id_siege=1)
    
    @pytest.fixture
    def joueur_partie_test(self, joueur_test, siege_test):
        return JoueurPartie(joueur_test, siege_test, 1000)
    
    @pytest.fixture
    def pot_test(self):
        return Pot()
    
    def test_creer_partie(self, dao, joueur_partie_test, pot_test):
        date_debut = "2024-01-01 10:00:00"
        partie = dao.creer_partie(
            joueurs=[joueur_partie_test],
            pot=pot_test,
            id_table=1,
            date_debut=date_debut
        )
        
        assert partie.id_partie == 1
        assert partie.id_table == 1
        assert partie.date_debut == date_debut
        assert partie.date_fin is None
        assert len(partie.joueurs) == 1
        assert dao.get_nombre_parties() == 1
    
    def test_get_partie_par_id(self, dao, joueur_partie_test, pot_test):
        partie = dao.creer_partie([joueur_partie_test], pot_test, 1, "2024-01-01 10:00:00")
        partie_recuperee = dao.get_partie_par_id(1)
        
        assert partie_recuperee == partie
        assert dao.get_partie_par_id(999) is None
    
    def test_get_toutes_parties(self, dao, joueur_partie_test, pot_test):
        partie1 = dao.creer_partie([joueur_partie_test], pot_test, 1, "2024-01-01 10:00:00")
        partie2 = dao.creer_partie([joueur_partie_test], pot_test, 2, "2024-01-01 11:00:00")
        
        parties = dao.get_toutes_parties()
        
        assert len(parties) == 2
        assert partie1 in parties
        assert partie2 in parties
    
    def test_get_parties_par_table(self, dao, joueur_partie_test, pot_test):
        dao.creer_partie([joueur_partie_test], pot_test, 1, "2024-01-01 10:00:00")
        dao.creer_partie([joueur_partie_test], pot_test, 2, "2024-01-01 11:00:00")
        dao.creer_partie([joueur_partie_test], pot_test, 1, "2024-01-01 12:00:00")
        
        parties_table_1 = dao.get_parties_par_table(1)
        
        assert len(parties_table_1) == 2
        assert all(partie.id_table == 1 for partie in parties_table_1)
    
    def test_get_parties_actives(self, dao, joueur_partie_test, pot_test):
        partie1 = dao.creer_partie([joueur_partie_test], pot_test, 1, "2024-01-01 10:00:00")
        partie2 = dao.creer_partie([joueur_partie_test], pot_test, 2, "2024-01-01 11:00:00")
        
        # Terminer une partie
        dao.terminer_partie(1, "2024-01-01 12:00:00")
        
        parties_actives = dao.get_parties_actives()
        
        assert len(parties_actives) == 1
        assert partie2 in parties_actives
        assert partie1 not in parties_actives
    
    def test_terminer_partie(self, dao, joueur_partie_test, pot_test):
        partie = dao.creer_partie([joueur_partie_test], pot_test, 1, "2024-01-01 10:00:00")
        
        date_fin = "2024-01-01 12:00:00"
        result = dao.terminer_partie(1, date_fin)
        
        assert result == True
        assert partie.date_fin == date_fin
        assert dao.terminer_partie(999, date_fin) == False
    
    def test_supprimer_partie(self, dao, joueur_partie_test, pot_test):
        dao.creer_partie([joueur_partie_test], pot_test, 1, "2024-01-01 10:00:00")
        
        assert dao.get_nombre_parties() == 1
        assert dao.supprimer_partie(1) == True
        assert dao.get_nombre_parties() == 0
        assert dao.supprimer_partie(999) == False
    
    def test_get_partie_par_joueur(self, dao, joueur_test, siege_test, pot_test):
        joueur_partie = JoueurPartie(joueur_test, siege_test, 1000)
        partie = dao.creer_partie([joueur_partie], pot_test, 1, "2024-01-01 10:00:00")
        
        partie_trouvee = dao.get_partie_par_joueur(1)
        
        assert partie_trouvee == partie
        assert dao.get_partie_par_joueur(999) is None
    
    def test_ajouter_retirer_joueur_partie(self, dao, joueur_test, siege_test, pot_test):
        joueur_partie1 = JoueurPartie(joueur_test, siege_test, 1000)
        partie = dao.creer_partie([joueur_partie1], pot_test, 1, "2024-01-01 10:00:00")
        
        # Ajouter un joueur
        joueur2 = Joueur(id_joueur=2, pseudo="Joueur2", mail="joueur2@test.com", mdp="password", age=30)
        joueur_partie2 = JoueurPartie(joueur2, siege_test, 1000)
        result_ajout = dao.ajouter_joueur_partie(1, joueur_partie2)
        
        assert result_ajout == True
        assert len(partie.joueurs) == 2
        
        # Retirer un joueur
        result_retrait = dao.retirer_joueur_partie(1, 2)
        
        assert result_retrait == True
        assert len(partie.joueurs) == 1
    
    def test_get_joueurs_partie(self, dao, joueur_partie_test, pot_test):
        partie = dao.creer_partie([joueur_partie_test], pot_test, 1, "2024-01-01 10:00:00")
        
        joueurs = dao.get_joueurs_partie(1)
        
        assert len(joueurs) == 1
        assert joueurs[0] == joueur_partie_test
        assert dao.get_joueurs_partie(999) == []