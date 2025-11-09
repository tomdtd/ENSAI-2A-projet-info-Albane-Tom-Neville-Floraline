from datetime import datetime
from src.business_object.joueur import Joueur
from src.business_object.JoueurPartie import JoueurPartie
from src.business_object.transaction import Transaction
from src.business_object.partie import Partie
from src.business_object.pot import Pot
from src.business_object.croupier import Croupier
from src.business_object.siege import Siege
from src.business_object.table import Table
from src.business_object.accesspartie import AccessPartie
from src.business_object.main import Main
from src.business_object.monnaie import Monnaie
from src.business_object.main_joueur_complete import MainJoueurComplete
from src.business_object.flop import Flop
from src.business_object.combinaison import Combinaison


class DeroulementPartie:
    """
    Super-classe orchestrant une partie de poker Texas Hold'em.
    Elle coordonne les joueurs, la table, le croupier, les blinds,
    les transactions et le déroulement des mains (pré-flop, flop, turn, river).
    """

    def __init__(self, joueurs: list[Joueur], big_blind: int, small_blind: int, logger=None):
        self.logger = logger
        self.big_blind = Monnaie(big_blind)
        self.small_blind = Monnaie(small_blind)
        self.access_partie = AccessPartie()
        self.table = self.access_partie.creer_table(nb_sieges=len(joueurs), blind_initial=self.small_blind)
        self.croupier = Croupier()
        self.pot = Pot()
        self.transactions: list[Transaction] = []
        self.partie = None
        self.joueurs_partie: list[JoueurPartie] = []

        # Affecter les joueurs aux sièges
        for joueur in joueurs:
            self.access_partie.rejoindre_table(joueur)
            siege = next(s for s in self.table.sieges if s.id_joueur == joueur.id_joueur)
            jp = JoueurPartie(joueur=joueur, siege=siege, solde_partie=joueur.credit)
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

        # Distribution des cartes par le croupier (2 cartes par joueur)
        for jp in self.joueurs_partie:
            jp.main = self.croupier.distribuer_main(nb_cartes=2)

        # Flop : 3 cartes communes
        flop = Flop(self.croupier.distribuer_cartes(nb_cartes=3))

        # Déroulement simplifié d'une main
        self._tour_de_mise()
        self._showdown(flop)

        # Fin de partie
        self.partie.finir_partie()

        if self.logger:
            self.logger.info(f"Partie {self.partie.id_partie} terminée.")

    def _collecter_blinds(self):
        """Collecte small blind et big blind et enregistre les transactions"""
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

    def _tour_de_mise(self):
        """Simule un tour de mise simplifié"""
        for jp in self.joueurs_partie:
            if jp.statut == "en attente":
                jp.miser(10)
                self.transactions.append(Transaction(solde=-10, date=datetime.now(), id_joueur=jp.joueur.id_joueur))
                self.pot.ajouter_mise(10)

    def _showdown(self, flop: Flop):
        """Compare les combinaisons des joueurs et détermine le vrai gagnant"""
        resultats = []

        for jp in self.joueurs_partie:
            if jp.statut == "en attente":
                main_complete = MainJoueurComplete.recuperer_main_et_flop(jp.main, flop)
                combinaison = main_complete.combinaison()
                resultats.append((jp, combinaison))

                if self.logger:
                    self.logger.info(f"{jp.joueur.pseudo} a {combinaison.name}")

        # Déterminer le gagnant : joueur avec la meilleure combinaison
        gagnant, meilleure_combinaison = max(resultats, key=lambda x: x[1])

        # Créditer le pot au gagnant
        gagnant.solde_partie.crediter(self.pot.get_montant())
        self.transactions.append(Transaction(solde=self.pot.get_montant(), date=datetime.now(), id_joueur=gagnant.joueur.id_joueur))

        print(f"Le gagnant est {gagnant.joueur.pseudo} avec la combinaison {meilleure_combinaison.name} et remporte {self.pot.get_montant()} jetons.")
