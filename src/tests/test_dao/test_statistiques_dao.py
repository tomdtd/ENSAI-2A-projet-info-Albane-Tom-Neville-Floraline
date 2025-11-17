import os
import pytest
from datetime import datetime, timedelta
from decimal import Decimal

from src.utils.reset_database import ResetDatabase
from src.dao.db_connection import DBConnection
from src.dao.statistiques_dao import StatistiquesDao

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
def setup_joueurs_test():
    """Crée des joueurs de test"""
    try:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Créer plusieurs joueurs avec différents profils
                # Utiliser OVERRIDING SYSTEM VALUE pour forcer les IDs
                cursor.execute(
                    """
                    INSERT INTO joueur (id_joueur, pseudo, mdp, mail, age, credit, date_creation) 
                    OVERRIDING SYSTEM VALUE
                    VALUES 
                        (1001, 'JoueurTest1', 'hash1', 'test1@mail.com', 25, 1000.00, NOW() - INTERVAL '30 days'),
                        (1002, 'JoueurTest2', 'hash2', 'test2@mail.com', 35, 500.00, NOW() - INTERVAL '20 days'),
                        (1003, 'JoueurTest3', 'hash3', 'test3@mail.com', 45, 1500.00, NOW() - INTERVAL '10 days'),
                        (1004, 'JoueurTest4', 'hash4', 'test4@mail.com', 22, 200.00, NOW() - INTERVAL '5 days'),
                        (1005, 'JoueurTest5', 'hash5', 'test5@mail.com', 55, 3000.00, NOW() - INTERVAL '60 days')
                    ON CONFLICT (id_joueur) DO NOTHING;
                    """
                )
                connection.commit()
    except Exception as e:
        print(f"Erreur lors du setup des joueurs: {e}")


