import pytest
from src.dao.deroulement_partie_dao import DeroulementPartieDao
from src.business_object.joueur import Joueur
from src.business_object.transaction import Transaction


@pytest.fixture
def dao():
    return DeroulementPartieDao()


@pytest.fixture
def session_id(dao):
    joueurs = [
        Joueur("Alice", "alice@mail.com", "pwd1", 30, id_joueur=1),
        Joueur("Bob", "bob@mail.com", "pwd2", 28, id_joueur=2),
    ]
    return dao.creer_session(joueurs=joueurs, big_blind=20, small_blind=10)


def to_int(val):
    return val.get() if hasattr(val, "get") else val


def test_creer_et_lancer_partie(dao, session_id):
    assert dao.get_session(session_id) is not None
    assert dao.get_blinds(session_id) == (10, 20)

    ok = dao.lancer_partie(session_id)
    assert ok is True

    partie = dao.get_partie(session_id)
    assert partie is not None
    assert len(partie.joueurs) == 2


def test_collecter_blinds(dao, session_id):
    # Assure que la partie est lancée (répartition des blinds faite dans lancer_partie)
    dao.lancer_partie(session_id)

    ok = dao.collecter_blinds(session_id)
    assert ok is True

    pot = dao.get_montant_pot(session_id)
    assert pot == 30  # SB + BB


def test_tour_de_table(dao, session_id):
    dao.lancer_partie(session_id)

    ok = dao.tour_de_table(session_id, "Pré-flop")
    assert ok is True

    pot = dao.get_montant_pot(session_id)
    # Après blinds 30 + deux mises de 10 = 50
    assert pot >= 50


def test_enregistrer_transaction(dao, session_id):
    dao.lancer_partie(session_id)

    tr = Transaction(solde=-10, date=None, id_joueur=1)
    ok = dao.enregistrer_transaction(session_id, tr)
    assert ok is True

    pot = dao.get_montant_pot(session_id)
    assert pot >= 40  # 30 blinds + 10 ajout


def test_get_gagnant_apres_showdown(dao, session_id):
    dao.lancer_partie(session_id)
    # Simule un gain de Bob
    tr_gain = Transaction(solde=50, date=None, id_joueur=2)
    dao.enregistrer_transaction(session_id, tr_gain)

    gagnant = dao.get_gagnant_apres_showdown(session_id)
    assert gagnant is not None
    assert gagnant.joueur.pseudo == "Bob"
