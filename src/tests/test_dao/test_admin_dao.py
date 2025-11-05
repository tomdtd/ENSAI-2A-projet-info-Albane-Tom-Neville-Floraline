import unittest
import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

from dao.Admin_dao import AdminDao
from business_object.admin import Admin

class TestAdminDao(unittest.TestCase):

    def setUp(self):
        """Setup avant chaque test"""
        self.admin_dao = AdminDao()
        self.admin_dao._get_connection = Mock()
        
        # Mock de la connexion et du curseur
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.admin_dao._get_connection.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_connection.__enter__ = Mock(return_value=self.mock_connection)
        self.mock_connection.__exit__ = Mock(return_value=None)

    def test_trouver_par_id_success(self):
        """Test de trouver_par_id avec succès"""
        # Données mock
        mock_admin_data = {
            "id_admin": 1,
            "nom_admin": "admin1",
            "mot_de_passe_hash": "hash123",
            "email": "admin1@test.com"
        }
        self.mock_cursor.fetchone.return_value = mock_admin_data
        
        # Appel de la méthode
        result = self.admin_dao.trouver_par_id(1)
        
        # Vérifications
        self.assertIsNotNone(result)
        self.assertEqual(result.admin_id, 1)
        self.assertEqual(result.name, "admin1")
        self.assertEqual(result.mdp, "hash123")
        self.assertEqual(result.mail, "admin1@test.com")
        
        # Vérification de l'appel SQL
        self.mock_cursor.execute.assert_called_once()
        call_args = self.mock_cursor.execute.call_args[0][1]
        self.assertEqual(call_args["admin_id"], 1)

    def test_trouver_par_id_not_found(self):
        """Test de trouver_par_id quand l'admin n'existe pas"""
        self.mock_cursor.fetchone.return_value = None
        
        result = self.admin_dao.trouver_par_id(9999)
        
        self.assertIsNone(result)

    def test_trouver_par_nom_success(self):
        """Test de trouver_par_nom avec succès"""
        mock_admin_data = {
            "id_admin": 2,
            "nom_admin": "admin2",
            "mot_de_passe_hash": "hash456",
            "email": "admin2@test.com"
        }
        self.mock_cursor.fetchone.return_value = mock_admin_data
        
        result = self.admin_dao.trouver_par_nom("admin2")
        
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "admin2")
        self.mock_cursor.execute.assert_called_once()

    def test_verifier_identifiants_success(self):
        """Test de vérification d'identifiants avec succès"""
        mock_admin_data = {
            "id_admin": 1,
            "nom_admin": "admin1",
            "mot_de_passe_hash": "correct_hash",
            "email": "admin1@test.com"
        }
        self.mock_cursor.fetchone.return_value = mock_admin_data
        
        result = self.admin_dao.verifier_identifiants("admin1", "correct_hash")
        
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "admin1")
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT id_admin, nom_admin, mot_de_passe_hash, email FROM administrateurs WHERE nom_admin = %(nom_admin)s AND mot_de_passe_hash = %(mot_de_passe_hash)s;",
            {"nom_admin": "admin1", "mot_de_passe_hash": "correct_hash"}
        )

    def test_verifier_identifiants_failure(self):
        """Test de vérification d'identifiants avec échec"""
        self.mock_cursor.fetchone.return_value = None
        
        result = self.admin_dao.verifier_identifiants("admin1", "wrong_hash")
        
        self.assertIsNone(result)

    def test_changer_mot_de_passe_success(self):
        """Test de changement de mot de passe avec succès"""
        self.mock_cursor.rowcount = 1
        
        result = self.admin_dao.changer_mot_de_passe(1, "new_hash")
        
        self.assertTrue(result)
        self.mock_cursor.execute.assert_called_once_with(
            "UPDATE administrateurs SET mot_de_passe_hash = %(nouveau_mot_de_passe_hash)s WHERE id_admin = %(admin_id)s;",
            {"admin_id": 1, "nouveau_mot_de_passe_hash": "new_hash"}
        )

    def test_changer_mot_de_passe_failure(self):
        """Test de changement de mot de passe avec échec"""
        self.mock_cursor.rowcount = 0
        
        result = self.admin_dao.changer_mot_de_passe(999, "new_hash")
        
        self.assertFalse(result)

    def test_valider_transaction_success(self):
        """Test de validation de transaction avec succès"""
        self.mock_cursor.rowcount = 1
        
        result = self.admin_dao.valider_transaction(1)
        
        self.assertTrue(result)
        # Vérifie que deux appels execute ont été faits (update + credit)
        self.assertEqual(self.mock_cursor.execute.call_count, 2)

    def test_valider_transaction_failure(self):
        """Test de validation de transaction avec échec"""
        self.mock_cursor.rowcount = 0
        
        result = self.admin_dao.valider_transaction(999)
        
        self.assertFalse(result)

    def test_lister_transactions_en_attente(self):
        """Test de listage des transactions en attente"""
        mock_transactions = [
            {
                "id_transaction": 1,
                "pseudo": "joueur1",
                "type_transaction": "depot",
                "montant": 100.0,
                "date_transaction": datetime.now(),
                "statut": "en_attente"
            },
            {
                "id_transaction": 2,
                "pseudo": "joueur2",
                "type_transaction": "retrait",
                "montant": 50.0,
                "date_transaction": datetime.now(),
                "statut": "en_attente"
            }
        ]
        self.mock_cursor.fetchall.return_value = mock_transactions
        
        result = self.admin_dao.lister_transactions_en_attente()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["pseudo"], "joueur1")
        self.assertEqual(result[1]["type_transaction"], "retrait")

    def test_banir_joueur_success(self):
        """Test de bannissement d'un joueur avec succès"""
        # Mock des données du joueur
        mock_joueur_data = {
            "pseudo": "joueur1",
            "mot_de_passe_hash": "hash123",
            "email": "joueur1@test.com",
            "credit": 100.0
        }
        self.mock_cursor.fetchone.return_value = mock_joueur_data
        
        result = self.admin_dao.banir_joueur(1, 1, "Comportement inapproprié")
        
        self.assertTrue(result)
        # Vérifie que trois appels execute ont été faits (select + insert + delete)
        self.assertEqual(self.mock_cursor.execute.call_count, 3)

    def test_banir_joueur_not_found(self):
        """Test de bannissement d'un joueur qui n'existe pas"""
        self.mock_cursor.fetchone.return_value = None
        
        with self.assertRaises(ValueError):
            self.admin_dao.banir_joueur(99999, 1, "Raison")

    def test_debannir_joueur_success(self):
        """Test de débannissement d'un joueur avec succès"""
        mock_joueur_banni_data = {
            "pseudo": "joueur1",
            "mot_de_passe_hash": "hash123",
            "email": "joueur1@test.com",
            "credit": 100.0
        }
        self.mock_cursor.fetchone.side_effect = [mock_joueur_banni_data, [0]]  # Existe pas dans joueurs
        
        result = self.admin_dao.debannir_joueur("joueur1")
        
        self.assertTrue(result)
        # Vérifie que quatre appels execute ont été faits (select joueur_banni + count + insert + delete)
        self.assertEqual(self.mock_cursor.execute.call_count, 4)

    def test_debannir_joueur_pseudo_existe_deja(self):
        """Test de débannissement quand le pseudo existe déjà"""
        mock_joueur_banni_data = {
            "pseudo": "joueur1",
            "mot_de_passe_hash": "hash123",
            "email": "joueur1@test.com",
            "credit": 100.0
        }
        self.mock_cursor.fetchone.side_effect = [mock_joueur_banni_data, [1]]  # Existe dans joueurs
        
        with self.assertRaises(ValueError):
            self.admin_dao.debannir_joueur("joueur1")

    def test_lister_joueurs_banis(self):
        """Test de listage des joueurs bannis"""
        mock_joueurs_banis = [
            {
                "pseudo": "joueur1",
                "email": "joueur1@test.com",
                "credit": 100.0,
                "date_ban": datetime.now(),
                "raison_ban": "Triche",
                "admin_banisseur": "admin1"
            }
        ]
        self.mock_cursor.fetchall.return_value = mock_joueurs_banis
        
        result = self.admin_dao.lister_joueurs_banis()
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["pseudo"], "joueur1")
        self.assertEqual(result[0]["raison_ban"], "Triche")

    def test_obtenir_statistiques_joueur(self):
        """Test d'obtention des statistiques d'un joueur"""
        mock_stats = {
            "pseudo": "joueur1",
            "email": "joueur1@test.com",
            "credit": 150.0,
            "date_creation": datetime.now(),
            "total_parties": 10,
            "parties_gagnees": 6,
            "parties_perdues": 4,
            "total_gain_perte": 50.0,
            "tables_differentes": 3,
            "total_transactions": 5
        }
        self.mock_cursor.fetchone.return_value = mock_stats
        
        result = self.admin_dao.obtenir_statistiques_joueur(1)
        
        self.assertEqual(result["pseudo"], "joueur1")
        self.assertEqual(result["total_parties"], 10)
        self.assertEqual(result["parties_gagnees"], 6)

    def test_obtenir_tables_jouees_par_joueur(self):
        """Test d'obtention des tables jouées par un joueur"""
        mock_tables = [
            {
                "id_table": 1,
                "nom_table": "Table VIP",
                "blind_initial": 10.0,
                "nb_parties": 5,
                "premiere_partie": datetime.now() - timedelta(days=10),
                "derniere_partie": datetime.now()
            }
        ]
        self.mock_cursor.fetchall.return_value = mock_tables
        
        result = self.admin_dao.obtenir_tables_jouees_par_joueur(1)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["nom_table"], "Table VIP")
        self.assertEqual(result[0]["nb_parties"], 5)

    def test_obtenir_statistiques_globales(self):
        """Test d'obtention des statistiques globales"""
        mock_stats_globales = {
            "total_joueurs": 100,
            "total_joueurs_banis": 5,
            "total_admins": 3,
            "total_parties": 500,
            "parties_terminees": 450,
            "parties_en_cours": 10,
            "pot_total_global": 10000.0
        }
        self.mock_cursor.fetchone.return_value = mock_stats_globales
        
        result = self.admin_dao.obtenir_statistiques_globales()
        
        self.assertEqual(result["total_joueurs"], 100)
        self.assertEqual(result["total_joueurs_banis"], 5)
        self.assertEqual(result["total_parties"], 500)

    def test_obtenir_top_joueurs(self):
        """Test d'obtention du classement des meilleurs joueurs"""
        mock_top_joueurs = [
            {
                "pseudo": "champion",
                "credit": 1000.0,
                "total_parties": 50,
                "parties_gagnees": 30,
                "total_gains": 500.0,
                "taux_victoire": 60.0
            },
            {
                "pseudo": "pro",
                "credit": 800.0,
                "total_parties": 40,
                "parties_gagnees": 22,
                "total_gains": 300.0,
                "taux_victoire": 55.0
            }
        ]
        self.mock_cursor.fetchall.return_value = mock_top_joueurs
        
        result = self.admin_dao.obtenir_top_joueurs(limite=5)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["pseudo"], "champion")
        self.assertEqual(result[0]["taux_victoire"], 60.0)

    def test_obtenir_activite_recente(self):
        """Test d'obtention de l'activité récente"""
        mock_activite = {
            "nouveaux_joueurs": 5,
            "parties_debutees": 20,
            "parties_terminees": 18,
            "transactions_recentes": 15,
            "volume_transactions_recent": 1500.0,
            "bannissements_recents": 1
        }
        self.mock_cursor.fetchone.return_value = mock_activite
        
        result = self.admin_dao.obtenir_activite_recente(jours=7)
        
        self.assertEqual(result["nouveaux_joueurs"], 5)
        self.assertEqual(result["parties_debutees"], 20)
        self.assertEqual(result["bannissements_recents"], 1)

    @patch('dao.admin_dao.logging')
    def test_exception_handling(self, mock_logging):
        """Test de la gestion des exceptions"""
        self.mock_cursor.execute.side_effect = Exception("Database error")
        
        # Test avec une méthode quelconque
        result = self.admin_dao.trouver_par_id(1)
        
        self.assertIsNone(result)
        mock_logging.info.assert_called()

class TestAdminDaoIntegration(unittest.TestCase):
    """Tests d'intégration avec une base de données réelle (nécessite une DB de test)"""
    
    @pytest.mark.integration
    def test_cycle_complet_bannissement(self):
        """Test d'intégration complet du cycle de bannissement"""
        # Note: Ce test nécessite une base de données de test configurée
        # avec des données appropriées
        pass

    @pytest.mark.integration  
    def test_verification_identifiants_reels(self):
        """Test d'intégration de vérification d'identifiants avec une vraie DB"""
        # Note: À implémenter avec une DB de test
        pass

if __name__ == '__main__':
    # Exécution des tests unitaires
    unittest.main()