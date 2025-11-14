import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase
from utils.securite import hash_password

from dao.db_connection import DBConnection
from dao.joueur_partie_dao import JoueurPartieDao
from dao.joueur_dao import JoueurDao
from dao.partie_dao import PartieDao

from business_object.joueur_partie import JoueurPartie
from business_object.joueur import Joueur
from business_object.siege import Siege
from business_object.partie import Partie
from business_object.pot import Pot


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

def test_creer_ok():
    """Création de Joueur Partie réussie"""

    # GIVEN
    joueur = Joueur(pseudo="gg", age=44, mail="gg@ensai.fr", mdp="123abc", credit=0)
    JoueurDao().creer(joueur)
    joueur_partie = JoueurPartie(joueur= joueur,
                                 siege= Siege(), 
                                 solde_partie=100)
    partie = Partie(id_table=1,joueurs=[],pot=Pot(), id_table= 1, date_debut="2025-11-05 14:32:10")
    PartieDao().creer_partie(partie)
    id_table = 1

    # WHEN
    creation_ok = JoueurPartieDao().creer(joueur_partie, id_table)

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
    id_table = 1234 # n'existe pas


    # WHEN
    creation_ok = JoueurPartieDao().creer(joueur_partie, id_table)

    # THEN
    assert not creation_ok

def test_supprimer_ok():
    """Suppression de JoueurPartie réussie"""

    # GIVEN
    joueur = Joueur(pseudo="pseudo", age=44, mail="pseudo@ensai.fr", mdp="123abc", credit=0)
    JoueurDao().creer(joueur)
    joueur_partie = JoueurPartie(joueur= joueur,
                                 siege= Siege(), 
                                 solde_partie=100)
    partie = Partie(id_table=1,joueurs=[],pot=Pot(), id_table= 1, date_debut="2025-11-05 14:32:10")
    PartieDao().creer_partie(partie)
    JoueurPartieDao().creer(joueur_partie, 1)

    # WHEN
    suppression_ok = JoueurPartieDao().supprimer(joueur_partie.joueur.id_joueur)

    # THEN
    assert suppression_ok

def test_modifier_ok():
    """Modification de JoueurPartie réussie"""

    # GIVEN
    joueur = Joueur(pseudo="pseudo2", age=44, mail="pseudo2@ensai.fr", mdp="123abc", credit=0)
    JoueurDao().creer(joueur)
    new_solde_partie = 200
    joueur_partie = JoueurPartie(joueur= joueur,
                                 siege= Siege(), 
                                 solde_partie=new_solde_partie)
    partie = Partie(id_table=1,joueurs=[],pot=Pot(), id_table= 1, date_debut="2025-11-05 14:32:10")
    PartieDao().creer_partie(partie)
    JoueurPartieDao().creer(joueur_partie, 1)

    # WHEN
    modification_ok = JoueurPartieDao().modifier(joueur_partie, 1)

    # THEN
    assert modification_ok

