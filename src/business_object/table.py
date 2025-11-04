from src.business_object.siege import Siege

class Table:
    def __init__(self, id_table: int, nb_sieges: int, blind_initial: Monnaie):
        self.id_table = id_table
        self.nb_sieges = nb_sieges
        self.blind_initial = blind_initial
        self.sieges = [Siege() for _ in range(nb_sieges)]

    def table_remplie(self) -> bool:
        """Renvoie un booléen selon si la table est remplie ou non"""
        return all(siege.est_occupe() for siege in self.sieges)

    def get_joueurs(self) -> list[Joueur]:
        """Retourne la liste des joueurs assis à cette table."""
        return [siege.joueur for siege in self.sieges if siege.est_occupe() and siege.joueur is not None]

