from src.business_object.siege import Siege
from src.business_object.monnaie import Monnaie
from src.business_object.joueur_partie import JoueurPartie
 
class Table:
    """
    Classe représentant une table de poker
    Attributs:
    ----------
        id_table (int): Identifiant unique de la table.
        nb_sieges (int): Nombre de sièges disponibles à la table.
        blind_initial (Monnaie): Montant de la blind initiale pour la table.
        sieges (list[Siege]): Liste des sièges à la table.
    Méthodes:
    ----------
        table_remplie() -> bool: Vérifie si la table est entièrement occupée.
        get_joueurs() -> list[int]: Retourne la liste des IDs des joueurs assis à la table.
    """
     
    def __init__(self, id_table: int, nb_sieges: int, blind_initial: Monnaie, nb_joueurs: int=0):
        self.id_table = id_table
        self.nb_sieges = nb_sieges
        self.nb_joueurs = nb_joueurs
        self.blind_initial = blind_initial
        self.sieges = [Siege(id_siege=i) for i in range(nb_sieges)]

    def table_remplie(self) -> bool:
        """Renvoie un booléen selon si la table est remplie ou non"""
        return all(siege.est_occupe() for siege in self.sieges)

    def get_joueurs(self) -> list[int]:
        """Retourne la liste des IDs des joueurs assis à cette table."""
        return [siege.id_joueur for siege in self.sieges if siege.est_occupe() and siege.id_joueur is not None] 