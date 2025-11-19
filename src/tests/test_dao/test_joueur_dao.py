import os
import pytest

from unittest.mock import patch

from src.utils.reset_database import ResetDatabase
from src.utils.securite import hash_password

from src.dao.db_connection import DBConnection
from src.dao.joueur_dao import JoueurDao

from src.business_object.joueur import Joueur
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

def test_trouver_par_id_existant():
    """Recherche par id d'un joueur existant"""

    # GIVEN
    id_joueur = 998

    # WHEN
    joueur = JoueurDao().trouver_par_id(id_joueur)

    # THEN
    assert joueur is not None


def test_trouver_par_id_non_existant():
    """Recherche par id d'un joueur n'existant pas"""

    # GIVEN
    id_joueur = 9999999999999

    # WHEN
    joueur = JoueurDao().trouver_par_id(id_joueur)

    # THEN
    assert joueur is None


def test_lister_tous():
    """Vérifie que la méthode renvoie une liste de Joueur
    de taille supérieure ou égale à 2
    """

    # GIVEN

    # WHEN
    joueurs = JoueurDao().lister_tous()

    # THEN
    assert isinstance(joueurs, list)
    for j in joueurs:
        assert isinstance(j, Joueur)
    assert len(joueurs) >= 2


def test_creer_ok():
    """Création de Joueur réussie"""

    # GIVEN
    joueur = Joueur(pseudo="gg", age=44, mail="gg@ensai.fr", mdp="123abc", credit=Monnaie(0))

    # WHEN
    creation_ok = JoueurDao().creer(joueur)

    # THEN
    assert creation_ok
    assert joueur.id_joueur


def test_creer_ko():
    """Création de Joueur échouée (age et mail incorrects)"""

    # GIVEN
    joueur = Joueur(pseudo="gg", age="chaine de caractere", mdp="123abc", mail=12, credit=Monnaie(0))

    # WHEN
    creation_ok = JoueurDao().creer(joueur)

    # THEN
    assert not creation_ok


def test_modifier_ok():
    """Modification de Joueur réussie"""

    # GIVEN
    new_mail = "maurice@mail.com"
    joueur = Joueur(id_joueur=997, pseudo="maurice", age=20, mdp="123abc", mail=new_mail, credit=Monnaie(0))

    # WHEN
    modification_ok = JoueurDao().modifier(joueur)

    # THEN
    assert modification_ok


def test_modifier_ko():
    """Modification de Joueur échouée (id inconnu)"""

    # GIVEN
    joueur = Joueur(id_joueur=8888, pseudo="id inconnu", age=1, mdp="123abc", mail="no@mail.com", credit=Monnaie(0))

    # WHEN
    modification_ok = JoueurDao().modifier(joueur)

    # THEN
    assert not modification_ok


def test_supprimer_ok():
    """Suppression de Joueur réussie"""

    # GIVEN
    joueur = Joueur(id_joueur=995, pseudo="miguel", age=1, mdp="123abc", mail="miguel@projet.fr", credit=Monnaie(0))

    # WHEN
    suppression_ok = JoueurDao().supprimer(joueur)

    # THEN
    assert suppression_ok


def test_supprimer_ko():
    """Suppression de Joueur échouée (id inconnu)"""

    # GIVEN
    joueur = Joueur(id_joueur=8888, pseudo="id inconnu", age=1, mdp="123abc", mail="no@z.fr", credit=Monnaie(0))

    # WHEN
    suppression_ok = JoueurDao().supprimer(joueur)

    # THEN
    assert not suppression_ok


def test_se_connecter_ok():
    """Connexion de Joueur réussie"""

    # GIVEN
    pseudo = "batricia"
    mdp = "9876"

    # WHEN
    joueur = JoueurDao().se_connecter(pseudo, hash_password(mdp, pseudo))

    # THEN
    assert isinstance(joueur, Joueur)


def test_se_connecter_ko():
    """Connexion de Joueur échouée (pseudo ou mdp incorrect)"""

    # GIVEN
    pseudo = "toto"
    mdp = "poiuytreza"

    # WHEN
    joueur = JoueurDao().se_connecter(pseudo, hash_password(mdp, pseudo))

    # THEN
    assert not joueur


if __name__ == "__main__": 
    pytest.main([__file__])