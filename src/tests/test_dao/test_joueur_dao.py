from unittest import TestCase, TextTestRunner, TestLoader

from dao.joueur_dao import JoueurDao


class TestAttackDao(TestCase):
    def test_trouver_par_id_existant(self):
        # GIVEN
        id_joueur = 5

        # WHEN
        joueur = JoueurDao().trouver_par_id(id_joueur)

        # THEN
        self.assertIsNotNone(joueur)

    def test_trouver_par_id_non_existant(self):
        # GIVEN
        id_joueur = 9999999999999

        # WHEN
        joueur = JoueurDao().trouver_par_id(id_joueur)

        # THEN
        self.assertIsNone(joueur)


if __name__ == "__main__":
    # Run the tests
    result = TextTestRunner().run(TestLoader().loadTestsFromTestCase(TestAttackDao))