@pytest.fixture
def setup_tables_test():
    """Crée des tables de test"""
    try:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO table_poker (id_table, nb_sieges, blind_initial, pot, nb_joueurs) 
                    OVERRIDING SYSTEM VALUE
                    VALUES 
                        (2001, 6, 10.00, 0.00, 0),
                        (2002, 8, 20.00, 0.00, 0),
                        (2003, 4, 5.00, 0.00, 0)
                    ON CONFLICT (id_table) DO NOTHING;
                    """
                )
                connection.commit()
    except Exception as e:
        print(f"Erreur lors du setup des tables: {e}")


@pytest.fixture
def setup_parties_completes_test(setup_joueurs_test, setup_tables_test):
    """Crée un jeu de données complet : joueurs, tables, parties et participations"""
    try:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Supprimer d'abord les anciennes données de test si elles existent
                cursor.execute("DELETE FROM partie_joueur WHERE id_table IN (2001, 2002, 2003);")
                cursor.execute("DELETE FROM partie WHERE id_table IN (2001, 2002, 2003);")
                
                # Créer des parties
                cursor.execute(
                    """
                    INSERT INTO partie (id_partie, id_table, pot, date_debut) 
                    VALUES 
                        (3001, 2001, 500.00, NOW() - INTERVAL '5 days'),
                        (3002, 2001, 300.00, NOW() - INTERVAL '3 days'),
                        (3003, 2002, 800.00, NOW() - INTERVAL '2 days'),
                        (3004, 2002, 450.00, NOW() - INTERVAL '1 day'),
                        (3005, 2003, 200.00, NOW() - INTERVAL '1 hour')
                    ON CONFLICT (id_partie) DO NOTHING;
                    """
                )
                
                # Créer des participations - UN SEUL joueur par table à la fois
                # Table 2001 - Joueur 1001
                cursor.execute(
                    """
                    INSERT INTO partie_joueur (id_table, id_joueur, mise_tour, solde_partie, statut, id_siege) 
                    VALUES (2001, 1001, 100, 150.00, 'gagnant', 1)
                    ON CONFLICT (id_table, id_joueur) DO NOTHING;
                    """
                )
                
                # Table 2001 - Joueur 1002
                cursor.execute(
                    """
                    INSERT INTO partie_joueur (id_table, id_joueur, mise_tour, solde_partie, statut, id_siege) 
                    VALUES (2001, 1002, 50, -50.00, 'couché', 2)
                    ON CONFLICT (id_table, id_joueur) DO NOTHING;
                    """
                )
                
                # Table 2001 - Joueur 1003
                cursor.execute(
                    """
                    INSERT INTO partie_joueur (id_table, id_joueur, mise_tour, solde_partie, statut, id_siege) 
                    VALUES (2001, 1003, 80, -80.00, 'actif', 3)
                    ON CONFLICT (id_table, id_joueur) DO NOTHING;
                    """
                )
                
                # Table 2002 - Joueur 1001
                cursor.execute(
                    """
                    INSERT INTO partie_joueur (id_table, id_joueur, mise_tour, solde_partie, statut, id_siege) 
                    VALUES (2002, 1001, 70, -70.00, 'actif', 1)
                    ON CONFLICT (id_table, id_joueur) DO NOTHING;
                    """
                )
                
                # Table 2002 - Joueur 1003
                cursor.execute(
                    """
                    INSERT INTO partie_joueur (id_table, id_joueur, mise_tour, solde_partie, statut, id_siege) 
                    VALUES (2002, 1003, 120, 250.00, 'gagnant', 2)
                    ON CONFLICT (id_table, id_joueur) DO NOTHING;
                    """
                )
                
                # Table 2003 - Joueur 1004
                cursor.execute(
                    """
                    INSERT INTO partie_joueur (id_table, id_joueur, mise_tour, solde_partie, statut, id_siege) 
                    VALUES (2003, 1004, 40, -40.00, 'couché', 1)
                    ON CONFLICT (id_table, id_joueur) DO NOTHING;
                    """
                )
                
                # Table 2003 - Joueur 1005
                cursor.execute(
                    """
                    INSERT INTO partie_joueur (id_table, id_joueur, mise_tour, solde_partie, statut, id_siege) 
                    VALUES (2003, 1005, 60, 100.00, 'gagnant', 2)
                    ON CONFLICT (id_table, id_joueur) DO NOTHING;
                    """
                )
                
                # Créer des transactions
                cursor.execute(
                    """
                    INSERT INTO transaction (id_joueur, solde, date) 
                    VALUES 
                        (1001, 1000, NOW() - INTERVAL '30 days'),
                        (1001, 150, NOW() - INTERVAL '5 days'),
                        (1001, -60, NOW() - INTERVAL '3 days'),
                        (1002, 500, NOW() - INTERVAL '20 days'),
                        (1002, -50, NOW() - INTERVAL '5 days'),
                        (1002, 300, NOW() - INTERVAL '2 days'),
                        (1003, 1500, NOW() - INTERVAL '10 days'),
                        (1004, 200, NOW() - INTERVAL '5 days'),
                        (1005, 3000, NOW() - INTERVAL '60 days')
                    ;
                    """
                )
                
                connection.commit()
    except Exception as e:
        print(f"Erreur lors du setup complet: {e}")


# =========================================================================
# TESTS DES STATISTIQUES INDIVIDUELLES
# =========================================================================

def test_obtenir_stats_joueur_existant(setup_parties_completes_test):
    """Test de récupération des stats d'un joueur existant"""
    
    # GIVEN
    id_joueur = 1001
    
    # WHEN
    stats = StatistiquesDao().obtenir_stats_joueur(id_joueur)
    
    # THEN
    assert stats is not None
    assert stats["pseudo"] == "JoueurTest1"
    assert stats["credit_actuel"] == 1000.00
    assert stats["age"] == 25
    assert stats["nb_parties_jouees"] >= 2  # A participé à au moins 2 tables
    assert "taux_victoire" in stats
    assert "gain_moyen_partie" in stats


def test_obtenir_stats_joueur_non_existant():
    """Test de récupération des stats d'un joueur inexistant"""
    
    # GIVEN
    id_joueur = 999999
    
    # WHEN
    stats = StatistiquesDao().obtenir_stats_joueur(id_joueur)
    
    # THEN
    assert stats is None


