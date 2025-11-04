class Siege:
    """
    Classe représentant un siège dans un contexte commercial.
    
    Attributs:
    ----------
        occupe (bool): Indique si le siège est occupé ou non.       

    Méthodes:
    ----------
        est_occupe() -> bool: Retourne l'état d'occupation du siège.    
    
    """
    def __init__(self):
        self.occupe = False

    def est_occupe(self) -> bool:
        return self.occupe