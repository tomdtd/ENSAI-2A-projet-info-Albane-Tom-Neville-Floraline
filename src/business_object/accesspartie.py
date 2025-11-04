from src.business_object.table import Table

class AccessPartie:
    def __init__(self):
        self.tables: list[Table] = []

    def rejoindre_table(self, joueur: 'Joueur') -> bool:
        for table in self.tables:
            for siege in table.sieges:
                if not siege.est_occupe():
                    siege.occupe = True  
                    return True
        return False

    def creer_table(self, nb_sieges: int, blind_initial: 'Monnaie') -> Table:
        new_id = len(self.tables) + 1
        nouvelle_table = Table(id_table=new_id, nb_sieges=nb_sieges, blind_initial=blind_initial)
        self.tables.append(nouvelle_table)
        return nouvelle_table
