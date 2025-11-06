import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.service.joueur_service import JoueurService
from dao.joueur_dao import JoueurDao
from business_object.joueur import Joueur
from utils.securite import hash_password

@pytest.fixture
def mock_joueur_dao():
    with patch.object(JoueurDao, 'creer') as mock_creer, \
         patch.object(JoueurDao, 'trouver_par_id') as mock_trouver_par_id, \
         patch.object(JoueurDao, 'lister_tous') as mock_lister_tous, \
         patch.object(JoueurDao, 'modifier') as mock_modifier, \
         patch.object(JoueurDao, 'supprimer') as mock_supprimer, \
         patch.object(JoueurDao, 'se_connecter') as mock_se_connecter:
        yield {
            "creer": mock_creer,
            "trouver_par_id": mock_trouver_par_id,
            "lister_tous": mock_lister_tous,
            "modifier": mock_modifier,
            "supprimer": mock_supprimer,
            "se_connecter": mock_se_connecter,
        }

def test_creer_ok(mock_joueur_dao):
    # GIVEN
    pseudo = "test_pseudo"
    mdp = "test_mdp"
    mail = "test@example.com"
    age = 25
    credit = 1000
    mock_joueur_dao["creer"].return_value = True

    # WHEN
    joueur_service = JoueurService()
    joueur = joueur_service.creer(pseudo, mdp, mail, age, credit)

    # THEN
    assert joueur is not None
    assert joueur.pseudo == pseudo
    assert joueur.mail == mail
    assert joueur.age == age
    assert joueur.credit == credit
    assert joueur.mdp == hash_password(mdp, pseudo)
    mock_joueur_dao["creer"].assert_called_once()

def test_creer_invalid_params():
    # GIVEN
    pseudo = ""
    mdp = ""
    mail = ""
    age = -1
    credit = -1

    # WHEN
    joueur_service = JoueurService()

    # THEN
    with pytest.raises(ValueError):
        joueur_service.creer(pseudo, mdp, mail, age, credit)

def test_trouver_par_id_ok(mock_joueur_dao):
    # GIVEN
    mock_joueur = Joueur(pseudo="test_pseudo", mail="test@example.com", credit=1000, mdp="test_mdp", age=25, id_joueur=1)
    mock_joueur_dao["trouver_par_id"].return_value = mock_joueur

    # WHEN
    joueur_service = JoueurService()
    joueur = joueur_service.trouver_par_id(1)

    # THEN
    assert joueur == mock_joueur
    mock_joueur_dao["trouver_par_id"].assert_called_once_with(1)

def test_trouver_par_id_invalid_id():
    # GIVEN
    id_joueur = None

    # WHEN
    joueur_service = JoueurService()

    # THEN
    with pytest.raises(ValueError):
        joueur_service.trouver_par_id(id_joueur)

def test_lister_tous(mock_joueur_dao):
    # GIVEN
    mock_joueurs = [
        Joueur(pseudo="joueur1", mail="joueur1@example.com", credit=1000, mdp="mdp1", age=25, id_joueur=1),
        Joueur(pseudo="joueur2", mail="joueur2@example.com", credit=2000, mdp="mdp2", age=30, id_joueur=2),
    ]
    mock_joueur_dao["lister_tous"].return_value = mock_joueurs

    # WHEN
    joueur_service = JoueurService()
    joueurs = joueur_service.lister_tous()

    # THEN
    assert len(joueurs) == 2
    assert joueurs[0].pseudo == "joueur1"
    assert joueurs[1].pseudo == "joueur2"
    mock_joueur_dao["lister_tous"].assert_called_once()

def test_modifier_ok(mock_joueur_dao):
    # GIVEN
    mock_joueur = Joueur(pseudo="test_pseudo", mail="test@example.com", credit=1000, mdp="test_mdp", age=25, id_joueur=1)
    mock_joueur_dao["modifier"].return_value = True

    # WHEN
    joueur_service = JoueurService()
    joueur = joueur_service.modifier(mock_joueur)

    # THEN
    assert joueur == mock_joueur
    mock_joueur_dao["modifier"].assert_called_once_with(mock_joueur)

def test_modifier_invalid_joueur():
    # GIVEN
    mock_joueur = None

    # WHEN
    joueur_service = JoueurService()

    # THEN
    with pytest.raises(ValueError):
        joueur_service.modifier(mock_joueur)

