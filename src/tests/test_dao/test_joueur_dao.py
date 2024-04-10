import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase
from utils.securite import hash_password

from dao.joueur_dao import JoueurDao

from dto.joueur import Joueur


@pytest.fixture(scope="session")
def setup_test_environment():
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_trouver_par_id_existant(setup_test_environment):
    """Recherche par id d'un joueur existant"""

    # GIVEN
    id_joueur = 998

    # WHEN
    joueur = JoueurDao().trouver_par_id(id_joueur)

    # THEN
    assert joueur is not None


def test_trouver_par_id_non_existant(setup_test_environment):
    """Recherche par id d'un joueur n'existant pas"""

    # GIVEN
    id_joueur = 9999999999999

    # WHEN
    joueur = JoueurDao().trouver_par_id(id_joueur)

    # THEN
    assert joueur is None


def test_lister_tous(setup_test_environment):
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


def test_creer_ok(setup_test_environment):
    """Création de Joueur réussie"""

    # GIVEN
    joueur = Joueur(pseudo="gg", age=44, mail="test@test.io")

    # WHEN
    creation_ok = JoueurDao().creer(joueur)

    # THEN
    assert creation_ok
    assert joueur.id_joueur


def test_creer_ko(setup_test_environment):
    """Création de Joueur échouée (age et mail incorrects)"""

    # GIVEN
    joueur = Joueur(pseudo="gg", age="chaine de caractere", mail=12)

    # WHEN
    creation_ok = JoueurDao().creer(joueur)

    # THEN
    assert not creation_ok


def test_modifier_ok(setup_test_environment):
    """Modification de Joueur réussie"""

    # GIVEN
    new_mail = "maurice@mail.com"
    joueur = Joueur(id_joueur=997, pseudo="maurice", age=20, mail=new_mail)

    # WHEN
    modification_ok = JoueurDao().modifier(joueur)

    # THEN
    assert modification_ok


def test_modifier_ko(setup_test_environment):
    """Modification de Joueur échouée (id inconnu)"""

    # GIVEN
    joueur = Joueur(id_joueur=8888, pseudo="id inconnu", age=1, mail="no@mail.com")

    # WHEN
    modification_ok = JoueurDao().modifier(joueur)

    # THEN
    assert not modification_ok


def test_supprimer_ok(setup_test_environment):
    """Suppression de Joueur réussie"""

    # GIVEN
    joueur = Joueur(id_joueur=995, pseudo="miguel", age=1, mail="miguel@projet.fr")

    # WHEN
    suppression_ok = JoueurDao().supprimer(joueur)

    # THEN
    assert suppression_ok


def test_supprimer_ko(setup_test_environment):
    """Suppression de Joueur échouée (id inconnu)"""

    # GIVEN
    joueur = Joueur(id_joueur=8888, pseudo="id inconnu", age=1, mail="no@z.fr")

    # WHEN
    suppression_ok = JoueurDao().supprimer(joueur)

    # THEN
    assert not suppression_ok


def test_se_connecter_ok(setup_test_environment):
    """Connexion de Joueur réussie"""

    # GIVEN
    pseudo = "batricia"
    mdp = "9876"

    # WHEN
    joueur = JoueurDao().se_connecter(pseudo, hash_password(mdp, pseudo))

    # THEN
    assert isinstance(joueur, Joueur)


def test_se_connecter_ko(setup_test_environment):
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
