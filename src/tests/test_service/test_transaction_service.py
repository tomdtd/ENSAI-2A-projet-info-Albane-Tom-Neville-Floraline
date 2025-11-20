import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.service.transaction_service import TransactionService
from src.dao.transaction_dao import TransactionDao
from src.business_object.transaction import Transaction


@pytest.fixture
def mock_transaction_dao():
    with patch.object(TransactionDao, 'creer') as mock_creer, \
         patch.object(TransactionDao, 'lister_par_joueur') as mock_lister_par_joueur:
        yield {
            "creer": mock_creer,
            "lister_par_joueur": mock_lister_par_joueur,
        }


def test_enregistrer_transaction(mock_transaction_dao):
    # GIVEN
    joueur_id = 1
    montant = 100
    mock_transaction_dao["creer"].return_value = True

    # WHEN
    transaction_service = TransactionService()
    transaction = transaction_service.enregistrer_transaction(joueur_id, montant)

    # THEN
    assert transaction is not None
    assert transaction.id_joueur == joueur_id
    assert transaction.solde == montant
    assert isinstance(transaction.date, datetime)
    mock_transaction_dao["creer"].assert_called_once()


def test_enregistrer_transaction_echec(mock_transaction_dao):
    # GIVEN
    joueur_id = 1
    montant = 100
    mock_transaction_dao["creer"].return_value = False

    # WHEN
    transaction_service = TransactionService()
    transaction = transaction_service.enregistrer_transaction(joueur_id, montant)

    # THEN
    assert transaction is None
    mock_transaction_dao["creer"].assert_called_once()


def test_historique_joueur(mock_transaction_dao):
    # GIVEN
    joueur_id = 1
    mock_transactions = [
        Transaction(id_transaction=1, id_joueur=joueur_id, solde=100, date=datetime.now()),
        Transaction(id_transaction=2, id_joueur=joueur_id, solde=200, date=datetime.now()),
    ]
    mock_transaction_dao["lister_par_joueur"].return_value = mock_transactions

    # WHEN
    transaction_service = TransactionService()
    historique = transaction_service.historique_joueur(joueur_id)

    # THEN
    assert len(historique) == 2
    assert historique[0].solde == 100
    assert historique[1].solde == 200
    mock_transaction_dao["lister_par_joueur"].assert_called_once_with(joueur_id)


def test_historique_joueur_vide(mock_transaction_dao):
    # GIVEN
    joueur_id = 999
    mock_transaction_dao["lister_par_joueur"].return_value = []

    # WHEN
    transaction_service = TransactionService()
    historique = transaction_service.historique_joueur(joueur_id)

    # THEN
    assert len(historique) == 0
    mock_transaction_dao["lister_par_joueur"].assert_called_once_with(joueur_id)


def test_enregistrer_transaction_avec_logger(mock_transaction_dao):
    # GIVEN
    joueur_id = 1
    montant = 100
    logger = MagicMock()
    mock_transaction_dao["creer"].return_value = True

    # WHEN
    transaction_service = TransactionService(logger=logger)
    transaction = transaction_service.enregistrer_transaction(joueur_id, montant)

    # THEN
    assert transaction is not None
    logger.info.assert_called_once()
