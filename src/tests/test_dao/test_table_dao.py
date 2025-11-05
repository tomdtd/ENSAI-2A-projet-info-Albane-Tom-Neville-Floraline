import unittest
import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from dao.table_dao import TableDao
from business_object.table import Table

class TestTableDao(unittest.TestCase):

    def setUp(self):
        """Setup avant chaque test"""
        self.table_dao = TableDao()
        self.table_dao._get_connection = Mock()
        
        # Mock de la connexion et du curseur
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.table_dao._get_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_connection.__enter__ = Mock(return_value=self.mock_connection)
        self.mock_connection.__exit__ = Mock(return_value=None)

    def test_creer_success(self):
        """Test de création d'une table avec succès"""
        # Setup
        table = Table(nom_table="Table VIP", nb_sieges_max=6, blind_initial=10.0)
        self.mock_cursor.fetchone.return_value = {"id_table": 1}
        
        # Execution
        result = self.table_dao.creer(table)
        
        # Vérifications
        self.assertTrue(result)
        self.assertEqual(table.id_table, 1)
        self.mock_cursor.execute.assert_called_once_with(
            "INSERT INTO tables (nom_table, nb_sieges_max, blind_initial)"
            "VALUES (%(nom_table)s, %(nb_sieges_max)s, %(blind_initial)s)"
            "RETURNING id_table;",
            {
                "nom_table": "Table VIP",
                "nb_sieges_max": 6,
                "blind_initial": 10.0
            }
        )

    def test_creer_failure(self):
        """Test de création d'une table avec échec"""
        # Setup
        table = Table(nom_table="Table VIP", nb_sieges_max=6, blind_initial=10.0)
        self.mock_cursor.fetchone.return_value = None
        
        # Execution
        result = self.table_dao.creer(table)
        
        # Vérifications
        self.assertFalse(result)
        self.assertIsNone(table.id_table)

    def test_trouver_par_id_success(self):
        """Test de recherche par ID avec succès"""
        # Setup
        mock_table_data = {
            "id_table": 1,
            "nom_table": "Table VIP",
            "nb_sieges_max": 6,
            "blind_initial": 10.0
        }
        self.mock_cursor.fetchone.return_value = mock_table_data
        
        # Execution
        result = self.table_dao.trouver_par_id(1)
        
        # Vérifications
        self.assertIsNotNone(result)
        self.assertEqual(result.id_table, 1)
        self.assertEqual(result.nom_table, "Table VIP")
        self.assertEqual(result.nb_sieges_max, 6)
        self.assertEqual(result.blind_initial, 10.0)
        
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT id_table, nom_table, nb_sieges_max, blind_initial "
            "FROM tables "
            "WHERE id_table = %(id_table)s;",
            {"id_table": 1}
        )

    def test_trouver_par_id_not_found(self):
        """Test de recherche par ID quand la table n'existe pas"""
        # Setup
        self.mock_cursor.fetchone.return_value = None
        
        # Execution
        result = self.table_dao.trouver_par_id(999)
        
        # Vérifications
        self.assertIsNone(result)

    def test_mettre_a_jour_success(self):
        """Test de mise à jour d'une table avec succès"""
        # Setup
        table = Table(id_table=1, nom_table="Table VIP Modifiée", nb_sieges_max=8, blind_initial=20.0)
        self.mock_cursor.rowcount = 1
        
        # Execution
        result = self.table_dao.mettre_a_jour(table)
        
        # Vérifications
        self.assertTrue(result)
        self.mock_cursor.execute.assert_called_once_with(
            "UPDATE tables "
            "SET nom_table = %(nom_table)s, nb_sieges_max = %(nb_sieges_max)s, blind_initial = %(blind_initial)s "
            "WHERE id_table = %(id_table)s;",
            {
                "id_table": 1,
                "nom_table": "Table VIP Modifiée",
                "nb_sieges_max": 8,
                "blind_initial": 20.0
            }
        )

    def test_mettre_a_jour_failure(self):
        """Test de mise à jour d'une table avec échec"""
        # Setup
        table = Table(id_table=999, nom_table="Table Inexistante", nb_sieges_max=6, blind_initial=10.0)
        self.mock_cursor.rowcount = 0
        
        # Execution
        result = self.table_dao.mettre_a_jour(table)
        
        # Vérifications
        self.assertFalse(result)

    def test_supprimer_success(self):
        """Test de suppression d'une table avec succès"""
        # Setup
        self.mock_cursor.fetchone.return_value = {"count_parties_actives": 0}
        self.mock_cursor.rowcount = 1
        
        # Execution
        result = self.table_dao.supprimer(1)
        
        # Vérifications
        self.assertTrue(result)
        # Vérifie que deux appels execute ont été faits (vérification + suppression)
        self.assertEqual(self.mock_cursor.execute.call_count, 2)

    def test_supprimer_avec_parties_en_cours(self):
        """Test de suppression d'une table avec parties en cours"""
        # Setup
        self.mock_cursor.fetchone.return_value = {"count_parties_actives": 2}
        
        # Execution & Vérification
        with self.assertRaises(ValueError, msg="Impossible de supprimer une table avec des parties en cours"):
            self.table_dao.supprimer(1)

    def test_supprimer_table_inexistante(self):
        """Test de suppression d'une table qui n'existe pas"""
        # Setup
        self.mock_cursor.fetchone.return_value = {"count_parties_actives": 0}
        self.mock_cursor.rowcount = 0
        
        # Execution
        result = self.table_dao.supprimer(999)
        
        # Vérifications
        self.assertFalse(result)

    def test_supprimer_toutes_success(self):
        """Test de suppression de toutes les tables avec succès"""
        # Setup
        self.mock_cursor.fetchone.return_value = {"count_parties_actives": 0}
        self.mock_cursor.rowcount = 3
        
        # Execution
        result = self.table_dao.supprimer_toutes()
        
        # Vérifications
        self.assertTrue(result)
        self.assertEqual(self.mock_cursor.execute.call_count, 2)

    def test_supprimer_toutes_avec_parties_en_cours(self):
        """Test de suppression de toutes les tables avec parties en cours"""
        # Setup
        self.mock_cursor.fetchone.return_value = {"count_parties_actives": 1}
        
        # Execution & Vérification
        with self.assertRaises(ValueError, msg="Impossible de supprimer les tables avec des parties en cours"):
            self.table_dao.supprimer_toutes()

    def test_lister_toutes(self):
        """Test de listage de toutes les tables"""
        # Setup
        mock_tables_data = [
            {"id_table": 1, "nom_table": "Table 1", "nb_sieges_max": 6, "blind_initial": 10.0},
            {"id_table": 2, "nom_table": "Table 2", "nb_sieges_max": 8, "blind_initial": 20.0},
            {"id_table": 3, "nom_table": "Table 3", "nb_sieges_max": 4, "blind_initial": 5.0}
        ]
        self.mock_cursor.fetchall.return_value = mock_tables_data
        
        # Execution
        result = self.table_dao.lister_toutes()
        
        # Vérifications
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].id_table, 1)
        self.assertEqual(result[0].nom_table, "Table 1")
        self.assertEqual(result[1].nb_sieges_max, 8)
        self.assertEqual(result[2].blind_initial, 5.0)
        
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT id_table, nom_table, nb_sieges_max, blind_initial "
            "FROM tables "
            "ORDER BY id_table;"
        )

    def test_lister_tables_avec_sieges_disponibles(self):
        """Test de listage des tables avec sièges disponibles"""
        # Setup
        mock_tables_disponibles = [
            {
                "id_table": 1,
                "nom_table": "Table VIP",
                "nb_sieges_max": 6,
                "blind_initial": 10.0,
                "sieges_occupes": 4,
                "sieges_disponibles": 2
            },
            {
                "id_table": 2,
                "nom_table": "Table Libre",
                "nb_sieges_max": 8,
                "blind_initial": 20.0,
                "sieges_occupes": 0,
                "sieges_disponibles": 8
            }
        ]
        self.mock_cursor.fetchall.return_value = mock_tables_disponibles
        
        # Execution
        result = self.table_dao.lister_tables_avec_sieges_disponibles()
        
        # Vérifications
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id_table"], 1)
        self.assertEqual(result[0]["nom_table"], "Table VIP")
        self.assertEqual(result[0]["sieges_occupes"], 4)
        self.assertEqual(result[0]["sieges_disponibles"], 2)
        self.assertEqual(result[1]["sieges_disponibles"], 8)

    def test_lister_tables_avec_sieges_disponibles_vide(self):
        """Test de listage des tables avec sièges disponibles quand aucune table disponible"""
        # Setup
        self.mock_cursor.fetchall.return_value = []
        
        # Execution
        result = self.table_dao.lister_tables_avec_sieges_disponibles()
        
        # Vérifications
        self.assertEqual(result, [])

    def test_compter_tables(self):
        """Test du comptage des tables"""
        # Setup
        self.mock_cursor.fetchone.return_value = {"count": 5}
        
        # Execution
        result = self.table_dao.compter_tables()
        
        # Vérifications
        self.assertEqual(result, 5)
        self.mock_cursor.execute.assert_called_once_with("SELECT COUNT(*) as count FROM tables;")

    def test_compter_tables_zero(self):
        """Test du comptage des tables quand il n'y en a aucune"""
        # Setup
        self.mock_cursor.fetchone.return_value = {"count": 0}
        
        # Execution
        result = self.table_dao.compter_tables()
        
        # Vérifications
        self.assertEqual(result, 0)

    @patch('dao.table_dao.logging')
    def test_exception_handling(self, mock_logging):
        """Test de la gestion des exceptions"""
        # Setup
        self.mock_cursor.execute.side_effect = Exception("Database error")
        
        # Execution
        result = self.table_dao.trouver_par_id(1)
        
        # Vérifications
        self.assertIsNone(result)
        mock_logging.info.assert_called()

    def test_lister_toutes_vide(self):
        """Test de listage quand il n'y a aucune table"""
        # Setup
        self.mock_cursor.fetchall.return_value = []
        
        # Execution
        result = self.table_dao.lister_toutes()
        
        # Vérifications
        self.assertEqual(result, [])

class TestTableDaoIntegration(unittest.TestCase):
    """Tests d'intégration avec une base de données réelle"""
    
    @pytest.mark.integration
    def test_cycle_complet_table(self):
        """Test d'intégration complet du cycle de vie d'une table"""
        # Note: Ce test nécessite une base de données de test configurée
        pass

    @pytest.mark.integration
    def test_requete_complexe_sieges_disponibles(self):
        """Test d'intégration de la requête complexe pour les sièges disponibles"""
        # Note: À implémenter avec une DB de test réelle
        pass

if __name__ == '__main__':
    unittest.main()