"""
Tests unitaires pour le module JoueurPartieDao
"""

import os
import pytest
from datetime import datetime

from src.utils.reset_database import ResetDatabase
from src.dao.db_connection import DBConnection
from src.dao.joueur_partie_dao import JoueurPartieDao
from src.dao.joueur_dao import JoueurDao
from src.business_object.joueur_partie import JoueurPartie
from src.business_object.joueur import Joueur
from src.business_object.siege import Siege
from src.business_object.monnaie import Monnaie
from src.business_object.liste_cartes import ListeCartes
from src.business_object.carte import Carte

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
    try:
        ResetDatabase().lancer(test_dao=True)
    except Exception as e:
        print(f"Erreur lors de la réinitialisation: {e}")


@pytest.fixture
def setup_joueur_test():
    """Crée un joueur de test"""
    try:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO joueur (id_joueur, pseudo, mdp, mail, age, credit) 
                    OVERRIDING SYSTEM VALUE
                    VALUES (5001, 'JoueurTest', 'hash123', 'joueur@test.com', 30, 1000.00)
                    ON CONFLICT (id_joueur) DO NOTHING;
                    """
                )
                connection.commit()
        return 5001
    except Exception as e:
        print(f"Erreur lors du setup du joueur: {e}")
        return None


@pytest.fixture
def setup_table_test():
    """Crée une table de test"""
    try:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO table_poker (id_table, nb_sieges, blind_initial, pot, nb_joueurs) 
                    OVERRIDING SYSTEM VALUE
                    VALUES (6001, 6, 10.00, 0.00, 0)
                    ON CONFLICT (id_table) DO NOTHING;
                    """
                )
                connection.commit()
        return 6001
    except Exception as e:
        print(f"Erreur lors du setup de la table: {e}")
        return None


@pytest.fixture
def setup_joueurs_et_table():
    """Crée plusieurs joueurs et une table de test"""
    try:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Créer des joueurs
                cursor.execute(
                    """
                    INSERT INTO joueur (id_joueur, pseudo, mdp, mail, age, credit) 
                    OVERRIDING SYSTEM VALUE
                    VALUES 
                        (5001, 'Joueur1', 'hash1', 'j1@test.com', 25, 1000.00),
                        (5002, 'Joueur2', 'hash2', 'j2@test.com', 30, 1500.00),
                        (5003, 'Joueur3', 'hash3', 'j3@test.com', 35, 2000.00)
                    ON CONFLICT (id_joueur) DO NOTHING;
                    """
                )
                
                # Créer une table
                cursor.execute(
                    """
                    INSERT INTO table_poker (id_table, nb_sieges, blind_initial, pot, nb_joueurs) 
                    OVERRIDING SYSTEM VALUE
                    VALUES (6001, 6, 10.00, 0.00, 0)
                    ON CONFLICT (id_table) DO NOTHING;
                    """
                )
                connection.commit()
        return {"joueurs": [5001, 5002, 5003], "table": 6001}
    except Exception as e:
        print(f"Erreur lors du setup complet: {e}")
        return None


# =========================================================================
# TESTS DE CRÉATION
# =========================================================================

def test_creer_joueur_partie_ok(setup_joueur_test, setup_table_test):
    """Test de création d'un joueur_partie réussie"""
    
    # GIVEN
    id_joueur = setup_joueur_test
    id_table = setup_table_test
    
    joueur = Joueur(pseudo="JoueurTest", mail="joueur@test.com", mdp="hash123", 
                    age=30, credit=Monnaie(1000), id_joueur=id_joueur)
    siege = Siege(id_siege=1)
    joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=500)
    
    # WHEN
    creation_ok = JoueurPartieDao().creer(joueur_partie, id_table)
    
    # THEN
    assert creation_ok
    
    # Vérifier que le joueur_partie existe dans la base
    with DBConnection().connection as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM partie_joueur WHERE id_joueur = %s AND id_table = %s",
                (id_joueur, id_table)
            )
            result = cursor.fetchone()
            assert result is not None
            assert result["id_joueur"] == id_joueur
            assert result["id_table"] == id_table
            assert result["id_siege"] == 1


