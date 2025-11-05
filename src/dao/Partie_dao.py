import logging
from datetime import datetime
from typing import List, Optional

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.partie import Partie

class PartieDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Parties de la base de données"""

    @log
    def creer(self, partie: Partie) -> bool:
        """Démarre une nouvelle partie sur une table

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
                        "INSERT INTO parties (id_table, date_debut, statut_partie, pot_total, cartes_communes) "
                        "VALUES (%(id_table)s, %(date_debut)s, %(statut_partie)s, %(pot_total)s, %(cartes_communes)s) "
                        "RETURNING id_partie;",
                        {
                            "id_table": partie.id_table,
                            "date_debut": partie.date_debut,
                            "statut_partie": partie.statut_partie,
                            "pot_total": partie.pot_total,
                            "cartes_communes": partie.cartes_communes,
                        }
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            partie.id_partie = res["id_partie"]
            created = True

        return created

    @log
    def trouver_par_id(self, id_partie: int) -> Optional[Partie]:
        """Récupère les informations d'une partie spécifique

        Parameters
        ----------
        id_partie : int

        Returns
        -------
        partie : Partie
            La partie trouvée
            None si aucune partie ne correspond à l'id
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_partie, id_table, date_debut, date_fin, statut_partie, pot_total, cartes_communes "
                        "FROM parties "
                        "WHERE id_partie = %(id_partie)s;",
                        {"id_partie": id_partie},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        partie = None
        if res:
            partie = Partie(
                id_partie=res["id_partie"],
                id_table=res["id_table"],
                date_debut=res["date_debut"],
                date_fin=res["date_fin"],
                statut_partie=res["statut_partie"],
                pot_total=res["pot_total"],
                cartes_communes=res["cartes_communes"],
            )

        return partie

    @log
    def mettre_a_jour(self, partie: Partie) -> bool:
        """Met à jour l'état d'une partie

        Parameters
        ----------
        partie : Partie

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
                        "UPDATE parties "
                        "SET id_table = %(id_table)s, date_debut = %(date_debut)s, "
                        "date_fin = %(date_fin)s, statut_partie = %(statut_partie)s, "
                        "pot_total = %(pot_total)s, cartes_communes = %(cartes_communes)s "
                        "WHERE id_partie = %(id_partie)s;",
                        {
                            "id_partie": partie.id_partie,
                            "id_table": partie.id_table,
                            "date_debut": partie.date_debut,
                            "date_fin": partie.date_fin,
                            "statut_partie": partie.statut_partie,
                            "pot_total": partie.pot_total,
                            "cartes_communes": partie.cartes_communes,
                        }
                    )
                    updated = cursor.rowcount > 0
        except Exception as e:
            logging.info(e)
            updated = False

        return updated

    @log
    def trouver_parties_par_statut(self, statut: str) -> List[Partie]:
        """Récupère toutes les parties ayant un certain statut

        Parameters
        ----------
        statut : str

        Returns
        -------
        list[Partie]
            liste des parties avec le statut demandé
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_partie, id_table, date_debut, date_fin, statut_partie, pot_total, cartes_communes "
                        "FROM parties "
                        "WHERE statut_partie = %(statut)s "
                        "ORDER BY date_debut DESC;",
                        {"statut": statut},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)

        parties = []
        if res:
            for row in res:
                partie = Partie(
                    id_partie=row["id_partie"],
                    id_table=row["id_table"],
                    date_debut=row["date_debut"],
                    date_fin=row["date_fin"],
                    statut_partie=row["statut_partie"],
                    pot_total=row["pot_total"],
                    cartes_communes=row["cartes_communes"],
                )
                parties.append(partie)

        return parties

    @log
    def trouver_parties_par_joueur(self, id_joueur: int) -> List[Partie]:
        """Récupère l'historique de toutes les parties jouées par un joueur

        Parameters
        ----------
        id_joueur : int

        Returns
        -------
        list[Partie]
            liste des parties du joueur
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT DISTINCT p.id_partie, p.id_table, p.date_debut, p.date_fin, 
                               p.statut_partie, p.pot_total, p.cartes_communes
                        FROM parties p
                        INNER JOIN joueurs_parties jp ON p.id_partie = jp.id_partie
                        WHERE jp.id_joueur = %(id_joueur)s
                        ORDER BY p.date_debut DESC;
                        """,
                        {"id_joueur": id_joueur},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)

        parties = []
        if res:
            for row in res:
                partie = Partie(
                    id_partie=row["id_partie"],
                    id_table=row["id_table"],
                    date_debut=row["date_debut"],
                    date_fin=row["date_fin"],
                    statut_partie=row["statut_partie"],
                    pot_total=row["pot_total"],
                    cartes_communes=row["cartes_communes"],
                )
                parties.append(partie)

        return parties

    @log
    def trouver_derniere_partie_sur_table(self, id_table: int) -> Optional[Partie]:
        """Récupère la partie la plus récente sur une table donnée

        Parameters
        ----------
        id_table : int

        Returns
        -------
        partie : Partie
            La dernière partie sur la table
            None si aucune partie trouvée
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_partie, id_table, date_debut, date_fin, statut_partie, pot_total, cartes_communes
                        FROM parties
                        WHERE id_table = %(id_table)s
                        ORDER BY date_debut DESC
                        LIMIT 1;
                        """,
                        {"id_table": id_table},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        partie = None
        if res:
            partie = Partie(
                id_partie=res["id_partie"],
                id_table=res["id_table"],
                date_debut=res["date_debut"],
                date_fin=res["date_fin"],
                statut_partie=res["statut_partie"],
                pot_total=res["pot_total"],
                cartes_communes=res["cartes_communes"],
            )

        return partie

    @log
    def lister_parties_par_periode(self, debut: datetime, fin: datetime) -> List[Partie]:
        """Lister les parties qui se sont déroulées dans un intervalle de temps

        Parameters
        ----------
        debut : datetime
        fin : datetime

        Returns
        -------
        list[Partie]
            liste des parties dans la période
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_partie, id_table, date_debut, date_fin, statut_partie, pot_total, cartes_communes
                        FROM parties
                        WHERE date_debut BETWEEN %(debut)s AND %(fin)s
                        ORDER BY date_debut DESC;
                        """,
                        {"debut": debut, "fin": fin},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)

        parties = []
        if res:
            for row in res:
                partie = Partie(
                    id_partie=row["id_partie"],
                    id_table=row["id_table"],
                    date_debut=row["date_debut"],
                    date_fin=row["date_fin"],
                    statut_partie=row["statut_partie"],
                    pot_total=row["pot_total"],
                    cartes_communes=row["cartes_communes"],
                )
                parties.append(partie)

        return parties

    @log
    def compter_parties_par_statut(self, statut: str) -> int:
        """Compte le nombre de parties avec un statut donné

        Parameters
        ----------
        statut : str

        Returns
        -------
        int
            nombre de parties avec le statut
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) as count FROM parties WHERE statut_partie = %(statut)s;",
                        {"statut": statut},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
 
        return res["count"] if res else 0