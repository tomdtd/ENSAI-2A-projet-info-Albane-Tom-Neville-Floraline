from datetime import datetime
from src.business_object.joueur import Joueur
from src.business_object.joueur_partie import JoueurPartie
from src.business_object.transaction import Transaction
from src.business_object.partie import Partie
from src.business_object.pot import Pot
from src.business_object.croupier import Croupier
from src.business_object.accesspartie import AccessPartie
from src.business_object.monnaie import Monnaie
from src.business_object.main_joueur_complete import MainJoueurComplete
from src.business_object.combinaison import Combinaison
from src.business_object.liste_cartes import ListeCartes


class DeroulementPartie:
    """
    Orchestration d'une partie de poker Texas Hold'em.
    """

    def __init__(self, joueurs: list[Joueur], big_blind: int, small_blind: int, logger=None):
        self.logger = logger
        self.big_blind = Monnaie(big_blind)
        self.small_blind = Monnaie(small_blind)
        self.access_partie = AccessPartie()
        self.table = self.access_partie.creer_table(nb_sieges=len(joueurs), blind_initial=self.small_blind)

        # ✅ Correction : création explicite de la pioche
        self.pioche = ListeCartes()
        self.croupier = Croupier(self.pioche)

        self.pot = Pot()
        self.transactions: list[Transaction] = []
        self.partie = None
        self.joueurs_partie: list[JoueurPartie] = []

        # Affecter les joueurs aux sièges
        for joueur in joueurs:
            self.access_partie.rejoindre_table(joueur)
            siege = next(s for s in self.table.sieges if s.id_joueur == joueur.id_joueur)
            jp = JoueurPartie(joueur=joueur, siege=siege, solde_partie=joueur.credit.get())
            self.joueurs_partie.append(jp)

    def lancer_partie(self):
        """Initialise et lance une partie complète"""
        self.partie = Partie(
            joueurs=self.joueurs_partie,
            jour=1,
            pot=self.pot,
            id_partie=1
        )

        # Répartition des blinds
        self.partie.repartition_blind()
        self._collecter_blinds()

        # Pré-flop
        self.croupier.distribuer(self.joueurs_partie, nb_cartes=2)
        self._tour_de_table("Pré-flop")

        # Flop
        flop = self.croupier.distribuer_flop()
        self._tour_de_table("Flop")

        # Turn
        turn = self.croupier.distribuer_turn()
        self._tour_de_table("Turn")

        # River
        river = self.croupier.distribuer_river()
        self._tour_de_table("River")

        cartes_communes = flop.get_cartes() + [turn] + [river]

        # Showdown
        self._showdown(cartes_communes)

        self.partie.finir_partie()

        if self.logger:
            self.logger.info(f"Partie {self.partie.id_partie} terminée.")

    def _collecter_blinds(self):
        actifs = [jp for jp in self.joueurs_partie if jp.statut == "en attente"]

        if len(actifs) < 2:
            raise RuntimeError("Pas assez de joueurs actifs pour lancer la partie.")

        sb = actifs[-2]
        bb = actifs[-1]

        sb.miser(self.small_blind.get())
        bb.miser(self.big_blind.get())

        self.transactions.append(Transaction(solde=-self.small_blind.get(), date=datetime.now(), id_joueur=sb.joueur.id_joueur))
        self.transactions.append(Transaction(solde=-self.big_blind.get(), date=datetime.now(), id_joueur=bb.joueur.id_joueur))

        self.pot.ajouter_mise(sb.mise_tour.get())
        self.pot.ajouter_mise(bb.mise_tour.get())

    def _tour_de_table(self, phase: str):
        print(f"--- Tour de table ({phase}) ---")
        for jp in self.joueurs_partie:
            if jp.statut == "en attente":
                jp.miser(10)
                self.transactions.append(Transaction(solde=-10, date=datetime.now(), id_joueur=jp.joueur.id_joueur))
                self.pot.ajouter_mise(10)
                print(f"{jp.joueur.pseudo} mise 10.")

    def _showdown(self, cartes_communes: list):
        resultats = []
        for jp in self.joueurs_partie:
            if jp.statut == "en attente":
                main_complete = MainJoueurComplete(list(jp.main.get_cartes()) + cartes_communes)
                combinaison = main_complete.combinaison()
                resultats.append((jp, combinaison))

                if self.logger:
                    self.logger.info(f"{jp.joueur.pseudo} a {combinaison.name}")

        gagnant, meilleure_combinaison = max(resultats, key=lambda x: x[1].value)
        gagnant.solde_partie.crediter(self.pot.get_montant().get())
        self.transactions.append(Transaction(solde=self.pot.get_montant().get(), date=datetime.now(), id_joueur=gagnant.joueur.id_joueur))

        print(f"Le gagnant est {gagnant.joueur.pseudo} avec la combinaison {meilleure_combinaison.name} "
              f"(score {meilleure_combinaison.value}) et remporte {self.pot.get_montant().get()} jetons.")
