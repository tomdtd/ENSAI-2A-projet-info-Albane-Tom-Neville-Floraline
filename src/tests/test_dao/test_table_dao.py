import pytest
from src.business_object.monnaie import Monnaie
from src.dao.table_dao import TableDAO


class TestTableDAO:
    
    @pytest.fixture
    def dao(self):
        return TableDAO()
    
    @pytest.fixture
    def monnaie_100(self):
        return Monnaie(100)
    
    def test_creer_table(self, dao, monnaie_100):
        table = dao.creer_table(6, monnaie_100)
        
        assert table.id_table == 1
        assert table.nb_sieges == 6
        assert table.blind_initial.valeur == 100
        assert dao.get_nombre_tables() == 1
    
    def test_get_table_par_id(self, dao, monnaie_100):
        table = dao.creer_table(4, monnaie_100)
        table_recuperee = dao.get_table_par_id(1)
        
        assert table_recuperee == table
        assert dao.get_table_par_id(999) is None
    
    def test_get_toutes_tables(self, dao, monnaie_100):
        table1 = dao.creer_table(4, monnaie_100)
        table2 = dao.creer_table(6, Monnaie(200))
        
        tables = dao.get_toutes_tables()
        
        assert len(tables) == 2
        assert table1 in tables
        assert table2 in tables
    
    def test_get_tables_disponibles(self, dao, monnaie_100):
        table1 = dao.creer_table(2, monnaie_100)
        table2 = dao.creer_table(2, monnaie_100)
        
        # Remplir la première table
        for siege in table1.sieges:
            siege.occupe = True
            siege.id_joueur = 1
        
        tables_disponibles = dao.get_tables_disponibles()
        
        assert len(tables_disponibles) == 1
        assert table2 in tables_disponibles
        assert table1 not in tables_disponibles
    
    def test_supprimer_table(self, dao, monnaie_100):
        dao.creer_table(4, monnaie_100)
        
        assert dao.get_nombre_tables() == 1
        assert dao.supprimer_table(1) == True
        assert dao.get_nombre_tables() == 0
        assert dao.supprimer_table(999) == False
    
    def test_get_table_par_joueur(self, dao, monnaie_100):
        table = dao.creer_table(4, monnaie_100)
        
        # Ajouter un joueur à la table
        table.sieges[0].occupe = True
        table.sieges[0].id_joueur = 101
        
        table_trouvee = dao.get_table_par_joueur(101)
        
        assert table_trouvee == table
        assert dao.get_table_par_joueur(999) is None
    
    def test_table_existe(self, dao, monnaie_100):
        dao.creer_table(4, monnaie_100)
        
        assert dao.table_existe(1) == True
        assert dao.table_existe(999) == False
    
    def test_ids_incrementaux(self, dao, monnaie_100):
        table1 = dao.creer_table(4, monnaie_100)
        table2 = dao.creer_table(6, monnaie_100)
        table3 = dao.creer_table(8, monnaie_100)
        
        assert table1.id_table == 1
        assert table2.id_table == 2
        assert table3.id_table == 3