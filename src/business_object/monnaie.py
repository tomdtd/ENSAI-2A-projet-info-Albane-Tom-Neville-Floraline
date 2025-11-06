class Monnaie:
    """
    Représente une quantité de monnaie (jetons).

    Attributs:
    ----------                  
    valeur : int        
        La valeur de la monnaie en jetons.
    Méthodes:                                   
    ---------
    crediter(montant: int) -> None
        Ajoute un montant à la valeur actuelle.

    debiter(montant: int) -> None
        Soustrait un montant de la valeur actuelle.

    get() -> int        
        Retourne la valeur actuelle d'un objet de ce type.
    """
    def __init__(self, valeur: int = 0):
        """
        Initialise la monnaie avec une valeur de départ.
        """
        if valeur < 0:
            raise ValueError("La valeur de la monnaie ne peut pas être négative.")
        self.valeur = valeur

    def crediter(self, montant: int):
        """Ajoute un montant à la valeur actuelle."""
        if montant > 0:
            self.valeur += montant

    def debiter(self, montant: int):
        """Soustrait un montant de la valeur actuelle."""
        if montant > 0:
            if self.valeur < montant:
                raise ValueError("Solde insuffisant pour débiter ce montant.")
            self.valeur -= montant

    def get(self) -> int:
        """Retourne la valeur actuelle."""
        return self.valeur

    def __repr__(self) -> str:
        return f"Monnaie({self.valeur})" 