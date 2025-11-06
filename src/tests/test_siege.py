import pytest
from src.business_object.siege import Siege
class TestSiegePytest:
    
    @pytest.fixture
    def siege_vide(self):
        return Siege(id_siege=1)
    
    def test_initialisation(self, siege_vide):
        assert siege_vide.id_siege == 1
        assert siege_vide.occupe == False
        assert siege_vide.id_joueur is None
    
    def test_est_occupe(self, siege_vide):
        assert siege_vide.est_occupe() == False
        
        siege_vide.occupe = True
        assert siege_vide.est_occupe() == True
    
    def test_occupation_avec_joueur(self, siege_vide):
        siege_vide.occupe = True
        siege_vide.id_joueur = "JoueurTest"
        
        assert siege_vide.est_occupe() == True
        assert siege_vide.id_joueur == "JoueurTest"
    
    @pytest.mark.parametrize("id_siege", [1, 2, 3, 5])
    def test_differents_ids(self, id_siege):
        siege = Siege(id_siege=id_siege)
        assert siege.id_siege == id_siege
        