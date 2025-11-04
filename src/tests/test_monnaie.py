import pytest
from src.business_object.monnaie import Monnaie

class TestMonnaie :
    def test_creation_ok(self):
        # GIVEN
        valeur_initiale = 100

        # WHEN
        monnaie = Monnaie(valeur_initiale)

        # THEN
        assert monnaie.get() == valeur_initiale

    def test_creation_valeur_negative_echec(self):
        # THEN + WHEN
        with pytest.raises(ValueError) as excinfo:
            Monnaie(-10)
        assert "ne peut pas être négative" in str(excinfo.value)

    def test_crediter_ok(self):
        # GIVEN
        monnaie = Monnaie(50)

        # WHEN
        monnaie.crediter(20)

        # THEN
        assert monnaie.get() == 70

    def test_crediter_montant_negatif_pas_de_changement(self):
        # GIVEN
        monnaie = Monnaie(50)

        # WHEN
        monnaie.crediter(-10)

        # THEN
        assert monnaie.get() == 50

    def test_debiter_ok(self):
        # GIVEN
        monnaie = Monnaie(100)

        # WHEN
        monnaie.debiter(40)

        # THEN
        assert monnaie.get() == 60

    def test_debiter_solde_insuffisant(self):
        # GIVEN
        monnaie = Monnaie(30)

        # WHEN / THEN
        with pytest.raises(ValueError) as excinfo:
            monnaie.debiter(50)
        assert "Solde insuffisant" in str(excinfo.value)

    def test_debiter_montant_negatif_pas_de_changement(self):
        # GIVEN
        monnaie = Monnaie(80)

        # WHEN
        monnaie.debiter(-20)

        # THEN
        assert monnaie.get() == 80
