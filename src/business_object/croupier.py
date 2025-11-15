from typing import List
from src.business_object.liste_cartes import ListeCartes
from src.business_object.joueur_partie import JoueurPartie
from src.business_object.flop import Flop
from src.business_object.carte import Carte


class Croupier:
    """
    Représente le croupier, qui gère la distribution des cartes
    lors d'une partie de poker Texas Hold'em.

    Attributes
    ----------
    pioche : ListeCartes
        La pioche de cartes utilisée par le croupier.

    Methods
    -------
    distribuer(joueurs_partie: List[JoueurPartie], nb_cartes: int) -> None
        Distribue un nombre de cartes privées à chaque joueur (pré-flop).
    distribuer_flop() -> Flop
        Distribue le flop (3 cartes communes).
    distribuer_turn() -> Carte
        Distribue le turn (1 carte commune).
    distribuer_river() -> Carte
        Distribue la river (1 carte commune).
    """

    def __init__(self, pioche: ListeCartes):
        self.pioche = pioche

    def distribuer(self, joueurs_partie: List[JoueurPartie], nb_cartes: int):
        """Distribue un nombre de cartes privées à chaque joueur (pré-flop)."""
        for _ in range(nb_cartes):
            for jp in joueurs_partie:
                carte = self.pioche.piocher()
                if carte:
                    jp.main.ajouter_carte(carte)
    
    def distribuer2(self, lst_id_joueurs_partie: list[int], nb_cartes: int):
        """Distribue un nombre de cartes privées à chaque joueur (pré-flop).
        Attributes
        ----------
        lst_id_joueurs_partie: list[int]
            Liste des joueurs a qui on doit distribuer.
        Returns
        ----------
        dict{int:ListeCartes()}
            Dictionnaire associant chaque id_joueur à sa main de cartes.
        """
        mains = {id_joueur: ListeCartes(cartes=[]) for id_joueur in lst_id_joueurs_partie}

        for _ in range(nb_cartes):
            for id_joueur in lst_id_joueurs_partie:
                carte = self.pioche.piocher()
                if carte is not None:
                    mains[id_joueur].ajouter_carte(carte)

        return mains
                    

    def distribuer_flop(self) -> Flop:
        """Distribue le flop (3 cartes communes)."""
        cartes_flop = [self.pioche.piocher() for _ in range(3)]
        cartes_flop = [c for c in cartes_flop if c is not None]
        if len(cartes_flop) != 3:
            raise RuntimeError("Impossible de distribuer le flop : cartes manquantes.")
        return Flop(cartes_flop)

    def distribuer_turn(self) -> Carte:
        """Distribue le turn (1 carte commune)."""
        carte = self.pioche.piocher()
        if carte is None:
            raise RuntimeError("Impossible de distribuer le turn : carte manquante.")
        return carte

    def distribuer_river(self) -> Carte:
        """Distribue la river (1 carte commune)."""
        carte = self.pioche.piocher()
        if carte is None:
            raise RuntimeError("Impossible de distribuer la river : carte manquante.")
        return carte