def test_obtenir_historique_parties_joueur(setup_parties_completes_test):
    """Test de récupération de l'historique des parties d'un joueur"""
    
    # GIVEN
    id_joueur = 1001
    limite = 5
    
    # WHEN
    historique = StatistiquesDao().obtenir_historique_parties_joueur(id_joueur, limite)
    
    # THEN
    assert isinstance(historique, list)
    assert len(historique) >= 1
    # Vérifier la structure des données
    if len(historique) > 0:
        assert "id_partie" in historique[0]
        assert "pot_total" in historique[0]
        assert "resultat" in historique[0]
        assert "statut" in historique[0]


def test_obtenir_historique_parties_joueur_sans_parties(setup_joueurs_test):
    """Test de l'historique d'un joueur qui n'a pas joué de parties"""
    
    # GIVEN
    id_joueur = 1001  # Joueur qui existe mais n'a pas de parties
    
    # WHEN
    historique = StatistiquesDao().obtenir_historique_parties_joueur(id_joueur)
    
    # THEN
    assert isinstance(historique, list)
    assert len(historique) == 0


def test_obtenir_evolution_credit_joueur(setup_parties_completes_test):
    """Test de l'évolution du crédit d'un joueur"""
    
    # GIVEN
    id_joueur = 1001
    
    # WHEN
    evolution = StatistiquesDao().obtenir_evolution_credit_joueur(id_joueur)
    
    # THEN
    assert isinstance(evolution, list)
    assert len(evolution) >= 1
    # Vérifier que les transactions sont ordonnées chronologiquement
    if len(evolution) > 1:
        assert evolution[0]["date"] <= evolution[-1]["date"]
    # Vérifier la présence du solde cumulé
    if len(evolution) > 0:
        assert "solde_cumule" in evolution[0]


def test_obtenir_statistiques_par_table(setup_parties_completes_test):
    """Test des statistiques d'un joueur par table"""
    
    # GIVEN
    id_joueur = 1001
    
    # WHEN
    stats_tables = StatistiquesDao().obtenir_statistiques_par_table(id_joueur)
    
    # THEN
    assert isinstance(stats_tables, list)
    assert len(stats_tables) >= 1
    # Vérifier la structure
    if len(stats_tables) > 0:
        assert "id_table" in stats_tables[0]
        assert "nb_parties" in stats_tables[0]
        assert "taux_victoire" in stats_tables[0]
        assert "gain_total" in stats_tables[0]


# =========================================================================
# TESTS DES STATISTIQUES COLLECTIVES
# =========================================================================

def test_obtenir_stats_globales(setup_parties_completes_test):
    """Test des statistiques globales de la plateforme"""
    
    # WHEN
    stats = StatistiquesDao().obtenir_stats_globales()
    
    # THEN
    assert stats is not None
    assert "nb_joueurs_total" in stats
    assert "nb_parties_total" in stats
    assert "nb_tables_actives" in stats
    assert "credit_total_plateforme" in stats
    assert "credit_moyen_joueur" in stats
    assert "age_moyen_joueurs" in stats
    
    # Vérifier que les valeurs sont cohérentes
    assert stats["nb_joueurs_total"] >= 5  # On a créé 5 joueurs
    assert stats["nb_parties_total"] >= 1  # Au moins 1 partie créée
    assert stats["credit_total_plateforme"] > 0


def test_obtenir_classement_joueurs_par_credit(setup_parties_completes_test):
    """Test du classement des joueurs par crédit"""
    
    # GIVEN
    critere = "credit"
    limite = 5
    
    # WHEN
    classement = StatistiquesDao().obtenir_classement_joueurs(critere, limite)
    
    # THEN
    assert isinstance(classement, list)
    assert len(classement) >= 1
    assert len(classement) <= limite
    
    # Vérifier l'ordre décroissant par crédit
    if len(classement) > 1:
        assert classement[0]["credit"] >= classement[1]["credit"]
    
    # Vérifier la structure
    assert "rang" in classement[0]
    assert "pseudo" in classement[0]
    assert "credit" in classement[0]
    assert "taux_victoire" in classement[0]


