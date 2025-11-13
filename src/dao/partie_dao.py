import logging
from typing import List, Optional
from utils.singleton import Singleton
from utils.log_decorator import log
from dao.db_connection import DBConnection
from business_object.partie import Partie
from business_object.joueur_partie import JoueurPartie
from business_object.pot import Pot
from business_object.joueur import Joueur
from business_object.siege import Siege
from business_object.monnaie import Monnaie


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
                    # Créer la partie
                    cursor.execute(
                        "INSERT INTO partie (id_table, pot, date_debut) "
                        "VALUES (%(id_table)s, %(pot)s, %(date_debut)s) "
                        "RETURNING id_partie;",
                        {
                            "id_table": partie.id_table,
                            "pot": partie.pot.valeur if hasattr(partie.pot, 'valeur') else 0,
                            "date_debut": partie.date_debut,
                        },
                    )
                    res = cursor.fetchone()
                    
                    if res:
                        partie.id_partie = res["id_partie"]
                        
                        # Ajouter les joueurs à la table partie_joueur
                        for joueur_partie in partie.joueurs:
                            cursor.execute(
                                "INSERT INTO partie_joueur (id_partie, id_joueur, mise_tour, solde_partie, statut, id_siege) "
                                "VALUES (%(id_partie)s, %(id_joueur)s, %(mise_tour)s, %(solde_partie)s, %(statut)s, %(id_siege)s)",
                                {
                                    "id_partie": partie.id_partie,
                                    "id_joueur": joueur_partie.joueur.id_joueur,
                                    "mise_tour": joueur_partie.mise_tour.valeur if hasattr(joueur_partie.mise_tour, 'valeur') else 0,
                                    "solde_partie": joueur_partie.solde_partie.valeur if hasattr(joueur_partie.solde_partie, 'valeur') else 0,
                                    "statut": joueur_partie.statut,
                                    "id_siege": joueur_partie.siege.id_siege if joueur_partie.siege else None,
                                },
                            )
                    
                connection.commit()
        except Exception as e:
            logging.exception("Erreur lors de la création de la partie")
            return False

        return res is not None

    @log
    def trouver_par_id(self, id_partie: int) -> Optional[Partie]:
        """Trouver une partie grace à son id

        Parameters
        ----------
        id_partie : int
            numéro id de la partie que l'on souhaite trouver

        Returns
        -------
        partie : Partie
            renvoie la partie que l'on cherche par id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Récupérer les informations de base de la partie
                    cursor.execute(
                        "SELECT p.*, tp.nb_sieges, tp.blind_initial "
                        "FROM partie p "
                        "JOIN table_poker tp ON p.id_table = tp.id_table "
                        "WHERE p.id_partie = %(id_partie)s;",
                        {"id_partie": id_partie},
                    )
                    partie_data = cursor.fetchone()
                    
                    if not partie_data:
                        return None
                    
                    # Récupérer les joueurs de la partie
                    cursor.execute(
                        "SELECT pj.*, j.pseudo, j.mail, j.age "
                        "FROM partie_joueur pj "
                        "JOIN joueur j ON pj.id_joueur = j.id_joueur "
                        "WHERE pj.id_partie = %(id_partie)s;",
                        {"id_partie": id_partie},
                    )
                    joueurs_data = cursor.fetchall()
                    
        except Exception as e:
            logging.exception(f"Erreur lors de la recherche de la partie {id_partie}")
            return None

        # Construire l'objet Partie
        pot = Pot()
        pot.valeur = partie_data["pot"]
        
        joueurs = []
        for j_data in joueurs_data:
            joueur = Joueur(
                id_joueur=j_data["id_joueur"],
                pseudo=j_data["pseudo"],
                mail=j_data["mail"],
                mdp="",  # Mot de passe non récupéré pour des raisons de sécurité
                age=j_data["age"],
                credit=0  # Non utilisé dans ce contexte
            )
            
            siege = Siege(id_siege=j_data["id_siege"]) if j_data["id_siege"] else None
            if siege:
                siege.occupe = True
                siege.id_joueur = j_data["id_joueur"]
            
            joueur_partie = JoueurPartie(
                joueur=joueur,
                siege=siege,
                solde_partie=j_data["solde_partie"]
            )
            joueur_partie.mise_tour = Monnaie(j_data["mise_tour"])
            joueur_partie.statut = j_data["statut"]
            
            joueurs.append(joueur_partie)
        
        partie = Partie(
            id_partie=partie_data["id_partie"],
            joueurs=joueurs,
            pot=pot,
            id_table=partie_data["id_table"],
            date_debut=partie_data["date_debut"]
        )
        partie.date_fin = partie_data["date_fin"]
        
        return partie

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
                        "SELECT id_partie FROM partie ORDER BY date_debut DESC;"
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.exception("Erreur lors du listing des parties")
            return []

        liste_parties = []
        for row in res:
            partie = self.trouver_par_id(row["id_partie"])
            if partie:
                liste_parties.append(partie)

        return liste_parties

    @log
    def modifier(self, partie: Partie) -> bool:
        """Modification d'une partie dans la base de données

        Parameters
        ----------
        partie : Partie

        Returns
        -------
        success : bool
            True si la modification est un succès
            False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Mettre à jour les informations de base de la partie
                    cursor.execute(
                        "UPDATE partie SET "
                        "pot = %(pot)s, "
                        "date_fin = %(date_fin)s "
                        "WHERE id_partie = %(id_partie)s;",
                        {
                            "pot": partie.pot.valeur if hasattr(partie.pot, 'valeur') else 0,
                            "date_fin": partie.date_fin,
                            "id_partie": partie.id_partie,
                        },
                    )
                    
                    # Mettre à jour les joueurs de la partie
                    for joueur_partie in partie.joueurs:
                        cursor.execute(
                            "UPDATE partie_joueur SET "
                            "mise_tour = %(mise_tour)s, "
                            "solde_partie = %(solde_partie)s, "
                            "statut = %(statut)s "
                            "WHERE id_partie = %(id_partie)s AND id_joueur = %(id_joueur)s;",
                            {
                                "mise_tour": joueur_partie.mise_tour.valeur if hasattr(joueur_partie.mise_tour, 'valeur') else 0,
                                "solde_partie": joueur_partie.solde_partie.valeur if hasattr(joueur_partie.solde_partie, 'valeur') else 0,
                                "statut": joueur_partie.statut,
                                "id_partie": partie.id_partie,
                                "id_joueur": joueur_partie.joueur.id_joueur,
                            },
                        )
                    
                connection.commit()
                return True
                
        except Exception as e:
            logging.exception(f"Erreur lors de la modification de la partie {partie.id_partie}")
            return False

    @log
    def supprimer(self, partie: Partie) -> bool:
        """Suppression d'une partie dans la base de données

        Parameters
        ----------
        partie : Partie
            partie à supprimer de la base de données

        Returns
        -------
        success : bool
            True si la partie a bien été supprimée
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM partie WHERE id_partie = %(id_partie)s;",
                        {"id_partie": partie.id_partie},
                    )
                    res = cursor.rowcount
                connection.commit()
        except Exception as e:
            logging.exception(f"Erreur lors de la suppression de la partie {partie.id_partie}")
            return False

        return res > 0

    @log
    def lister_par_table(self, id_table: int) -> List[Partie]:
        """Lister les parties d'une table spécifique

        Parameters
        ----------
        id_table : int
            identifiant de la table

        Returns
        -------
        liste_parties : list[Partie]
            liste des parties de la table
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_partie FROM partie "
                        "WHERE id_table = %(id_table)s "
                        "ORDER BY date_debut DESC;",
                        {"id_table": id_table},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.exception(f"Erreur lors du listing des parties de la table {id_table}")
            return []

        liste_parties = []
        for row in res:
            partie = self.trouver_par_id(row["id_partie"])
            if partie:
                liste_parties.append(partie)

        return liste_parties

    @log
    def lister_actives(self) -> List[Partie]:
        """Lister les parties actives (non terminées)

        Returns
        -------
        liste_parties : list[Partie]
            liste des parties actives
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_partie FROM partie "
                        "WHERE date_fin IS NULL "
                        "ORDER BY date_debut DESC;"
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.exception("Erreur lors du listing des parties actives")
            return []

        liste_parties = []
        for row in res:
            partie = self.trouver_par_id(row["id_partie"])
            if partie:
                liste_parties.append(partie)

        return liste_parties

    @log
    def trouver_par_joueur(self, id_joueur: int) -> List[Partie]:
        """Trouver les parties d'un joueur

        Parameters
        ----------
        id_joueur : int
            identifiant du joueur

        Returns
        -------
        liste_parties : list[Partie]
            liste des parties du joueur
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT DISTINCT pj.id_partie FROM partie_joueur pj "
                        "WHERE pj.id_joueur = %(id_joueur)s "
                        "ORDER BY pj.id_partie DESC;",
                        {"id_joueur": id_joueur},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.exception(f"Erreur lors de la recherche des parties du joueur {id_joueur}")
            return []

        liste_parties = []
        for row in res:
            partie = self.trouver_par_id(row["id_partie"])
            if partie:
                liste_parties.append(partie)

        return liste_parties