def test_creer_joueur_partie_ko():
    """Test de création d'un joueur_partie échouée (joueur inexistant)"""
    
    # GIVEN
    id_joueur_inexistant = 999999
    id_table_inexistant = 999999
    
    joueur = Joueur(pseudo="Inexistant", mail="test@test.com", mdp="hash", 
                    age=25, credit=Monnaie(100), id_joueur=id_joueur_inexistant)
    siege = Siege(id_siege=1)
    joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=100)
    
    # WHEN
    creation_ok = JoueurPartieDao().creer(joueur_partie, id_table_inexistant)
    
    # THEN
    assert not creation_ok


def test_creer_joueur_partie_doublon(setup_joueur_test, setup_table_test):
    """Test de création d'un doublon (même joueur, même table)"""
    
    # GIVEN
    id_joueur = setup_joueur_test
    id_table = setup_table_test
    
    joueur = Joueur(pseudo="JoueurTest", mail="joueur@test.com", mdp="hash123", 
                    age=30, credit=Monnaie(1000), id_joueur=id_joueur)
    siege = Siege(id_siege=1)
    joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=500)
    
    # Première création
    JoueurPartieDao().creer(joueur_partie, id_table)
    
    # WHEN - Tentative de recréation
    creation_ok = JoueurPartieDao().creer(joueur_partie, id_table)
    
    # THEN
    assert not creation_ok  # La clé primaire composite empêche le doublon


# =========================================================================
# TESTS DE MODIFICATION
# =========================================================================

def test_modifier_joueur_partie_ok(setup_joueur_test, setup_table_test):
    """Test de modification d'un joueur_partie réussie"""
    
    # GIVEN
    id_joueur = setup_joueur_test
    id_table = setup_table_test
    
    joueur = Joueur(pseudo="JoueurTest", mail="joueur@test.com", mdp="hash123", 
                    age=30, credit=Monnaie(1000), id_joueur=id_joueur)
    siege = Siege(id_siege=1)
    joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=500)
    
    # Créer le joueur_partie
    JoueurPartieDao().creer(joueur_partie, id_table)
    
    # Modifier les valeurs
    joueur_partie.mise_tour = Monnaie(100)
    joueur_partie.solde_partie = Monnaie(400)
    joueur_partie.statut = "en jeu"
    
    # WHEN
    modification_ok = JoueurPartieDao().modifier(joueur_partie, id_table)
    
    # THEN
    assert modification_ok
    
    # Vérifier les modifications
    with DBConnection().connection as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM partie_joueur WHERE id_joueur = %s AND id_table = %s",
                (id_joueur, id_table)
            )
            result = cursor.fetchone()
            assert result["mise_tour"] == 100
            assert float(result["solde_partie"]) == 400.0
            assert result["statut"] == "en jeu"


def test_modifier_joueur_partie_ko():
    """Test de modification d'un joueur_partie inexistant"""
    
    # GIVEN
    id_joueur_inexistant = 999999
    id_table_inexistant = 999999
    
    joueur = Joueur(pseudo="Inexistant", mail="test@test.com", mdp="hash", 
                    age=25, credit=Monnaie(100), id_joueur=id_joueur_inexistant)
    siege = Siege(id_siege=1)
    joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=100)
    
    # WHEN
    modification_ok = JoueurPartieDao().modifier(joueur_partie, id_table_inexistant)
    
    # THEN
    assert not modification_ok


# =========================================================================
# TESTS DE SUPPRESSION
# =========================================================================

def test_supprimer_joueur_partie_ok(setup_joueur_test, setup_table_test):
    """Test de suppression d'un joueur_partie réussie"""
    
    # GIVEN
    id_joueur = setup_joueur_test
    id_table = setup_table_test
    
    joueur = Joueur(pseudo="JoueurTest", mail="joueur@test.com", mdp="hash123", 
                    age=30, credit=Monnaie(1000), id_joueur=id_joueur)
    siege = Siege(id_siege=1)
    joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=500)
    
    # Créer le joueur_partie
    JoueurPartieDao().creer(joueur_partie, id_table)
    
    # WHEN
    suppression_ok = JoueurPartieDao().supprimer(id_joueur)
    
    # THEN
    assert suppression_ok
    
    # Vérifier que le joueur_partie n'existe plus
    with DBConnection().connection as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM partie_joueur WHERE id_joueur = %s AND id_table = %s",
                (id_joueur, id_table)
            )
            result = cursor.fetchone()
            assert result is None


