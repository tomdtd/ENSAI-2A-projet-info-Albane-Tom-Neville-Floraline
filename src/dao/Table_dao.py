import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.table import Table

class TableDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Tables de la base de données"""

    @log
    def creer(self, table: Table) -> bool:
        """Creation d'une table dans la base de données

        Parameters
        ----------
        table : Table

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
                        "INSERT INTO tables (nom_table, nb_sieges_max, blind_initial)"
                        "VALUES (%(nom_table)s, %(nb_sieges_max)s, %(blind_initial)s)"
                        "RETURNING id_table;",
                        {
                            "nom_table": table.nom_table,
                            "nb_sieges_max": table.nb_sieges_max,
                            "blind_initial": table.blind_initial,
                        }
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            table.id_table = res["id_table"]
            created = True

        return created

    @log
    def trouver_par_id(self, id_table: int) -> Table:
        """trouver une table grace à son id

        Parameters
        ----------
        id_table : int

        Returns
        -------
        table : Table
            La table trouvée
            None si aucune table ne correspond à l'id
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_table, nom_table, nb_sieges_max, blind_initial "
                        "FROM tables "
                        "WHERE id_table = %(id_table)s;",
                        {"id_table": id_table},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        table = None
        if res:
            table = Table(
                id_table=res["id_table"],
                nom_table=res["nom_table"],
                nb_sieges_max=res["nb_sieges_max"],
                blind_initial=res["blind_initial"],
            )

        return table

    @log
    def mettre_a_jour(self, table: Table) -> bool:
        """Modifie les propriétés d'une table

        Parameters
        ----------
        table : Table

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
                        "UPDATE tables "
                        "SET nom_table = %(nom_table)s, nb_sieges_max = %(nb_sieges_max)s, blind_initial = %(blind_initial)s "
                        "WHERE id_table = %(id_table)s;",
                        {
                            "id_table": table.id_table,
                            "nom_table": table.nom_table,
                            "nb_sieges_max": table.nb_sieges_max,
                            "blind_initial": table.blind_initial,
                        }
                    )
                    updated = cursor.rowcount > 0
        except Exception as e:
            logging.info(e)
            updated = False

        return updated

    @log
    def supprimer(self, id_table: int) -> bool:
        """Supprime une table (si elle n'a pas de parties en cours)

        Parameters
        ----------
        id_table : int

        Returns
        -------
        deleted : bool
            True si la suppression est un succès
            False sinon
        """

        # Vérifier s'il y a des parties en cours sur cette table
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) as count_parties_actives "
                        "FROM parties "
                        "WHERE id_table = %(id_table)s AND statut_partie IN ('en_attente', 'en_cours');",
                        {"id_table": id_table},
                    )
                    res = cursor.fetchone()
                    
                    if res and res["count_parties_actives"] > 0:
                        raise ValueError("Impossible de supprimer une table avec des parties en cours")
                    
                    # Suppression de la table
                    cursor.execute(
                        "DELETE FROM tables WHERE id_table = %(id_table)s;",
                        {"id_table": id_table},
                    )
                    deleted = cursor.rowcount > 0
        except Exception as e:
            logging.info(e)
            raise e

        return deleted

    @log
    def supprimer_toutes(self) -> bool:
        """Supprime toutes les tables (action administrateur)

        Parameters
        ----------
        None

        Returns
        -------
        deleted : bool
            True si la suppression est un succès
            False sinon
        """

        # Vérifier s'il y a des parties en cours sur n'importe quelle table
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) as count_parties_actives "
                        "FROM parties "
                        "WHERE statut_partie IN ('en_attente', 'en_cours');"
                    )
                    res = cursor.fetchone()
                    
                    if res and res["count_parties_actives"] > 0:
                        raise ValueError("Impossible de supprimer les tables avec des parties en cours")
                    
                    # Suppression de toutes les tables
                    cursor.execute("DELETE FROM tables;")
                    deleted = cursor.rowcount > 0
        except Exception as e:
            logging.info(e)
            raise e

        return deleted

    @log
    def lister_toutes(self) -> list[Table]:
        """Récupère la liste de toutes les tables disponibles

        Parameters
        ----------
        None

        Returns
        -------
        list[Table]
            liste de toutes les tables
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_table, nom_table, nb_sieges_max, blind_initial "
                        "FROM tables "
                        "ORDER BY id_table;"
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)

        tables = []
        if res:
            for row in res:
                table = Table(
                    id_table=row["id_table"],
                    nom_table=row["nom_table"],
                    nb_sieges_max=row["nb_sieges_max"],
                    blind_initial=row["blind_initial"],
                )
                tables.append(table)

        return tables

    @log
    def lister_tables_avec_sieges_disponibles(self) -> list[dict]:
        """Trouve les tables avec des sièges disponibles

        Parameters
        ----------
        None

        Returns
        -------
        list[dict]
            liste de dictionnaires avec les infos des tables et le nombre de sièges occupés
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 
                            t.id_table,
                            t.nom_table,
                            t.nb_sieges_max,
                            t.blind_initial,
                            COUNT(jp.id_joueur) as sieges_occupes,
                            (t.nb_sieges_max - COUNT(jp.id_joueur)) as sieges_disponibles
                        FROM tables t
                        LEFT JOIN parties p ON t.id_table = p.id_table 
                            AND p.statut_partie = 'en_attente'
                        LEFT JOIN joueurs_parties jp ON p.id_partie = jp.id_partie 
                            AND jp.statut_dans_la_partie != 'quitte'
                        GROUP BY t.id_table, t.nom_table, t.nb_sieges_max, t.blind_initial
                        HAVING (t.nb_sieges_max - COUNT(jp.id_joueur)) > 0 OR COUNT(jp.id_joueur) = 0
                        ORDER BY t.id_table;
                        """
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)

        tables_disponibles = []
        if res:
            for row in res:
                table_info = {
                    'id_table': row['id_table'],
                    'nom_table': row['nom_table'],
                    'nb_sieges_max': row['nb_sieges_max'],
                    'blind_initial': row['blind_initial'],
                    'sieges_occupes': row['sieges_occupes'],
                    'sieges_disponibles': row['sieges_disponibles']
                }
                tables_disponibles.append(table_info)

        return tables_disponibles

    @log
    def compter_tables(self) -> int:
        """Retourne le nombre total de tables

        Parameters
        ----------
        None

        Returns
        -------
        int
            nombre total de tables
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) as count FROM tables;")
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        return res["count"] if res else 0