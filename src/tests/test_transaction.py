import pytest
from datetime import datetime
from src.business_object.transaction import Transaction


class TestTransaction:
    """Tests unitaires pour la classe Transaction."""
                                                     
    def test_transaction_valide_ok(self):
        """Vérifie la création correcte d'une transaction valide."""
        # GIVEN
        date_now = datetime(2025, 10, 29, 15, 30, 0)

        # WHEN
        transaction = Transaction(1, "joueur123", 500, date_now)

        # THEN
        assert transaction.id_transaction == 1
        assert transaction.id_joueur == "joueur123"
        assert transaction.solde == 500
        assert transaction.date == date_now

    def test_transaction_str_repr(self):
        """Vérifie que les méthodes __str__ et __repr__ renvoient le bon format."""
        # GIVEN
        date_now = datetime(2025, 10, 29, 15, 30, 0)
        transaction = Transaction(2, "Tom", -150, date_now)

        # WHEN
        str_output = str(transaction)
        repr_output = repr(transaction)

        # THEN
        assert "Transaction 2" in str_output
        assert "Tom" in str_output
        assert "-150" in str_output
        assert "2025-10-29" in str_output

        assert "Transaction" in repr_output
        assert "id_transaction=2" in repr_output
        assert "id_joueur='Tom'" in repr_output

    def test_transaction_id_transaction_invalide(self):
        """Vérifie qu'une transaction sans id provoque une erreur."""
        with pytest.raises(TypeError):
            Transaction(None, "Tom", 100, datetime.now())

    def test_transaction_joueur_id_invalide(self):
        """Vérifie qu'une transaction sans joueur provoque une erreur."""
        with pytest.raises(TypeError):
            Transaction(1, None, 100, datetime.now())

    def test_transaction_solde_invalide(self):
        """Vérifie qu'une transaction sans solde provoque une erreur."""
        with pytest.raises(TypeError):
            Transaction(1, "Tom", None, datetime.now())

    def test_transaction_date_invalide(self):
        """Vérifie qu'une transaction sans date provoque une erreur."""
        with pytest.raises(TypeError):
            Transaction(1, "Tom", 100, None)