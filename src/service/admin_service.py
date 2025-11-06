from typing import Optional, List, Dict
from utils.log_decorator import log
from dao.Admin_dao import AdminDao
from business_object.admin import Admin
from utils.securite import hash_password, verify_password

class AdminService:
    """Classe contenant les méthodes de service pour les administrateurs."""

    @log
    def trouver_par_id(self, admin_id: int) -> Optional[Admin]:
        """Trouver un administrateur par son ID."""
        return AdminDao().trouver_par_id(admin_id)

    @log
    def trouver_par_nom(self, nom_admin: str) -> Optional[Admin]:
        """Trouver un administrateur par son nom."""
        return AdminDao().trouver_par_nom(nom_admin)

    @log
    def verifier_identifiants(self, nom_admin: str, mot_de_passe: str) -> Optional[Admin]:
        """Vérifier les identifiants de connexion d'un administrateur."""
        admin = AdminDao().trouver_par_nom(nom_admin)
        if admin and verify_password(mot_de_passe, admin.mdp, nom_admin):
            return admin
        return None

    @log
    def changer_mot_de_passe(self, admin_id: int, ancien_mot_de_passe: str, nouveau_mot_de_passe: str) -> bool:
        """Changer le mot de passe d'un administrateur."""
        admin = AdminDao().trouver_par_id(admin_id)
        if not admin:
            return False

        if not verify_password(ancien_mot_de_passe, admin.mdp, admin.nom):
            return False

        nouveau_mot_de_passe_hash = hash_password(nouveau_mot_de_passe, admin.nom)
        return AdminDao().changer_mot_de_passe(admin_id, nouveau_mot_de_passe_hash)

    @log
    def valider_transaction(self, id_transaction: int) -> bool:
        """Valider une transaction financière."""
        return AdminDao().valider_transaction(id_transaction)

    @log
    def lister_transactions_en_attente(self) -> List[Dict]:
        """Lister toutes les transactions en attente de validation."""
        return AdminDao().lister_transactions_en_attente()

    @log
    def banir_joueur(self, id_joueur: int, id_admin: int, raison_ban: str) -> bool:
        """Bannir un joueur en le déplaçant vers la table joueurs_banis."""
        if not raison_ban.strip():
            raise ValueError("La raison du bannissement ne peut pas être vide.")
        return AdminDao().banir_joueur(id_joueur, id_admin, raison_ban)

    @log
    def debannir_joueur(self, pseudo: str) -> bool:
        """Débannir un joueur en le restaurant dans la table joueurs."""
        return AdminDao().debannir_joueur(pseudo)

    @log
    def lister_joueurs_banis(self) -> List[Dict]:
        """Lister tous les joueurs bannis."""
        return AdminDao().lister_joueurs_banis()

    @log
    def obtenir_statistiques_joueur(self, id_joueur: int) -> Dict:
        """Obtenir les statistiques détaillées d'un joueur."""
        return AdminDao().obtenir_statistiques_joueur(id_joueur)

    @log
    def obtenir_tables_jouees_par_joueur(self, id_joueur: int) -> List[Dict]:
        """Obtenir la liste des tables auxquelles un joueur a joué."""
        return AdminDao().obtenir_tables_jouees_par_joueur(id_joueur)

    @log
    def obtenir_statistiques_globales(self) -> Dict:
        """Obtenir les statistiques globales de la plateforme."""
        return AdminDao().obtenir_statistiques_globales()

    @log
    def obtenir_top_joueurs(self, limite: int = 10) -> List[Dict]:
        """Obtenir le classement des meilleurs joueurs, le top 10 par exemple."""
        return AdminDao().obtenir_top_joueurs(limite)

    @log
    def obtenir_activite_recente(self, jours: int = 7) -> Dict:
        """Obtenir les statistiques d'activité récente, sur la dernière semaine par exemple."""
        return AdminDao().obtenir_activite_recente(jours)
