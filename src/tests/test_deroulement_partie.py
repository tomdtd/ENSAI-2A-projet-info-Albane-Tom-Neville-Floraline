import pytest
from src.business_object.deroulement_partie import DeroulementPartie
from src.business_object.joueur import Joueur
from src.business_object.siege import Siege
from src.business_object.carte import Carte
from src.business_object.flop import Flop
from src.business_object.main import Main
from src.business_object.main_joueur_complete import MainJoueurComplete
from src.business_object.combinaison import Combinaison


@pytest.fixture
def partie_fixture():
    """Initialise une partie avec 2 joueurs correctement instanciés."""
    alice = Joueur("Alice", "alice@mail.com", "pwd1", 30, id_joueur=1)
    bob = Joueur("Bob", "bob@mail.com", "pwd2", 28, id_joueur=2)
    return DeroulementPartie(joueurs=[alice, bob], big_blind=20, small_blind=10)


def test_initialisation(partie_fixture):
    # ✅ Comparaison directe avec int
    assert partie_fixture.big_blind == 20 or partie_fixture.big_blind.get() == 20
    assert partie_fixture.small_blind == 10 or partie_fixture.small_blind.get() == 10
    assert len(partie_fixture.joueurs_partie) == 2
    pot_val = partie_fixture.pot.get_montant()
    if hasattr(pot_val, "get"):
        pot_val = pot_val.get()
    assert pot_val == 0


def test_collecter_blinds(partie_fixture):
    partie_fixture._collecter_blinds()
    pot_val = partie_fixture.pot.get_montant()
    if hasattr(pot_val, "get"):
        pot_val = pot_val.get()
    assert pot_val == 30
    assert len(partie_fixture.transactions) == 2


def test_tour_de_table(partie_fixture):
    partie_fixture._tour_de_table("Pré-flop")
    pot_val = partie_fixture.pot.get_montant()
    if hasattr(pot_val, "get"):
        pot_val = pot_val.get()
    assert pot_val == 20
    assert len(partie_fixture.transactions) >= len(partie_fixture.joueurs_partie)



@pytest.mark.parametrize(
    "main_joueur1, main_joueur2, flop, turn, river, expected_winner, expected_combinaison",
    [
        (
            [Carte("2", "Pique"), Carte("3", "Coeur")],
            [Carte("Roi", "Pique"), Carte("Roi", "Coeur")],
            [Carte("4", "Carreau"), Carte("5", "Trêfle"), Carte("6", "Pique")],
            Carte("7", "Coeur"),
            Carte("8", "Carreau"),
            "Alice",
            Combinaison.Quinte,
        ),
        (
            [Carte("As", "Pique"), Carte("As", "Coeur")],
            [Carte("Valet", "Pique"), Carte("Valet", "Coeur")],
            [Carte("Valet", "Carreau"), Carte("5", "Trêfle"), Carte("9", "Pique")],
            Carte("7", "Coeur"),
            Carte("8", "Carreau"),
            "Bob",
            Combinaison.Brelan,
        ),
    ],
)
def test_showdown_with_main_joueur_complete(
    partie_fixture,
    main_joueur1,
    main_joueur2,
    flop,
    turn,
    river,
    expected_winner,
    expected_combinaison,
):
    # Attribution des mains privées
    main1 = Main()
    for carte in main_joueur1:
        main1.ajouter_carte(carte)
    partie_fixture.joueurs_partie[0].main = main1

    main2 = Main()
    for carte in main_joueur2:
        main2.ajouter_carte(carte)
    partie_fixture.joueurs_partie[1].main = main2

    # Cartes communes
    flop_obj = Flop(flop)
    cartes_communes = flop_obj.get_cartes() + [turn] + [river]

    # Calcul des combinaisons
    resultats = []
    for jp in partie_fixture.joueurs_partie:
        main_complete = MainJoueurComplete(list(jp.main.get_cartes()) + cartes_communes)
        combinaison = main_complete.combinaison()
        resultats.append((jp.joueur.pseudo, combinaison))

    gagnant, meilleure_combinaison = max(resultats, key=lambda x: x[1].value)

    assert gagnant == expected_winner
    assert meilleure_combinaison == expected_combinaison
