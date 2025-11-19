import logging

from src.utils.singleton import Singleton
from src.utils.log_decorator import log

from src.dao.db_connection import DBConnection

from src.business_object.joueur import Joueur
from src.business_object.monnaie import Monnaie


class JoueurDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Joueurs de la base de données"""

    @log
    def creer(self, joueur) -> bool:
        """Creation d'un joueur dans la base de données

        Parameters
        ----------
        joueur : Joueur

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
                        "INSERT INTO joueur (pseudo, mdp, mail, age, credit)"
                        "VALUES (%(pseudo)s, %(mdp)s, %(mail)s, %(age)s, %(credit)s)"
                        "RETURNING id_joueur;                                              ",
                        {
                            "pseudo": joueur.pseudo,
                            "mdp": joueur.mdp,
                            "mail": joueur.mail,
                            "age": joueur.age,
                            "credit": joueur.credit.get(),
                        },
                    )
                    res = cursor.fetchone()
                connection.commit() 
        except Exception as e:
            #logging.info(e)
            logging.exception("Erreur lors de la création du joueur")

        created = False
        if res:
            joueur.id_joueur = res["id_joueur"]
            created = True

        return created

    @log
    def trouver_par_id(self, id_joueur) -> Joueur:
        """Trouver un joueur grace à son id

        Parameters
        ----------
        id_joueur : int
            numéro id du joueur que l'on souhaite trouver

        Returns
        -------
        joueur : Joueur
            renvoie le joueur que l'on cherche par id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM joueur                      "
                        " WHERE id_joueur = %(id_joueur)s;  ",
                        {"id_joueur": id_joueur},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        joueur = None
        if res:
            joueur = Joueur(
                pseudo=res["pseudo"],
                age=res["age"],
                mdp=res["mdp"],
                mail=res["mail"],
                credit=res["credit"],
            )

        return joueur

    @log
    def lister_tous(self) -> list[Joueur]:
        """lister tous les joueurs

        Parameters
        ----------
        None

        Returns
        -------
        liste_joueurs : list[Joueur]
            renvoie la liste de tous les joueurs dans la base de données
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                              "
                        "  FROM joueur;                        "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        liste_joueurs = []

        if res:
            for row in res:
                joueur = Joueur(
                    pseudo=row["pseudo"],
                    mdp=row["mdp"],
                    mail=row["mail"],
                    age=row["age"],
                    credit=row["credit"],
                )

                liste_joueurs.append(joueur)

        return liste_joueurs

    @log
    def modifier(self, joueur) -> bool:
        """Modification d'un joueur dans la base de données

        Parameters
        ----------
        joueur : Joueur

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
                        "UPDATE joueur                                      "
                        "   SET pseudo      = %(pseudo)s,                   "
                        "       mdp         = %(mdp)s,                      "
                        "       mail        = %(mail)s,                     "
                        "       age         = %(age)s,                      "
                        "       credit      = %(credit)s                    "
                        " WHERE id_joueur = %(id_joueur)s;                  ",
                        {
                            "pseudo": joueur.pseudo,
                            "mdp": joueur.mdp,
                            "mail": joueur.mail,
                            "age": joueur.age,
                            "credit": joueur.credit.get(),
                            "id_joueur": joueur.id_joueur,
                        },
                    )
                    res = cursor.rowcount
                connection.commit() 
        except Exception as e:
            logging.info(e)

        return res == 1

    @log
    def supprimer(self, joueur) -> bool:
        """Suppression d'un joueur dans la base de données

        Parameters
        ----------
        joueur : Joueur
            joueur à supprimer de la base de données

        Returns
        -------
            True si le joueur a bien été supprimé
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer le compte d'un joueur
                    cursor.execute(
                        "DELETE FROM joueur                  "
                        " WHERE id_joueur=%(id_joueur)s      ",
                        {"id_joueur": joueur.id_joueur},
                    )
                    res = cursor.rowcount
                connection.commit()
        except Exception as e:
            logging.info(e)
            raise

        return res > 0

    @log
    def se_connecter(self, pseudo, mdp) -> Joueur:
        """se connecter grâce à son pseudo et son mot de passe

        Parameters
        ----------
        pseudo : str
            pseudo du joueur que l'on souhaite trouver
        mdp : str
            mot de passe du joueur

        Returns
        -------
        joueur : Joueur
            renvoie le joueur que l'on cherche
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM joueur                      "
                        " WHERE pseudo = %(pseudo)s         "
                        "   AND mdp = %(mdp)s;              ",
                        {"pseudo": pseudo, "mdp": mdp},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
        joueur = None

        if res:
            joueur = Joueur(
                pseudo=res["pseudo"],
                mdp=res["mdp"],
                mail=res["mail"],
                age=res["age"],
                credit=Monnaie(res["credit"]),
                id_joueur=res["id_joueur"] 
            )

        return joueur
    
    @log
    def modifier_credit(self, id_joueur, credit) -> bool:
        """Modifier uniquement le crédit d'un joueur.

        Parameters
        ----------
        id_joueur : int
            id du joueur dont on veut changer le crédit
        credit : Monnaie | int | float | Decimal | str
            nouvelle valeur du crédit — si c'est un Monnaie, on utilise .get()

        Returns
        -------
        bool
            True si une ligne a été modifiée, False sinon
        """
        res = 0
        try:
            # Récupérer la valeur numérique si on reçoit un objet Monnaie
            if isinstance(credit, Monnaie):
                credit_val = credit.get()
            else:
                credit_val = credit

            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE joueur "
                        "   SET credit = %(credit)s "
                        " WHERE id_joueur = %(id_joueur)s;",
                        {"credit": credit_val, "id_joueur": id_joueur},
                    )
                    res = cursor.rowcount
                connection.commit()
        except Exception:
            logging.exception("Erreur lors de la modification du crédit du joueur (modifier_credit)")
            return False

        return res == 1
    
    @log
    def recuperer_credit(self, id_joueur) -> Monnaie | None:
        """Récupère le crédit d'un joueur par son id.

        Parameters
        ----------
        id_joueur : int
            Identifiant du joueur.

        Returns
        -------
        Monnaie | None
            Objet Monnaie contenant le crédit si trouvé, sinon None.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT credit "
                        "  FROM joueur  "
                        " WHERE id_joueur = %(id_joueur)s;",
                        {"id_joueur": id_joueur},
                    )
                    res = cursor.fetchone()
        except Exception:
            logging.exception("Erreur lors de la récupération du crédit (recuperer_credit)")
            return None

        if not res:
            return None

        # On retourne un objet Monnaie pour rester cohérent avec le reste du code
        return Monnaie(res["credit"])

