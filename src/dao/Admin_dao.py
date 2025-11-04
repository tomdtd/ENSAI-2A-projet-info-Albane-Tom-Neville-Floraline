import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.admin import Admin

class AdminDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Administrateurs de la base de données"""

    @log
    def trouver_par_id(self, admin_id: int) -> Optional[Admin]:
        """Trouver un administrateur par son ID

        Parameters
        ----------
        admin_id : int

        Returns
        -------
        admin : Admin
            L'administrateur trouvé
            None si aucun administrateur ne correspond à l'id
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT admin_id, name, mdp, mail "
                        "FROM admins "
                        "WHERE admin_id = %(admin_id)s;",
                        {"admin_id": admin_id},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        admin = None
        if res:
            admin = Admin(
                admin_id=res["admin_id"],
                name=res["name"],
                mdp=res["mdp"],
                mail=res["mail"],
            )

        return admin

    @log
    def trouver_par_nom(self, name: str) -> Optional[Admin]:
        """Trouver un administrateur par son nom

        Parameters
        ----------
        name : str

        Returns
        -------
        admin : Admin
            L'administrateur trouvé
            None si aucun administrateur ne correspond au nom
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT admin_id, name, mdp, mail "
                        "FROM admins "
                        "WHERE name = %(name)s;",
                        {"name": name},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        admin = None
        if res:
            admin = Admin(
                admin_id=res["admin_id"],
                name=res["name"],
                mdp=res["mdp"],
                mail=res["mail"],
            )

        return admin

    @log
    def verifier_identifiants(self, name: str, mdp: str) -> Optional[Admin]:
        """Vérifier les identifiants de connexion d'un administrateur

        Parameters
        ----------
        name : str
        mdp : str

        Returns
        -------
        admin : Admin
            L'administrateur si les identifiants sont corrects
            None sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT admin_id, name, mdp, mail "
                        "FROM admins "
                        "WHERE name = %(name)s AND mdp = %(mdp)s;",
                        {"name": name, "mdp": mdp},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        admin = None
        if res:
            admin = Admin(
                admin_id=res["admin_id"],
                name=res["name"],
                mdp=res["mdp"],
                mail=res["mail"],
            )

        return admin

    @log
    def changer_mot_de_passe(self, admin_id: int, nouveau_mdp: str) -> bool:
        """Changer le mot de passe d'un administrateur

        Parameters
        ----------
        admin_id : int
        nouveau_mdp : str

        Returns
        -------
        updated : bool
            True si la mise à jour est un succès
            False sinon
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE admins "
                        "SET mdp = %(nouveau_mdp)s "
                        "WHERE admin_id = %(admin_id)s;",
                        {
                            "admin_id": admin_id,
                            "nouveau_mdp": nouveau_mdp,
                        }
                    )
                    updated = cursor.rowcount > 0
        except Exception as e:
            logging.info(e)
            updated = False

        return updated

    # === GESTION DES TRANSACTIONS ===

    @log
    def valider_transaction(self, id_transaction: int) -> bool:
        """Valider une transaction financière

        Parameters
        ----------
        id_transaction : int

        Returns
        -------
        validated : bool
            True si la validation est un succès
            False sinon
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Marquer la transaction comme validée
                    cursor.execute(
                        "UPDATE transactions "
                        "SET statut = 'validee', date_validation = %(date_validation)s "
                        "WHERE id_transaction = %(id_transaction)s AND statut = 'en_attente';",
                        {
                            "id_transaction": id_transaction,
                            "date_validation": datetime.now(),
                        }
                    )
                    validated = cursor.rowcount > 0
                    
                    # Si c'est un dépôt, créditer le joueur
                    if validated:
                        cursor.execute(
                            """
                            UPDATE joueurs j
                            SET credit = j.credit + t.montant
                            FROM transactions t
                            WHERE t.id_transaction = %(id_transaction)s 
                            AND t.id_joueur = j.id_joueur 
                            AND t.type_transaction = 'depot';
                            """,
                            {"id_transaction": id_transaction},
                        )
        except Exception as e:
            logging.info(e)
            validated = False

        return validated

    @log
    def lister_transactions_en_attente(self) -> List[Dict]:
        """Lister toutes les transactions en attente de validation

        Returns
        -------
        list[dict]
            Liste des transactions en attente
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT t.id_transaction, j.pseudo, t.type_transaction, 
                               t.montant, t.date_transaction, t.statut
                        FROM transactions t
                        JOIN joueurs j ON t.id_joueur = j.id_joueur
                        WHERE t.statut = 'en_attente'
                        ORDER BY t.date_transaction DESC;
                        """
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)

        return list(res) if res else []

    # === GESTION DES JOUEURS ===

    @log
    def banir_joueur(self, id_joueur: int, raison: str) -> bool:
        """Bannir un joueur

        Parameters
        ----------
        id_joueur : int
        raison : str

        Returns
        -------
        banned : bool
            True si le bannissement est un succès
            False sinon
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Marquer le joueur comme banni
                    cursor.execute(
                        "UPDATE joueurs "
                        "SET est_banni = TRUE, date_bannissement = %(date_bannissement)s, raison_bannissement = %(raison)s "
                        "WHERE id_joueur = %(id_joueur)s;",
                        {
                            "id_joueur": id_joueur,
                            "date_bannissement": datetime.now(),
                            "raison": raison,
                        }
                    )
                    banned = cursor.rowcount > 0
        except Exception as e:
            logging.info(e)
            banned = False

        return banned

    @log
    def debannir_joueur(self, id_joueur: int) -> bool:
        """Débannir un joueur

        Parameters
        ----------
        id_joueur : int

        Returns
        -------
        unbanned : bool
            True si le débannissement est un succès
            False sinon
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE joueurs "
                        "SET est_banni = FALSE, date_bannissement = NULL, raison_bannissement = NULL "
                        "WHERE id_joueur = %(id_joueur)s;",
                        {"id_joueur": id_joueur},
                    )
                    unbanned = cursor.rowcount > 0
        except Exception as e:
            logging.info(e)
            unbanned = False

        return unbanned

    # === STATISTIQUES INDIVIDUELLES ===

    @log
    def obtenir_statistiques_joueur(self, id_joueur: int) -> Dict:
        """Obtenir les statistiques détaillées d'un joueur

        Parameters
        ----------
        id_joueur : int

        Returns
        -------
        dict
            Statistiques du joueur
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 
                            j.pseudo,
                            j.email,
                            j.credit,
                            j.date_creation,
                            j.est_banni,
                            
                            -- Statistiques des parties
                            COUNT(DISTINCT jp.id_partie) as total_parties,
                            COUNT(DISTINCT CASE WHEN jp.gain_perte > 0 THEN jp.id_partie END) as parties_gagnees,
                            COUNT(DISTINCT CASE WHEN jp.gain_perte < 0 THEN jp.id_partie END) as parties_perdues,
                            COUNT(DISTINCT CASE WHEN jp.gain_perte = 0 THEN jp.id_partie END) as parties_egales,
                            
                            -- Gains/Pertes
                            COALESCE(SUM(jp.gain_perte), 0) as total_gain_perte,
                            COALESCE(MAX(jp.gain_perte), 0) as gain_max,
                            COALESCE(MIN(jp.gain_perte), 0) as perte_max,
                            
                            -- Tables jouées
                            COUNT(DISTINCT p.id_table) as tables_differentes,
                            
                            -- Statistiques transactions
                            COUNT(DISTINCT t.id_transaction) as total_transactions,
                            COALESCE(SUM(CASE WHEN t.type_transaction = 'depot' THEN t.montant ELSE 0 END), 0) as total_depots,
                            COALESCE(SUM(CASE WHEN t.type_transaction = 'retrait' THEN t.montant ELSE 0 END), 0) as total_retraits,
                            COALESCE(SUM(CASE WHEN t.type_transaction = 'gain_partie' THEN t.montant ELSE 0 END), 0) as total_gains_parties
                            
                        FROM joueurs j
                        LEFT JOIN joueurs_parties jp ON j.id_joueur = jp.id_joueur
                        LEFT JOIN parties p ON jp.id_partie = p.id_partie
                        LEFT JOIN transactions t ON j.id_joueur = t.id_joueur
                        WHERE j.id_joueur = %(id_joueur)s
                        GROUP BY j.id_joueur, j.pseudo, j.email, j.credit, j.date_creation, j.est_banni;
                        """,
                        {"id_joueur": id_joueur},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        return dict(res) if res else {}

    @log
    def obtenir_tables_jouees_par_joueur(self, id_joueur: int) -> List[Dict]:
        """Obtenir la liste des tables auxquelles un joueur a joué

        Parameters
        ----------
        id_joueur : int

        Returns
        -------
        list[dict]
            Liste des tables jouées
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT DISTINCT 
                            t.id_table,
                            t.nom_table,
                            t.blind_initial,
                            COUNT(DISTINCT jp.id_partie) as nb_parties,
                            MIN(p.date_debut) as premiere_partie,
                            MAX(p.date_debut) as derniere_partie
                        FROM tables t
                        JOIN parties p ON t.id_table = p.id_table
                        JOIN joueurs_parties jp ON p.id_partie = jp.id_partie
                        WHERE jp.id_joueur = %(id_joueur)s
                        GROUP BY t.id_table, t.nom_table, t.blind_initial
                        ORDER BY derniere_partie DESC;
                        """,
                        {"id_joueur": id_joueur},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)

        return list(res) if res else []

    # === STATISTIQUES COLLECTIVES ===

    @log
    def obtenir_statistiques_globales(self) -> Dict:
        """Obtenir les statistiques globales de la plateforme

        Returns
        -------
        dict
            Statistiques globales
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 
                            -- Joueurs
                            COUNT(*) as total_joueurs,
                            COUNT(CASE WHEN est_banni THEN 1 END) as joueurs_bannis,
                            COUNT(CASE WHEN est_admin THEN 1 END) as total_admins,
                            AVG(credit) as credit_moyen,
                            
                            -- Parties
                            COUNT(DISTINCT id_partie) as total_parties,
                            COUNT(DISTINCT CASE WHEN statut_partie = 'terminee' THEN id_partie END) as parties_terminees,
                            COUNT(DISTINCT CASE WHEN statut_partie = 'en_cours' THEN id_partie END) as parties_en_cours,
                            COUNT(DISTINCT CASE WHEN statut_partie = 'en_attente' THEN id_partie END) as parties_en_attente,
                            AVG(pot_total) as pot_moyen,
                            SUM(pot_total) as pot_total_global,
                            
                            -- Tables
                            COUNT(DISTINCT id_table) as total_tables,
                            AVG(nb_sieges_max) as sieges_moyens,
                            
                            -- Transactions
                            COUNT(DISTINCT id_transaction) as total_transactions,
                            SUM(CASE WHEN type_transaction = 'depot' THEN montant ELSE 0 END) as total_depots_platforme,
                            SUM(CASE WHEN type_transaction = 'retrait' THEN montant ELSE 0 END) as total_retraits_platforme,
                            SUM(CASE WHEN type_transaction = 'gain_partie' THEN montant ELSE 0 END) as total_gains_parties_platforme
                            
                        FROM (
                            SELECT j.id_joueur, j.est_banni, j.est_admin, j.credit FROM joueurs j
                        ) j
                        CROSS JOIN (
                            SELECT p.id_partie, p.statut_partie, p.pot_total FROM parties p
                        ) p
                        CROSS JOIN (
                            SELECT t.id_table, t.nb_sieges_max FROM tables t
                        ) t
                        CROSS JOIN (
                            SELECT tr.id_transaction, tr.type_transaction, tr.montant FROM transactions tr
                        ) tr;
                        """
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        return dict(res) if res else {}

    @log
    def obtenir_top_joueurs(self, limite: int = 10) -> List[Dict]:
        """Obtenir le classement des meilleurs joueurs

        Parameters
        ----------
        limite : int, optional
            Nombre de joueurs à retourner, par défaut 10

        Returns
        -------
        list[dict]
            Classement des joueurs
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 
                            j.pseudo,
                            j.credit,
                            COUNT(DISTINCT jp.id_partie) as total_parties,
                            COUNT(DISTINCT CASE WHEN jp.gain_perte > 0 THEN jp.id_partie END) as parties_gagnees,
                            COALESCE(SUM(jp.gain_perte), 0) as total_gains,
                            ROUND(COUNT(DISTINCT CASE WHEN jp.gain_perte > 0 THEN jp.id_partie END) * 100.0 / 
                                  NULLIF(COUNT(DISTINCT jp.id_partie), 0), 2) as taux_victoire
                        FROM joueurs j
                        LEFT JOIN joueurs_parties jp ON j.id_joueur = jp.id_joueur
                        WHERE j.est_banni = FALSE
                        GROUP BY j.id_joueur, j.pseudo, j.credit
                        ORDER BY total_gains DESC, taux_victoire DESC
                        LIMIT %(limite)s;
                        """,
                        {"limite": limite},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)

        return list(res) if res else []

    @log
    def obtenir_activite_recente(self, jours: int = 7) -> Dict:
        """Obtenir les statistiques d'activité récente

        Parameters
        ----------
        jours : int, optional
            Nombre de jours à analyser, par défaut 7

        Returns
        -------
        dict
            Statistiques d'activité récente
        """

        res = None
        date_limite = datetime.now() - timedelta(days=jours)

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 
                            -- Nouveaux joueurs
                            COUNT(CASE WHEN j.date_creation >= %(date_limite)s THEN 1 END) as nouveaux_joueurs,
                            
                            -- Parties récentes
                            COUNT(CASE WHEN p.date_debut >= %(date_limite)s THEN 1 END) as parties_debutees,
                            COUNT(CASE WHEN p.date_fin >= %(date_limite)s THEN 1 END) as parties_terminees,
                            
                            -- Transactions récentes
                            COUNT(CASE WHEN t.date_transaction >= %(date_limite)s THEN 1 END) as transactions_recentes,
                            SUM(CASE WHEN t.date_transaction >= %(date_limite)s THEN t.montant ELSE 0 END) as volume_transactions_recent
                            
                        FROM joueurs j
                        CROSS JOIN parties p
                        CROSS JOIN transactions t
                        WHERE p.date_debut >= %(date_limite)s OR p.date_fin >= %(date_limite)s 
                           OR t.date_transaction >= %(date_limite)s OR j.date_creation >= %(date_limite)s;
                        """,
                        {"date_limite": date_limite},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        return dict(res) if res else {}