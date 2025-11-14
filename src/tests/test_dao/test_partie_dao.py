import os
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from utils.reset_database import ResetDatabase
from dao.db_connection import DBConnection
from dao.partie_dao import PartieDao
from business_object.partie import Partie
from business_object.joueur_partie import JoueurPartie
from business_object.pot import Pot
from business_object.joueur import Joueur
from business_object.siege import Siege
from business_object.monnaie import Monnaie

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
                # Créer une table de test
                cursor.execute(
                    "INSERT INTO table_poker (id_table, nb_sieges, blind_initial, nb_joueurs) "
                    "VALUES (999, 6, 10.00, 0) "
                    "ON CONFLICT (id_table) DO NOTHING;"
                )
                connection.commit()
    except Exception as e:
        print(f"Erreur lors de la création de la table de test: {e}")


@pytest.fixture
def setup_partie_test_data():
    """Setup des données de test pour les parties"""
    try:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Créer des parties de test avec des dates contrôlées
                cursor.execute(
                    "INSERT INTO partie (id_partie, id_table, pot, date_debut) "
                    "VALUES (998, 999, 100.00, NOW() - INTERVAL '2 hour');"
                )
                cursor.execute(
                    "INSERT INTO partie (id_partie, id_table, pot, date_debut) "
                    "VALUES (999, 999, 200.00, NOW() - INTERVAL '1 hour');"
                )
                connection.commit()
    except Exception as e:
        print(f"Erreur lors du setup des parties: {e}")


def test_trouver_par_id_existant(setup_partie_test_data):
    """Recherche par id d'une partie existante"""

    # GIVEN
    id_partie = 998

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

    # WHEN
    parties = PartieDao().lister_toutes()

    # THEN
    assert isinstance(parties, list)
    for p in parties:
        assert isinstance(p, Partie)
    # Au moins nos 2 parties de test
    test_parties = [p for p in parties if p.id_partie in [998, 999]]
    assert len(test_parties) >= 2


def test_creer_ok():
    """Création d'une partie réussie"""

    # GIVEN
    pot = Pot(150.00)
    partie = Partie(
        id_partie=1000,
        joueurs=[],
        pot=pot,
        id_table=999,
        date_debut=datetime.now()
    )

    # WHEN
    creation_ok = PartieDao().creer(partie)

    # THEN
    assert creation_ok
    
    # Vérification que la partie a bien été créée
    partie_cree = PartieDao().trouver_par_id(1000)
    assert partie_cree is not None
    assert partie_cree.id_partie == 1000


def test_creer_ko():
    """Création d'une partie échouée (données incorrectes)"""

    # GIVEN
    # Création d'une partie avec un ID null pour provoquer une erreur
    # (selon le schéma, id_partie est PRIMARY KEY et ne peut pas être null)
    pot = Pot(150.00)
    partie = Partie(
        id_partie=None,  # ID null pour provoquer une erreur
        joueurs=[],
        pot=pot,
        id_table=999,
        date_debut=datetime.now()
    )

    # WHEN
    creation_ok = PartieDao().creer(partie)

    # THEN
    assert not creation_ok


def test_modifier_ok(setup_partie_test_data):
    """Modification d'une partie réussie"""

    # GIVEN
    partie = PartieDao().trouver_par_id(998)
    assert partie is not None
    nouveau_pot = 300.00
    partie.pot = Pot(nouveau_pot)

    # WHEN
    modification_ok = PartieDao().modifier(partie)

    # THEN
    assert modification_ok
    
    # Vérification que la modification a bien été enregistrée
    partie_modifiee = PartieDao().trouver_par_id(998)
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
        id_partie=1001,
        joueurs=[],
        pot=pot,
        id_table=999,
        date_debut=datetime.now()
    )
    creation_ok = PartieDao().creer(partie)
    assert creation_ok, "La création doit réussir pour tester la suppression"

    # Vérifier que la partie existe
    assert PartieDao().trouver_par_id(1001) is not None

    # WHEN
    suppression_ok = PartieDao().supprimer(1001)

    # THEN
    assert suppression_ok
    # Vérifier que la partie n'existe plus
    assert PartieDao().trouver_par_id(1001) is None


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
    id_table = 999

    # WHEN
    derniere_partie = PartieDao().trouver_derniere_partie_sur_table(id_table)

    # THEN
    assert derniere_partie is not None
    assert derniere_partie.id_table == id_table
    # La dernière partie devrait être celle avec la date_debut la plus récente (id_partie=999)
    assert derniere_partie.id_partie == 999


def test_lister_parties_par_periode(setup_partie_test_data):
    """Lister les parties dans une période donnée"""

    # GIVEN
    debut = datetime.now() - timedelta(days=1)
    fin = datetime.now() + timedelta(days=1)

    # WHEN
    parties = PartieDao().lister_parties_par_periode(debut, fin)

    # THEN
    assert isinstance(parties, list)
    # Nos 2 parties de test doivent être dans la période
    test_parties = [p for p in parties if p.id_partie in [998, 999]]
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