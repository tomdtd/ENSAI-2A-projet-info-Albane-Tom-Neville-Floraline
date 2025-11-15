import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.table import Table
from business_object.monnaie import Monnaie
from business_object.liste_cartes import ListeCartes


class TableDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Tables de poker de la base de données"""

    @log
    def creer(self, table: Table) -> bool:
        """Création d'une table de poker dans la base de données

        Parameters
        ----------
        table : Table
            La table à créer

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
                        "INSERT INTO table_poker (nb_sieges, blind_initial) "
                        "VALUES (%(nb_sieges)s, %(blind_initial)s) "
                        "RETURNING id_table;",
                     {"nb_sieges": table.nb_sieges, "blind_initial": table.blind_initial.get()},
                    )
                    res = cursor.fetchone()
                    table.id_table = res["id_table"]
                connection.commit()
        except Exception as e:
            logging.exception("Erreur lors de la création de la table")
            return False

        return res is not None

    @log
    def trouver_par_id(self, id_table: int) -> Table:
        """Trouver une table grâce à son id

        Parameters
        ----------
        id_table : int
            numéro id de la table que l'on souhaite trouver

        Returns
        -------
        table : Table
            renvoie la table que l'on cherche par id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM table_poker                 "
                        " WHERE id_table = %(id_table)s;    ",
                        {"id_table": id_table},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception("Erreur lors de la recherche de la table par id")
            return None

        table = None
        if res:
            table = Table(
                id_table=res["id_table"],
                nb_sieges=res["nb_sieges"],
                blind_initial=Monnaie(res["blind_initial"]),

            )
            # Note: nb_joueurs n'est pas un attribut de Table, donc on ne le set pas

        return table

    @log
    def lister_toutes(self) -> list[Table]:
        """Lister toutes les tables de poker

        Returns
        -------
        liste_tables : list[Table]
            renvoie la liste de toutes les tables dans la base de données
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                              "
                        "  FROM table_poker;                   "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.exception("Erreur lors du listage de toutes les tables")
            return []

        liste_tables = []

        if res:
            for row in res:
                table = Table(
                    id_table=row["id_table"],
                    nb_sieges=row["nb_sieges"],
                    blind_initial=Monnaie(row["blind_initial"]),
                )
                liste_tables.append(table)

        return liste_tables

    @log
    def modifier(self, table: Table) -> bool:
        """Modification d'une table dans la base de données

        Parameters
        ----------
        table : Table
            La table à modifier

        Returns
        -------
        modified : bool
            True si la modification est un succès
            False sinon
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE table_poker                             "
                        "   SET nb_sieges      = %(nb_sieges)s,        "
                        "       blind_initial  = %(blind_initial)s    "
                        " WHERE id_table = %(id_table)s;               ",
                        {
                            "nb_sieges": table.nb_sieges,
                            "blind_initial": table.blind_initial.get(),
                            "id_table": table.id_table,
                        }
                    )
                    res = cursor.rowcount
                connection.commit()
        except Exception as e:
            logging.exception("Erreur lors de la modification de la table")
            return False

        return res == 1

    @log
    def supprimer(self, id_table: int) -> bool:
        """Suppression d'une table dans la base de données

        Parameters
        ----------
        id_table : int
            ID de la table à supprimer

        Returns
        -------
        deleted : bool
            True si la table a bien été supprimée
            False sinon
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM table_poker             "
                        " WHERE id_table = %(id_table)s      ",
                        {"id_table": id_table},
                    )
                    res = cursor.rowcount
                connection.commit()
        except Exception as e:
            logging.exception("Erreur lors de la suppression de la table")
            return False

        return res > 0

    @log
    def lister_tables_avec_sieges_disponibles(self) -> list[Table]:
        """Lister les tables avec des sièges disponibles

        Returns
        -------
        liste_tables : list[Table]
            renvoie la liste des tables ayant des sièges disponibles
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                              "
                        "  FROM table_poker                    "
                        " WHERE nb_joueurs < nb_sieges;        "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.exception("Erreur lors du listage des tables avec sièges disponibles")
            return []

        liste_tables = []

        if res:
            for row in res:
                table = Table(
                    id_table=row["id_table"],
                    nb_sieges=row["nb_sieges"],
                    blind_initial=Monnaie(row["blind_initial"]),
                )
                liste_tables.append(table)

        return liste_tables

    @log
    def incrementer_nb_joueurs(self, id_table: int) -> bool:
        """Incrémente le nombre de joueurs d'une table de 1"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE table_poker "
                        "   SET nb_joueurs = nb_joueurs + 1 "
                        " WHERE id_table = %(id_table)s;",
                        {"id_table": id_table},
                    )
                    res = cursor.rowcount
                connection.commit()
        except Exception as e:
            logging.exception("Erreur lors de l'incrémentation du nombre de joueurs de la table %s", id_table)
            return False

        return res == 1
    
    @log
    def get_id_joueur_tour(self, id_table: int) -> int:
        """Retourne l'id du joueur dont c'est le tour pour la table donnée"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_joueur_tour FROM table_poker WHERE id_table = %(id_table)s;",
                        {"id_table": id_table},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception("Erreur lors de la récupération de id_joueur_tour")
            return None

        return res.get("id_joueur_tour") if res else None
    
    @log
    def set_id_joueur_tour(self, id_table: int, id_joueur_tour: int=0) -> bool:
        """Met à jour l'id du joueur dont c'est le tour pour la table donnée"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE table_poker SET id_joueur_tour = %(id_joueur_tour)s WHERE id_table = %(id_table)s;",
                        {"id_joueur_tour": id_joueur_tour, "id_table": id_table},
                    )
                    res = cursor.rowcount
                connection.commit()
        except Exception as e:
            logging.exception("Erreur lors de la mise à jour de id_joueur_tour")
            return False

        return res == 1
    
    @log
    def set_flop(self, id_table: int, flop: ListeCartes) -> bool:
        """Met à jour le flop pour une table donnée"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE table_poker SET flop=%(flop)s WHERE id_table=%(id_table)s;",
                        {"flop": ListeCartes.cartes_to_str(flop), "id_table": id_table}
                    )
                    res = cursor.rowcount
                connection.commit()
        except Exception as e:
            logging.exception("Erreur lors de la mise à jour du flop")
            return False
        return res == 1

    @log
    def set_turn(self, id_table: int, turn: ListeCartes) -> bool:
        """Met à jour le turn pour une table donnée"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE table_poker SET turn=%(turn)s WHERE id_table=%(id_table)s;",
                        {"turn": ListeCartes.cartes_to_str(turn), "id_table": id_table}
                    )
                    res = cursor.rowcount
                connection.commit()
        except Exception as e:
            logging.exception("Erreur lors de la mise à jour du turn")
            return False
        return res == 1

    @log
    def set_river(self, id_table: int, river: ListeCartes) -> bool:
        """Met à jour la river pour une table donnée"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE table_poker SET river=%(river)s WHERE id_table=%(id_table)s;",
                        {"river": ListeCartes.cartes_to_str(river), "id_table": id_table}
                    )
                    res = cursor.rowcount
                connection.commit()
        except Exception as e:
            logging.exception("Erreur lors de la mise à jour de la river")
            return False
        return res == 1

    @log
    def get_cartes_communess(self, id_table: int) -> dict:
        """Récupère le flop, turn et river d'une table"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT flop, turn, river FROM table_poker WHERE id_table=%(id_table)s;",
                        {"id_table": id_table}
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception("Erreur lors de la récupération des cartes communes")
            return {"flop": ListeCartes(), "turn": ListeCartes(), "river": ListeCartes()}

        if res:
            return {
                "flop": ListeCartes.str_to_cartes(res["flop"]),
                "turn": ListeCartes.str_to_cartes(res["turn"]),
                "river": ListeCartes.str_to_cartes(res["river"]),
            }
        else:
            return {"flop": ListeCartes(), "turn": ListeCartes(), "river": ListeCartes()}
