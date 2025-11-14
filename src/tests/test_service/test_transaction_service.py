import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.service.transaction_service import TransactionService
from src.business_object.transaction import Transaction

@pytest.fixture
def transaction_service():
    return TransactionService()

def test_enregistrer_transaction(transaction_service):
    # GIVEN
    joueur_id = 1
    montant = 100

    # WHEN
    transaction = transaction_service.enregistrer_transaction(joueur_id, montant)

    # THEN
    assert transaction is not None
    assert transaction.id_transaction == 1
    assert transaction.id_joueur == joueur_id
    assert transaction.solde == montant
    assert isinstance(transaction.date, datetime)
    assert len(transaction_service.transactions) == 1

def test_enregistrer_plusieurs_transactions(transaction_service):
    # GIVEN
    joueur_id = 1
    montants = [100, 200, 300]

    # WHEN
    transactions = []
    for montant in montants:
        transaction = transaction_service.enregistrer_transaction(joueur_id, montant)
        transactions.append(transaction)

    # THEN
    assert len(transactions) == 3
    assert len(transaction_service.transactions) == 3
    for i, transaction in enumerate(transactions):
        assert transaction.id_transaction == i + 1
        assert transaction.id_joueur == joueur_id
        assert transaction.solde == montants[i]
        assert isinstance(transaction.date, datetime)

def test_historique_joueur(transaction_service):
    # GIVEN
    joueur_id_1 = 1
    joueur_id_2 = 2
    montants_1 = [100, 200]
    montants_2 = [300, 400]

    for montant in montants_1:
        transaction_service.enregistrer_transaction(joueur_id_1, montant)
    for montant in montants_2:
        transaction_service.enregistrer_transaction(joueur_id_2, montant)

    # WHEN
    historique_1 = transaction_service.historique_joueur(joueur_id_1)
    historique_2 = transaction_service.historique_joueur(joueur_id_2)

    # THEN
    assert len(historique_1) == 2
    assert len(historique_2) == 2
    for i, transaction in enumerate(historique_1):
        assert transaction.solde == montants_1[i]
    for i, transaction in enumerate(historique_2):
        assert transaction.solde == montants_2[i]

def test_solde_total_joueur(transaction_service):
    # GIVEN
    joueur_id_1 = 1
    joueur_id_2 = 2
    montants_1 = [100, 200]
    montants_2 = [300, 400]

    for montant in montants_1:
        transaction_service.enregistrer_transaction(joueur_id_1, montant)
    for montant in montants_2:
        transaction_service.enregistrer_transaction(joueur_id_2, montant)

    # WHEN
    solde_1 = transaction_service.solde_total_joueur(joueur_id_1)
    solde_2 = transaction_service.solde_total_joueur(joueur_id_2)

    # THEN
    assert solde_1 == sum(montants_1)
    assert solde_2 == sum(montants_2)

def test_afficher_historique(transaction_service, capsys):
    # GIVEN
    joueur_id = 1
    montants = [100, 200]

    for montant in montants:
        transaction_service.enregistrer_transaction(joueur_id, montant)

    # WHEN
    transaction_service.afficher_historique(joueur_id)

    # THEN
    captured = capsys.readouterr()
    assert "Transaction" in captured.out

def test_enregistrer_transaction_avec_logger(transaction_service):
    # GIVEN
    joueur_id = 1
    montant = 100
    logger = MagicMock()
    transaction_service.logger = logger

    # WHEN
    transaction = transaction_service.enregistrer_transaction(joueur_id, montant)

    # THEN
    assert transaction is not None
    logger.info.assert_called_once()
