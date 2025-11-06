from typing import List, Optional, Dict
from src.business_object.partie import Partie
from src.business_object.joueur_partie import JoueurPartie
from src.business_object.pot import Pot
from src.business_object.joueur import Joueur
from src.business_object.siege import Siege
from src.business_object.monnaie import Monnaie


class PartieDAO:
    """
    Data Access Object pour la gestion des parties de poker
    """
    
    def __init__(self):
        self._parties: Dict[int, Partie] = {}  # Dictionnaire pour stocker les parties en mémoire
        self._next_id = 1  # Compteur pour les IDs
    
    def creer_partie(self, joueurs: List[JoueurPartie], pot: Pot, id_table: int, date_debut: str) -> Partie:
        """Crée une nouvelle partie et la sauvegarde"""
        partie = Partie(
            id_partie=self._next_id,
            joueurs=joueurs,
            pot=pot,
            id_table=id_table,
            date_debut=date_debut
        )
        
        self._parties[self._next_id] = partie
        self._next_id += 1
        
        return partie
    
    def get_partie_par_id(self, id_partie: int) -> Optional[Partie]:
        """Récupère une partie par son ID"""
        return self._parties.get(id_partie)
    
    def get_toutes_parties(self) -> List[Partie]:
        """Récupère toutes les parties"""
        return list(self._parties.values())
    
    def get_parties_par_table(self, id_table: int) -> List[Partie]:
        """Récupère toutes les parties d'une table spécifique"""
        return [partie for partie in self._parties.values() if partie.id_table == id_table]
    
    def get_parties_actives(self) -> List[Partie]:
        """Récupère les parties qui ne sont pas terminées (date_fin est None)"""
        return [partie for partie in self._parties.values() if partie.date_fin is None]
    
    def terminer_partie(self, id_partie: int, date_fin: str) -> bool:
        """Termine une partie en définissant sa date de fin"""
        partie = self.get_partie_par_id(id_partie)
        if partie:
            partie.date_fin = date_fin
            return True
        return False
    
    def supprimer_partie(self, id_partie: int) -> bool:
        """Supprime une partie par son ID"""
        if id_partie in self._parties:
            del self._parties[id_partie]
            return True
        return False
    
    def get_partie_par_joueur(self, id_joueur: int) -> Optional[Partie]:
        """Trouve la partie active où un joueur participe"""
        for partie in self._parties.values():
            for joueur_partie in partie.joueurs:
                if joueur_partie.joueur.id_joueur == id_joueur and partie.date_fin is None:
                    return partie
        return None
    
    def ajouter_joueur_partie(self, id_partie: int, joueur_partie: JoueurPartie) -> bool:
        """Ajoute un joueur à une partie"""
        partie = self.get_partie_par_id(id_partie)
        if partie and partie.date_fin is None:
            partie.joueurs.append(joueur_partie)
            return True
        return False
    
    def retirer_joueur_partie(self, id_partie: int, id_joueur: int) -> bool:
        """Retire un joueur d'une partie"""
        partie = self.get_partie_par_id(id_partie)
        if partie and partie.date_fin is None:
            for i, joueur_partie in enumerate(partie.joueurs):
                if joueur_partie.joueur.id_joueur == id_joueur:
                    partie.joueurs.pop(i)
                    return True
        return False
    
    def get_nombre_parties(self) -> int:
        """Retourne le nombre total de parties"""
        return len(self._parties)
    
    def partie_existe(self, id_partie: int) -> bool:
        """Vérifie si une partie existe"""
        return id_partie in self._parties
    
    def get_joueurs_partie(self, id_partie: int) -> List[JoueurPartie]:
        """Récupère tous les joueurs d'une partie"""
        partie = self.get_partie_par_id(id_partie)
        if partie:
            return partie.joueurs
        return []