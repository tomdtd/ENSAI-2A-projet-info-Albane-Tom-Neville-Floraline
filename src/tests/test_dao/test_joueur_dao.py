import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase
from utils.securite import hash_password

from dao.db_connection import DBConnection
from dao.joueur_dao import JoueurDao

from business_object.joueur import Joueur


joueurs = [
    (999, "admin",    "0000",    "admin@projet.fr", 0,  0),
    (998, "a",        "a",       "a@ensai.fr",      20, 10),
    (997, "maurice",  "1234",    "maurice@ensai.fr",20, 50),
    (996, "batricia", "9876",    "bat@projet.fr",   25, 30),
    (995, "miguel",   "abcd",    "miguel@projet.fr",23, 15),
    (994, "gilbert",  "toto",    "gilbert@projet.fr",21, 40),
    (993, "junior",   "aaaa",    "junior@projet.fr", 15, 20),
]

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        # reset de la base (script SQL préparé dans ResetDatabase)
        ResetDatabase().lancer(test_dao=True)

        # insertion idempotente : OVERRIDING SYSTEM VALUE + ON CONFLICT DO NOTHING
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                for id_joueur, pseudo, mdp_plain, mail, age, credit in joueurs:
                    mdp_hashed = hash_password(mdp_plain, pseudo)
                    cursor.execute(
                        """
                        INSERT INTO joueur(id_joueur, pseudo, mdp, mail, age, credit)
                        OVERRIDING SYSTEM VALUE
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id_joueur) DO NOTHING
                        """,
                        (id_joueur, pseudo, mdp_hashed, mail, age, credit),
                    )
            connection.commit()

        yield
"""
# ou remplacer par le code initial
# @pytest.fixture(scope="session", autouse=True)
# def setup_test_environment():
#     """Initialisation des données de test"""
#     with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
#         ResetDatabase().lancer(test_dao=True)
#         yield
# 
"""


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
    joueur = Joueur(pseudo="gg", age=44, mail="gg@ensai.fr", mdp="123abc", credit=0)

    # WHEN
    creation_ok = JoueurDao().creer(joueur)

    # THEN
    assert creation_ok
    assert joueur.id_joueur


def test_creer_ko():
    """Création de Joueur échouée (age et mail incorrects)"""

    # GIVEN
    joueur = Joueur(pseudo="gg", age="chaine de caractere", mdp="123abc", mail=12, credit=0)

    # WHEN
    creation_ok = JoueurDao().creer(joueur)

    # THEN
    assert not creation_ok


def test_modifier_ok():
    """Modification de Joueur réussie"""

    # GIVEN
    new_mail = "maurice@mail.com"
    joueur = Joueur(id_joueur=997, pseudo="maurice", age=20, mdp="123abc", mail=new_mail, credit=0)

    # WHEN
    modification_ok = JoueurDao().modifier(joueur)

    # THEN
    assert modification_ok


def test_modifier_ko():
    """Modification de Joueur échouée (id inconnu)"""

    # GIVEN
    joueur = Joueur(id_joueur=8888, pseudo="id inconnu", age=1, mdp="123abc", mail="no@mail.com", credit=0)

    # WHEN
    modification_ok = JoueurDao().modifier(joueur)

    # THEN
    assert not modification_ok


def test_supprimer_ok():
    """Suppression de Joueur réussie"""

    # GIVEN
    joueur = Joueur(id_joueur=995, pseudo="miguel", age=1, mdp="123abc", mail="miguel@projet.fr", credit=0)

    # WHEN
    suppression_ok = JoueurDao().supprimer(joueur)

    # THEN
    assert suppression_ok


def test_supprimer_ko():
    """Suppression de Joueur échouée (id inconnu)"""

    # GIVEN
    joueur = Joueur(id_joueur=8888, pseudo="id inconnu", age=1, mdp="123abc", mail="no@z.fr", credit=0)

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