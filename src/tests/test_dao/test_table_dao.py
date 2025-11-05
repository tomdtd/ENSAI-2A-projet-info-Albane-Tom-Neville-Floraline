import pytest
from unittest.mock import Mock, patch
from dao.Table_dao import TableDao
from business_object.table import Table

@pytest.fixture
def mock_db_connection():
    """Fixture pour simuler la connexion à la base de données"""
    with patch('dao.table_dao.DBConnection') as mock_db:
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_db.return_value.connection.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.__exit__.return_value = None
        yield mock_cursor

def test_creer_success(mock_db_connection):
    """Test de création d'une table avec succès"""
    # Setup
    table = Table(nom_table="Table VIP", nb_sieges_max=6, blind_initial=10.0)
    mock_db_connection.fetchone.return_value = {"id_table": 1}

    # Execution
    table_dao = TableDao()
    result = Table_dao.creer(table)

    # Vérifications
    assert result is True
    assert table.id_table == 1
    mock_db_connection.execute.assert_called_once_with(
        "INSERT INTO tables (nom_table, nb_sieges_max, blind_initial)"
        "VALUES (%(nom_table)s, %(nb_sieges_max)s, %(blind_initial)s)"
        "RETURNING id_table;",
        {
            "nom_table": "Table VIP",
            "nb_sieges_max": 6,
            "blind_initial": 10.0
        }
    )

def test_creer_failure(mock_db_connection):
    """Test de création d'une table avec échec"""
    # Setup
    table = Table(nom_table="Table VIP", nb_sieges_max=6, blind_initial=10.0)
    mock_db_connection.fetchone.return_value = None

    # Execution
    Table_dao = TableDao()
    result = Table_dao.creer(table)

    # Vérifications
    assert result is False
    assert table.id_table is None

def test_trouver_par_id_success(mock_db_connection):
    """Test de recherche par ID avec succès"""
    # Setup
    mock_table_data = {
        "id_table": 1,
        "nom_table": "Table VIP",
        "nb_sieges_max": 6,
        "blind_initial": 10.0
    }
    mock_db_connection.fetchone.return_value = mock_table_data

    # Execution
    Table_dao = TableDao()
    result = Table_dao.trouver_par_id(1)

    # Vérifications
    assert result is not None
    assert result.id_table == 1
    assert result.nom_table == "Table VIP"
    assert result.nb_sieges_max == 6
    assert result.blind_initial == 10.0
    mock_db_connection.execute.assert_called_once_with(
        "SELECT id_table, nom_table, nb_sieges_max, blind_initial "
        "FROM tables "
        "WHERE id_table = %(id_table)s;",
        {"id_table": 1}
    )

def test_trouver_par_id_not_found(mock_db_connection):
    """Test de recherche par ID quand la table n'existe pas"""
    # Setup
    mock_db_connection.fetchone.return_value = None

    # Execution
    Table_dao = TableDao()
    result = Table_dao.trouver_par_id(999)

    # Vérifications
    assert result is None

def test_mettre_a_jour_success(mock_db_connection):
    """Test de mise à jour d'une table avec succès"""
    # Setup
    table = Table(id_table=1, nom_table="Table VIP Modifiée", nb_sieges_max=8, blind_initial=20.0)
    mock_db_connection.rowcount = 1

    # Execution
    Table_dao = TableDao()
    result = Table_dao.mettre_a_jour(table)

    # Vérifications
    assert result is True
    mock_db_connection.execute.assert_called_once_with(
        "UPDATE tables "
        "SET nom_table = %(nom_table)s, nb_sieges_max = %(nb_sieges_max)s, blind_initial = %(blind_initial)s "
        "WHERE id_table = %(id_table)s;",
        {
            "id_table": 1,
            "nom_table": "Table VIP Modifiée",
            "nb_sieges_max": 8,
            "blind_initial": 20.0
        }
    )

def test_mettre_a_jour_failure(mock_db_connection):
    """Test de mise à jour d'une table avec échec"""
    # Setup
    table = Table(id_table=999, nom_table="Table Inexistante", nb_sieges_max=6, blind_initial=10.0)
    mock_db_connection.rowcount = 0

    # Execution
    Table_dao = TableDao()
    result = Table_dao.mettre_a_jour(table)

    # Vérifications
    assert result is False

def test_supprimer_success(mock_db_connection):
    """Test de suppression d'une table avec succès"""
    # Setup
    mock_db_connection.fetchone.return_value = {"count_parties_actives": 0}
    mock_db_connection.rowcount = 1

    # Execution
    Table_dao = TableDao()
    result = Table_dao.supprimer(1)

    # Vérifications
    assert result is True
    assert mock_db_connection.execute.call_count == 2

def test_supprimer_avec_parties_en_cours(mock_db_connection):
    """Test de suppression d'une table avec parties en cours"""
    # Setup
    mock_db_connection.fetchone.return_value = {"count_parties_actives": 2}

    # Execution & Vérification
    Table_dao = TableDao()
    with pytest.raises(ValueError, match="Impossible de supprimer une table avec des parties en cours"):
        Table_dao.supprimer(1)

