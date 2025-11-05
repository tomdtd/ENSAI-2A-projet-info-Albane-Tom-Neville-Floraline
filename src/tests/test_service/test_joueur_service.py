import pytest
from unittest.mock import patch, MagicMock
from utils.securite import hash_password
from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao
from service.joueur_service import JoueurService

@pytest.fixture
def mock_joueur_dao():
    # Mock de JoueurDao pour éviter d'appeler la base de données
    with patch.object(JoueurDao, 'creer') as mock_creer, \
         patch.object(JoueurDao, 'lister_tous') as mock_lister_tous, \
         patch.object(JoueurDao, 'trouver_par_id') as mock_trouver_par_id, \
         patch.object(JoueurDao, 'modifier') as mock_modifier, \
         patch.object(JoueurDao, 'supprimer') as mock_supprimer, \
         patch.object(JoueurDao, 'se_connecter') as mock_se_connecter:

        yield {
            "creer": mock_creer,
            "lister_tous": mock_lister_tous,
            "trouver_par_id": mock_trouver_par_id,
            "modifier": mock_modifier,
            "supprimer": mock_supprimer,
            "se_connecter": mock_se_connecter,
        }

def test_creer_joueur_ok(mock_joueur_dao):
    # GIVEN
    mock_joueur_dao["creer"].return_value = True
    pseudo = "test_pseudo"
    mdp = "test_mdp"
    age = 25
    mail = "test@example.com"
    credit = 1000

    # WHEN
    joueur_service = JoueurService()
    joueur = joueur_service.creer(pseudo, mdp, age, mail, credit)

    # THEN
    assert joueur is not None
    assert joueur.pseudo == pseudo
    assert joueur.mdp == hash_password(mdp, pseudo)
    assert joueur.age == age
    assert joueur.mail == mail
    assert joueur.credit == credit
    mock_joueur_dao["creer"].assert_called_once()

def test_creer_joueur_ko(mock_joueur_dao):
    # GIVEN
    mock_joueur_dao["creer"].return_value = False
    pseudo = "test_pseudo"
    mdp = "test_mdp"
    age = 25
    mail = "test@example.com"
    credit = 1000

    # WHEN
    joueur_service = JoueurService()
    joueur = joueur_service.creer(pseudo, mdp, age, mail, credit)

    # THEN
    assert joueur is None
    mock_joueur_dao["creer"].assert_called_once()

