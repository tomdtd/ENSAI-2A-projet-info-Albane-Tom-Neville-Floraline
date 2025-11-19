import pytest
from unittest.mock import patch, MagicMock
from src.business_object.admin import Admin
from src.service.admin_service import AdminService
from src.dao.admin_dao import AdminDao
from src.utils.securite import hash_password

@pytest.fixture
def mock_admin_dao():
    # Mock de AdminDao pour éviter d'appeler la base de données
    with patch.object(AdminDao, 'trouver_par_id') as mock_trouver_par_id, \
         patch.object(AdminDao, 'trouver_par_nom') as mock_trouver_par_nom, \
         patch.object(AdminDao, 'changer_mot_de_passe') as mock_changer_mot_de_passe, \
         patch.object(AdminDao, 'valider_transaction') as mock_valider_transaction, \
         patch.object(AdminDao, 'lister_transactions_en_attente') as mock_lister_transactions_en_attente, \
         patch.object(AdminDao, 'banir_joueur') as mock_banir_joueur, \
         patch.object(AdminDao, 'debannir_joueur') as mock_debannir_joueur, \
         patch.object(AdminDao, 'lister_joueurs_banis') as mock_lister_joueurs_banis, \
         patch.object(AdminDao, 'obtenir_statistiques_joueur') as mock_obtenir_statistiques_joueur, \
         patch.object(AdminDao, 'obtenir_tables_jouees_par_joueur') as mock_obtenir_tables_jouees_par_joueur, \
         patch.object(AdminDao, 'obtenir_statistiques_globales') as mock_obtenir_statistiques_globales, \
         patch.object(AdminDao, 'obtenir_top_joueurs') as mock_obtenir_top_joueurs, \
         patch.object(AdminDao, 'obtenir_activite_recente') as mock_obtenir_activite_recente:

        yield {
            "trouver_par_id": mock_trouver_par_id,
            "trouver_par_nom": mock_trouver_par_nom,
            "changer_mot_de_passe": mock_changer_mot_de_passe,
            "valider_transaction": mock_valider_transaction,
            "lister_transactions_en_attente": mock_lister_transactions_en_attente,
            "banir_joueur": mock_banir_joueur,
            "debannir_joueur": mock_debannir_joueur,
            "lister_joueurs_banis": mock_lister_joueurs_banis,
            "obtenir_statistiques_joueur": mock_obtenir_statistiques_joueur,
            "obtenir_tables_jouees_par_joueur": mock_obtenir_tables_jouees_par_joueur,
            "obtenir_statistiques_globales": mock_obtenir_statistiques_globales,
            "obtenir_top_joueurs": mock_obtenir_top_joueurs,
            "obtenir_activite_recente": mock_obtenir_activite_recente,
        }

def test_trouver_par_id(mock_admin_dao):
    # GIVEN
    admin_id = 1
    mock_admin = Admin(admin_id=admin_id, nom="AdminTest", mdp="hash", mail="admin@example.com")
    mock_admin_dao["trouver_par_id"].return_value = mock_admin

    # WHEN
    admin_service = AdminService()
    admin = admin_service.trouver_par_id(admin_id)

    # THEN
    assert admin == mock_admin
    mock_admin_dao["trouver_par_id"].assert_called_once_with(admin_id)

def test_trouver_par_nom(mock_admin_dao):
    # GIVEN
    nom_admin = "AdminTest"
    mock_admin = Admin(admin_id=1, nom=nom_admin, mdp="hash", mail="admin@example.com")
    mock_admin_dao["trouver_par_nom"].return_value = mock_admin

    # WHEN
    admin_service = AdminService()
    admin = admin_service.trouver_par_nom(nom_admin)

    # THEN
    assert admin == mock_admin
    mock_admin_dao["trouver_par_nom"].assert_called_once_with(nom_admin)

def test_verifier_identifiants_ok(mock_admin_dao):
    # GIVEN
    nom_admin = "AdminTest"
    mot_de_passe = "motdepasse"
    mot_de_passe_hash = hash_password(mot_de_passe, nom_admin)
    mock_admin = Admin(admin_id=1, nom=nom_admin, mdp=mot_de_passe_hash, mail="admin@example.com")
    mock_admin_dao["trouver_par_nom"].return_value = mock_admin

    # WHEN
    admin_service = AdminService()
    admin = admin_service.verifier_identifiants(nom_admin, mot_de_passe)

    # THEN
    assert admin == mock_admin
    mock_admin_dao["trouver_par_nom"].assert_called_once_with(nom_admin)

