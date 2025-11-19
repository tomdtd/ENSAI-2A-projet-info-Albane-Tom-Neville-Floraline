import logging
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from typing import Optional, List

from src.utils.log_decorator import log
from src.dao.admin_dao import AdminDao
from src.business_object.admin import Admin
from src.dao.db_connection import DBConnection


class TestAdminDao:
    """Tests pour la classe AdminDao"""

    def setup_method(self):
        """Initialisation avant chaque test"""
        # Réinitialiser le singleton
        AdminDao._instances = {}

    # =========================================================================
    # TESTS MÉTHODE CREER
    # =========================================================================

    def test_creer_admin_success(self):
        """Test création d'un admin réussie"""
        admin = Admin(nom="TestAdmin", mdp="password123", mail="test@admin.com")
        
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {"admin_id": 1}
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            result = dao.creer(admin)
            
            assert result is True
            assert admin.admin_id == 1
            mock_cursor.execute.assert_called_once()

    def test_creer_admin_avec_id_existant(self):
        """Test création avec un ID déjà défini (doit échouer)"""
        admin = Admin(nom="TestAdmin", mdp="password123", mail="test@admin.com", admin_id=5)
        
        dao = AdminDao()
        result = dao.creer(admin)
        
        assert result is False

    def test_creer_admin_exception(self):
        """Test création avec exception base de données"""
        admin = Admin(nom="TestAdmin", mdp="password123", mail="test@admin.com")
        
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_conn.__enter__.return_value.cursor.side_effect = Exception("DB Error")
            
            dao = AdminDao()
            result = dao.creer(admin)
            
            assert result is False

    # =========================================================================
    # TESTS MÉTHODE TROUVER_PAR_ID
    # =========================================================================

    def test_trouver_par_id_success(self):
        """Test recherche par ID réussie"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {
                "admin_id": 1,
                "nom": "AdminTest",
                "mdp": "pass123",
                "mail": "admin@test.com"
            }
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            admin = dao.trouver_par_id(1)
            
            assert admin is not None
            assert admin.admin_id == 1
            assert admin.nom == "AdminTest"

    def test_trouver_par_id_non_trouve(self):
        """Test recherche par ID non trouvé"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = None
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            admin = dao.trouver_par_id(999)
            
            assert admin is None

    def test_trouver_par_id_exception(self):
        """Test recherche par ID avec exception"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_conn.__enter__.return_value.cursor.side_effect = Exception("DB Error")
            
            dao = AdminDao()
            admin = dao.trouver_par_id(1)
            
            assert admin is None

    # =========================================================================
    # TESTS MÉTHODE TROUVER_PAR_NOM
    # =========================================================================

    def test_trouver_par_nom_success(self):
        """Test recherche par nom réussie"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {
                "admin_id": 1,
                "nom": "AdminTest",
                "mdp": "pass123",
                "mail": "admin@test.com"
            }
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            admin = dao.trouver_par_nom("AdminTest")
            
            assert admin is not None
            assert admin.nom == "AdminTest"

    def test_trouver_par_nom_non_trouve(self):
        """Test recherche par nom non trouvé"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = None
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            admin = dao.trouver_par_nom("Inexistant")
            
            assert admin is None

    # =========================================================================
    # TESTS MÉTHODE TROUVER_PAR_MAIL
    # =========================================================================

    def test_trouver_par_mail_success(self):
        """Test recherche par email réussie"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {
                "admin_id": 1,
                "nom": "AdminTest",
                "mdp": "pass123",
                "mail": "admin@test.com"
            }
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            admin = dao.trouver_par_mail("admin@test.com")
            
            assert admin is not None
            assert admin.mail == "admin@test.com"

    def test_trouver_par_mail_non_trouve(self):
        """Test recherche par email non trouvé"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = None
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            admin = dao.trouver_par_mail("inexistant@test.com")
            
            assert admin is None

    # =========================================================================
    # TESTS MÉTHODE LISTER_TOUS
    # =========================================================================

    def test_lister_tous_success(self):
        """Test listing de tous les admins"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = [
                {"admin_id": 1, "nom": "Admin1", "mdp": "pass1", "mail": "admin1@test.com"},
                {"admin_id": 2, "nom": "Admin2", "mdp": "pass2", "mail": "admin2@test.com"}
            ]
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            admins = dao.lister_tous()
            
            assert len(admins) == 2
            assert admins[0].nom == "Admin1"
            assert admins[1].nom == "Admin2"

    def test_lister_tous_vide(self):
        """Test listing quand aucun admin"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = []
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            admins = dao.lister_tous()
            
            assert len(admins) == 0

    def test_lister_tous_exception(self):
        """Test listing avec exception"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_conn.__enter__.return_value.cursor.side_effect = Exception("DB Error")
            
            dao = AdminDao()
            admins = dao.lister_tous()
            
            assert len(admins) == 0

    # =========================================================================
    # TESTS MÉTHODE MODIFIER
    # =========================================================================

    def test_modifier_admin_success(self):
        """Test modification d'un admin réussie"""
        admin = Admin(nom="AdminModifie", mdp="newpass", mail="new@test.com", admin_id=1)
        
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.rowcount = 1
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            result = dao.modifier(admin)
            
            assert result is True

    def test_modifier_admin_sans_id(self):
        """Test modification sans ID (doit échouer)"""
        admin = Admin(nom="AdminModifie", mdp="newpass", mail="new@test.com")
        
        dao = AdminDao()
        result = dao.modifier(admin)
        
        assert result is False

    def test_modifier_admin_non_trouve(self):
        """Test modification d'un admin inexistant"""
        admin = Admin(nom="AdminModifie", mdp="newpass", mail="new@test.com", admin_id=999)
        
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.rowcount = 0
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            result = dao.modifier(admin)
            
            assert result is False

    # =========================================================================
    # TESTS MÉTHODE SUPPRIMER
    # =========================================================================

    def test_supprimer_admin_success(self):
        """Test suppression d'un admin réussie"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.rowcount = 1
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            result = dao.supprimer(1)
            
            assert result is True

    def test_supprimer_admin_non_trouve(self):
        """Test suppression d'un admin inexistant"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.rowcount = 0
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            result = dao.supprimer(999)
            
            assert result is False

    # =========================================================================
    # TESTS MÉTHODE SE_CONNECTER
    # =========================================================================

    def test_se_connecter_success(self):
        """Test connexion réussie"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {
                "admin_id": 1,
                "nom": "AdminTest",
                "mdp": "password123",
                "mail": "admin@test.com"
            }
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            admin = dao.se_connecter("AdminTest", "password123")
            
            assert admin is not None
            assert admin.nom == "AdminTest"

    def test_se_connecter_mauvais_mot_de_passe(self):
        """Test connexion avec mauvais mot de passe"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = None
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            admin = dao.se_connecter("AdminTest", "wrongpassword")
            
            assert admin is None

    # =========================================================================
    # TESTS MÉTHODE CHANGER_MOT_DE_PASSE
    # =========================================================================

    def test_changer_mot_de_passe_success(self):
        """Test changement de mot de passe réussi"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {"admin_id": 1}
            mock_cursor.rowcount = 1
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            result = dao.changer_mot_de_passe(1, "oldpass", "newpass")
            
            assert result is True

    def test_changer_mot_de_passe_mauvais_ancien(self):
        """Test changement avec mauvais ancien mot de passe"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = None
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            result = dao.changer_mot_de_passe(1, "wrongpass", "newpass")
            
            assert result is False

    # =========================================================================
    # TESTS MÉTHODES DE BANNISSEMENT
    # =========================================================================

    def test_bannir_joueur_success(self):
        """Test bannissement d'un joueur réussi"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {"id_ban": 1}
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            result = dao.bannir_joueur(10, 1, "Tricherie", 7)
            
            assert result is True
            assert mock_cursor.execute.call_count == 2  # UPDATE + INSERT

    def test_bannir_joueur_permanent(self):
        """Test bannissement permanent"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {"id_ban": 1}
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            result = dao.bannir_joueur(10, 1, "Comportement toxique", None)
            
            assert result is True

    def test_debannir_joueur_success(self):
        """Test débannissement réussi"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.rowcount = 1
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            result = dao.debannir_joueur(10)
            
            assert result is True

    def test_est_joueur_banni_oui(self):
        """Test vérification joueur banni"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {"id_ban": 1, "date_fin_ban": None}
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            result = dao.est_joueur_banni(10)
            
            assert result is True

    def test_est_joueur_banni_non(self):
        """Test vérification joueur non banni"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = None
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            result = dao.est_joueur_banni(10)
            
            assert result is False

    def test_get_bannissement_actif_success(self):
        """Test récupération bannissement actif"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {
                "id_ban": 1,
                "id_joueur": 10,
                "raison_ban": "Tricherie",
                "admin_nom": "AdminTest",
                "joueur_pseudo": "JoueurTest"
            }
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            ban = dao.get_bannissement_actif(10)
            
            assert ban is not None
            assert ban["raison_ban"] == "Tricherie"

    def test_lister_joueurs_bannis_success(self):
        """Test listing des joueurs bannis"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = [
                {"id_ban": 1, "joueur_pseudo": "Joueur1", "raison_ban": "Raison1"},
                {"id_ban": 2, "joueur_pseudo": "Joueur2", "raison_ban": "Raison2"}
            ]
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            bannis = dao.lister_joueurs_bannis()
            
            assert len(bannis) == 2

    def test_lister_historique_bannissements_tous(self):
        """Test historique complet des bannissements"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = [
                {"id_ban": 1, "joueur_pseudo": "Joueur1"},
                {"id_ban": 2, "joueur_pseudo": "Joueur2"}
            ]
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            historique = dao.lister_historique_bannissements()
            
            assert len(historique) == 2

    def test_lister_historique_bannissements_par_admin(self):
        """Test historique des bannissements par admin"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = [
                {"id_ban": 1, "id_admin": 1, "joueur_pseudo": "Joueur1"}
            ]
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            historique = dao.lister_historique_bannissements(id_admin=1)
            
            assert len(historique) == 1

    def test_supprimer_bannissement_success(self):
        """Test suppression d'un bannissement"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.rowcount = 1
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            result = dao.supprimer_bannissement(1)
            
            assert result is True

    def test_nettoyer_bannissements_expires_success(self):
        """Test nettoyage des bannissements expirés"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.rowcount = 3
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            dao = AdminDao()
            result = dao.nettoyer_bannissements_expires()
            
            assert result == 3

    # =========================================================================
    # TESTS SINGLETON
    # =========================================================================

    def test_singleton_pattern(self):
        """Test que AdminDao est bien un singleton"""
        dao1 = AdminDao()
        dao2 = AdminDao()
        
        assert dao1 is dao2