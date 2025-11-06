from typing import List, Optional
from src.business_object.table import Table
from src.business_object.monnaie import Monnaie


class TableDao:
    """
    Data Access Object pour la gestion des tables de poker
    """
    
    def __init__(self):
        self._tables = {}  # Dictionnaire pour stocker les tables en mémoire
        self._next_id = 1  # Compteur pour les IDs
    
    def creer_table(self, nb_sieges: int, blind_initial: Monnaie) -> Table:
        """Crée une nouvelle table et la sauvegarde"""
        table = Table(
            id_table=self._next_id,
            nb_sieges=nb_sieges,
            blind_initial=blind_initial
        )
        
        self._tables[self._next_id] = table
        self._next_id += 1
        
        return table
    
    def get_table_par_id(self, id_table: int) -> Optional[Table]:
        """Récupère une table par son ID"""
        return self._tables.get(id_table)
    
    def get_toutes_tables(self) -> List[Table]:
        """Récupère toutes les tables"""
        return list(self._tables.values())
    
    def get_tables_disponibles(self) -> List[Table]:
        """Récupère les tables qui ne sont pas pleines"""
        return [table for table in self._tables.values() if not table.table_remplie()]
    
    def supprimer_table(self, id_table: int) -> bool:
        """Supprime une table par son ID"""
        if id_table in self._tables:
            del self._tables[id_table]
            return True
        return False
    
    def get_table_par_joueur(self, id_joueur: int) -> Optional[Table]:
        """Trouve la table où un joueur est assis"""
        for table in self._tables.values():
            if id_joueur in table.get_joueurs():
                return table
        return None
    
    def get_nombre_tables(self) -> int:
        """Retourne le nombre total de tables"""
        return len(self._tables)
    
    def table_existe(self, id_table: int) -> bool:
        """Vérifie si une table existe"""
        return id_table in self._tables