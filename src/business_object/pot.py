"""Implémentation de la classe Pot."""

from src.business_object.transaction import Transaction
from datetime import datetime


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
