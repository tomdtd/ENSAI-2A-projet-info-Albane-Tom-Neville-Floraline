import os
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from src.utils.reset_database import ResetDatabase
from src.dao.db_connection import DBConnection
from src.dao.partie_dao import PartieDao
from src.business_object.partie import Partie
from src.business_object.joueur_partie import JoueurPartie
from src.business_object.pot import Pot
from src.business_object.joueur import Joueur
from src.business_object.siege import Siege
from src.business_object.monnaie import Monnaie

from pathlib import Path
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def conn_info():
    """Initialisation de la base de données de test"""
    chemin = Path(__file__).parent / ".env_test"
    load_dotenv(dotenv_path=chemin, override=True)
    try:
        ResetDatabase().lancer(test_dao=True)
    except Exception as e:
        pytest.exit(f"Impossible d'initialiser la base de test : {e}")
    yield


@pytest.fixture(scope="function", autouse=True)
def clean_test_data():
    """Nettoyage des données de test avant chaque test"""
    # S'assurer que les tables existent en réinitialisant la base
    try:
        ResetDatabase().lancer(test_dao=True)
    except Exception as e:
        print(f"Erreur lors de la réinitialisation: {e}")

    # Maintenant créer les données de test de base
    try:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Créer une table de test avec OVERRIDING SYSTEM VALUE
                cursor.execute(
                    "INSERT INTO table_poker (id_table, nb_sieges, blind_initial, nb_joueurs) "
                    "OVERRIDING SYSTEM VALUE "
                    "VALUES (999, 6, 10.00, 0) "
                    "ON CONFLICT (id_table) DO NOTHING;"
                )
                connection.commit()
    except Exception as e:
        print(f"Erreur lors de la création de la table de test: {e}")


@pytest.fixture
def setup_partie_test_data():
    """Setup des données de test pour les parties"""
    ids_parties = [9001, 9002]  # IDs fixes pour les tests
    try:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Créer des parties de test avec des dates contrôlées et des IDs fixes
                cursor.execute(
                    "INSERT INTO partie (id_partie, id_table, pot, date_debut) "
                    "VALUES (9001, 999, 100.00, NOW() - INTERVAL '2 hour') "
                    "ON CONFLICT (id_partie) DO NOTHING;"
                )
                cursor.execute(
                    "INSERT INTO partie (id_partie, id_table, pot, date_debut) "
                    "VALUES (9002, 999, 200.00, NOW() - INTERVAL '1 hour') "
                    "ON CONFLICT (id_partie) DO NOTHING;"
                )
                connection.commit()
    except Exception as e:
        print(f"Erreur lors du setup des parties: {e}")

    return ids_parties


def test_trouver_par_id_existant(setup_partie_test_data):
    """Recherche par id d'une partie existante"""

    # GIVEN
    ids_parties = setup_partie_test_data
    assert len(ids_parties) == 2, "La fixture devrait créer 2 parties"
    id_partie = ids_parties[0]

    # WHEN
    partie = PartieDao().trouver_par_id(id_partie)

    # THEN
    assert partie is not None
    assert partie.id_partie == id_partie
    assert partie.id_table == 999
    assert partie.pot.get_montant() == 100.00


def test_trouver_par_id_non_existant():
    """Recherche par id d'une partie n'existant pas"""

    # GIVEN
    id_partie = 9999999999999

    # WHEN
    partie = PartieDao().trouver_par_id(id_partie)

    # THEN
    assert partie is None


def test_lister_toutes(setup_partie_test_data):
    """Vérifie que la méthode renvoie une liste de Partie"""

    # GIVEN
    ids_parties = setup_partie_test_data

    # WHEN
    parties = PartieDao().lister_toutes()

    # THEN
    assert isinstance(parties, list)
    for p in parties:
        assert isinstance(p, Partie)
    # Au moins nos 2 parties de test
    test_parties = [p for p in parties if p.id_partie in ids_parties]
    assert len(test_parties) >= 2


def test_creer_ok():
    """Création d'une partie réussie"""

    # GIVEN
    pot = Pot(150.00)
    partie = Partie(
        id_partie=None,  # Laisser la base générer l'ID
        joueurs=[],
        pot=pot,
        id_table=999,
        date_debut=datetime.now()
    )

    # WHEN
    creation_ok = PartieDao().creer(partie)

    # THEN
    assert creation_ok
    assert partie.id_partie is not None, "L'ID devrait être généré par la base"

    # Vérification que la partie a bien été créée
    partie_cree = PartieDao().trouver_par_id(partie.id_partie)
    assert partie_cree is not None
    assert partie_cree.id_partie == partie.id_partie