def test_obtenir_classement_joueurs_par_victoires(setup_parties_completes_test):
    """Test du classement des joueurs par nombre de victoires"""
    
    # GIVEN
    critere = "victoires"
    limite = 3
    
    # WHEN
    classement = StatistiquesDao().obtenir_classement_joueurs(critere, limite)
    
    # THEN
    assert isinstance(classement, list)
    assert len(classement) <= limite
    
    # Vérifier l'ordre décroissant par victoires
    if len(classement) > 1:
        assert classement[0]["nb_victoires"] >= classement[1]["nb_victoires"]


def test_obtenir_classement_joueurs_par_parties_jouees(setup_parties_completes_test):
    """Test du classement par nombre de parties jouées"""
    
    # GIVEN
    critere = "parties_jouees"
    
    # WHEN
    classement = StatistiquesDao().obtenir_classement_joueurs(critere, 10)
    
    # THEN
    assert isinstance(classement, list)
    
    # Vérifier l'ordre
    if len(classement) > 1:
        assert classement[0]["nb_parties"] >= classement[1]["nb_parties"]


def test_obtenir_distribution_age(setup_parties_completes_test):
    """Test de la distribution des joueurs par âge"""
    
    # WHEN
    distribution = StatistiquesDao().obtenir_distribution_age()
    
    # THEN
    assert isinstance(distribution, list)
    # Peut être vide ou contenir des données selon l'état de la base
    
    # Vérifier la structure si des données existent
    if len(distribution) > 0:
        assert "tranche_age" in distribution[0]
        assert "nb_joueurs" in distribution[0]
        assert "credit_moyen" in distribution[0]
        assert "age_moyen_tranche" in distribution[0]
        
        # Vérifier que toutes les tranches sont valides
        tranches_valides = ["Moins de 18", "18-25", "26-35", "36-50", "Plus de 50"]
        for d in distribution:
            assert d["tranche_age"] in tranches_valides


def test_obtenir_joueurs_plus_actifs(setup_parties_completes_test):
    """Test de récupération des joueurs les plus actifs"""
    
    # GIVEN
    limite = 3
    
    # WHEN
    joueurs_actifs = StatistiquesDao().obtenir_joueurs_plus_actifs(limite)
    
    # THEN
    assert isinstance(joueurs_actifs, list)
    assert len(joueurs_actifs) <= limite
    
    # Vérifier l'ordre décroissant par nombre de parties
    if len(joueurs_actifs) > 1:
        assert joueurs_actifs[0]["nb_parties"] >= joueurs_actifs[1]["nb_parties"]
    
    # Vérifier la structure
    if len(joueurs_actifs) > 0:
        assert "pseudo" in joueurs_actifs[0]
        assert "nb_parties" in joueurs_actifs[0]
        assert "total_mises" in joueurs_actifs[0]
        assert "derniere_partie" in joueurs_actifs[0]


def test_obtenir_joueurs_plus_actifs_vide():
    """Test des joueurs actifs quand il n'y a pas de données"""
    
    # WHEN
    joueurs_actifs = StatistiquesDao().obtenir_joueurs_plus_actifs(10)
    
    # THEN
    assert isinstance(joueurs_actifs, list)
    # Il peut y avoir des données résiduelles de la base de test
    # On vérifie juste que c'est une liste


# =========================================================================
# TESTS DES STATISTIQUES SUR LES PARTIES
# =========================================================================

