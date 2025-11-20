import os
import pytest

from unittest.mock import patch

from src.utils.reset_database import ResetDatabase
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


def test_creer_et_trouver_table():
    """Test de création d'une table et recherche par id"""

    # GIVEN
    table = Table(
        nb_sieges=6,
        blind_initial=Monnaie(10.0)
    )

    # WHEN
    creation_ok = TableDao().creer(table)

    # THEN
    assert creation_ok
    assert table.id_table is not None  # L'ID a été généré automatiquement

    # Vérifier qu'on peut la retrouver
    table_trouvee = TableDao().trouver_par_id(table.id_table)
    assert table_trouvee is not None
    assert table_trouvee.id_table == table.id_table
    assert table_trouvee.nb_sieges == 6
    assert table_trouvee.blind_initial.get() == 10.0


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

    # WHEN
    tables = TableDao().lister_toutes()

    # THEN
    assert isinstance(tables, list)
    for table in tables:
        assert isinstance(table, Table)
    assert len(tables) >= 1


def test_modifier_table():
    """Test de modification d'une table"""

    # GIVEN - Créer une table à modifier
    table = Table(
        nb_sieges=4,
        blind_initial=Monnaie(5.0)
    )
    TableDao().creer(table)
    id_table = table.id_table

    # Modifier la table
    table.nb_sieges = 8
    table.blind_initial = Monnaie(20.0)

    # WHEN
    modification_ok = TableDao().modifier(table)

    # THEN
    assert modification_ok

    # Vérifier que les modifications ont été enregistrées
    table_modifiee = TableDao().trouver_par_id(id_table)
    assert table_modifiee.nb_sieges == 8
    assert table_modifiee.blind_initial.get() == 20.0


def test_supprimer_table():
    """Test de suppression d'une table"""

    # GIVEN - Créer une table à supprimer
    table = Table(
        nb_sieges=4,
        blind_initial=Monnaie(5.0)
    )
    TableDao().creer(table)
    id_table = table.id_table

    # Vérifier que la table existe
    assert TableDao().trouver_par_id(id_table) is not None

    # WHEN
    suppression_ok = TableDao().supprimer(id_table)

    # THEN
    assert suppression_ok
    assert TableDao().trouver_par_id(id_table) is None


if __name__ == "__main__":
    pytest.main([__file__])