from src.business_object.table import Table
from src.business_object.joueur import Joueur
from src.business_object.monnaie import Monnaie


class AccessPartie:
    """
    Classe d'accès aux tables de poker.
    Attributs:
    ----------
     tables : list[Table]
        Liste des tables de poker disponibles dans le système.

    Méthodes:
    ---------
    creer_table(nb_sieges: int, blind_initial: Monnaie) -> Table
        Crée une nouvelle table avec un nombre de sièges et une blind initiale.

    rejoindre_table(joueur: Joueur) -> bool
        Permet à un joueur de rejoindre la première table avec un siège libre.
        Met à jour le siège avec l'identifiant du joueur.
        Retourne True si l'affectation a réussi, False sinon.
    """

    def __init__(self):
        self.tables: list[Table] = []

    def rejoindre_table(self, joueur: Joueur) -> bool:
        """
        Permet à un joueur de rejoindre la première table avec un siège libre.
        Met à jour le siège avec l'identifiant du joueur.
        Retourne True si l'affectation a réussi, False sinon.
        """
        for table in self.tables:
            if not table.table_remplie():
                for siege in table.sieges:
                    if not siege.est_occupe():
                        siege.occupe = True
                        siege.id_joueur = joueur.id_joueur
                        joueur.jouer_partie()
                        return True
        return False

    def creer_table(self, nb_sieges: int, blind_initial: Monnaie) -> Table:
        """
        Crée une nouvelle table avec un identifiant unique et l’ajoute à la liste.
        """
        new_id = len(self.tables) + 1
        nouvelle_table = Table(id_table=new_id, nb_sieges=nb_sieges, blind_initial=blind_initial)
        self.tables.append(nouvelle_table)
        return nouvelle_table
