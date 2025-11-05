from utils.log_decorator import log
from tabulate import tabulate
from business_object.joueur import Joueur
from src.business_object.JoueurPartie import JoueurPartie
from src.business_object.pot import Pot
from src.business_object.partie import Partie
from business_object.monnaie import Monnaie


class PartieService:
    """Service pour orchestrer le lancement et la gestion d'une partie de poker"""

    def __init__(self, logger=None):
        self.logger = logger
        self.id_compteur = 1  # Identifiant unique de partie

    @log
    def lancer_partie(self, joueurs: list[Joueur], dealer_id: int) -> str:
        """Instancie une Partie, répartit les blinds, joue un tour et affiche le résumé"""
        try:
            # Initialiser les JoueurPartie avec Monnaie et statut par défaut
            joueurs_partie = []
            for j in joueurs:
                jp = JoueurPartie(
                    joueur=j,
                    solde_partie=Monnaie(valeur=int(j.credit)),
                    statut="actif",
                    mise_tour=Monnaie(valeur=0),
                    siege=None,
                    main=None
                )
                joueurs_partie.append(jp)

            # Créer le pot initial
            pot = Pot()

            # Créer la partie
            partie = Partie(
                joueurs=joueurs_partie,
                jour=1,
                pot=pot,
                id_partie=self.id_compteur
            )
            self.id_compteur += 1

            # Répartition des blinds
            partie.repartition_blind()

            # Gérer les blinds du tour
            partie.gérer_blind()

            # Fin de partie
            partie.finir_partie()

            # Affichage du résumé avec tabulate
            resume = [
                [jp.joueur.pseudo, jp.solde_partie.get(), jp.statut]
                for jp in partie.joueurs
            ]
            print(tabulate(resume, headers=["Pseudo", "Crédit", "Statut"], tablefmt="grid"))

            return f"Partie {partie.id_partie} terminée avec succès."
        except Exception as e:
            return f"Erreur lors du lancement de la partie : {str(e)}"
