from src.business_object.siege import Siege

class Table:
    def __init__(self, id_table: int, nb_sieges: int, blind_initial: Monnaie):
        self.id_table = id_table
        self.nb_sieges = nb_sieges
        self.blind_initial = blind_initial
        self.sieges = [Siege() for _ in range(nb_sieges)]

    def table_remplie(self) -> bool:
        return all(siege.est_occupe() for siege in self.sieges)

