"""Implémentation de la classe MainJoueurComplete."""

from src.business_object.liste_cartes import ListeCartes

class MainJoueurComplete(ListeCartes):
    """
    La classe MainJoueurComplete permet de modéliser la main complete d'un joueur.
    C'est à dire les deux cartes dans sa main ainsi que les cartes du flop.
    Cette classe hérite de la classe ListeCartes.

    Parameters
    ----------
    cartes : list[Carte]
    Une liste de 2 à 7 cartes.

    Attributes
    ----------
    __cartes : list[Carte]
    Les cartes de la main complete du joueur.
    """
    def __init__(self, cartes):
        if len(cartes) < 2 or len(cartes) > 7 :
                raise ValueError(f"Le flop doit contenir entre 2 et 7 cartes.")
        super().__init__(cartes)
    
    @classmethod #permet de créer a partir des classes main et flop 
                 # main_complete = MainJoueurComplete.recuperer_main_et_flop(main, flop)
    def recuperer_main_et_flop(cls, main: "MainJoueur", flop: "Flop"):
        return cls(list(main.get_cartes()) + flop.get_cartes())

    def combinaison(self):
        "Determine la combinaison de la main complete d'un joueur."
        self.cartes.sort()
        