def test_supprimer_ok(mock_joueur_dao):
    # GIVEN
    mock_joueur = Joueur(pseudo="test_pseudo", mail="test@example.com", credit=1000, mdp="test_mdp", age=25, id_joueur=1)
    mock_joueur_dao["supprimer"].return_value = True

    # WHEN
    joueur_service = JoueurService()
    success = joueur_service.supprimer(mock_joueur)

    # THEN
    assert success
    mock_joueur_dao["supprimer"].assert_called_once_with(mock_joueur)

def test_supprimer_invalid_joueur():
    # GIVEN
    mock_joueur = None

    # WHEN
    joueur_service = JoueurService()

    # THEN
    with pytest.raises(ValueError):
        joueur_service.supprimer(mock_joueur)

def test_se_connecter_ok(mock_joueur_dao):
    # GIVEN
    pseudo = "test_pseudo"
    mdp = "test_mdp"
    mock_joueur = Joueur(pseudo=pseudo, mail="test@example.com", credit=1000, mdp=hash_password(mdp, pseudo), age=25, id_joueur=1)
    mock_joueur_dao["se_connecter"].return_value = mock_joueur

    # WHEN
    joueur_service = JoueurService()
    joueur = joueur_service.se_connecter(pseudo, mdp)

    # THEN
    assert joueur == mock_joueur
    mock_joueur_dao["se_connecter"].assert_called_once_with(pseudo, hash_password(mdp, pseudo))

def test_se_connecter_invalid_params():
    # GIVEN
    pseudo = ""
    mdp = ""

    # WHEN
    joueur_service = JoueurService()

    # THEN
    with pytest.raises(ValueError):
        joueur_service.se_connecter(pseudo, mdp)

def test_changer_mot_de_passe_ok(mock_joueur_dao):
    # GIVEN
    ancien_mdp = "old_mdp"
    nouveau_mdp = "new_mdp"
    pseudo = "test_pseudo"
    mock_joueur = Joueur(pseudo=pseudo, mail="test@example.com", credit=1000, mdp=hash_password(ancien_mdp, pseudo), age=25, id_joueur=1)
    mock_joueur_dao["modifier"].return_value = True

    # WHEN
    joueur_service = JoueurService()
    success = joueur_service.changer_mot_de_passe(mock_joueur, ancien_mdp, nouveau_mdp)

    # THEN
    assert success
    assert mock_joueur.mdp == hash_password(nouveau_mdp, pseudo)
    mock_joueur_dao["modifier"].assert_called_once_with(mock_joueur)

def test_changer_mot_de_passe_invalid_ancien_mdp():
    # GIVEN
    ancien_mdp = "wrong_old_mdp"
    nouveau_mdp = "new_mdp"
    pseudo = "test_pseudo"
    mock_joueur = Joueur(pseudo=pseudo, mail="test@example.com", credit=1000, mdp=hash_password("old_mdp", pseudo), age=25, id_joueur=1)

    # WHEN
    joueur_service = JoueurService()

    # THEN
    with pytest.raises(ValueError):
        joueur_service.changer_mot_de_passe(mock_joueur, ancien_mdp, nouveau_mdp)

def test_pseudo_deja_utilise_oui():
    """Le pseudo est déjà utilisé dans liste_joueurs"""
    mock_joueurs = [
        Joueur(pseudo="jp", age="10", mail="jp@mail.fr", mdp="1234"),
        Joueur(pseudo="lea", age="10", mail="lea@mail.fr", mdp="0000"),
        Joueur(pseudo="gg", age="10", mail="gg@mail.fr", mdp="abcd"),
    ]
    # GIVEN
    pseudo = "lea"

    # WHEN
    JoueurDao().lister_tous = MagicMock(return_value=mock_joueurs)
    res = JoueurService().pseudo_deja_utilise(pseudo)

    # THEN
    assert res


def test_pseudo_deja_utilise_non():
    """Le pseudo n'est pas utilisé dans liste_joueurs"""
    mock_joueurs = [
        Joueur(pseudo="joueur1", age="45", mail="joueur1@mail.fr", mdp="1234"),
        Joueur(pseudo="joueur2", age="75", mail="joueur2@mail.fr", mdp="0000"),
        Joueur(pseudo="joueur3", age="32", mail="joueur3@mail.fr", mdp="abcd"),
    ]
    # GIVEN
    pseudo = "chaton"

    # WHEN
    JoueurDao().lister_tous = MagicMock(return_value=mock_joueurs)
    res = JoueurService().pseudo_deja_utilise(pseudo)

    # THEN
    assert not res
