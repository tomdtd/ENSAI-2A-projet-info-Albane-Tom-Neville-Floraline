import pytest
from src.business_object.siege import Siege
from src.business_object.monnaie import Monnaie
from src.business_object.table import Table

class TestTable:
    
    @pytest.fixture
    def monnaie_initial(self):
        return Monnaie(100)
    
    @pytest.fixture
    def table_vide(self, monnaie_initial):
        """Retourne une table vide avec 6 sièges"""
        return Table(id_table=1, nb_sieges=6, blind_initial=monnaie_initial)
    
    def test_initialisation(self, monnaie_initial):
        """Test de l'initialisation d'une table"""
        table = Table(id_table=1, nb_sieges=6, blind_initial=monnaie_initial)
        
        assert table.id_table == 1
        assert table.nb_sieges == 6
        assert table.blind_initial == monnaie_initial
        assert len(table.sieges) == 6
    
    def test_table_remplie_vide(self, table_vide):
        """Test table_remplie() sur une table vide"""
        assert table_vide.table_remplie() == False
    
    def test_table_remplie_pleine(self, table_vide):
        """Test table_remplie() sur une table pleine"""
        # Occuper tous les sièges
        for i in range(6):
            table_vide.sieges[i].occupe = True
            table_vide.sieges[i].id_joueur = i + 1
        
        assert table_vide.table_remplie() == True
    
    def test_get_joueurs_table_vide(self, table_vide):
        """Test get_joueurs() sur une table vide"""
        joueurs = table_vide.get_joueurs()
        assert len(joueurs) == 0
        assert joueurs == []
    
    def test_get_joueurs_table_pleine(self, table_vide):
        """Test get_joueurs() sur une table pleine"""
        # Occuper tous les sièges
        for i in range(6):
            table_vide.sieges[i].occupe = True
            table_vide.sieges[i].id_joueur = i + 1
        
        joueurs = table_vide.get_joueurs()
        assert len(joueurs) == 6
        assert set(joueurs) == {1, 2, 3, 4, 5, 6}
    
    def test_get_joueurs_partiel(self, table_vide):
        """Test get_joueurs() sur une table partiellement remplie"""
        # Occuper seulement 3 sièges
        for i in range(3):
            table_vide.sieges[i].occupe = True
            table_vide.sieges[i].id_joueur = i + 1
        
        joueurs = table_vide.get_joueurs()
        assert len(joueurs) == 3
        assert set(joueurs) == {1, 2, 3}
    
    def test_siege_occupe_sans_joueur(self, table_vide):
        """Test d'un siège occupé sans id_joueur"""
        table_vide.sieges[0].occupe = True
        table_vide.sieges[0].id_joueur = None
        
        joueurs = table_vide.get_joueurs()
        assert len(joueurs) == 0