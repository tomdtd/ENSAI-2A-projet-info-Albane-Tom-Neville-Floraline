"""Implémentation de la classe MainJoueur."""

from carte import Carte

class MainJoueur():
    """
    La classe MainJoueur permet de modéliser les deux cartes dans la main d'un joueur.

    Parameters
    ----------
    cartes : tuple[Carte]
    Un tuple contenant deux cartes.

    Attributes
    ----------
    __cartes : tuple[Carte]
    Un tuple contenant deux cartes.
    """

    def __init__(self, cartes):
        if not isinstance(cartes, tuple):
            raise ValueError(f"{cartes} doit être un tuple.")
        elif len(cartes) != 2:
            raise ValueError(f"{cartes} doit contenir deux cartes.")
        elif not all(isinstance(carte, Carte) for carte in cartes):
            raise ValueError(f"Tous les elements de {cartes} doivent être des cartes.")
        else:
            self.__cartes = cartes



