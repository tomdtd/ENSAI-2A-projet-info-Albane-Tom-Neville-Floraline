from datetime import datetime
from utils.log_decorator import log
from src.business_object.transaction import Transaction


class TransactionService:
    """Service pour gérer les transactions financières des joueurs"""

    def __init__(self, logger=None):
        self.logger = logger
        self.id_compteur = 1  # Identifiant unique de transaction
        self.transactions: list[Transaction] = []

    @log
    def enregistrer_transaction(self, joueur_id: int, montant: int) -> Transaction:
        """
        Crée et enregistre une transaction (crédit ou débit) pour un joueur.
        """
        transaction = Transaction(
            id_transaction=self.id_compteur,
            id_joueur=joueur_id,
            solde=montant,
            date=datetime.now()
        )
        self.transactions.append(transaction)
        self.id_compteur += 1

        if self.logger:
            self.logger.info(f"Transaction enregistrée : {transaction}")

        return transaction

    @log
    def historique_joueur(self, joueur_id: int) -> list[Transaction]:
        """
        Retourne l'historique des transactions pour un joueur donné.
        """
        return [t for t in self.transactions if t.id_joueur == joueur_id]

    @log
    def solde_total_joueur(self, joueur_id: int) -> int:
        """
        Calcule le solde cumulé d’un joueur à partir de ses transactions.
        """
        return sum(t.solde for t in self.transactions if t.id_joueur == joueur_id)

    @log
    def afficher_historique(self, joueur_id: int) -> None:
        """
        Affiche l’historique des transactions d’un joueur.
        """
        historique = self.historique_joueur(joueur_id)
        for t in historique:
            print(t)
