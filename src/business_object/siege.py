class Siege:
    """
    Classe représentant un siège à une table de poker
    
    Attributs:
    ----------
        id_siege : identifiant du siege
        occupe (bool): Indique si le siège est occupé ou non.
        id_joueur(Joueur) : référence du joueur occupant le siège, son ID       

    Méthodes:
    ----------
        est_occupe() -> bool: Retourne l'état d'occupation du siège.    
    
    """
    def __init__(self, id_siege=None):
        self.id_siege = id_siege
        self.occupe = False
        self.id_joueur = None

    def est_occupe(self) -> bool:
        return self.occupe