def test_supprimer_joueur_partie_ko():
    """Test de suppression d'un joueur_partie inexistant"""
    
    # GIVEN
    id_joueur_inexistant = 999999
    
    # WHEN
    suppression_ok = JoueurPartieDao().supprimer(id_joueur_inexistant)
    
    # THEN
    assert not suppression_ok


# =========================================================================
# TESTS DE RECHERCHE
# =========================================================================

def test_trouver_par_table_avec_joueurs(setup_joueurs_et_table):
    """Test de recherche des joueurs d'une table avec plusieurs joueurs"""
    
    # GIVEN
    setup_data = setup_joueurs_et_table
    id_table = setup_data["table"]
    ids_joueurs = setup_data["joueurs"]
    
    # Ajouter les joueurs à la table
    for i, id_joueur in enumerate(ids_joueurs):
        joueur = Joueur(pseudo=f"Joueur{i+1}", mail=f"j{i+1}@test.com", 
                       mdp="hash", age=25+i*5, credit=Monnaie(1000), id_joueur=id_joueur)
        siege = Siege(id_siege=i+1)
        joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=500)
        JoueurPartieDao().creer(joueur_partie, id_table)
    
    # WHEN
    joueurs_table = JoueurPartieDao().trouver_par_table(id_table)
    
    # THEN
    assert joueurs_table is not None
    assert len(joueurs_table) == 3
    assert all(id_j in joueurs_table for id_j in ids_joueurs)


def test_trouver_par_table_vide(setup_table_test):
    """Test de recherche des joueurs d'une table vide"""
    
    # GIVEN
    id_table = setup_table_test
    
    # WHEN
    joueurs_table = JoueurPartieDao().trouver_par_table(id_table)
    
    # THEN
    assert joueurs_table is None or len(joueurs_table) == 0


def test_trouver_par_table_inexistante():
    """Test de recherche sur une table inexistante"""
    
    # GIVEN
    id_table_inexistant = 999999
    
    # WHEN/THEN - Devrait lever une exception ou retourner None
    try:
        joueurs_table = JoueurPartieDao().trouver_par_table(id_table_inexistant)
        # Si aucune exception, vérifier que le résultat est vide
        assert joueurs_table is None or len(joueurs_table) == 0
    except Exception:
        # Une exception est acceptable
        pass


# =========================================================================
# TESTS DES CARTES
# =========================================================================

def test_donner_cartes_main_joueur_ok(setup_joueur_test, setup_table_test):
    """Test d'attribution de cartes à un joueur"""
    
    # GIVEN
    id_joueur = setup_joueur_test
    id_table = setup_table_test
    
    joueur = Joueur(pseudo="JoueurTest", mail="joueur@test.com", mdp="hash123", 
                    age=30, credit=Monnaie(1000), id_joueur=id_joueur)
    siege = Siege(id_siege=1)
    joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=500)
    JoueurPartieDao().creer(joueur_partie, id_table)
    
    # Créer une main de cartes
    carte1 = Carte(valeur="As", couleur="Coeur")
    carte2 = Carte(valeur="Roi", couleur="Pique")
    main = ListeCartes([])
    main.ajouter_carte(carte1)
    main.ajouter_carte(carte2)
    
    # WHEN
    attribution_ok = JoueurPartieDao().donner_cartes_main_joueur(id_table, id_joueur, main)
    
    # THEN
    assert attribution_ok
    
    # Vérifier que les cartes sont bien enregistrées
    cartes_recuperees = JoueurPartieDao().trouver_cartes_main_joueur(id_table, id_joueur)
    assert cartes_recuperees is not None
    assert len(cartes_recuperees.cartes) == 2


def test_donner_cartes_main_joueur_ko():
    """Test d'attribution de cartes à un joueur inexistant"""

    # GIVEN
    id_joueur_inexistant = 999999
    id_table_inexistant = 999999

    carte = Carte(valeur="As", couleur="Coeur")
    main = ListeCartes([])
    main.ajouter_carte(carte)
    
    # WHEN
    attribution_ok = JoueurPartieDao().donner_cartes_main_joueur(
        id_table_inexistant, id_joueur_inexistant, main
    )
    
    # THEN
    assert not attribution_ok


