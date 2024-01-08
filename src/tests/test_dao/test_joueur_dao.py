import os

from unittest import mock, TestCase, TextTestRunner, TestLoader

from utils.reset_database import ResetDatabase
from utils.securite import hash_password

from dao.joueur_dao import JoueurDao

from dto.joueur import Joueur


@mock.patch.dict(os.environ, {"SCHEMA": "projet_test_dao"})
class TestJoueurDao(TestCase):
    """Tests des méthodes de la classe JoueurDao
    Pour éviter de polluer la base de données, les tests sont effectués
    sur un schéma prévu à cet effet
    """

    def setUpClass():
        """Méthode déclenchée avant tous les tests de la classe"""
        ResetDatabase().lancer(test_dao=True)

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

    def test_lister_tous(self):
        # GIVEN

        # WHEN
        joueurs = JoueurDao().lister_tous()

        # THEN
        self.assertIsInstance(joueurs, list)
        self.assertGreaterEqual(len(joueurs), 2)

    def test_creer_ok(self):
        # GIVEN
        joueur = Joueur(pseudo="gg", age=44, mail="test@test.io")

        # WHEN
        creation_ok = JoueurDao().creer(joueur)

        # THEN
        self.assertTrue(creation_ok)
        self.assertIsNotNone(joueur.id_joueur)

    def test_creer_ko(self):
        # GIVEN
        joueur = Joueur(pseudo="gg", age="chaine de caractere", mail=12)

        # WHEN
        creation_ok = JoueurDao().creer(joueur)

        # THEN
        self.assertFalse(creation_ok)

    def test_modifier_ok(self):
        # GIVEN
        new_mail = "maurice@mail.com"
        joueur = Joueur(id_joueur=997, pseudo="maurice", age=20, mail=new_mail)

        # WHEN
        modification_ok = JoueurDao().modifier(joueur)

        # THEN
        self.assertTrue(modification_ok)

    def test_modifier_ko(self):
        # GIVEN
        joueur = Joueur(id_joueur=8888, pseudo="id inconnu", age=1, mail="no@mail.com")

        # WHEN
        modification_ok = JoueurDao().modifier(joueur)

        # THEN
        self.assertFalse(modification_ok)

    def test_supprimer_ok(self):
        # GIVEN
        joueur = Joueur(id_joueur=995, pseudo="miguel", age=1, mail="miguel@projet.fr")

        # WHEN
        suppression_ok = JoueurDao().supprimer(joueur)

        # THEN
        self.assertTrue(suppression_ok)

    def test_supprimer_ko(self):
        # GIVEN
        joueur = Joueur(id_joueur=8888, pseudo="id inconnu", age=1, mail="no@z.fr")

        # WHEN
        suppression_ok = JoueurDao().supprimer(joueur)

        # THEN
        self.assertFalse(suppression_ok)

    def test_se_connecter_ok(self):
        # GIVEN
        pseudo = "batricia"
        mdp = "9876"

        # WHEN
        joueur = JoueurDao().se_connecter(pseudo, hash_password(mdp, pseudo))

        # THEN
        self.assertIsInstance(joueur, Joueur)

    def test_se_connecter_ko(self):
        # GIVEN
        pseudo = "toto"
        mdp = "poiuytreza"

        # WHEN
        joueur = JoueurDao().se_connecter(pseudo, hash_password(mdp, pseudo))

        # THEN
        self.assertIsNone(joueur)


if __name__ == "__main__":
    # Lancement des tests
    result = TextTestRunner().run(TestLoader().loadTestsFromTestCase(TestJoueurDao))
