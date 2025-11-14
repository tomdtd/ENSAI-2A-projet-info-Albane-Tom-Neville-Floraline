"""Implémentation de la classe Pot."""

from src.business_object.monnaie import Monnaie

class Pot:
    """
    La classe Pot modélise la cagnotte commune d'une partie de poker.
    """
    def __init__(self, montant_initial: int = 0):
        """
        Parameters
        ----------
        montant_initial : int, optional
            Montant initial du pot, par défaut 0
        """
        self.montant_pot = Monnaie(montant_initial)

    def ajouter_mise(self, montant: int):
        """Ajoute une mise au pot."""
        self.montant_pot.crediter(montant)

    def reinitialiser_pot(self):
        """Remet le pot à zéro."""
        self.montant_pot = Monnaie(0)

    def get_montant(self) -> int:
        """Retourne le montant total du pot."""
        return self.montant_pot.get()

    @property
    def valeur(self) -> int:
        """Propriété pour accéder à la valeur du pot (compatibilité avec les tests existants)."""
        return self.get_montant()