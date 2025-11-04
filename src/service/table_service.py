from tabulate import tabulate

from utils.log_decorator import log
from utils.securite import hash_password

from business_object.table import Table
from dao.table_dao import TableDao

class TableService :
    """Classe contenant les méthodes de service des tables"""

    @log
    def creer_table(self, nb_sieges: int, blind_initial: 'Monnaie') -> Table:
        """Crée une nouvelle table avec un nombre de sièges et un blind initial."""
        nouvelle_table = AccessPartie().creer_table(nb_sieges, blind_initial)
        if TableDao().creer(nouvelle_table):
            return nouvelle_table
        return None

    @log 
    def rejoindre_table(self, joueur: Joueur, id_table: int) -> bool:
        """Un joueur rejoint une table s'il y a un siège disponible."""
        table = TableDao().trouver_par_id(id_table)
        if table:
            for siege in table.sieges:
                if not siege.est_occupe():
                    siege.occupe = True
                    siege.id_joueur = joueur.id_joueur  
                    return TableDao().modifier(table)
        return False

    @log
    def lister_tables_disponibles(self) -> list[Table]:
        """Liste toutes les tables qui ont au moins un siège disponible."""
        tables = TableDao().lister_tous()
        return [table for table in tables if not table.table_remplie()]

    @log
    def quitter_table(self, joueur: Joueur, id_table: int) -> bool:
        """Un joueur quitte une table et libère son siège."""
        table = TableDao().trouver_par_id(id_table)
        if table:
            for siege in table.sieges:
                if siege.id_joueur == joueur.id_joueur:
                    siege.occupe = False
                    siege.id_joueur = None
                    return TableDao().modifier(table)
        return False


