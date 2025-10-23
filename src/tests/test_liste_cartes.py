import pytest
from src.business_object.liste_cartes import ListeCartes

class TestListeCartes():
    def test_creation_liste_cartes_ok(self):
        # GIVEN
        liste_cartes = [pytest.as_coeur]

        # WHEN
        cartes = ListeCartes(liste_cartes)

        # THEN
        assert cartes.get_cartes() == [pytest.as_coeur]
    
    def test_creation_carte_echec_1(self):
        # GIVEN
        liste_cartes = (pytest.as_coeur, pytest.deux_pique)

        message_attendu = f"{liste_cartes} doit être une liste."

        # THEN
        with pytest.raises(ValueError, match=re.escape(expected_message)):
            # WHEN
            ListeCartes(liste_cartes)

    def test_creation_carte_echec_2(self):
        # GIVEN
        liste_cartes = [pytest.as_coeur, "2 de Pique"]

        message_attendu = f"Tous les elements de {liste_cartes} doivent être des cartes."

        # THEN
        with pytest.raises(ValueError, match=re.escape(expected_message)):
            # WHEN
            ListeCartes(liste_cartes)
                                        