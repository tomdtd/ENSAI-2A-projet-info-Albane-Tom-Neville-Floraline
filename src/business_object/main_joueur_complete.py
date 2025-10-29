"""Implémentation de la classe MainJoueurComplete."""

from src.business_object.liste_cartes import ListeCartes
from src.business_object.combinaison import Combinaison
from src.business_object.carte import Carte

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
                raise ValueError(f"La main complète doit contenir entre 2 et 7 cartes.")
        super().__init__(cartes)

    @classmethod #permet de créer a partir des classes main et flop
                 # main_complete = MainJoueurComplete.recuperer_main_et_flop(main, flop)
    def recuperer_main_et_flop(cls, main: "MainJoueur", flop: "Flop"):
        return cls(list(main.get_cartes()) + flop.get_cartes())

    def combinaison(self):
        "Determine la combinaison de la main complete d'un joueur."
        cartes = self.get_cartes()
        valeurs = [c.valeur for c in cartes]
        couleurs = [c.couleur for c in cartes]

        ordre_valeurs = {val: i for i, val in enumerate(Carte.VALEURS())}
        indices = [ordre_valeurs[v] for v in valeurs]

        compte_valeurs = {v: valeurs.count(v) for v in set(valeurs)}
        compte_couleurs = {c: couleurs.count(c) for c in set(couleurs)}

        # Vérification quinte flush / quinte royale
        for couleur in set(couleurs):
            cartes_couleur = [c for c in cartes if c.couleur == couleur]
            valeurs_couleur = {c.valeur for c in cartes_couleur}

            # Vérifie Quinte Royale (même couleur, valeurs spécifiques)
            if {"10", "Valet", "Dame", "Roi", "As"}.issubset(valeurs_couleur):
                return Combinaison.QuinteRoyale

            # Vérifie Quinte Flush (5 valeurs consécutives, même couleur)
            valeurs_connues = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Valet", "Dame", "Roi", "As"]
            indices_couleur = [valeurs_connues.index(v) for v in valeurs_couleur if v in valeurs_connues]
            indices_couleur.sort()
            for i in range(len(indices_couleur) - 4):
                if indices_couleur[i + 4] - indices_couleur[i] == 4 and len(set(indices_couleur[i:i + 5])) == 5:
                    return Combinaison.QuinteFlush

        # Vérification flush seule
        for couleur, count in compte_couleurs.items():
            if count >= 5:
                return Combinaison.Flush

        # Vérification quinte seule
        indices_uniques = sorted(set(indices))
        for i in range(len(indices_uniques) - 4):
            if indices_uniques[i:i+5] == list(range(indices_uniques[i], indices_uniques[i]+5)):
                return Combinaison.Quinte

        # Vérification autres combinaisons
        counts = sorted(compte_valeurs.values(), reverse=True)
        if 4 in counts:
            return Combinaison.Carre
        if 3 in counts and 2 in counts:
            return Combinaison.Full
        if 3 in counts:
            return Combinaison.Brelan
        if counts.count(2) == 2:
            return Combinaison.DoublePaire
        if 2 in counts:
            return Combinaison.Paire

        return Combinaison.CarteHaute
