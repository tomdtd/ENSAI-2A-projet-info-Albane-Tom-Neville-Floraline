import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase
from utils.securite import hash_password

from dao.db_connection import DBConnection
from dao.joueur_partie_dao import JoueurPartieDao
from dao.joueur_dao import JoueurDao
from dao.Partie_dao import PartieDao

from business_object.JoueurPartie import JoueurPartie
from business_object.joueur import Joueur
from business_object.siege import Siege
from business_object.partie import Partie
from business_object.pot import Pot


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield

def test_creer_ok():
    """Création de Joueur Partie réussie"""

    # GIVEN
    joueur = Joueur(pseudo="gg", age=44, mail="gg@ensai.fr", mdp="123abc", credit=0)
    JoueurDao().creer(joueur)
    joueur_partie = JoueurPartie(joueur= joueur,
                                 siege= Siege(), 
                                 solde_partie=100)
    partie = Partie(id_partie=123,joueurs=[], jour=1,pot=Pot())
    PartieDao().creer(partie)
    id_partie = 123

    # WHEN
    creation_ok = JoueurPartieDao().creer(joueur_partie, id_partie)

    # THEN
    assert creation_ok
    assert joueur_partie.id_joueur

def test_creer_ko():
    """Création de Joueur Partie échouée (id de la partie incorrect)"""

    # GIVEN
    joueur = Joueur(pseudo="gg", age=44, mail="gg@ensai.fr", mdp="123abc", credit=0)
    JoueurDao().creer(joueur)
    joueur_partie = JoueurPartie(joueur= joueur,
                                 siege= Siege(), 
                                 solde_partie=100)
    id_partie = 1234 # n'existe pas


    # WHEN
    creation_ok = JoueurPartieDao().creer(joueur_partie, id_partie)

    # THEN
    assert not creation_ok

def test_supprimer_ok():
    """Suppression de JoueurPartie réussie"""

    # GIVEN
    joueur_partie = JoueurPartie(1, 999, 0, 0, 'en attente', 3)

    # WHEN
    suppression_ok = JoueurPartieDao().supprimer(joueur_partie.id_joueur)

    # THEN
    assert suppression_ok

