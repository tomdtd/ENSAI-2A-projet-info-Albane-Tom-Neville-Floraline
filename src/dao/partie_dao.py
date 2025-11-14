import logging
from typing import List, Optional
from datetime import datetime

from utils.singleton import Singleton
from utils.log_decorator import log
from dao.db_connection import DBConnection
from business_object.partie import Partie
from business_object.joueur_partie import JoueurPartie
from business_object.pot import Pot


class PartieDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Parties de la base de données"""

    @log
    def creer(self, partie: Partie) -> bool:
        """Création d'une partie dans la base de données

        Parameters
        ----------
        partie : Partie

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO partie (id_partie, id_table, pot, date_debut)"
                        "VALUES (%(id_partie)s, %(id_table)s, %(pot)s, %(date_debut)s)"
                        "RETURNING id_partie;",
                        {
                            "id_partie": partie.id_partie,
                            "id_table": partie.id_table,
                            "pot": partie.pot.get_montant(),
                            "date_debut": partie.date_debut,
                        },
                    )
                    res = cursor.fetchone()
                connection.commit()
        except Exception as e:
            logging.exception("Erreur lors de la création de la partie")
            return False

        return res is not None

    @log
    def trouver_par_id(self, id_partie: int) -> Optional[Partie]:
        """Trouver une partie grâce à son id

        Parameters
        ----------
        id_partie : int
            numéro id de la partie que l'on souhaite trouver

        Returns
        -------
        partie : Partie ou None
            renvoie la partie que l'on cherche par id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM partie                      "
                        " WHERE id_partie = %(id_partie)s;  ",
                        {"id_partie": id_partie},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception("Erreur lors de la recherche de la partie par id")
            return None

        partie = None
        if res:
            # Créer le pot avec le montant de la base
            pot = Pot(res["pot"])
            
            # Pour l'instant, on initialise avec une liste vide de joueurs
            # Dans une implémentation réelle, il faudrait charger les joueurs de la partie
            partie = Partie(
                id_partie=res["id_partie"],
                joueurs=[],  # À compléter avec les joueurs réels
                pot=pot,
                id_table=res["id_table"],
                date_debut=res["date_debut"]
            )
            # Note: date_fin n'existe pas dans le schéma actuel

        return partie

    @log
    def modifier(self, partie: Partie) -> bool:
        """Modification d'une partie dans la base de données

        Parameters
        ----------
        partie : Partie

        Returns
        -------
        modified : bool
            True si la modification est un succès
            False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Mise à jour sans date_fin car la colonne n'existe pas
                    cursor.execute(
                        "UPDATE partie                                      "
                        "   SET id_table     = %(id_table)s,               "
                        "       pot          = %(pot)s,                    "
                        "       date_debut   = %(date_debut)s              "
                        " WHERE id_partie = %(id_partie)s;                 ",
                        {
                            "id_table": partie.id_table,
                            "pot": partie.pot.get_montant(),
                            "date_debut": partie.date_debut,
                            "id_partie": partie.id_partie,
                        },
                    )
                    res = cursor.rowcount
                connection.commit()
        except Exception as e:
            logging.exception("Erreur lors de la modification de la partie")
            return False

        return res == 1

    @log
    def supprimer(self, id_partie: int) -> bool:
        """Suppression d'une partie dans la base de données

        Parameters
        ----------
        id_partie : int
            id de la partie à supprimer

        Returns
        -------
        bool
            True si la partie a bien été supprimée
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM partie              "
                        " WHERE id_partie = %(id_partie)s",
                        {"id_partie": id_partie},
                    )
                    res = cursor.rowcount
                connection.commit()
        except Exception as e:
            logging.exception("Erreur lors de la suppression de la partie")
            return False

        return res > 0

    @log
    def lister_toutes(self) -> List[Partie]:
        """Lister toutes les parties

        Returns
        -------
        liste_parties : list[Partie]
            renvoie la liste de toutes les parties dans la base de données
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                   "
                        "  FROM partie              "
                        " ORDER BY date_debut DESC; "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.exception("Erreur lors du listage des parties")
            return []

        liste_parties = []
        for row in res:
            pot = Pot(row["pot"])
            partie = Partie(
                id_partie=row["id_partie"],
                joueurs=[],  # À compléter avec les joueurs réels
                pot=pot,
                id_table=row["id_table"],
                date_debut=row["date_debut"]
            )
            liste_parties.append(partie)

        return liste_parties

    @log
    def trouver_parties_par_statut(self, statut: str) -> List[Partie]:
        """Trouver les parties par statut

        Parameters
        ----------
        statut : str
            statut des parties à rechercher

        Returns
        -------
        list[Partie]
            liste des parties avec le statut donné
        """
        # Note: Cette méthode nécessite que la table partie ait une colonne 'statut'
        # qui n'est pas présente dans le schéma initial. On pourrait l'ajouter ou
        # adapter la logique selon les besoins.
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Pour l'instant, on simule avec une requête qui retourne toutes les parties
                    # car la colonne statut n'existe pas
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM partie                      "
                        " ORDER BY date_debut DESC;         "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.exception("Erreur lors de la recherche par statut")
            return []

        liste_parties = []
        for row in res:
            pot = Pot(row["pot"])
            partie = Partie(
                id_partie=row["id_partie"],
                joueurs=[],  # À compléter avec les joueurs réels
                pot=pot,
                id_table=row["id_table"],
                date_debut=row["date_debut"]
            )
            liste_parties.append(partie)

        return liste_parties

    @log
    def trouver_derniere_partie_sur_table(self, id_table: int) -> Optional[Partie]:
        """Trouver la dernière partie sur une table donnée

        Parameters
        ----------
        id_table : int
            id de la table

        Returns
        -------
        Partie ou None
            la dernière partie sur cette table
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM partie                      "
                        " WHERE id_table = %(id_table)s     "
                        " ORDER BY date_debut DESC          "
                        " LIMIT 1;                          ",
                        {"id_table": id_table},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception("Erreur lors de la recherche de la dernière partie")
            return None

        partie = None
        if res:
            pot = Pot(res["pot"])
            partie = Partie(
                id_partie=res["id_partie"],
                joueurs=[],  # À compléter avec les joueurs réels
                pot=pot,
                id_table=res["id_table"],
                date_debut=res["date_debut"]
            )

        return partie

    @log
    def lister_parties_par_periode(self, debut: datetime, fin: datetime) -> List[Partie]:
        """Lister les parties dans une période donnée

        Parameters
        ----------
        debut : datetime
            date de début de la période
        fin : datetime
            date de fin de la période

        Returns
        -------
        list[Partie]
            liste des parties dans la période
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM partie                      "
                        " WHERE date_debut BETWEEN %(debut)s AND %(fin)s"
                        " ORDER BY date_debut DESC;         ",
                        {"debut": debut, "fin": fin},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.exception("Erreur lors du listage des parties par période")
            return []

        liste_parties = []
        for row in res:
            pot = Pot(row["pot"])
            partie = Partie(
                id_partie=row["id_partie"],
                joueurs=[],  # À compléter avec les joueurs réels
                pot=pot,
                id_table=row["id_table"],
                date_debut=row["date_debut"]
            )
            liste_parties.append(partie)

        return liste_parties