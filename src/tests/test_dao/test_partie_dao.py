# test_partie_dao_pytest.py
import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

from dao.partie_dao import PartieDao
from business_object.partie import Partie

class TestPartieDaoPytest:

    @pytest.fixture
    def partie_dao(self):
        """Fixture pour PartieDao"""
        dao = PartieDao()
        dao._get_connection = Mock()
        mock_connection = Mock()
        mock_cursor = Mock()
        dao._get_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.__enter__ = Mock(return_value=mock_connection)
        mock_connection.__exit__ = Mock(return_value=None)
        
        return dao, mock_connection, mock_cursor

    @pytest.fixture
    def sample_partie(self):
        """Fixture pour une partie de test"""
        return Partie(
            id_table=1,
            date_debut=datetime(2024, 1, 1, 10, 0, 0),
            statut_partie="en_attente",
            pot_total=0.0
        )

    def test_creer_success_pytest(self, partie_dao, sample_partie):
        """Test de création avec pytest"""
        dao, _, mock_cursor = partie_dao
        mock_cursor.fetchone.return_value = {"id_partie": 1}
        
        result = dao.creer(sample_partie)
        
        assert result is True
        assert sample_partie.id_partie == 1
        mock_cursor.execute.assert_called_once()

    def test_trouver_par_id_not_found_pytest(self, partie_dao):
        """Test recherche par ID non trouvé avec pytest"""
        dao, _, mock_cursor = partie_dao
        mock_cursor.fetchone.return_value = None
        
        result = dao.trouver_par_id(999)
        
        assert result is None

    @pytest.mark.parametrize("rowcount,expected", [
        (1, True),
        (0, False)
    ])
    def test_mettre_a_jour_parametrize(self, partie_dao, sample_partie, rowcount, expected):
        """Test paramétré de mise à jour"""
        dao, _, mock_cursor = partie_dao
        sample_partie.id_partie = 1
        mock_cursor.rowcount = rowcount
        
        result = dao.mettre_a_jour(sample_partie)
        
        assert result == expected

    @pytest.mark.parametrize("statut,expected_count", [
        ("en_cours", 2),
        ("terminee", 1),
        ("en_attente", 0)
    ])
    def test_trouver_parties_par_statut_parametrize(self, partie_dao, statut, expected_count):
        """Test paramétré de recherche par statut"""
        dao, _, mock_cursor = partie_dao
        
        if expected_count > 0:
            mock_parties = [
                {
                    "id_partie": i,
                    "id_table": i,
                    "date_debut": datetime(2024, 1, 1, 10 + i, 0, 0),
                    "date_fin": None,
                    "statut_partie": statut,
                    "pot_total": 100.0 * i,
                    "cartes_communes": None
                } for i in range(1, expected_count + 1)
            ]
            mock_cursor.fetchall.return_value = mock_parties
        else:
            mock_cursor.fetchall.return_value = []
        
        result = dao.trouver_parties_par_statut(statut)
        
        assert len(result) == expected_count
        if expected_count > 0:
            assert all(p.statut_partie == statut for p in result)

    def test_trouver_parties_par_joueur_complex_query(self, partie_dao):
        """Test de la requête complexe pour les parties par joueur"""
        dao, _, mock_cursor = partie_dao
        
        mock_cursor.fetchall.return_value = [
            {
                "id_partie": 1,
                "id_table": 1,
                "date_debut": datetime(2024, 1, 1, 10, 0, 0),
                "date_fin": datetime(2024, 1, 1, 10, 30, 0),
                "statut_partie": "terminee",
                "pot_total": 200.0,
                "cartes_communes": "AS,KD,5C,8S,JD"
            }
        ]
        
        result = dao.trouver_parties_par_joueur(1)
        
        assert len(result) == 1
        # Vérifie que la requête avec jointure a été exécutée
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0][0]
        assert "INNER JOIN joueurs_parties" in call_args
        assert "DISTINCT" in call_args

    def test_trouver_derniere_partie_sur_table_with_limit(self, partie_dao):
        """Test de la recherche de dernière partie avec LIMIT"""
        dao, _, mock_cursor = partie_dao
        
        mock_cursor.fetchone.return_value = {
            "id_partie": 5,
            "id_table": 1,
            "date_debut": datetime(2024, 1, 1, 15, 0, 0),
            "date_fin": None,
            "statut_partie": "en_cours",
            "pot_total": 75.0,
            "cartes_communes": "AS,KD"
        }
        
        result = dao.trouver_derniere_partie_sur_table(1)
        
        assert result is not None
        call_args = mock_cursor.execute.call_args[0][0]
        assert "LIMIT 1" in call_args
        assert "ORDER BY date_debut DESC" in call_args

    def test_lister_parties_par_periode_date_range(self, partie_dao):
        """Test du listage par période avec plage de dates"""
        dao, _, mock_cursor = partie_dao
        
        debut = datetime(2024, 1, 1, 0, 0, 0)
        fin = datetime(2024, 1, 31, 23, 59, 59)
        mock_cursor.fetchall.return_value = []
        
        result = dao.lister_parties_par_periode(debut, fin)
        
        mock_cursor.execute.assert_called_once_with(
            "SELECT id_partie, id_table, date_debut, date_fin, statut_partie, pot_total, cartes_communes "
            "FROM parties WHERE date_debut BETWEEN %(debut)s AND %(fin)s ORDER BY date_debut DESC;",
            {"debut": debut, "fin": fin}
        )

    def test_compter_parties_par_statut_pytest(self, partie_dao):
        """Test du comptage avec pytest"""
        dao, _, mock_cursor = partie_dao
        mock_cursor.fetchone.return_value = {"count": 5}
        
        result = dao.compter_parties_par_statut("en_cours")
        
        assert result == 5

    def test_partie_validation_dans_business_object(self):
        """Test de la validation dans la classe Partie"""
        # Test validation statut_partie
        with pytest.raises(ValueError, match="Statut de partie invalide"):
            Partie(statut_partie="invalide")
        
        # Test validation pot_total
        with pytest.raises(ValueError, match="Le pot total ne peut pas être négatif"):
            Partie(pot_total=-10.0)
        
        # Test création valide
        partie_valide = Partie(statut_partie="en_attente", pot_total=0.0)
        assert partie_valide.statut_partie == "en_attente"
        assert partie_valide.pot_total == 0.0

    def test_partie_methodes_utilitaires(self, sample_partie):
        """Test des méthodes utilitaires de la classe Partie"""
        # Test est_terminee
        sample_partie.statut_partie = "terminee"
        assert sample_partie.est_terminee() is True
        sample_partie.statut_partie = "en_cours"
        assert sample_partie.est_terminee() is False
        
        # Test est_en_cours
        sample_partie.statut_partie = "en_cours"
        assert sample_partie.est_en_cours() is True
        
        # Test est_en_attente
        sample_partie.statut_partie = "en_attente"
        assert sample_partie.est_en_attente() is True
        
        # Test terminer
        sample_partie.terminer()
        assert sample_partie.statut_partie == "terminee"
        assert sample_partie.date_fin is not None
        
        # Test demarrer
        sample_partie.demarrer()
        assert sample_partie.statut_partie == "en_cours"
        
        # Test __str__
        str_representation = str(sample_partie)
        assert "Partie" in str_representation
        assert "en_cours" in str_representation

    def test_partie_date_debut_auto(self):
        """Test de la date de début automatique"""
        partie = Partie()
        assert partie.date_debut is not None
        # La date de début devrait être proche de maintenant
        assert (datetime.now() - partie.date_debut).total_seconds() < 1

