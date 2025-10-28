class Pot:
    """
    Représente le pot commun d'une partie.
    Attributs
    ----------
    montant_pot : Monnaie                           
        Le montant total du pot.
    Méthodes
    --------- 
    ajouter_mise(montant: int) -> None
        Ajoute une mise au pot.                         
    reinitialiser_pot() -> None
        Remet le pot à zéro.        
        
    get_montant() -> int
        Retourne le montant total du pot.   
    """
    def __init__(self):
        self.montant_pot = Monnaie(0)

    def ajouter_mise(self, montant: int):
        """Ajoute une mise au pot."""
        self.montant_pot.crediter(montant)

    def reinitialiser_pot(self):
        """Remet le pot à zéro."""
        self.montant_pot = Monnaie(0)

    def get_montant(self) -> int:
        """Retourne le montant total du pot."""
        return self.montant_pot.get()