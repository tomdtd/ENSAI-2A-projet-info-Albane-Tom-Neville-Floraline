from datetime import datetime
from utils.log_decorator import log
from dao.transaction_dao import TransactionDao
from business_object.transaction import Transaction

class TransactionService:
    """Service pour gérer les transactions financières des joueurs"""

    def __init__(self, logger=None):
        self.logger = logger
        self.dao = TransactionDao()

    @log
    def enregistrer_transaction(self, joueur_id: int, montant: int) -> Transaction:
        """Crée et enregistre une transaction (crédit ou débit) pour un joueur."""
        transaction = Transaction(
            id_transaction=None,  # la DB gère l'ID
            id_joueur=joueur_id,
            solde=montant,
            date=datetime.now()
        )
        success = self.dao.creer(transaction)
        if not success:
            if self.logger:
                self.logger.error(f"Impossible d'enregistrer la transaction : {transaction}")
            return None
        if self.logger:
            self.logger.info(f"Transaction enregistrée : {transaction}")
        return transaction

    @log
    def historique_joueur(self, joueur_id: int) -> list[Transaction]:
        """Retourne l'historique des transactions pour un joueur depuis la DB"""
        return self.dao.lister_par_joueur(joueur_id)