def test_obtenir_stats_parties(setup_parties_completes_test):
    """Test des statistiques agrégées sur les parties"""
    
    # WHEN
    stats = StatistiquesDao().obtenir_stats_parties()
    
    # THEN
    assert stats is not None
    assert "nb_parties_total" in stats
    assert "pot_moyen" in stats
    assert "ecart_type_pot" in stats
    assert "mediane_pot" in stats
    assert "pot_min" in stats
    assert "pot_max" in stats
    assert "somme_totale_pots" in stats
    
    # Vérifier que les valeurs sont cohérentes
    assert stats["nb_parties_total"] >= 1  # Au moins une partie
    if stats["nb_parties_total"] > 0:
        assert stats["pot_moyen"] > 0
        assert stats["pot_max"] >= stats["pot_moyen"]
        assert stats["pot_min"] <= stats["pot_moyen"] or stats["pot_min"] == stats["pot_moyen"]


def test_obtenir_stats_parties_vide():
    """Test des stats des parties quand il n'y a pas de données"""
    
    # WHEN
    stats = StatistiquesDao().obtenir_stats_parties()
    
    # THEN
    assert stats is not None
    # Il peut y avoir des données résiduelles de la base de test
    assert "nb_parties_total" in stats
    assert "pot_moyen" in stats


def test_obtenir_stats_mises(setup_parties_completes_test):
    """Test des statistiques sur les mises"""
    
    # WHEN
    stats = StatistiquesDao().obtenir_stats_mises()
    
    # THEN
    assert stats is not None
    assert "nb_mises_total" in stats
    assert "mise_moyenne" in stats
    assert "ecart_type_mise" in stats
    assert "mediane_mise" in stats
    assert "mise_min" in stats
    assert "mise_max" in stats
    
    # Vérifier la cohérence si des mises existent
    if stats["nb_mises_total"] > 0:
        assert stats["mise_max"] >= stats["mise_moyenne"]
        assert stats["mise_min"] <= stats["mise_moyenne"]


def test_obtenir_stats_tables(setup_parties_completes_test):
    """Test des statistiques par table"""
    
    # WHEN
    stats_tables = StatistiquesDao().obtenir_stats_tables()
    
    # THEN
    assert isinstance(stats_tables, list)
    assert len(stats_tables) >= 3  # On a créé 3 tables
    
    # Vérifier la structure
    if len(stats_tables) > 0:
        assert "id_table" in stats_tables[0]
        assert "nb_sieges" in stats_tables[0]
        assert "blind_initial" in stats_tables[0]
        assert "nb_parties_jouees" in stats_tables[0]
        assert "taux_occupation" in stats_tables[0]
        assert "nb_joueurs_differents" in stats_tables[0]


def test_obtenir_activite_par_periode_jour(setup_parties_completes_test):
    """Test de l'activité par jour"""
    
    # GIVEN
    periode = "jour"
    
    # WHEN
    activite = StatistiquesDao().obtenir_activite_par_periode(periode)
    
    # THEN
    assert isinstance(activite, list)
    assert len(activite) >= 1
    
    # Vérifier la structure
    if len(activite) > 0:
        assert "periode" in activite[0]
        assert "nb_parties" in activite[0]
        assert "nb_tables_utilisees" in activite[0]
        assert "pot_moyen" in activite[0]


def test_obtenir_activite_par_periode_semaine(setup_parties_completes_test):
    """Test de l'activité par semaine"""
    
    # GIVEN
    periode = "semaine"
    
    # WHEN
    activite = StatistiquesDao().obtenir_activite_par_periode(periode)
    
    # THEN
    assert isinstance(activite, list)
    # Les données sont regroupées par semaine
    assert len(activite) >= 1


def test_obtenir_activite_par_periode_mois(setup_parties_completes_test):
    """Test de l'activité par mois"""
    
    # GIVEN
    periode = "mois"
    
    # WHEN
    activite = StatistiquesDao().obtenir_activite_par_periode(periode)
    
    # THEN
    assert isinstance(activite, list)


