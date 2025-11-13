import pytest
from unittest.mock import patch, MagicMock
from business_object.table import Table
from business_object.joueur import Joueur
from service.table_service import TableService
from dao.table_dao import TableDao
from business_object.accesspartie import AccessPartie

@pytest.fixture
def mock_table_dao():
    with patch.object(TableDao, 'creer') as mock_creer, \
         patch.object(TableDao, 'trouver_par_id') as mock_trouver_par_id, \
         patch.object(TableDao, 'modifier') as mock_modifier, \
         patch.object(TableDao, 'lister_tous') as mock_lister_tous:

        yield {
            "creer": mock_creer,
            "trouver_par_id": mock_trouver_par_id,
            "modifier": mock_modifier,
            "lister_tous": mock_lister_tous,
        }

@pytest.fixture
def mock_access_partie():
    with patch.object(AccessPartie, 'creer_table') as mock_creer_table:
        yield {
            "creer_table": mock_creer_table,
        }

def test_creer_table_ok(mock_table_dao, mock_access_partie):
    # GIVEN
    nb_sieges = 5
    blind_initial = 10
    mock_table = Table(id_table=1, nb_sieges=nb_sieges, blind_initial=blind_initial)
    mock_access_partie["creer_table"].return_value = mock_table
    mock_table_dao["creer"].return_value = True

    # WHEN
    table_service = TableService()
    table = table_service.creer_table(nb_sieges, blind_initial)

    # THEN
    assert table == mock_table
    mock_access_partie["creer_table"].assert_called_once_with(nb_sieges, blind_initial)
    mock_table_dao["creer"].assert_called_once_with(mock_table)

def test_creer_table_ko(mock_table_dao, mock_access_partie):
    # GIVEN
    nb_sieges = 5
    blind_initial = 10
    mock_table = Table(id_table=1, nb_sieges=nb_sieges, blind_initial=blind_initial)
    mock_access_partie["creer_table"].return_value = mock_table
    mock_table_dao["creer"].return_value = False

    # WHEN
    table_service = TableService()
    table = table_service.creer_table(nb_sieges, blind_initial)

    # THEN
    assert table is None
    mock_access_partie["creer_table"].assert_called_once_with(nb_sieges, blind_initial)
    mock_table_dao["creer"].assert_called_once_with(mock_table)

def test_rejoindre_table_ok(mock_table_dao):
    # GIVEN
    joueur = Joueur(id_joueur=1, pseudo="Joueur1", age=25, mail="joueur1@example.com", credit=1000)
    id_table = 1
    mock_table = Table(id_table=id_table, nb_sieges=8, blind_initial=10)
    mock_table.sieges = [MagicMock(occupe=False, id_joueur=None) for _ in range(5)]
    mock_table_dao["trouver_par_id"].return_value = mock_table
    mock_table_dao["modifier"].return_value = True

    # WHEN
    table_service = TableService()
    result = table_service.rejoindre_table(joueur, id_table)

    # THEN
    assert result is True
    mock_table_dao["trouver_par_id"].assert_called_once_with(id_table)
    mock_table_dao["modifier"].assert_called_once_with(mock_table)
    assert any(siege.id_joueur == joueur.id_joueur for siege in mock_table.sieges)

def test_rejoindre_table_ko_table_inexistante(mock_table_dao):
    # GIVEN
    joueur = Joueur(id_joueur=1, pseudo="Joueur1", age=25, mail="joueur1@example.com", credit=1000)
    id_table = 1
    mock_table_dao["trouver_par_id"].return_value = None

    # WHEN
    table_service = TableService()
    result = table_service.rejoindre_table(joueur, id_table)

    # THEN
    assert result is False
    mock_table_dao["trouver_par_id"].assert_called_once_with(id_table)
    mock_table_dao["modifier"].assert_not_called()

def test_rejoindre_table_ko_table_remplie(mock_table_dao):
    # GIVEN
    joueur = Joueur(id_joueur=1, pseudo="Joueur1", age=25, mail="joueur1@example.com", credit=1000)
    id_table = 1
    mock_table = Table(id_table=id_table, nb_sieges=8, blind_initial=10)
    mock_table.sieges = [MagicMock(occupe=True, id_joueur=1) for _ in range(8)]
    mock_table_dao["trouver_par_id"].return_value = mock_table

    # WHEN
    table_service = TableService()
    result = table_service.rejoindre_table(joueur, id_table)

    # THEN
    assert result is False
    mock_table_dao["trouver_par_id"].assert_called_once_with(id_table)
    mock_table_dao["modifier"].assert_not_called()

def test_lister_tables_disponibles(mock_table_dao):
    # GIVEN
    mock_tables = [
        Table(id_table=1, nb_sieges=5, blind_initial=10),
        Table(id_table=2, nb_sieges=5, blind_initial=10),
    ]
    mock_tables[0].sieges = [MagicMock(occupe=False) for _ in range(5)]
    mock_tables[1].sieges = [MagicMock(occupe=True) for _ in range(5)]
    mock_table_dao["lister_tous"].return_value = mock_tables

    # WHEN
    table_service = TableService()
    tables_disponibles = table_service.lister_tables_disponibles()

    # THEN
    assert len(tables_disponibles) == 1
    assert tables_disponibles[0].id_table == 1
    mock_table_dao["lister_tous"].assert_called_once()

def test_quitter_table_ok(mock_table_dao):
    # GIVEN
    joueur = Joueur(id_joueur=1, pseudo="Joueur1", age=25, mail="joueur1@example.com", credit=1000)
    id_table = 1
    mock_table = Table(id_table=id_table, nb_sieges=5, blind_initial=10)
    mock_siege = MagicMock(occupe=True, id_joueur=joueur.id_joueur)
    mock_table.sieges = [mock_siege] + [MagicMock(occupe=False, id_joueur=None) for _ in range(4)]
    mock_table_dao["trouver_par_id"].return_value = mock_table
    mock_table_dao["modifier"].return_value = True

    # WHEN
    table_service = TableService()
    result = table_service.quitter_table(joueur, id_table)

    # THEN
    assert result is True
    assert mock_siege.occupe is False
    assert mock_siege.id_joueur is None
    mock_table_dao["trouver_par_id"].assert_called_once_with(id_table)
    mock_table_dao["modifier"].assert_called_once_with(mock_table)

def test_quitter_table_ko_table_inexistante(mock_table_dao):
    # GIVEN
    joueur = Joueur(id_joueur=1, pseudo="Joueur1", age=25, mail="joueur1@example.com", credit=1000)
    id_table = 1
    mock_table_dao["trouver_par_id"].return_value = None

    # WHEN
    table_service = TableService()
    result = table_service.quitter_table(joueur, id_table)

    # THEN
    assert result is False
    mock_table_dao["trouver_par_id"].assert_called_once_with(id_table)
    mock_table_dao["modifier"].assert_not_called()

def test_quitter_table_ko_joueur_non_trouve(mock_table_dao):
    # GIVEN
    joueur = Joueur(id_joueur=1, pseudo="Joueur1", age=25, mail="joueur1@example.com", credit=1000)
    id_table = 1
    mock_table = Table(id_table=id_table, nb_sieges=5, blind_initial=10)
    mock_table.sieges = [MagicMock(occupe=True, id_joueur=2) for _ in range(5)]
    mock_table_dao["trouver_par_id"].return_value = mock_table

    # WHEN
    table_service = TableService()
    result = table_service.quitter_table(joueur, id_table)

    # THEN
    assert result is False
    mock_table_dao["trouver_par_id"].assert_called_once_with(id_table)
    mock_table_dao["modifier"].assert_not_called()