def test_lister_tous_joueurs(mock_joueur_dao):
    # GIVEN
    mock_joueurs = [
        Joueur(pseudo="joueur1", age=25, mail="joueur1@example.com", credit=1000),
        Joueur(pseudo="joueur2", age=30, mail="joueur2@example.com", credit=2000),
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

def test_lister_tous_joueurs_sans_mdp(mock_joueur_dao):
    # GIVEN
    mock_joueurs = [
        Joueur(pseudo="joueur1", age=25, mail="joueur1@example.com", credit=1000, mdp="mdp1"),
        Joueur(pseudo="joueur2", age=30, mail="joueur2@example.com", credit=2000, mdp="mdp2"),
    ]
    mock_joueur_dao["lister_tous"].return_value = mock_joueurs

    # WHEN
    joueur_service = JoueurService()
    joueurs = joueur_service.lister_tous(inclure_mdp=False)

    # THEN
    assert joueurs[0].mdp is None
    assert joueurs[1].mdp is None
    mock_joueur_dao["lister_tous"].assert_called_once()

def test_trouver_par_id_ok(mock_joueur_dao):
    # GIVEN
    mock_joueur = Joueur(id_joueur=1, pseudo="test_pseudo", age=25, mail="test@example.com", credit=1000)
    mock_joueur_dao["trouver_par_id"].return_value = mock_joueur

    # WHEN
    joueur_service = JoueurService()
    joueur = joueur_service.trouver_par_id(1)

    # THEN
    assert joueur == mock_joueur
    mock_joueur_dao["trouver_par_id"].assert_called_once_with(1)

def test_trouver_par_id_ko(mock_joueur_dao):
    # GIVEN
    mock_joueur_dao["trouver_par_id"].return_value = None

    # WHEN
    joueur_service = JoueurService()
    joueur = joueur_service.trouver_par_id(999)

    # THEN
    assert joueur is None
    mock_joueur_dao["trouver_par_id"].assert_called_once_with(999)

def test_modifier_joueur_ok(mock_joueur_dao):
    # GIVEN
    mock_joueur = Joueur(id_joueur=1, pseudo="test_pseudo", age=25, mail="test@example.com", credit=1000, mdp="old_mdp")
    mock_joueur_dao["modifier"].return_value = True

    # WHEN
    joueur_service = JoueurService()
    mock_joueur.mdp = "new_mdp"
    joueur = joueur_service.modifier(mock_joueur)

    # THEN
    assert joueur == mock_joueur
    assert joueur.mdp == hash_password("new_mdp", mock_joueur.pseudo)
    mock_joueur_dao["modifier"].assert_called_once()

def test_modifier_joueur_ko(mock_joueur_dao):
    # GIVEN
    mock_joueur = Joueur(id_joueur=1, pseudo="test_pseudo", age=25, mail="test@example.com", credit=1000, mdp="old_mdp")
    mock_joueur_dao["modifier"].return_value = False

    # WHEN
    joueur_service = JoueurService()
    joueur = joueur_service.modifier(mock_joueur)

    # THEN
    assert joueur is None
    mock_joueur_dao["modifier"].assert_called_once()

def test_supprimer_joueur_ok(mock_joueur_dao):
    # GIVEN
    mock_joueur = Joueur(id_joueur=1, pseudo="test_pseudo", age=25, mail="test@example.com", credit=1000)
    mock_joueur_dao["supprimer"].return_value = True

    # WHEN
    joueur_service = JoueurService()
    success = joueur_service.supprimer(mock_joueur)

    # THEN
    assert success
    mock_joueur_dao["supprimer"].assert_called_once()

def test_supprimer_joueur_ko(mock_joueur_dao):
    # GIVEN
    mock_joueur = Joueur(id_joueur=1, pseudo="test_pseudo", age=25, mail="test@example.com", credit=1000)
    mock_joueur_dao["supprimer"].return_value = False

    # WHEN
    joueur_service = JoueurService()
    success = joueur_service.supprimer(mock_joueur)

    # THEN
    assert not success
    mock_joueur_dao["supprimer"].assert_called_once()

def test_se_connecter_ok(mock_joueur_dao):
    # GIVEN
    pseudo = "test_pseudo"
    mdp = "test_mdp"
    mock_joueur = Joueur(id_joueur=1, pseudo=pseudo, age=25, mail="test@example.com", credit=1000, mdp=hash_password(mdp, pseudo))
    mock_joueur_dao["se_connecter"].return_value = mock_joueur

    # WHEN
    joueur_service = JoueurService()
    joueur = joueur_service.se_connecter(pseudo, mdp)

    # THEN
    assert joueur == mock_joueur
    mock_joueur_dao["se_connecter"].assert_called_once_with(pseudo, hash_password(mdp, pseudo))

def test_se_connecter_ko(mock_joueur_dao):
    # GIVEN
    pseudo = "test_pseudo"
    mdp = "wrong_mdp"
    mock_joueur_dao["se_connecter"].return_value = None

    # WHEN
    joueur_service = JoueurService()
    joueur = joueur_service.se_connecter(pseudo, mdp)

    # THEN
    assert joueur is None
    mock_joueur_dao["se_connecter"].assert_called_once_with(pseudo, hash_password(mdp, pseudo))

def test_pseudo_deja_utilise_ok(mock_joueur_dao):
    # GIVEN
    mock_joueurs = [
        Joueur(pseudo="joueur1", age=25, mail="joueur1@example.com", credit=1000),
        Joueur(pseudo="joueur2", age=30, mail="joueur2@example.com", credit=2000),
    ]
    mock_joueur_dao["lister_tous"].return_value = mock_joueurs

    # WHEN
    joueur_service = JoueurService()
    pseudo_utilise = joueur_service.pseudo_deja_utilise("joueur1")

    # THEN
    assert pseudo_utilise
    mock_joueur_dao["lister_tous"].assert_called_once()

def test_pseudo_deja_utilise_ko(mock_joueur_dao):
    # GIVEN
    mock_joueurs = [
        Joueur(pseudo="joueur1", age=25, mail="joueur1@example.com", credit=1000),
        Joueur(pseudo="joueur2", age=30, mail="joueur2@example.com", credit=2000),
    ]
    mock_joueur_dao["lister_tous"].return_value = mock_joueurs

    # WHEN
    joueur_service = JoueurService()
    pseudo_utilise = joueur_service.pseudo_deja_utilise("nouveau_pseudo")

    # THEN
    assert not pseudo_utilise
    mock_joueur_dao["lister_tous"].assert_called_once()
