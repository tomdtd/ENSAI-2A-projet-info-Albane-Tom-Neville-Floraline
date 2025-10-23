class partie : 
    """
    Classe représentant une partie du jeu
    Attributes:
    ----------
    joueurs : list[JoueurPartie] 

    Liste des joueurs dans la partie

    jour int:
    Jour actuel de la partie            
    
    pot Pot: 
    Pot de la partie     

    id_partie : int 
    Identifiant unique de la partie            

    Methods:
    ------- 
    repartition_blind() : 
        Gère la répartition des blinds entre les joueurs    
    
    finir_partie() : 
        Termine la partie et détermine le gagnant
    
    gérer_blind() :
        Gère les blinds pour chaque tour de la partie
    """
    def __init__(self, id_partie : int, joueurs : list[JoueurPartie], jour : int, pot : Pot):
        self.id_partie = id_partie
        self.joueurs = joueurs  
        self.jour = jour
        self.pot = pot 

    def __str__(self):
        return f"Partie(id_partie={self.id_partie}, joueurs={self.joueurs}, jour={self.jour}, pot={self.pot})"  

    def repartition_blind() : 
        pass 
    def finir_partie() : 
        pass 
    def gérer_blind() : 
        pass