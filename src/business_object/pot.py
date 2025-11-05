"""Implémentation de la classe Pot."""

from src.business_object.transaction import Transaction
from src.business_object.monnaie import Monnaie



class Pot:
    """
    La classe Pot modélise la cagnotte commune d'une partie de poker.

    Parameters
    ----------
    montant_pot : Monnaie
    joueurs_contributeurs : list[JoueurPartie]

    Attributes
    ----------
    __id_pot : int
        Identifiant unique du pot.
    __joueurs_contributeurs : list[JoueurPartie]
        Liste des transactions ayant alimenté le pot.
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