# Tests de performance
class TestPartieDaoPerformance:
    """Tests de performance pour PartieDao"""
    
    @pytest.mark.performance
    def test_performance_trouver_parties_par_joueur(self, partie_dao):
        """Test de performance pour la recherche des parties par joueur"""
        dao, _, mock_cursor = partie_dao
        
        # Simuler un grand nombre de parties
        mock_parties = [
            {
                "id_partie": i,
                "id_table": i % 5 + 1,
                "date_debut": datetime(2024, 1, 1, i % 24, 0, 0),
                "date_fin": None,
                "statut_partie": "terminee",
                "pot_total": 100.0 * i,
                "cartes_communes": "AS,KD,5C,8S,JD"
            } for i in range(1000)
        ]
        mock_cursor.fetchall.return_value = mock_parties
        
        import time
        start_time = time.time()
        
        result = dao.trouver_parties_par_joueur(1)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert execution_time < 0.2
        assert len(result) == 1000

    @pytest.mark.performance
    def test_performance_lister_parties_par_periode(self, partie_dao):
        """Test de performance pour le listage par période"""
        dao, _, mock_cursor = partie_dao
        
        mock_cursor.fetchall.return_value = []
        
        import time
        start_time = time.time()
        
        debut = datetime(2024, 1, 1, 0, 0, 0)
        fin = datetime(2024, 12, 31, 23, 59, 59)
        result = dao.lister_parties_par_periode(debut, fin)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert execution_time < 0.1

# Tests edge cases
class TestPartieDaoEdgeCases:
    """Tests des cas limites pour PartieDao"""
    
    def test_creer_partie_sans_date(self, partie_dao):
        """Test création d'une partie sans date spécifiée"""
        dao, _, mock_cursor = partie_dao
        mock_cursor.fetchone.return_value = {"id_partie": 1}
        
        partie = Partie(id_table=1, statut_partie="en_attente")
        result = dao.creer(partie)
        
        assert result is True
        # La date_debut devrait être automatiquement définie
        assert partie.date_debut is not None

    def test_mettre_a_jour_partie_sans_id(self, partie_dao):
        """Test mise à jour d'une partie sans ID"""
        dao, _, mock_cursor = partie_dao
        
        partie = Partie(id_table=1, statut_partie="en_cours")
        result = dao.mettre_a_jour(partie)
        
        assert result is False

    def test_partie_avec_cartes_communes_longues(self, partie_dao):
        """Test avec des cartes communes longues"""
        dao, _, mock_cursor = partie_dao
        
        cartes_longues = "AS,KD,5C,8S,JD,2H,3D,4S,9C,TH"  # Plus de 5 cartes
        mock_cursor.fetchone.return_value = {
            "id_partie": 1,
            "id_table": 1,
            "date_debut": datetime.now(),
            "date_fin": None,
            "statut_partie": "en_cours",
            "pot_total": 100.0,
            "cartes_communes": cartes_longues
        }
        
        result = dao.trouver_par_id(1)
        
        assert result is not None
        assert result.cartes_communes == cartes_longues

    def test_periode_inverse(self, partie_dao):
        """Test avec une période inversée (fin avant début)"""
        dao, _, mock_cursor = partie_dao
        
        debut = datetime(2024, 1, 2, 0, 0, 0)
        fin = datetime(2024, 1, 1, 23, 59, 59)
        mock_cursor.fetchall.return_value = []
        
        result = dao.lister_parties_par_periode(debut, fin)
        
        # La requête devrait quand même s'exécuter
        assert result == []
        mock_cursor.execute.assert_called_once()