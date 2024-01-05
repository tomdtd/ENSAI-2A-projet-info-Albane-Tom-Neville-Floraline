import os

from unittest import mock, TestCase, TextTestRunner, TestLoader

from utils.reset_database_test import ResetDatabaseTest
from dao.joueur_dao import JoueurDao


@mock.patch.dict(os.environ, {"SCHEMA": "projet_test_dao"})
class TestJoueurDao(TestCase):
    def setUpClass():
        """Méthode déclenchée avant tous les tests de la classe"""
        ResetDatabaseTest().lancer()

    def test_trouver_par_id_existant(self):
        # GIVEN
        id_joueur = 998

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
    # Lancement des tests
    result = TextTestRunner().run(TestLoader().loadTestsFromTestCase(TestJoueurDao))
