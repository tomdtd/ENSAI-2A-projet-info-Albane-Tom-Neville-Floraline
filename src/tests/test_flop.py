import pytest
from src.business_object.flop import Flop
from src.business_object.carte import Carte
from src.business_object.liste_cartes import ListeCartes

class TestFlop():
    def test_flop_valide_ok(self) :
        # GIVEN
        cartes = [
            Carte("As", "Pique"),
            Carte("Roi", "Coeur"),
            Carte("Dame", "Trêfle")
        ]

        # WHEN
        flop = Flop(cartes)

        # THEN
        assert len(flop.cartes) == 3
        assert flop.cartes == cartes
    
    def test_flop_non_valide(self): 
        # GIVEN
        cartes = [
            Carte("As", "Pique"),
            Carte("Roi", "Coeur")
        ]

        # WHEN / THEN
        with pytest.raises(ValueError) as excinfo:
            Flop(cartes)
        assert "Le flop doit contenir entre 3 et 5 cartes" in str(excinfo.value)

