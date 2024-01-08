from unittest import TestCase, TextTestRunner, TestLoader
from unittest.mock import MagicMock

from service.joueur_service import JoueurService

from dao.joueur_dao import JoueurDao

from dto.joueur import Joueur


class TestJoueurService(TestCase):
    def test_creer_ok(self):
        # GIVEN
        pseudo, mdp, age, mail, fan_pokemon = "jp", "1234", 15, "z@mail.oo", True
        JoueurDao().creer = MagicMock(return_value=True)

        # WHEN
        joueur = JoueurService().creer(pseudo, mdp, age, mail, fan_pokemon)

        # THEN
        self.assertEqual(joueur.pseudo, pseudo)

    def test_creer_echec(self):
        # GIVEN
        pseudo, mdp, age, mail, fan_pokemon = "jp", "1234", 15, "z@mail.oo", True
        JoueurDao().creer = MagicMock(return_value=False)

        # WHEN
        joueur = JoueurService().creer(pseudo, mdp, age, mail, fan_pokemon)

        # THEN
        self.assertIsNone(joueur)

    def test_pseudo_deja_utilise_oui(self):
        # GIVEN
        pseudo = "lea"

        j1 = Joueur(pseudo="jp", age="10", mail=None)
        j2 = Joueur(pseudo="lea", age="10", mail=None)
        j3 = Joueur(pseudo="gg", age="10", mail=None)
        liste_joueurs = [j1, j2, j3]

        JoueurDao().lister_tous = MagicMock(return_value=liste_joueurs)

        # WHEN
        res = JoueurService().pseudo_deja_utilise(pseudo)

        # THEN
        self.assertTrue(res)

    def test_pseudo_deja_utilise_non(self):
        # GIVEN
        pseudo = "chaton"

        j1 = Joueur(pseudo="jp", age="10", mail=None)
        j2 = Joueur(pseudo="lea", age="10", mail=None)
        j3 = Joueur(pseudo="gg", age="10", mail=None)
        liste_joueurs = [j1, j2, j3]

        JoueurDao().lister_tous = MagicMock(return_value=liste_joueurs)

        # WHEN
        res = JoueurService().pseudo_deja_utilise(pseudo)

        # THEN
        self.assertFalse(res)


if __name__ == "__main__":
    # Run the tests
    result = TextTestRunner().run(TestLoader().loadTestsFromTestCase(TestJoueurService))
