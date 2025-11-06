import pytest
from src.business_object.monnaie import Monnaie
from src.business_object.table import Table


class TestTable:
    """Tests simples pour la classe Table"""
    
    def test_creation_table(self):
        """Test la création d'une table"""
        table = Table(1, 6, Monnaie(100))
        
        assert table.id_table == 1
        assert table.nb_sieges == 6
        assert table.blind_initial.valeur == 100
        
    def test_table_vide_non_remplie(self):
        """Test qu'une table vide n'est pas remplie"""
        table = Table(1, 4, Monnaie(50))
        
        assert table.table_remplie() == False
        
    def test_table_pleine_est_remplie(self):
        """Test qu'une table pleine est remplie"""
        table = Table(1, 3, Monnaie(50))
        
        # Remplir tous les sièges avec des IDs différents
        for i, siege in enumerate(table.sieges):
            siege.id_joueur = i + 1
            siege.occupe = True
        assert table.table_remplie() == True
        
    def test_get_joueurs_table_vide(self):
        """Test get_joueurs sur une table vide"""
        table = Table(1, 4, Monnaie(100))
        
        joueurs = table.get_joueurs()
        
        assert joueurs == []
        
    def test_get_joueurs_avec_joueurs(self):
        """Test get_joueurs avec des joueurs"""
        table = Table(1, 4, Monnaie(100))
        
        # Ajouter quelques joueurs 
        table.sieges[0].id_joueur = 101
        table.sieges[0].est_occupe()
        table.sieges[2].id_joueur = 102
        table.sieges[2].est_occupe()
        
        joueurs = table.get_joueurs()
        
        assert joueurs == [101, 102]