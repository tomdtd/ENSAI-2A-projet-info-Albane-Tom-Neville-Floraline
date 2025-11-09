import pytest
from src.service.deroulement_partie import DeroulementPartie
from src.business_object.joueur import Joueur
from src.business_object.flop import Flop
from src.business_object.carte import Carte
from src.business_object.main import Main
from src.business_object.main_joueur_complete import MainJoueurComplete
from src.business_object.combinaison import Combinaison


# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture
def joueurs_fixture():
    """Crée une liste de joueurs avec crédits initiaux"""
    return [
        Joueur(id_joueur=1, pseudo="Alice", credit=1000),
        Joueur(id_joueur=2, pseudo="Bob", credit=1000),
        Joueur(id_joueur=3, pseudo="Charlie", credit=1000),
    ]


@pytest.fixture
def partie_fixture(joueurs_fixture):
    """Initialise une partie avec DeroulementPartie"""
    return DeroulementPartie(joueurs=joueurs_fixture, big_blind=20, small_blind=10)


# -----------------------------
# Tests unitaires des méthodes
# -----------------------------
def test_initialisation(partie_fixture):
    """Vérifie que la partie est correctement initialisée"""
    assert partie_fixture.big_blind.get() == 20
    assert partie_fixture.small_blind.get() == 10
    assert len(partie_fixture.joueurs_partie) == 3
    assert partie_fixture.pot.get_montant() == 0


def test_collecter_blinds(partie_fixture):
    """Vérifie que les blinds sont collectés"""
    partie_fixture._collecter_blinds()
    assert partie_fixture.pot.get_montant() == 30  # small blind + big blind
    assert len(partie_fixture.transactions) == 2


def test_tour_de_mise(partie_fixture):
    """Vérifie qu'un tour de mise ajoute des transactions"""
    partie_fixture._tour_de_mise()
    assert partie_fixture.pot.get_montant() == 30  # 3 joueurs misent 10 chacun
    assert len(partie_fixture.transactions) == 3


def test_showdown_désigne_gagnant(partie_fixture):
    """Vérifie que le showdown attribue le pot à un gagnant"""
    # Simuler un flop
    flop = Flop([Carte("As", "Pique"), Carte("Roi", "Coeur"), Carte("10", "Carreau")])

    # Donner une main simplifiée à chaque joueur
    for jp in partie_fixture.joueurs_partie:
        jp.main = Main([Carte("2", "Pique"), Carte("3", "Coeur")])

    # Ajouter un pot fictif
    partie_fixture.pot.ajouter_mise(100)

    partie_fixture._showdown(flop)

    # Vérifier qu'un joueur a reçu le pot
    gagnant_detecte = any(jp.solde_partie.get() > 1000 for jp in partie_fixture.joueurs_partie)
    assert gagnant_detecte
    assert len(partie_fixture.transactions) >= 1


def test_lancer_partie(partie_fixture):
    """Vérifie que lancer_partie exécute toutes les étapes"""
    partie_fixture.lancer_partie()
    assert partie_fixture.partie is not None
    assert partie_fixture.pot.get_montant() >= 0
    assert len(partie_fixture.transactions) > 0
