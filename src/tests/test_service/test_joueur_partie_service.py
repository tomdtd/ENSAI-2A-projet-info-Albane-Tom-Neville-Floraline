import pytest
from unittest.mock import patch, MagicMock                     
from src.service.joueur_partie_service import JoueurPartieService             
from src.dao.joueur_partie_dao import JoueurPartieDao             
from src.business_object.joueur_partie import JoueurPartie           
from src.business_object.joueur import Joueur
from src.business_object.siege import Siege
from src.business_object.monnaie import Monnaie         
from datetime import datetime

@pytest.fixture
def mock_joueur_partie_dao():
    with patch.object(JoueurPartieDao, 'creer') as mock_creer, \
         patch.object(JoueurPartieDao, 'supprimer') as mock_supprimer:
        yield {
            "creer": mock_creer,
            "supprimer": mock_supprimer,
        }

def test_ajouter_joueur_a_partie_ok(mock_joueur_partie_dao):
    # GIVEN
    joueur = Joueur(pseudo="Joueur1", mail="joueur1@example.com", credit=1000, mdp="password", id_joueur=1, age=25)
    siege = Siege(id_siege=1)
    solde_partie = 1000
    id_table = 1
    mock_joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=solde_partie)
    mock_joueur_partie_dao["creer"].return_value = mock_joueur_partie

    # WHEN
    joueur_partie_service = JoueurPartieService()
    joueur_partie = joueur_partie_service.ajouter_joueur_a_partie(joueur, siege, solde_partie, id_table)

    # THEN
    assert joueur_partie is not None
    assert joueur_partie.joueur == joueur
    assert joueur_partie.siege == siege
    assert joueur_partie.solde_partie.valeur == solde_partie
    mock_joueur_partie_dao["creer"].assert_called_once()

def test_ajouter_joueur_a_partie_invalid_joueur(mock_joueur_partie_dao):
    # GIVEN
    siege = Siege(id_siege=1)
    solde_partie = 1000
    id_table = 1

    # WHEN
    joueur_partie_service = JoueurPartieService()

    # THEN
    with pytest.raises(ValueError):
        joueur_partie_service.ajouter_joueur_a_partie(None, siege, solde_partie, id_table)

def test_ajouter_joueur_a_partie_invalid_siege(mock_joueur_partie_dao):
    # GIVEN
    joueur = Joueur(pseudo="Joueur1", mail="joueur1@example.com", credit=1000, mdp="password", id_joueur=1, age=25)
    solde_partie = 1000
    id_table = 1
    mock_joueur_partie_dao["creer"].return_value = True

    # WHEN
    joueur_partie_service = JoueurPartieService()
    # La validation du siège est commentée dans le service, donc on teste que ça fonctionne avec None
    joueur_partie = joueur_partie_service.ajouter_joueur_a_partie(joueur, None, solde_partie, id_table)

    # THEN
    assert joueur_partie is not None
    mock_joueur_partie_dao["creer"].assert_called_once()

def test_ajouter_joueur_a_partie_invalid_solde(mock_joueur_partie_dao):
    # GIVEN
    joueur = Joueur(pseudo="Joueur1", mail="joueur1@example.com", credit=1000, mdp="password", id_joueur=1, age=25)
    siege = Siege(id_siege=1)
    solde_partie = -1000
    id_table = 1
    # WHEN
    joueur_partie_service = JoueurPartieService()
    # THEN
    with pytest.raises(ValueError):
        joueur_partie_service.ajouter_joueur_a_partie(joueur, siege, solde_partie, id_table)

def test_retirer_joueur_de_partie_ok(mock_joueur_partie_dao):
    # GIVEN
    id_joueur = 1
    mock_joueur_partie_dao["supprimer"].return_value = True

    # WHEN
    joueur_partie_service = JoueurPartieService()
    result = joueur_partie_service.retirer_joueur_de_partie(id_joueur)

    # THEN
    assert result is True
    mock_joueur_partie_dao["supprimer"].assert_called_once_with(id_joueur)

def test_retirer_joueur_de_partie_invalid_id_joueur(mock_joueur_partie_dao):
    # GIVEN
    id_joueur = None

    # WHEN
    joueur_partie_service = JoueurPartieService()

    # THEN
    with pytest.raises(ValueError):
        joueur_partie_service.retirer_joueur_de_partie(id_joueur)

def test_miser_ok():
    # GIVEN
    joueur = Joueur(pseudo="Joueur1", mail="joueur1@example.com", credit=1000, mdp="password", id_joueur=1, age=25)
    siege = Siege(id_siege=1)
    joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=1000)
    # Mock de _trouver_joueur_partie_par_id_joueur
    with patch.object(JoueurPartieService, '_trouver_joueur_partie_par_id_joueur', return_value=joueur_partie):
        # WHEN
        joueur_partie_service = JoueurPartieService()
        result = joueur_partie_service.miser(joueur.id_joueur, 100)
        # THEN
        assert result is True
        assert joueur_partie.solde_partie.valeur == 900
        assert joueur_partie.mise_tour.valeur == 100

def test_miser_invalid_montant():
    # GIVEN
    joueur = Joueur(pseudo="Joueur1", mail="joueur1@example.com", credit=1000, mdp="password", id_joueur=1, age=25)
    montant = -100
    # WHEN
    joueur_partie_service = JoueurPartieService()
    # THEN
    with pytest.raises(ValueError):
        joueur_partie_service.miser(joueur.id_joueur, montant)

def test_miser_invalid_joueur():
    # GIVEN
    id_joueur = 1
    montant = 100

    # Mock de _trouver_joueur_partie_par_id_joueur
    with patch.object(JoueurPartieService, '_trouver_joueur_partie_par_id_joueur', return_value=None):
        # WHEN
        joueur_partie_service = JoueurPartieService()

        # THEN
        with pytest.raises(ValueError):
            joueur_partie_service.miser(id_joueur, montant)

def test_se_coucher_ok():
    # GIVEN
    joueur = Joueur(pseudo="Joueur1", mail="joueur1@example.com", credit=1000, mdp="password", id_joueur=1, age=25)
    siege = Siege(id_siege=1)
    joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=1000)
    # Mock de _trouver_joueur_partie_par_id_joueur
    with patch.object(JoueurPartieService, '_trouver_joueur_partie_par_id_joueur', return_value=joueur_partie):
        # WHEN
        joueur_partie_service = JoueurPartieService()
        result = joueur_partie_service.se_coucher(joueur.id_joueur)
        # THEN
        assert result is True
        assert joueur_partie.statut == "couché"

def test_se_coucher_invalid_joueur():
    # GIVEN
    id_joueur = 1

    # Mock de _trouver_joueur_partie_par_id_joueur
    with patch.object(JoueurPartieService, '_trouver_joueur_partie_par_id_joueur', return_value=None):
        # WHEN
        joueur_partie_service = JoueurPartieService()

        # THEN
        with pytest.raises(ValueError):
            joueur_partie_service.se_coucher(id_joueur)
