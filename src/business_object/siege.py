class Siege:
    """
    Classe représentant un siège à une table de poker
    
    Attributs:
    ----------
        occupe (bool): Indique si le siège est occupé ou non.
        id_joueur(Joueur) : référence du joueur occupant le siège, son ID       

    Méthodes:
    ----------
        est_occupe() -> bool: Retourne l'état d'occupation du siège.    
    
    """
    def __init__(self):
        self.occupe = False
        self.id_joueur = None

    def est_occupe(self) -> bool:
        return self.occupe