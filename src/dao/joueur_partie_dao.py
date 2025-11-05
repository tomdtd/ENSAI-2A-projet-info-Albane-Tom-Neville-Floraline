import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.joueur import Joueur


class JoueurPartieDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Joueurs lors d'une partie dans la base de données"""
    @log
    def creer(self, joueur, id_partie) -> bool:
        """Creation d'un joueur_partie dans la base de données

        Parameters
        ----------
        joueur_partie : JoueurPartie
            Objet contenant les informations du joueur, son siège, son solde, etc.
        id_partie : int
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
                        "INSERT INTO partie_joueur (id_partie, id_joueur, mise_joueur, solde_partie, statut, id_siege )"
                        "VALUES (%(id_partie)s, %(id_joueur)s, %(mise_joueur)s, %(solde_partie)s, %(statut)s, %(id_siege)s)"
                        "RETURNING id_joueur;                                              ",
                        {
                            "id_partie": jp.id_partie,
                            "id_joueur": jp.id_joueur,
                            "mise_joueur": str(jp.mise_joueur),
                            "solde_partie": str(jp.solde_partie),
                            "statut": jp.statut,
                            "id_siege": jp.id_siege,
                        },
                    )
                    res = cursor.fetchone()
                connection.commit() 
        except Exception as e:
            #logging.info(e)
            logging.exception("Erreur lors de la création du joueur_partie")

        created = False
        if res:
            joueur.id_joueur = res["id_joueur"]
            created = True

        return created




