from src.business_object.JoueurPartie import JoueurPartie
from src.business_object.pot import Pot
from src.business_object.carte import Carte

class Partie : 
    """
    Classe représentant une partie du jeu
    Attributs:
    ----------
    joueurs : list[JoueurPartie] 

    Liste des joueurs dans la partie

    pot : Pot 
    Pot de la partie     

    id_partie : int 
    Identifiant unique de la partie            

    id_table : int      
    Identifiant de la table où se déroule la partie

    date_debut : str
    Date de début de la partie  

    date_fin : str
    Date de fin de la partie    

    carte_communes : list[str]
    Cartes communes sur la table

    Methodes:
    ------- 
    repartition_blind() : 
        Gère la répartition des blinds entre les joueurs    
    
    finir_partie() : 
        Termine la partie et détermine le gagnant
    
    gérer_blind() :
        Gère les blinds pour chaque tour de la partie

    """
    def __init__(self, id_partie : int, joueurs : list[JoueurPartie], pot : Pot, id_table : int, date_debut : str):
        self.id_partie = id_partie
        self.joueurs = joueurs  
        self.pot = pot 
        self.id_table = id_table
        self.date_debut = date_debut
        self.date_fin = None
    def __str__(self):
        return f"Partie(id_partie={self.id_partie}, joueurs={self.joueurs}, pot={self.pot})"  

    # def repartition_blind() : # Attribuer les blinds aux joueurs au début
    #    pass 
    def finir_partie() : # Mettre fin à la partie et déterminer le gagnant
        pass 
    def gerer_blind(self) : # Sortie c'est le joueur qui doit poser la blind
        n = len(self.joueurs)
        if n >=1 :
            b = self.joueurs[-1]
            for i in range(0,n-1):
                self.joueurs[i+1] = self.joueurs[i]
                # Logique pour gérer les blinds pour chaque joueur
            self.joueurs[0] = b
            