def test_trouver_cartes_main_joueur_avec_cartes(setup_joueur_test, setup_table_test):
    """Test de récupération des cartes d'un joueur"""
    
    # GIVEN
    id_joueur = setup_joueur_test
    id_table = setup_table_test
    
    joueur = Joueur(pseudo="JoueurTest", mail="joueur@test.com", mdp="hash123", 
                    age=30, credit=Monnaie(1000), id_joueur=id_joueur)
    siege = Siege(id_siege=1)
    joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=500)
    JoueurPartieDao().creer(joueur_partie, id_table)
    
    # Attribuer des cartes
    carte1 = Carte(valeur="As", couleur="Coeur")
    carte2 = Carte(valeur="Roi", couleur="Pique")
    main = ListeCartes([])
    main.ajouter_carte(carte1)
    main.ajouter_carte(carte2)
    JoueurPartieDao().donner_cartes_main_joueur(id_table, id_joueur, main)
    
    # WHEN
    cartes = JoueurPartieDao().trouver_cartes_main_joueur(id_table, id_joueur)
    
    # THEN
    assert cartes is not None
    assert len(cartes.cartes) == 2


def test_trouver_cartes_main_joueur_sans_cartes(setup_joueur_test, setup_table_test):
    """Test de récupération des cartes d'un joueur qui n'en a pas"""
    
    # GIVEN
    id_joueur = setup_joueur_test
    id_table = setup_table_test
    
    joueur = Joueur(pseudo="JoueurTest", mail="joueur@test.com", mdp="hash123", 
                    age=30, credit=Monnaie(1000), id_joueur=id_joueur)
    siege = Siege(id_siege=1)
    joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=500)
    JoueurPartieDao().creer(joueur_partie, id_table)
    
    # WHEN
    cartes = JoueurPartieDao().trouver_cartes_main_joueur(id_table, id_joueur)
    
    # THEN
    assert cartes is not None
    assert len(cartes.cartes) == 0  # Liste vide


def test_trouver_cartes_main_joueur_inexistant():
    """Test de récupération des cartes d'un joueur inexistant"""
    
    # GIVEN
    id_joueur_inexistant = 999999
    id_table_inexistant = 999999
    
    # WHEN
    cartes = JoueurPartieDao().trouver_cartes_main_joueur(id_table_inexistant, id_joueur_inexistant)
    
    # THEN
    assert cartes is not None
    assert len(cartes.cartes) == 0


# =========================================================================
# TESTS DES STATUTS
# =========================================================================

def test_modifier_statut_ok(setup_joueur_test, setup_table_test):
    """Test de modification du statut d'un joueur"""
    
    # GIVEN
    id_joueur = setup_joueur_test
    id_table = setup_table_test
    
    joueur = Joueur(pseudo="JoueurTest", mail="joueur@test.com", mdp="hash123", 
                    age=30, credit=Monnaie(1000), id_joueur=id_joueur)
    siege = Siege(id_siege=1)
    joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=500)
    JoueurPartieDao().creer(joueur_partie, id_table)
    
    nouveau_statut = "en jeu"
    
    # WHEN
    modification_ok = JoueurPartieDao().modifier_statut(id_joueur, id_table, nouveau_statut)
    
    # THEN
    assert modification_ok
    
    # Vérifier le changement
    statut_recupere = JoueurPartieDao().recuperer_statut(id_joueur, id_table)
    assert statut_recupere == nouveau_statut


def test_modifier_statut_ko():
    """Test de modification du statut d'un joueur inexistant"""
    
    # GIVEN
    id_joueur_inexistant = 999999
    id_table_inexistant = 999999
    
    # WHEN
    modification_ok = JoueurPartieDao().modifier_statut(
        id_joueur_inexistant, id_table_inexistant, "en jeu"
    )
    
    # THEN
    assert not modification_ok


def test_recuperer_statut_ok(setup_joueur_test, setup_table_test):
    """Test de récupération du statut d'un joueur"""
    
    # GIVEN
    id_joueur = setup_joueur_test
    id_table = setup_table_test
    
    joueur = Joueur(pseudo="JoueurTest", mail="joueur@test.com", mdp="hash123", 
                    age=30, credit=Monnaie(1000), id_joueur=id_joueur)
    siege = Siege(id_siege=1)
    joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=500)
    JoueurPartieDao().creer(joueur_partie, id_table)
    
    # WHEN
    statut = JoueurPartieDao().recuperer_statut(id_joueur, id_table)
    
    # THEN
    assert statut is not None
    assert statut == "en attente"  # Statut par défaut


