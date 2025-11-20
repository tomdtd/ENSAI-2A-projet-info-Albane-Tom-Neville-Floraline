import os
import pytest

from unittest.mock import patch, MagicMock

from src.utils.reset_database import ResetDatabase
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


class TestTransactionDao:
    """Tests pour la classe TransactionDao"""

    def setup_method(self):
        """Initialisation avant chaque test"""
        TransactionDao._instances = {}

    def test_creer_transaction(self):
        """Test création d'une transaction"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {"id_transaction": 1}
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

            transaction = Transaction(id_joueur=999, solde=100, date=datetime.now())
            dao = TransactionDao()
            result = dao.creer(transaction)

            assert result is True
            assert transaction.id_transaction == 1

    def test_lister_par_joueur(self):
        """Test listage des transactions d'un joueur"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = [
                {
                    "id_transaction": 1,
                    "id_joueur": 999,
                    "solde": 100,
                    "date": datetime.now(),
                    "statut": "validee",
                    "id_admin": 1,
                    "date_validation": datetime.now()
                }
            ]
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

            dao = TransactionDao()
            transactions = dao.lister_par_joueur(999)

            assert len(transactions) == 1
            assert transactions[0].statut == "validee"

    def test_trouver_par_id(self):
        """Test recherche par ID"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {
                "id_transaction": 1,
                "id_joueur": 999,
                "solde": 100,
                "date": datetime.now(),
                "statut": "validee",
                "id_admin": 1,
                "date_validation": datetime.now()
            }
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

            dao = TransactionDao()
            transaction = dao.trouver_par_id(1)

            assert transaction is not None
            assert transaction.statut == "validee"

    def test_lister_toutes(self):
        """Test listage de toutes les transactions"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = [
                {
                    "id_transaction": 1,
                    "id_joueur": 999,
                    "solde": 100,
                    "date": datetime.now(),
                    "statut": "en_attente",
                    "id_admin": None,
                    "date_validation": None
                }
            ]
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

            dao = TransactionDao()
            transactions = dao.lister_toutes()

            assert len(transactions) == 1

    def test_supprimer(self):
        """Test suppression d'une transaction"""
        with patch.object(DBConnection, 'connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.rowcount = 1
            mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

            dao = TransactionDao()
            result = dao.supprimer(1)

            assert result is True
