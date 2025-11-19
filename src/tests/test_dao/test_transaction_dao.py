import os
import pytest

from unittest.mock import patch

from src.utils.reset_database import ResetDatabase
from src.utils.securite import hash_password

from src.dao.db_connection import DBConnection
from src.dao.transaction_dao import TransactionDao

from src.business_object.transaction import Transaction
from datetime import datetime

from pathlib import Path
from dotenv import load_dotenv

@pytest.fixture(scope="session", autouse=True)
def conn_info():
    chemin = Path(__file__).parent / ".env_test"
    load_dotenv(dotenv_path=chemin, override=True)
    try:
        ResetDatabase().lancer(test_dao=True)
    except Exception as e:
        pytest.exit(f"Impossible d'initialiser la base de test : {e}")
    yield

def test_creer_ok():
    """Création d'une Transaction' réussie"""

    # GIVEN
    transaction = Transaction(id_transaction=1, id_joueur=999, solde=5, date=datetime.strptime("2025-11-05 14:32:10", "%Y-%m-%d %H:%M:%S"))

    # WHEN
    creation_ok = TransactionDao().creer(transaction)

    # THEN
    assert creation_ok
    assert transaction.id_transaction

