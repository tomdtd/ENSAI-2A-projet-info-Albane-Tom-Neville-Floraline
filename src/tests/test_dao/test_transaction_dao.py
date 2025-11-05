import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase
from utils.securite import hash_password

from dao.db_connection import DBConnection
from dao.transaction_dao import TransactionDao

from business_object.transaction import Transaction

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield

def test_creer_ok():
    """Création d'une Transaction' réussie"""

    # GIVEN
    transaction = Transaction(id_transaction=1, id_joueur=999, solde=5, date=1)

    # WHEN
    creation_ok = TransactionDao().creer(transaction)

    # THEN
    assert creation_ok
    assert transaction.id_transaction
