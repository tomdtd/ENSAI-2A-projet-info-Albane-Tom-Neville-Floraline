import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase
from src.dao.db_connection import DBConnection
from src.dao.table_dao import TableDao

from src.business_object.table import Table
from src.business_object.monnaie import Monnaie

from pathlib import Path
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def conn_info():
    chemin = Path(__file__).parent / ".env_test"
    load_dotenv(dotenv_path=chemin, override=True)
    try:
        ResetDatabase().lancer(test_dao=True)
    except Exception as e:
        pytest.exit(f"Impossible d'initialiser la base de test : {e}")
    yield


def test_trouver_par_id_existant():
    """Recherche par id d'une table existante"""

    # GIVEN
    id_table = 1

    # WHEN
    table = TableDao().trouver_par_id(id_table)

    # THEN
    assert table is not None
    assert table.id_table == id_table
    assert isinstance(table, Table)


def test_trouver_par_id_non_existant():
    """Recherche par id d'une table n'existant pas"""

    # GIVEN
    id_table = 9999999999999

    # WHEN
    table = TableDao().trouver_par_id(id_table)

    # THEN
    assert table is None


def test_lister_toutes():
    """Vérifie que la méthode renvoie une liste de Table"""

    # GIVEN

    # WHEN
    tables = TableDao().lister_toutes()

    # THEN
    assert isinstance(tables, list)
    for table in tables:
        assert isinstance(table, Table)
    assert len(tables) >= 1


def test_creer_ok():
    """Création de Table réussie"""

    # GIVEN
    table = Table(
        id_table=100,
        nb_sieges=6,
        blind_initial=Monnaie(10.0)
    )

    # WHEN
    creation_ok = TableDao().creer(table)

    # THEN
    assert creation_ok


def test_creer_ko():
    """Création de Table échouée (données incorrectes)"""

    # GIVEN
    # Table avec des données invalides (id_table déjà existant)
    table = Table(
        id_table=1,  # ID déjà existant
        nb_sieges=6,
        blind_initial=Monnaie(10.0)
    )

    # WHEN
    creation_ok = TableDao().creer(table)

    # THEN
    # La création devrait échouer à cause de la violation de clé primaire
    assert not creation_ok


def test_modifier_ok():
    """Modification de Table réussie"""

    # GIVEN
    # Créer d'abord une table à modifier
    table = Table(
        id_table=102,
        nb_sieges=4,
        blind_initial=Monnaie(5.0)
    )
    TableDao().creer(table)
    
    # Modifier la table
    table.nb_sieges = 8
    table.blind_initial = Monnaie(20.0)

    # WHEN
    modification_ok = TableDao().modifier(table)

    # THEN
    assert modification_ok
    
    # Vérifier que les modifications ont bien été enregistrées
    table_modifiee = TableDao().trouver_par_id(102)
    assert table_modifiee.nb_sieges == 8
    assert table_modifiee.blind_initial.get() == 20.0


def test_modifier_ko():
    """Modification de Table échouée (id inconnu)"""

    # GIVEN
    table = Table(
        id_table=999999,
        nb_sieges=4,
        blind_initial=Monnaie(5.0)
    )

    # WHEN
    modification_ok = TableDao().modifier(table)

    # THEN
    assert not modification_ok


def test_supprimer_ok():
    """Suppression de Table réussie"""

    # GIVEN
    # Créer d'abord une table à supprimer
    table = Table(
        id_table=103,
        nb_sieges=4,
        blind_initial=Monnaie(5.0)
    )
    TableDao().creer(table)
    
    # Vérifier que la table existe
    table_existante = TableDao().trouver_par_id(103)
    assert table_existante is not None

    # WHEN
    suppression_ok = TableDao().supprimer(103)

    # THEN
    assert suppression_ok
    
    # Vérifier que la table n'existe plus
    table_supprimee = TableDao().trouver_par_id(103)
    assert table_supprimee is None


def test_supprimer_ko():
    """Suppression de Table échouée (id inconnu)"""

    # GIVEN
    id_table_inexistant = 999999

    # WHEN
    suppression_ok = TableDao().supprimer(id_table_inexistant)

    # THEN
    assert not suppression_ok


def test_lister_tables_avec_sieges_disponibles():
    """Test de la liste des tables avec sièges disponibles"""

    # GIVEN
    # S'assurer qu'il y a des tables avec des sièges disponibles
    # (la base de test devrait déjà en contenir)

    # WHEN
    tables_disponibles = TableDao().lister_tables_avec_sieges_disponibles()

    # THEN
    assert isinstance(tables_disponibles, list)
    
    # Vérifier que tous les éléments sont des Tables
    for table in tables_disponibles:
        assert isinstance(table, Table)


def test_table_avec_monnaie():
    """Test que l'objet Monnaie est correctement géré"""

    # GIVEN
    table = Table(
        id_table=106,
        nb_sieges=4,
        blind_initial=Monnaie(15.50)
    )

    # WHEN
    creation_ok = TableDao().creer(table)
    table_recuperee = TableDao().trouver_par_id(106)

    # THEN
    assert creation_ok
    assert table_recuperee is not None
    assert isinstance(table_recuperee.blind_initial, Monnaie)
    assert table_recuperee.blind_initial.get() == 15.50


if __name__ == "__main__":
    pytest.main([__file__])