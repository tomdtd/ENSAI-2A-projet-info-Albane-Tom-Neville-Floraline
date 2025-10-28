"""Implémentation de la classe ListeCartes."""

from src.business_object.carte import Carte

class ListeCartes():
    """
    La classe ListeCartes permet de modéliser une liste de carte.

    Parameters
    ----------
    cartes : list[Carte]
    Une liste de cartes.

    Attributes
    ----------
    __cartes : list[Carte]
    Liste de cartes.
    """

    def __init__(self, cartes=None):
        if cartes is None: # a voir si c'est utile de renvoyer l'ensemble des cartes si cartes=None
            self.__cartes = [
                Carte(valeur, couleur)
                for couleur in Carte.COULEURS()
                for valeur in Carte.VALEURS()
            ] * 2
        elif not isinstance(cartes, list):
            raise ValueError(f"{cartes} doit être une liste.")
        elif not all(isinstance(carte, Carte) for carte in cartes):
            raise ValueError(f"Tous les elements de {cartes} doivent être des cartes.")
        else:
            self.__cartes = cartes

    def __str__(self):
        return "[" + ", ".join(str(carte) for carte in self.__cartes) + "]"

    def __len__(self):
        return len(self.__cartes)

    def ajouter_carte(self, carte):
        if not isinstance(carte, Carte):
            raise ValueError(f"{carte} doit être une Carte.")
        else:
            self.__cartes.append(carte)

    def get_cartes(self):
        return self.__cartes
    
    @property
    def cartes(self):
        """Retourne la liste des cartes."""
        return self.__cartes