def test_verifier_identifiants_ko(mock_admin_dao):
    # GIVEN
    nom_admin = "AdminTest"
    mot_de_passe = "wrongpassword"
    mot_de_passe_hash = hash_password("correctpassword", nom_admin)
    mock_admin = Admin(admin_id=1, nom=nom_admin, mdp=mot_de_passe_hash, mail="admin@example.com")
    mock_admin_dao["trouver_par_nom"].return_value = mock_admin

    # WHEN
    admin_service = AdminService()
    admin = admin_service.verifier_identifiants(nom_admin, mot_de_passe)

    # THEN
    assert admin is None
    mock_admin_dao["trouver_par_nom"].assert_called_once_with(nom_admin)

def test_changer_mot_de_passe_ok(mock_admin_dao):
    # GIVEN
    admin_id = 1
    ancien_mot_de_passe = "oldpassword"
    nouveau_mot_de_passe = "newpassword"
    nom_admin = "AdminTest"
    ancien_mot_de_passe_hash = hash_password(ancien_mot_de_passe, nom_admin)
    mock_admin = Admin(admin_id=admin_id, nom=nom_admin, mdp=ancien_mot_de_passe_hash, mail="admin@example.com")
    mock_admin_dao["trouver_par_id"].return_value = mock_admin
    mock_admin_dao["changer_mot_de_passe"].return_value = True

    # WHEN
    admin_service = AdminService()
    result = admin_service.changer_mot_de_passe(admin_id, ancien_mot_de_passe, nouveau_mot_de_passe)

    # THEN
    assert result is True
    mock_admin_dao["trouver_par_id"].assert_called_once_with(admin_id)
    mock_admin_dao["changer_mot_de_passe"].assert_called_once()


def test_changer_mot_de_passe_ancien_mot_de_passe_incorrect(mock_admin_dao):
    # GIVEN
    admin_id = 1
    ancien_mot_de_passe = "wrongoldpassword"
    nouveau_mot_de_passe = "newpassword"
    nom_admin = "AdminTest"
    ancien_mot_de_passe_hash = hash_password("correctoldpassword", nom_admin)
    mock_admin = Admin(admin_id=admin_id, nom=nom_admin, mdp=ancien_mot_de_passe_hash, mail="admin@example.com")
    mock_admin_dao["trouver_par_id"].return_value = mock_admin

    # WHEN
    admin_service = AdminService()
    result = admin_service.changer_mot_de_passe(admin_id, ancien_mot_de_passe, nouveau_mot_de_passe)

    # THEN
    assert result is False
    mock_admin_dao["trouver_par_id"].assert_called_once_with(admin_id)
    mock_admin_dao["changer_mot_de_passe"].assert_not_called()

def test_valider_transaction_ok(mock_admin_dao):
    # GIVEN
    id_transaction = 1
    mock_admin_dao["valider_transaction"].return_value = True

    # WHEN
    admin_service = AdminService()
    result = admin_service.valider_transaction(id_transaction)

    # THEN
    assert result is True
    mock_admin_dao["valider_transaction"].assert_called_once_with(id_transaction)

def test_valider_transaction_ko(mock_admin_dao):
    # GIVEN
    id_transaction = 1
    mock_admin_dao["valider_transaction"].return_value = False

    # WHEN
    admin_service = AdminService()
    result = admin_service.valider_transaction(id_transaction)

    # THEN
    assert result is False
    mock_admin_dao["valider_transaction"].assert_called_once_with(id_transaction)

def test_lister_transactions_en_attente(mock_admin_dao):
    # GIVEN
    mock_transactions = [
        {"id_transaction": 1, "pseudo": "Joueur1", "type_transaction": "depot", "montant": 100},
        {"id_transaction": 2, "pseudo": "Joueur2", "type_transaction": "retrait", "montant": 50},
    ]
    mock_admin_dao["lister_transactions_en_attente"].return_value = mock_transactions

    # WHEN
    admin_service = AdminService()
    transactions = admin_service.lister_transactions_en_attente()

    # THEN
    assert transactions == mock_transactions
    mock_admin_dao["lister_transactions_en_attente"].assert_called_once()

def test_banir_joueur_ok(mock_admin_dao):
    # GIVEN
    id_joueur = 1
    id_admin = 1
    raison_ban = "Triche"
    mock_admin_dao["banir_joueur"].return_value = True

    # WHEN
    admin_service = AdminService()
    result = admin_service.banir_joueur(id_joueur, id_admin, raison_ban)

    # THEN
    assert result is True
    mock_admin_dao["banir_joueur"].assert_called_once_with(id_joueur, id_admin, raison_ban)

