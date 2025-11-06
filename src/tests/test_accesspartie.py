import pytest
from src.business_object.accesspartie import AccessPartie
from src.business_object.joueur import Joueur
from src.business_object.siege import Siege
from src.business_object.monnaie import Monnaie
from src.business_object.JoueurPartie import JoueurPartie


# Mocks pour les dépendances
class MockJoueur:
    def __init__(self, id_joueur, pseudo, credit):
        self.id_joueur = id_joueur
        self.pseudo = pseudo
        self.credit = credit
        self.mail = f"{pseudo}@test.fr"
        self.age = 25
        self.mdp = "***"

    def jouer_partie(self):
        pass  # Simule l'action sans effet


class TestAccessPartie:

    @pytest.fixture
    def partie(self):
        return AccessPartie()

    @pytest.fixture
    def blind(self):
        return Monnaie(10)

    @pytest.fixture
    def joueurs(self):
        return [
            MockJoueur(1, "maurice", 50),
            MockJoueur(2, "batricia", 30),
            MockJoueur(3, "miguel", 15),
            MockJoueur(4, "gilbert", 40),
            MockJoueur(5, "junior", 20),
        ]

    def test_rejoindre_table_success(self, partie, blind, joueurs, capfd):
        table = partie.creer_table(nb_sieges=5, blind_initial=blind)

        for joueur in joueurs:
            success = partie.rejoindre_table(joueur)
            assert success is True

            # Vérifie l'affectation
            siege = next((s for s in table.sieges if s.id_joueur == joueur.id_joueur), None)
            assert siege is not None

            jp = JoueurPartie(joueur=joueur, siege=siege, solde_partie=joueur.credit)
            print(
                f"{jp.joueur.pseudo} rejoint une table avec "
                f"{jp.solde_partie.get()} jetons."
            )

        out, _ = capfd.readouterr()
        for joueur in joueurs:
            assert joueur.pseudo in out
        assert "table" in out

    def test_rejoindre_table_fail_when_full(self, partie, blind, capfd):
        table = partie.creer_table(nb_sieges=2, blind_initial=blind)

        joueurs = [
            MockJoueur(10, "alice", 100),
            MockJoueur(11, "bob", 80),
            MockJoueur(12, "charlie", 60),
        ]

        results = []
        for joueur in joueurs:
            success = partie.rejoindre_table(joueur)
            results.append((joueur.pseudo, success))
            if success:
                print(f"{joueur.pseudo} a rejoint la table.")
            else:
                print(f"{joueur.pseudo} n'a pas pu rejoindre la table.")

        out, _ = capfd.readouterr()
        assert results[0][1] is True
        assert results[1][1] is True
        assert results[2][1] is False
        assert "charlie n'a pas pu rejoindre la table." in out
