import pytest
from datetime import datetime
from src.business_object.transaction import Transaction

class TestTransaction:
    """Tests unitaires pour la classe Transaction."""

    def test_transaction_valide_ok(self):
        """Vérifie la création correcte d'une transaction valide."""
        # GIVEN
        date_now = datetime(2025, 10, 29, 15, 30, 0)
        id_transaction = 1
        id_joueur = 123
        solde = 500

        # WHEN
        transaction = Transaction(id_joueur=id_joueur, solde=solde, date=date_now, id_transaction=id_transaction)

        # THEN
        assert transaction.id_transaction == id_transaction
        assert transaction.id_joueur == id_joueur
        assert transaction.solde == solde
        assert transaction.date == date_now

    def test_transaction_sans_id_transaction(self):
        """Vérifie la création d'une transaction sans id_transaction."""
        # GIVEN
        date_now = datetime(2025, 10, 29, 15, 30, 0)
        id_joueur = 123
        solde = 500

        # WHEN
        transaction = Transaction(id_joueur=id_joueur, solde=solde, date=date_now)

        # THEN
        assert transaction.id_transaction is None
        assert transaction.id_joueur == id_joueur
        assert transaction.solde == solde
        assert transaction.date == date_now

    def test_transaction_str_repr(self):
        """Vérifie que les méthodes __str__ et __repr__ renvoient le bon format."""
        # GIVEN
        date_now = datetime(2025, 10, 29, 15, 30, 0)
        transaction = Transaction(id_joueur=123, solde=-150, date=date_now, id_transaction=2)

        # WHEN
        str_output = str(transaction)
        repr_output = repr(transaction)

        # THEN
        assert "Transaction 2" in str_output
        assert "123" in str_output
        assert "-150" in str_output
        assert "2025-10-29" in str_output
        assert "Transaction" in repr_output
        assert "id_transaction=2" in repr_output
        assert "id_joueur=123" in repr_output

    def test_transaction_id_transaction_invalide(self):
        """Vérifie qu'une transaction avec un id_transaction invalide provoque une erreur."""
        with pytest.raises(TypeError):
            Transaction(id_joueur=123, solde=100, date=datetime.now(), id_transaction="not_an_int")

    def test_transaction_joueur_id_invalide(self):
        """Vérifie qu'une transaction avec un id_joueur invalide provoque une erreur."""
        with pytest.raises(TypeError):
            Transaction(id_joueur="not_an_int", solde=100, date=datetime.now())

    def test_transaction_solde_invalide(self):
        """Vérifie qu'une transaction avec un solde invalide provoque une erreur."""
        with pytest.raises(TypeError):
            Transaction(id_joueur=123, solde="not_an_int", date=datetime.now())

    def test_transaction_date_invalide(self):
        """Vérifie qu'une transaction avec une date invalide provoque une erreur."""
        with pytest.raises(TypeError):
            Transaction(id_joueur=123, solde=100, date="not_a_datetime")