def test_banir_joueur_raison_vide():
    # GIVEN
    id_joueur = 1
    id_admin = 1
    raison_ban = ""

    # WHEN
    admin_service = AdminService()

    # THEN
    with pytest.raises(ValueError):
        admin_service.banir_joueur(id_joueur, id_admin, raison_ban)

def test_debannir_joueur_ok(mock_admin_dao):
    # GIVEN
    pseudo = "JoueurTest"
    mock_admin_dao["debannir_joueur"].return_value = True

    # WHEN
    admin_service = AdminService()
    result = admin_service.debannir_joueur(pseudo)

    # THEN
    assert result is True
    mock_admin_dao["debannir_joueur"].assert_called_once_with(pseudo)

def test_lister_joueurs_banis(mock_admin_dao):
    # GIVEN
    mock_joueurs_banis = [
        {"pseudo": "Joueur1", "email": "joueur1@example.com", "credit": 100, "date_ban": "2023-01-01", "raison_ban": "Triche"},
        {"pseudo": "Joueur2", "email": "joueur2@example.com", "credit": 200, "date_ban": "2023-01-02", "raison_ban": "Insultes"},
    ]
    mock_admin_dao["lister_joueurs_banis"].return_value = mock_joueurs_banis

    # WHEN
    admin_service = AdminService()
    joueurs_banis = admin_service.lister_joueurs_banis()

    # THEN
    assert joueurs_banis == mock_joueurs_banis
    mock_admin_dao["lister_joueurs_banis"].assert_called_once()

def test_obtenir_statistiques_joueur(mock_admin_dao):
    # GIVEN
    id_joueur = 1
    mock_statistiques = {"pseudo": "Joueur1", "total_parties": 10, "parties_gagnees": 5}
    mock_admin_dao["obtenir_statistiques_joueur"].return_value = mock_statistiques

    # WHEN
    admin_service = AdminService()
    statistiques = admin_service.obtenir_statistiques_joueur(id_joueur)

    # THEN
    assert statistiques == mock_statistiques
    mock_admin_dao["obtenir_statistiques_joueur"].assert_called_once_with(id_joueur)

def test_obtenir_tables_jouees_par_joueur(mock_admin_dao):
    # GIVEN
    id_joueur = 1
    mock_tables = [
        {"id_table": 1, "nom_table": "Table1", "nb_parties": 5},
        {"id_table": 2, "nom_table": "Table2", "nb_parties": 3},
    ]
    mock_admin_dao["obtenir_tables_jouees_par_joueur"].return_value = mock_tables

    # WHEN
    admin_service = AdminService()
    tables = admin_service.obtenir_tables_jouees_par_joueur(id_joueur)

    # THEN
    assert tables == mock_tables
    mock_admin_dao["obtenir_tables_jouees_par_joueur"].assert_called_once_with(id_joueur)

def test_obtenir_statistiques_globales(mock_admin_dao):
    # GIVEN
    mock_statistiques = {"total_joueurs": 100, "total_parties": 50, "total_tables": 10}
    mock_admin_dao["obtenir_statistiques_globales"].return_value = mock_statistiques

    # WHEN
    admin_service = AdminService()
    statistiques = admin_service.obtenir_statistiques_globales()

    # THEN
    assert statistiques == mock_statistiques
    mock_admin_dao["obtenir_statistiques_globales"].assert_called_once()

def test_obtenir_top_joueurs(mock_admin_dao):
    # GIVEN
    limite = 10
    mock_top_joueurs = [
        {"pseudo": "Joueur1", "total_gains": 1000, "taux_victoire": 80},
        {"pseudo": "Joueur2", "total_gains": 800, "taux_victoire": 75},
    ]
    mock_admin_dao["obtenir_top_joueurs"].return_value = mock_top_joueurs

    # WHEN
    admin_service = AdminService()
    top_joueurs = admin_service.obtenir_top_joueurs(limite)

    # THEN
    assert top_joueurs == mock_top_joueurs
    mock_admin_dao["obtenir_top_joueurs"].assert_called_once_with(limite)

def test_obtenir_activite_recente(mock_admin_dao):
    # GIVEN
    jours = 7
    mock_activite = {"nouveaux_joueurs": 10, "parties_debutees": 5, "volume_transactions_recent": 1000}
    mock_admin_dao["obtenir_activite_recente"].return_value = mock_activite

    # WHEN
    admin_service = AdminService()
    activite = admin_service.obtenir_activite_recente(jours)

    # THEN
    assert activite == mock_activite
    mock_admin_dao["obtenir_activite_recente"].assert_called_once_with(jours)