def test_supprimer_table_inexistante(mock_db_connection):
    """Test de suppression d'une table qui n'existe pas"""
    # Setup
    mock_db_connection.fetchone.return_value = {"count_parties_actives": 0}
    mock_db_connection.rowcount = 0

    # Execution
    Table_dao = TableDao()
    result = Table_dao.supprimer(999)

    # Vérifications
    assert result is False

def test_supprimer_toutes_success(mock_db_connection):
    """Test de suppression de toutes les tables avec succès"""
    # Setup
    mock_db_connection.fetchone.return_value = {"count_parties_actives": 0}
    mock_db_connection.rowcount = 3

    # Execution
    Table_dao = TableDao()
    result = Table_dao.supprimer_toutes()

    # Vérifications
    assert result is True
    assert mock_db_connection.execute.call_count == 2

def test_supprimer_toutes_avec_parties_en_cours(mock_db_connection):
    """Test de suppression de toutes les tables avec parties en cours"""
    # Setup
    mock_db_connection.fetchone.return_value = {"count_parties_actives": 1}

    # Execution & Vérification
    Table_dao = TableDao()
    with pytest.raises(ValueError, match="Impossible de supprimer les tables avec des parties en cours"):
        Table_dao.supprimer_toutes()

def test_lister_toutes(mock_db_connection):
    """Test de listage de toutes les tables"""
    # Setup
    mock_tables_data = [
        {"id_table": 1, "nom_table": "Table 1", "nb_sieges_max": 6, "blind_initial": 10.0},
        {"id_table": 2, "nom_table": "Table 2", "nb_sieges_max": 8, "blind_initial": 20.0},
        {"id_table": 3, "nom_table": "Table 3", "nb_sieges_max": 4, "blind_initial": 5.0}
    ]
    mock_db_connection.fetchall.return_value = mock_tables_data

    # Execution
    Table_dao = TableDao()
    result = Table_dao.lister_tous()

    # Vérifications
    assert len(result) == 3
    assert result[0].id_table == 1
    assert result[0].nom_table == "Table 1"
    assert result[1].nb_sieges_max == 8
    assert result[2].blind_initial == 5.0
    mock_db_connection.execute.assert_called_once_with(
        "SELECT id_table, nom_table, nb_sieges_max, blind_initial "
        "FROM tables "
        "ORDER BY id_table;"
    )

def test_lister_toutes_vide(mock_db_connection):
    """Test de listage quand il n'y a aucune table"""
    # Setup
    mock_db_connection.fetchall.return_value = []

    # Execution
    Table_dao = TableDao()
    result = Table_dao.lister_tous()

    # Vérifications
    assert result == []

def test_lister_tables_avec_sieges_disponibles(mock_db_connection):
    """Test de listage des tables avec sièges disponibles"""
    # Setup
    mock_tables_disponibles = [
        {
            "id_table": 1,
            "nom_table": "Table VIP",
            "nb_sieges_max": 6,
            "blind_initial": 10.0,
            "sieges_occupes": 4,
            "sieges_disponibles": 2
        },
        {
            "id_table": 2,
            "nom_table": "Table Libre",
            "nb_sieges_max": 8,
            "blind_initial": 20.0,
            "sieges_occupes": 0,
            "sieges_disponibles": 8
        }
    ]
    mock_db_connection.fetchall.return_value = mock_tables_disponibles

    # Execution
    Table_dao = TableDao()
    result = Table_dao.lister_tables_avec_sieges_disponibles()

    # Vérifications
    assert len(result) == 2
    assert result[0]["id_table"] == 1
    assert result[0]["nom_table"] == "Table VIP"
    assert result[0]["sieges_occupes"] == 4
    assert result[0]["sieges_disponibles"] == 2
    assert result[1]["sieges_disponibles"] == 8

def test_lister_tables_avec_sieges_disponibles_vide(mock_db_connection):
    """Test de listage des tables avec sièges disponibles quand aucune table disponible"""
    # Setup
    mock_db_connection.fetchall.return_value = []

    # Execution
    Table_dao = TableDao()
    result = table_dao.lister_tables_avec_sieges_disponibles()

    # Vérifications
    assert result == []

def test_compter_tables(mock_db_connection):
    """Test du comptage des tables"""
    # Setup
    mock_db_connection.fetchone.return_value = {"count": 5}

    # Execution
    table_dao = TableDao()
    result = table_dao.compter_tables()

    # Vérifications
    assert result == 5
    mock_db_connection.execute.assert_called_once_with("SELECT COUNT(*) as count FROM tables;")

def test_compter_tables_zero(mock_db_connection):
    """Test du comptage des tables quand il n'y en a aucune"""
    # Setup
    mock_db_connection.fetchone.return_value = {"count": 0}

    # Execution
    table_dao = TableDao()
    result = table_dao.compter_tables()

    # Vérifications
    assert result == 0

def test_exception_handling(mock_db_connection):
    """Test de la gestion des exceptions"""
    # Setup
    mock_db_connection.execute.side_effect = Exception("Database error")

    # Execution
    table_dao = TableDao()
    result = table_dao.trouver_par_id(1)

    # Vérifications
    assert result is None