def test_recuperer_statut_ko():
    """Test de récupération du statut d'un joueur inexistant"""
    
    # GIVEN
    id_joueur_inexistant = 999999
    id_table_inexistant = 999999
    
    # WHEN
    statut = JoueurPartieDao().recuperer_statut(id_joueur_inexistant, id_table_inexistant)
    
    # THEN
    assert statut is None


def test_modifier_puis_recuperer_statut(setup_joueur_test, setup_table_test):
    """Test de modification puis récupération du statut"""
    
    # GIVEN
    id_joueur = setup_joueur_test
    id_table = setup_table_test
    
    joueur = Joueur(pseudo="JoueurTest", mail="joueur@test.com", mdp="hash123", 
                    age=30, credit=Monnaie(1000), id_joueur=id_joueur)
    siege = Siege(id_siege=1)
    joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=500)
    JoueurPartieDao().creer(joueur_partie, id_table)
    
    # Liste de statuts à tester
    statuts = ["en jeu", "s'est couché", "gagnant", "perdant"]
    
    for nouveau_statut in statuts:
        # WHEN
        JoueurPartieDao().modifier_statut(id_joueur, id_table, nouveau_statut)
        statut_recupere = JoueurPartieDao().recuperer_statut(id_joueur, id_table)
        
        # THEN
        assert statut_recupere == nouveau_statut


# =========================================================================
# TESTS D'INTÉGRATION
# =========================================================================

def test_cycle_complet_joueur_partie(setup_joueur_test, setup_table_test):
    """Test du cycle complet : création, modification, suppression"""
    
    # GIVEN
    id_joueur = setup_joueur_test
    id_table = setup_table_test
    
    joueur = Joueur(pseudo="JoueurTest", mail="joueur@test.com", mdp="hash123", 
                    age=30, credit=Monnaie(1000), id_joueur=id_joueur)
    siege = Siege(id_siege=1)
    joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=500)
    
    # WHEN/THEN - Création
    assert JoueurPartieDao().creer(joueur_partie, id_table)
    
    # Modification du statut
    assert JoueurPartieDao().modifier_statut(id_joueur, id_table, "en jeu")
    assert JoueurPartieDao().recuperer_statut(id_joueur, id_table) == "en jeu"
    
    # Attribution de cartes
    carte = Carte(valeur="As", couleur="Coeur")
    main = ListeCartes([])
    main.ajouter_carte(carte)
    assert JoueurPartieDao().donner_cartes_main_joueur(id_table, id_joueur, main)
    
    # Modification du joueur_partie
    joueur_partie.mise_tour = Monnaie(50)
    assert JoueurPartieDao().modifier(joueur_partie, id_table)
    
    # Suppression
    assert JoueurPartieDao().supprimer(id_joueur)


def test_plusieurs_joueurs_meme_table(setup_joueurs_et_table):
    """Test avec plusieurs joueurs sur la même table"""
    
    # GIVEN
    setup_data = setup_joueurs_et_table
    id_table = setup_data["table"]
    ids_joueurs = setup_data["joueurs"]
    
    # WHEN - Ajouter tous les joueurs
    for i, id_joueur in enumerate(ids_joueurs):
        joueur = Joueur(pseudo=f"Joueur{i+1}", mail=f"j{i+1}@test.com", 
                       mdp="hash", age=25+i*5, credit=Monnaie(1000), id_joueur=id_joueur)
        siege = Siege(id_siege=i+1)
        joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=500)
        assert JoueurPartieDao().creer(joueur_partie, id_table)
    
    # THEN
    joueurs_table = JoueurPartieDao().trouver_par_table(id_table)
    assert len(joueurs_table) == 3
    
    # Modifier le statut de chaque joueur
    for id_joueur in ids_joueurs:
        assert JoueurPartieDao().modifier_statut(id_joueur, id_table, "en jeu")
    
    # Vérifier les statuts
    for id_joueur in ids_joueurs:
        assert JoueurPartieDao().recuperer_statut(id_joueur, id_table) == "en jeu"


if __name__ == "__main__":
    pytest.main([__file__])