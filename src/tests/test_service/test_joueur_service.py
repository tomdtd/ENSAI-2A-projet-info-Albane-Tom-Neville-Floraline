from unittest import TestCase, TextTestRunner, TestLoader
from unittest.mock import MagicMock

from service.joueur_service import JoueurService
from dao.joueur_dao import JoueurDao


class TestJoueurService(TestCase):
    def test_creation_ok(self):
        # GIVEN
        pseudo, mdp, age, mail, fan_pokemon = "jp", "1234", 15, "z@mail.oo", True
        JoueurDao().creer = MagicMock(return_value=True)

        # WHEN
        joueur = JoueurService().creer(pseudo, mdp, age, mail, fan_pokemon)

        # THEN
        self.assertEqual(joueur.pseudo, pseudo)

    def test_creation_echec(self):
        # GIVEN
        pseudo, mdp, age, mail, fan_pokemon = "jp", "1234", 15, "z@mail.oo", True
        JoueurDao().creer = MagicMock(return_value=False)

        # WHEN
        joueur = JoueurService().creer(pseudo, mdp, age, mail, fan_pokemon)

        # THEN
        self.assertIsNone(joueur)


if __name__ == "__main__":
    # Run the tests
    result = TextTestRunner().run(TestLoader().loadTestsFromTestCase(TestJoueurService))
