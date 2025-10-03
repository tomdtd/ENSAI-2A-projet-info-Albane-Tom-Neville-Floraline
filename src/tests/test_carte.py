import pytest
from src.business_object.carte import Carte

class TestCarte():
    def test_creation_carte_ok(self):
        # GIVEN
        valeur = "As"
        couleur = "Pique"

        # WHEN
        carte = Carte(valeur, couleur)

        # THEN
        assert carte.valeur == valeur
        assert carte.couleur == couleur
        assert str(carte) == "As de pique"
        assert repr(carte) == "Carte('As', 'Pique')"

    def test_creation_carte_non_ok(self):
        # GIVEN
        valeur = "11"  # valeur inexistante
        couleur = "Pique"

        # WHEN / THEN
        with pytest.raises(ValueError) as excinfo:
            Carte(valeur, couleur)
        assert "non valide" in str(excinfo.value)