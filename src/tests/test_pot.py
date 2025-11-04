import pytest
from src.business_object.pot import Pot

class TestPot : 
    def test_initialisation_pot(self):
        # GIVEN / WHEN
        pot = Pot()

        # THEN
        assert isinstance(pot.montant_pot, Monnaie)
        assert pot.get_montant() == 0

    def test_ajouter_mise_augmenter_montant(self):
        # GIVEN
        pot = Pot()

        # WHEN
        pot.ajouter_mise(50)

        # THEN
        assert pot.get_montant() == 50

    def test_ajouter_plusieurs_mises(self):
        # GIVEN
        pot = Pot()

        # WHEN
        pot.ajouter_mise(30)
        pot.ajouter_mise(20)

        # THEN
        assert pot.get_montant() == 50

    def test_ajouter_mise_zero_ou_negative(self):
        # GIVEN
        pot = Pot()

        # WHEN
        pot.ajouter_mise(0)
        pot.ajouter_mise(-10)

        # THEN
        # Aucune mise négative ne doit être ajoutée
        assert pot.get_montant() == 0

    def test_reinitialiser_pot(self):
        # GIVEN
        pot = Pot()
        pot.ajouter_mise(100)

        # WHEN
        pot.reinitialiser_pot()

        # THEN
        assert pot.get_montant() == 0
        assert isinstance(pot.montant_pot, Monnaie)