def test_creer_ko():
    """Création d'une partie échouée (id_table inexistant)"""

    # GIVEN
    # Création d'une partie avec un id_table qui n'existe pas
    pot = Pot(150.00)
    partie = Partie(
        id_partie=None,
        joueurs=[],
        pot=pot,
        id_table=888888,  # Table inexistante
        date_debut=datetime.now()
    )

    # WHEN
    creation_ok = PartieDao().creer(partie)

    # THEN
    assert not creation_ok


def test_modifier_ok(setup_partie_test_data):
    """Modification d'une partie réussie"""

    # GIVEN
    ids_parties = setup_partie_test_data
    id_partie = ids_parties[0]
    partie = PartieDao().trouver_par_id(id_partie)
    assert partie is not None
    nouveau_pot = 300.00
    partie.pot = Pot(nouveau_pot)

    # WHEN
    modification_ok = PartieDao().modifier(partie)

    # THEN
    assert modification_ok

    # Vérification que la modification a bien été enregistrée
    partie_modifiee = PartieDao().trouver_par_id(id_partie)
    assert partie_modifiee.pot.get_montant() == nouveau_pot


def test_modifier_ko():
    """Modification d'une partie échouée (id inconnu)"""

    # GIVEN
    pot = Pot(500.00)
    partie = Partie(
        id_partie=999999,
        joueurs=[],
        pot=pot,
        id_table=999,
        date_debut=datetime.now()
    )

    # WHEN
    modification_ok = PartieDao().modifier(partie)

    # THEN
    assert not modification_ok


def test_supprimer_ok():
    """Suppression d'une partie réussie"""

    # GIVEN
    # Créer une partie temporaire pour la suppression
    pot = Pot(100.00)
    partie = Partie(
        id_partie=None,  # Laisser la base générer l'ID
        joueurs=[],
        pot=pot,
        id_table=999,
        date_debut=datetime.now()
    )
    creation_ok = PartieDao().creer(partie)
    assert creation_ok, "La création doit réussir pour tester la suppression"
    assert partie.id_partie is not None

    # Vérifier que la partie existe
    id_partie_cree = partie.id_partie
    assert PartieDao().trouver_par_id(id_partie_cree) is not None

    # WHEN
    suppression_ok = PartieDao().supprimer(id_partie_cree)

    # THEN
    assert suppression_ok
    # Vérifier que la partie n'existe plus
    assert PartieDao().trouver_par_id(id_partie_cree) is None


def test_supprimer_ko():
    """Suppression d'une partie échouée (id inconnu)"""

    # GIVEN
    id_partie_inexistant = 999999

    # WHEN
    suppression_ok = PartieDao().supprimer(id_partie_inexistant)

    # THEN
    assert not suppression_ok


def test_trouver_derniere_partie_sur_table(setup_partie_test_data):
    """Trouver la dernière partie sur une table"""

    # GIVEN
    ids_parties = setup_partie_test_data
    id_table = 999

    # WHEN
    derniere_partie = PartieDao().trouver_derniere_partie_sur_table(id_table)

    # THEN
    assert derniere_partie is not None
    assert derniere_partie.id_table == id_table
    # La dernière partie devrait être celle avec la date_debut la plus récente (la deuxième créée)
    assert derniere_partie.id_partie == ids_parties[1]


def test_lister_parties_par_periode(setup_partie_test_data):
    """Lister les parties dans une période donnée"""

    # GIVEN
    ids_parties = setup_partie_test_data
    debut = datetime.now() - timedelta(days=1)
    fin = datetime.now() + timedelta(days=1)

    # WHEN
    parties = PartieDao().lister_parties_par_periode(debut, fin)

    # THEN
    assert isinstance(parties, list)
    # Nos 2 parties de test doivent être dans la période
    test_parties = [p for p in parties if p.id_partie in ids_parties]
    assert len(test_parties) == 2


def test_lister_parties_par_periode_aucune():
    """Lister les parties dans une période sans résultats"""

    # GIVEN
    debut = datetime.now() + timedelta(days=10)
    fin = datetime.now() + timedelta(days=20)

    # WHEN
    parties = PartieDao().lister_parties_par_periode(debut, fin)

    # THEN
    assert isinstance(parties, list)
    # Aucune partie ne devrait être dans cette période future
    assert len(parties) == 0


if __name__ == "__main__":
    pytest.main([__file__])