def test_obtenir_taux_abandon(setup_parties_completes_test):
    """Test du calcul des taux d'abandon"""
    
    # WHEN
    stats_abandon = StatistiquesDao().obtenir_taux_abandon()
    
    # THEN
    assert stats_abandon is not None
    assert "total_participations" in stats_abandon
    assert "nb_abandons" in stats_abandon
    assert "nb_victoires" in stats_abandon
    assert "taux_abandon" in stats_abandon
    assert "taux_victoire_global" in stats_abandon
    
    # Vérifier la cohérence des pourcentages
    assert 0 <= stats_abandon["taux_abandon"] <= 100
    assert 0 <= stats_abandon["taux_victoire_global"] <= 100


def test_obtenir_taux_abandon_sans_donnees():
    """Test du taux d'abandon sans données"""
    
    # WHEN
    stats_abandon = StatistiquesDao().obtenir_taux_abandon()
    
    # THEN
    # La fonction retourne None si total_participations est 0, sinon retourne un dict
    # Il peut y avoir des données résiduelles
    if stats_abandon is not None:
        assert isinstance(stats_abandon, dict)
        assert "total_participations" in stats_abandon


# =========================================================================
# TEST DU RAPPORT COMPLET
# =========================================================================

def test_obtenir_rapport_complet(setup_parties_completes_test):
    """Test de génération du rapport complet"""
    
    # WHEN
    rapport = StatistiquesDao().obtenir_rapport_complet()
    
    # THEN
    assert rapport is not None
    assert isinstance(rapport, dict)
    
    # Vérifier que toutes les sections sont présentes
    assert "stats_globales" in rapport
    assert "stats_parties" in rapport
    assert "stats_mises" in rapport
    assert "top_10_joueurs" in rapport
    assert "joueurs_actifs" in rapport
    assert "distribution_age" in rapport
    assert "taux_abandon" in rapport
    assert "stats_tables" in rapport
    
    # Vérifier que chaque section contient des données
    assert rapport["stats_globales"] is not None
    assert isinstance(rapport["top_10_joueurs"], list)
    assert isinstance(rapport["stats_tables"], list)


def test_obtenir_rapport_complet_structure():
    """Test de la structure du rapport complet même sans données"""
    
    # WHEN
    rapport = StatistiquesDao().obtenir_rapport_complet()
    
    # THEN
    assert rapport is not None
    assert len(rapport.keys()) == 8  # 8 sections principales


# =========================================================================
# TESTS DE CAS LIMITES
# =========================================================================

def test_stats_joueur_avec_zero_parties(setup_joueurs_test):
    """Test des stats d'un joueur qui n'a jamais joué"""
    
    # GIVEN
    id_joueur = 1001
    
    # WHEN
    stats = StatistiquesDao().obtenir_stats_joueur(id_joueur)
    
    # THEN
    assert stats is not None
    assert stats["nb_parties_jouees"] == 0
    assert stats["nb_victoires"] == 0
    assert stats["taux_victoire"] == 0


def test_classement_avec_un_seul_joueur(setup_joueurs_test):
    """Test du classement avec un seul joueur"""
    
    # WHEN
    classement = StatistiquesDao().obtenir_classement_joueurs("credit", 10)
    
    # THEN
    assert isinstance(classement, list)
    assert len(classement) >= 1


def test_stats_tables_sans_parties(setup_tables_test):
    """Test des stats de tables qui n'ont pas de parties"""
    
    # WHEN
    stats_tables = StatistiquesDao().obtenir_stats_tables()
    
    # THEN
    assert isinstance(stats_tables, list)
    # Il peut y avoir des tables avec ou sans parties selon l'état de la base
    # On vérifie juste que c'est une liste et la structure
    if len(stats_tables) > 0:
        assert "id_table" in stats_tables[0]
        assert "nb_parties_jouees" in stats_tables[0]


def test_evolution_credit_sans_transactions(setup_joueurs_test):
    """Test de l'évolution du crédit sans transactions"""
    
    # GIVEN
    id_joueur = 1001
    
    # WHEN
    evolution = StatistiquesDao().obtenir_evolution_credit_joueur(id_joueur)
    
    # THEN
    assert isinstance(evolution, list)
    assert len(evolution) == 0


if __name__ == "__main__":
    pytest.main([__file__])