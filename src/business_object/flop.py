"""Implémentation de la classe Flop."""

from liste_cartes import ListeCartes

class Flop(ListeCartes):
    """
    La classe Flop permet de modéliser le flop lors du jeu. 
    Cette classe hérite de la classe ListeCartes.

    Parameters
    ----------
    cartes : list[Carte]
    Une liste de 3 à 5 cartes.

    Attributes
    ----------
    __cartes : list[Carte]
    Les cartes du flop.
    """
    def __init__(self, cartes):
        if len(cartes) < 3 or len(cartes) > 5 :
                raise ValueError(f"Le flop doit contenir entre 3 et 5 cartes.")
        super().__init__(cartes)
        