import logging
import os
import pytest
from unittest.mock import patch 
from typing import Optional, List
from datetime import datetime, timedelta

from src.utils.log_decorator import log
from src.utils.reset_database import ResetDatabase
from src.utils.singleton import Singleton
from src.dao.db_connection import DBConnection
from src.business_object.admin import Admin



class AdminDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Administrateurs de la base de données"""

    @log
    def creer(self, admin: Admin) -> bool:
        """Création d'un administrateur dans la base de données

        Parameters
        ----------
        admin : Admin
            L'objet Admin à créer (admin_id doit être None)

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """
        # Vérifier que l'admin_id est None (pour éviter les créations avec ID forcé)
        if admin.admin_id is not None:
            logging.warning("Tentative de création d'un administrateur avec un ID déjà défini")
            return False

        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO admin (nom, mdp, mail) "
                        "VALUES (%(nom)s, %(mdp)s, %(mail)s) "
                        "RETURNING admin_id;",
                        {
                            "nom": admin.nom,
                            "mdp": admin.mdp,
                            "mail": admin.mail,
                        },
                    )
                    res = cursor.fetchone()
                connection.commit()
        except Exception as e:
            logging.exception("Erreur lors de la création de l'administrateur")
            return False

        created = False
        if res:
            admin.admin_id = res["admin_id"]  # Attribution de l'ID généré
            created = True

        return created

    @log
    def trouver_par_id(self, admin_id: int) -> Optional[Admin]:
        """Trouver un administrateur grâce à son id

        Parameters
        ----------
        admin_id : int
            numéro id de l'administrateur que l'on souhaite trouver

        Returns
        -------
        admin : Admin ou None
            renvoie l'administrateur que l'on cherche par id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM admin                       "
                        " WHERE admin_id = %(admin_id)s;    ",
                        {"admin_id": admin_id},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception("Erreur lors de la recherche de l'administrateur par id")
            return None

        admin = None
        if res:
            admin = Admin(
                nom=res["nom"],
                mdp=res["mdp"],
                mail=res["mail"],
                admin_id=res["admin_id"]
            )

        return admin

    @log
    def trouver_par_nom(self, nom: str) -> Optional[Admin]:
        """Trouver un administrateur grâce à son nom

        Parameters
        ----------
        nom : str
            nom de l'administrateur que l'on souhaite trouver

        Returns
        -------
        admin : Admin ou None
            renvoie l'administrateur que l'on cherche par nom
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM admin                       "
                        " WHERE nom = %(nom)s;              ",
                        {"nom": nom},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception("Erreur lors de la recherche de l'administrateur par nom")
            return None

        admin = None
        if res:
            admin = Admin(
                nom=res["nom"],
                mdp=res["mdp"],
                mail=res["mail"],
                admin_id=res["admin_id"]
            )

        return admin

    @log
    def trouver_par_mail(self, mail: str) -> Optional[Admin]:
        """Trouver un administrateur grâce à son email

        Parameters
        ----------
        mail : str
            email de l'administrateur que l'on souhaite trouver

        Returns
        -------
        admin : Admin ou None
            renvoie l'administrateur que l'on cherche par email
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM admin                       "
                        " WHERE mail = %(mail)s;            ",
                        {"mail": mail},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception("Erreur lors de la recherche de l'administrateur par mail")
            return None

        admin = None
        if res:
            admin = Admin(
                nom=res["nom"],
                mdp=res["mdp"],
                mail=res["mail"],
                admin_id=res["admin_id"]
            )

        return admin

    @log
    def lister_tous(self) -> List[Admin]:
        """Lister tous les administrateurs

        Returns
        -------
        liste_admins : list[Admin]
            renvoie la liste de tous les administrateurs dans la base de données
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                   "
                        "  FROM admin               "
                        " ORDER BY nom;             "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.exception("Erreur lors du listage des administrateurs")
            return []

        liste_admins = []
        for row in res:
            admin = Admin(
                nom=row["nom"],
                mdp=row["mdp"],
                mail=row["mail"],
                admin_id=row["admin_id"]
            )
            liste_admins.append(admin)

        return liste_admins

    @log
    def modifier(self, admin: Admin) -> bool:
        """Modification d'un administrateur dans la base de données

        Parameters
        ----------
        admin : Admin
            L'objet Admin à modifier (doit avoir un admin_id valide)

        Returns
        -------
        modified : bool
            True si la modification est un succès
            False sinon
        """
        # Vérifier que l'admin_id est défini
        if admin.admin_id is None:
            logging.warning("Tentative de modification d'un administrateur sans ID")
            return False

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE admin                                  "
                        "   SET nom      = %(nom)s,                    "
                        "       mdp      = %(mdp)s,                    "
                        "       mail     = %(mail)s                    "
                        " WHERE admin_id = %(admin_id)s;               ",
                        {
                            "nom": admin.nom,
                            "mdp": admin.mdp,
                            "mail": admin.mail,
                            "admin_id": admin.admin_id,
                        },
                    )
                    res = cursor.rowcount
                connection.commit()
        except Exception as e:
            logging.exception("Erreur lors de la modification de l'administrateur")
            return False

        return res == 1

    @log
    def supprimer(self, admin_id: int) -> bool:
        """Suppression d'un administrateur dans la base de données

        Parameters
        ----------
        admin_id : int
            id de l'administrateur à supprimer

        Returns
        -------
        bool
            True si l'administrateur a bien été supprimé
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM admin              "
                        " WHERE admin_id = %(admin_id)s",
                        {"admin_id": admin_id},
                    )
                    res = cursor.rowcount
                connection.commit()
        except Exception as e:
            logging.exception("Erreur lors de la suppression de l'administrateur")
            return False

        return res > 0

    @log
    def se_connecter(self, nom: str, mdp: str) -> Optional[Admin]:
        """Connexion d'un administrateur grâce à son nom et mot de passe

        Parameters
        ----------
        nom : str
            nom de l'administrateur
        mdp : str
            mot de passe de l'administrateur

        Returns
        -------
        admin : Admin ou None
            renvoie l'administrateur si les identifiants sont corrects
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM admin                       "
                        " WHERE nom = %(nom)s               "
                        "   AND mdp = %(mdp)s;              ",
                        {"nom": nom, "mdp": mdp},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception("Erreur lors de la connexion de l'administrateur")
            return None

        admin = None
        if res:
            admin = Admin(
                nom=res["nom"],
                mdp=res["mdp"],
                mail=res["mail"],
                admin_id=res["admin_id"]
            )

        return admin

    @log
    def changer_mot_de_passe(self, admin_id: int, ancien_mdp: str, nouveau_mdp: str) -> bool:
        """Changer le mot de passe d'un administrateur

        Parameters
        ----------
        admin_id : int
            id de l'administrateur
        ancien_mdp : str
            ancien mot de passe
        nouveau_mdp : str
            nouveau mot de passe

        Returns
        -------
        bool
            True si le changement a réussi
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Vérifier d'abord que l'ancien mot de passe est correct
                    cursor.execute(
                        "SELECT admin_id                   "
                        "  FROM admin                      "
                        " WHERE admin_id = %(admin_id)s    "
                        "   AND mdp = %(ancien_mdp)s;      ",
                        {"admin_id": admin_id, "ancien_mdp": ancien_mdp},
                    )
                    verification = cursor.fetchone()
                    
                    if not verification:
                        return False  # Ancien mot de passe incorrect
                    
                    # Mettre à jour le mot de passe
                    cursor.execute(
                        "UPDATE admin                      "
                        "   SET mdp = %(nouveau_mdp)s      "
                        " WHERE admin_id = %(admin_id)s;   ",
                        {"nouveau_mdp": nouveau_mdp, "admin_id": admin_id},
                    )
                    res = cursor.rowcount
                connection.commit()
        except Exception as e:
            logging.exception("Erreur lors du changement de mot de passe")
            return False

        return res == 1

    # =========================================================================
    # MÉTHODES DE GESTION DES BANNISSEMENTS
    # =========================================================================

    @log
    def bannir_joueur(self, id_joueur: int, id_admin: int, raison: str, 
                     duree_jours: Optional[int] = None) -> bool:
        """Bannir un joueur

        Parameters
        ----------
        id_joueur : int
            ID du joueur à bannir
        id_admin : int
            ID de l'administrateur qui bannit
        raison : str
            Raison du bannissement
        duree_jours : int, optional
            Durée du bannissement en jours (None pour permanent)

        Returns
        -------
        bool
            True si le bannissement a réussi
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Calculer la date de fin si durée spécifiée
                    date_fin_ban = None
                    if duree_jours is not None:
                        date_fin_ban = datetime.now() + timedelta(days=duree_jours)
                    
                    # Désactiver les bannissements actifs existants pour ce joueur
                    cursor.execute(
                        "UPDATE joueur_bannis           "
                        "   SET actif = FALSE           "
                        " WHERE id_joueur = %(id_joueur)s "
                        "   AND actif = TRUE;           ",
                        {"id_joueur": id_joueur}
                    )
                    
                    # Insérer le nouveau bannissement
                    cursor.execute(
                        "INSERT INTO joueur_bannis (id_joueur, id_admin, raison_ban, date_fin_ban, actif) "
                        "VALUES (%(id_joueur)s, %(id_admin)s, %(raison_ban)s, %(date_fin_ban)s, TRUE) "
                        "RETURNING id_ban;",
                        {
                            "id_joueur": id_joueur,
                            "id_admin": id_admin,
                            "raison_ban": raison,
                            "date_fin_ban": date_fin_ban,
                        },
                    )
                    res = cursor.fetchone()
                connection.commit()
                return res is not None
        except Exception as e:
            logging.exception("Erreur lors du bannissement du joueur")
            return False

    @log
    def debannir_joueur(self, id_joueur: int) -> bool:
        """Débannir un joueur (lever tous ses bannissements actifs)

        Parameters
        ----------
        id_joueur : int
            ID du joueur à débannir

        Returns
        -------
        bool
            True si le débannissement a réussi
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE joueur_bannis           "
                        "   SET actif = FALSE           "
                        " WHERE id_joueur = %(id_joueur)s "
                        "   AND actif = TRUE;           ",
                        {"id_joueur": id_joueur}
                    )
                    res = cursor.rowcount
                connection.commit()
                return res > 0
        except Exception as e:
            logging.exception("Erreur lors du débannissement du joueur")
            return False

    @log
    def est_joueur_banni(self, id_joueur: int) -> bool:
        """Vérifier si un joueur est actuellement banni

        Parameters
        ----------
        id_joueur : int
            ID du joueur

        Returns
        -------
        bool
            True si le joueur est banni
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_ban, date_fin_ban           "
                        "  FROM joueur_bannis                  "
                        " WHERE id_joueur = %(id_joueur)s      "
                        "   AND actif = TRUE                   "
                        "   AND (date_fin_ban IS NULL OR date_fin_ban > NOW());",
                        {"id_joueur": id_joueur}
                    )
                    res = cursor.fetchone()
                    return res is not None
        except Exception as e:
            logging.exception("Erreur lors de la vérification du bannissement")
            return False

    @log
    def get_bannissement_actif(self, id_joueur: int) -> Optional[dict]:
        """Récupérer les informations du bannissement actif d'un joueur

        Parameters
        ----------
        id_joueur : int
            ID du joueur

        Returns
        -------
        dict ou None
            Informations du bannissement ou None si pas banni
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT jb.*, a.nom as admin_nom, j.pseudo as joueur_pseudo "
                        "  FROM joueur_bannis jb                 "
                        "  JOIN admin a ON jb.id_admin = a.admin_id "
                        "  JOIN joueur j ON jb.id_joueur = j.id_joueur "
                        " WHERE jb.id_joueur = %(id_joueur)s      "
                        "   AND jb.actif = TRUE                   "
                        "   AND (jb.date_fin_ban IS NULL OR jb.date_fin_ban > NOW());",
                        {"id_joueur": id_joueur}
                    )
                    res = cursor.fetchone()
                    return dict(res) if res else None
        except Exception as e:
            logging.exception("Erreur lors de la récupération du bannissement")
            return None

    @log
    def lister_joueurs_bannis(self) -> List[dict]:
        """Lister tous les joueurs actuellement bannis

        Returns
        -------
        list[dict]
            Liste des joueurs bannis avec leurs informations
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT jb.*, a.nom as admin_nom, j.pseudo as joueur_pseudo, "
                        "       j.mail as joueur_mail, j.age as joueur_age "
                        "  FROM joueur_bannis jb                 "
                        "  JOIN admin a ON jb.id_admin = a.admin_id "
                        "  JOIN joueur j ON jb.id_joueur = j.id_joueur "
                        " WHERE jb.actif = TRUE                   "
                        "   AND (jb.date_fin_ban IS NULL OR jb.date_fin_ban > NOW()) "
                        " ORDER BY jb.date_ban DESC;"
                    )
                    res = cursor.fetchall()
                    return [dict(row) for row in res]
        except Exception as e:
            logging.exception("Erreur lors du listage des joueurs bannis")
            return []

    @log
    def lister_historique_bannissements(self, id_admin: Optional[int] = None) -> List[dict]:
        """Lister l'historique complet des bannissements

        Parameters
        ----------
        id_admin : int, optional
            Filtrer par administrateur spécifique

        Returns
        -------
        list[dict]
            Historique des bannissements
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    if id_admin:
                        cursor.execute(
                            "SELECT jb.*, a.nom as admin_nom, j.pseudo as joueur_pseudo "
                            "  FROM joueur_bannis jb                 "
                            "  JOIN admin a ON jb.id_admin = a.admin_id "
                            "  JOIN joueur j ON jb.id_joueur = j.id_joueur "
                            " WHERE jb.id_admin = %(id_admin)s       "
                            " ORDER BY jb.date_ban DESC;",
                            {"id_admin": id_admin}
                        )
                    else:
                        cursor.execute(
                            "SELECT jb.*, a.nom as admin_nom, j.pseudo as joueur_pseudo "
                            "  FROM joueur_bannis jb                 "
                            "  JOIN admin a ON jb.id_admin = a.admin_id "
                            "  JOIN joueur j ON jb.id_joueur = j.id_joueur "
                            " ORDER BY jb.date_ban DESC;"
                        )
                    res = cursor.fetchall()
                    return [dict(row) for row in res]
        except Exception as e:
            logging.exception("Erreur lors du listage de l'historique des bannissements")
            return []

    @log
    def supprimer_bannissement(self, id_ban: int) -> bool:
        """Supprimer définitivement un bannissement de l'historique

        Parameters
        ----------
        id_ban : int
            ID du bannissement à supprimer

        Returns
        -------
        bool
            True si la suppression a réussi
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM joueur_bannis      "
                        " WHERE id_ban = %(id_ban)s;    ",
                        {"id_ban": id_ban}
                    )
                    res = cursor.rowcount
                connection.commit()
                return res > 0
        except Exception as e:
            logging.exception("Erreur lors de la suppression du bannissement")
            return False

    @log
    def nettoyer_bannissements_expires(self) -> int:
        """Désactiver automatiquement les bannissements expirés

        Returns
        -------
        int
            Nombre de bannissements nettoyés
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE joueur_bannis           "
                        "   SET actif = FALSE           "
                        " WHERE actif = TRUE            "
                        "   AND date_fin_ban IS NOT NULL "
                        "   AND date_fin_ban <= NOW();  "
                    )
                    res = cursor.rowcount
                connection.commit()
                return res
        except Exception as e:
            logging.exception("Erreur lors du nettoyage des bannissements expirés")
            return 0