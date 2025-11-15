import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.joueur import Joueur


class JoueurPartieDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Joueurs lors d'une partie dans la base de données"""
    @log
    def creer(self, joueur_partie, id_table) -> bool:
        """Creation d'un joueur_partie dans la base de données

        Parameters
        ----------
        joueur_partie : JoueurPartie
            Objet contenant les informations du joueur, son siège, son solde, etc.
        id_table : int
            L'identifiant de la partie

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
                        "INSERT INTO partie_joueur (id_table, id_joueur, mise_tour, solde_partie, statut, id_siege)"
                        "VALUES (%(id_table)s, %(id_joueur)s, %(mise_tour)s, %(solde_partie)s, %(statut)s, %(id_siege)s)"
                        "RETURNING id_joueur;                                              ",
                        {
                            "id_table": id_table,
                            "id_joueur": joueur_partie.joueur.id_joueur,
                            "mise_tour": joueur_partie.mise_tour.valeur,
                            "solde_partie": joueur_partie.solde_partie.valeur,
                            "statut": joueur_partie.statut,
                            "id_siege": joueur_partie.siege.id_siege,
                        },
                    )
                    res = cursor.fetchone()
                connection.commit() 
        except Exception as e:
            logging.exception("Erreur lors de la création du joueur_partie")

        created = False
        if res:
            joueur_partie.id_joueur = res["id_joueur"]
            created = True

        return created

    @log
    def supprimer(self, id_joueur) -> bool:
        """Suppression d'un joueur dans la table partie_joueur

        Parameters
        ----------
        id_joueur : int
            id du joueur à supprimer de la table partie_joueur

        Returns
        -------
            True si le joueur a bien été supprimé
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer le compte d'un joueur
                    cursor.execute(
                        "DELETE FROM partie_joueur                  "
                        " WHERE id_joueur=%(id_joueur)s      ",
                        {"id_joueur": id_joueur},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise

        return res > 0
    
    
    @log
    def modifier(self, joueur_partie, id_table) -> bool:
        """Modification d'un joueur partie dans la base de données

        Parameters
        ----------
        joueur_partie : JoueurPartie

        Returns
        -------
        created : bool
            True si la modification est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE partie_joueur                               "
                        "   SET mise_tour     = %(mise_tour)s,              "
                        "       solde_partie  = %(solde_partie)s,           "
                        "       statut        = %(statut)s,                 "
                        "       id_siege      = %(id_siege)s                "
                        " WHERE id_joueur = %(id_joueur)s AND id_table = %(id_table)s;                  ",
                        {
                            "id_table": id_table,
                            "id_joueur":joueur_partie.joueur.id_joueur,
                            "mise_tour": joueur_partie.mise_tour.valeur,
                            "solde_partie": joueur_partie.solde_partie.valeur,
                            "statut": joueur_partie.statut,
                            "id_siege": joueur_partie.siege.id_siege,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)

        return res == 1
    
    @log
    def trouver_par_table(self, id_table) -> list:
        """Trouver tous les JoueurPartie appartenant à une table.

        Parameters
        ----------
        id_table : int

        Returns
        -------
        joueurs_partie_table : list
            Joueurs appartenant à la table.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM partie_joueur                     "
                        " WHERE id_table = %(id_table)s;  ",
                        {"id_table": id_table},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise
    
        joueurs_partie_table = None
        if res:
            joueurs_partie_table = [row["id_joueur"] for row in res]

        return joueurs_partie_table
    
    @log
    def trouver_cartes_main_joueur(self, id_table: int, id_joueur: int) -> ListeCartes:
        """Récupère la main d'un joueur dans une partie précise"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT cartes_main FROM partie_joueur "
                        "WHERE id_table=%(id_table)s AND id_joueur=%(id_joueur)s;",
                        {"id_table": id_table, "id_joueur": id_joueur},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception("Erreur lors de la récupération des cartes du joueur")
            return ListeCartes() 

        if res and res["cartes_main"]:
            return ListeCartes.str_to_cartes(res["cartes_main"])
        return ListeCartes() 
    
    @log
    def donner_cartes_main_joueur(self, id_table: int, id_joueur: int, main: ListeCartes) -> bool:
        """Attribue une main de cartes à un joueur dans une partie précise"""
        cartes_str = ListeCartes.cartes_to_str(main)
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE partie_joueur "
                        "SET cartes_main=%(cartes_main)s "
                        "WHERE id_table=%(id_table)s AND id_joueur=%(id_joueur)s;",
                        {"cartes_main": cartes_str, "id_table": id_table, "id_joueur": id_joueur},
                    )
                    res = cursor.rowcount
                connection.commit()
        except Exception as e:
            logging.exception("Erreur lors de l'attribution des cartes au joueur")
            return False

        return res == 1


