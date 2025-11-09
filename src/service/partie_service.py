from utils.log_decorator import log
from business_object.joueur import Joueur
from src.business_object.joueur_partie import JoueurPartie
from src.business_object.pot import Pot
from src.business_object.partie import Partie
from src.business_object.accesspartie import AccessPartie
from business_object.monnaie import Monnaie


class PartieService:
    """Service pour coordonner le lancement et la gestion d'une partie de poker"""

    def __init__(self, logger=None):
        self.logger = logger
        self.id_compteur = 1  # Identifiant unique de partie

    @log
    def lancer_partie(self, joueurs: list[Joueur], dealer_id: int) -> str:
        """Gère la partie"""
        try:
            # Créer une table via AccessPartie
            access = AccessPartie()
            table = access.creer_table(nb_sieges=len(joueurs), blind_initial=Monnaie(10))

            # Affecter les joueurs aux sièges
            joueurs_partie = []
            for joueur in joueurs:
                success = access.rejoindre_table(joueur)
                if not success:
                    raise RuntimeError(f"Impossible d'affecter le joueur {joueur.pseudo} "
                                       f"à une table.")

                # Récupérer le siège occupé
                siege = next((s for s in table.sieges if s.id_joueur == joueur.id_joueur), None)
                if siege is None:
                    raise RuntimeError(f"Siège introuvable pour le joueur {joueur.pseudo}.")

                # Créer l'objet JoueurPartie
                jp = JoueurPartie(
                    joueur=joueur,
                    solde_partie=Monnaie(valeur=int(joueur.credit)),
                    statut="actif",
                    mise_tour=Monnaie(valeur=0),
                    siege=siege,
                    main=None
                )
                joueurs_partie.append(jp)

            # Créer le pot et la partie
            pot = Pot()
            partie = Partie(
                joueurs=joueurs_partie,
                jour=1,
                pot=pot,
                id_partie=self.id_compteur
            )
            self.id_compteur += 1

            # Répartition des blinds et déroulement du tour
            partie.repartition_blind()
            partie.gérer_blind()
            partie.finir_partie()

        except Exception as e:
            return f"Erreur lors du lancement de la partie : {str(e)}"
