from tabulate import tabulate
from utils.log_decorator import log
from tabulate import tabulate
from utils.log_decorator import log
from business_object.accesspartie import AccessPartie
from business_object.monnaie import Monnaie
from business_object.joueur import Joueur


class PartieService:
    """Classe contenant les méthodes de service pour gérer les parties"""

    def __init__(self):
        self.access_partie = AccessPartie()

    @log
    def creer_table(self, nb_sieges: int, blind: float):
        """Créer une nouvelle table avec un nombre de sièges et un blind"""
        blind_monnaie = Monnaie(blind)
        return self.access_partie.creer_table(nb_sieges, blind_monnaie)

    @log
    def rejoindre_table(self, joueur: Joueur) -> bool:
        """Permet à un joueur de rejoindre une table avec siège libre"""
        return self.access_partie.rejoindre_table(joueur)

    @log
    def afficher_tables(self) -> str:
        """Affiche toutes les tables créées avec leur état"""
        entetes = ["ID Table", "Blind", "Sièges", "Occupés"]
        lignes = []

        for table in self.access_partie.tables:
            nb_occupes = sum(1 for s in table.sieges if s.est_occupe())
            lignes.append([
                table.id_table,
                str(table.blind_initial),
                len(table.sieges),
                nb_occupes
            ])

        str_tables = "-" * 100
        str_tables += "\nListe des tables \n"
        str_tables += "-" * 100 + "\n"
        str_tables += tabulate(
            tabular_data=lignes,
            headers=entetes,
            tablefmt="psql",
            floatfmt=".2f"
        )
        str_tables += "\n"

        return str_tables
