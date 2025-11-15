"""Implémentation de la classe ListeCartes."""

from business_object.carte import Carte
import random

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
    
    def piocher(self) -> Carte:
        """Pioche une carte aléatoire et la retire de la liste.
        Returns
        -------
        Carte | None
            La carte piochée, ou None si la pioche est vide.
        """
        if not self.__cartes:
            return None
        index = random.randint(0, len(self.__cartes) - 1)
        return self.__cartes.pop(index)

    def cartes_to_str(liste_cartes):
        """Convertit une ListeCartes en chaîne."""
        return ','.join(str(carte) for carte in liste_cartes.cartes)
    
    def str_to_cartes(s):
        """Convertit une chaîne en ListeCartes."""
        from business_object.carte import Carte
        from business_object.liste_cartes import ListeCartes
        cartes = [Carte.from_str(c.strip()) for c in s.split(',') if c]
        return ListeCartes(cartes)