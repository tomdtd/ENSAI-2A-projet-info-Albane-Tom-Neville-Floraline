import pytest
from src.dao.partie_dao import PartieDao
from src.business_object.partie import Partie, JoueurPartie
from src.business_object.pot import Pot
from src.business_object.joueur import Joueur
from src.business_object.siege import Siege
from src.business_object.monnaie import Monnaie

# test/dao/test_partie_dao.py

import unittest
import logging
from datetime import datetime, timedelta

# Assurez-vous que les chemins d'importation sont corrects par rapport à la structure de votre projet
from src.dao.partie_dao import PartieDao
from src.dao.db_connection import DBConnection

from src.business_object.partie import Partie
from src.business_object.joueur_partie import JoueurPartie
from src.business_object.pot import Pot
from src.business_object.joueur import Joueur
from src.business_object.siege import Siege
from src.business_object.monnaie import Monnaie

# Désactiver les logs pendant les tests pour une sortie plus propre, sauf en cas d'erreur
# Vous pouvez commenter cette ligne si vous souhaitez voir les logs de l'application
logging.disable(logging.CRITICAL)


class TestPartieDao(unittest.TestCase):
    """Classe de test pour PartieDao"""

    def setUp(self):
        """
        Met en place l'environnement de test avant chaque test.
        - Crée des joueurs et une table de poker de test directement dans la BDD.
        - Crée deux parties via le DAO pour les tests de lecture, modification, suppression.
        """
        self.partie_dao = PartieDao()
        self.joueur1 = Joueur(
            id_joueur=1001, pseudo="TestPlayer1", mail="test1@example.com", mdp="pass", age=25
        )
        self.joueur2 = Joueur(
            id_joueur=1002, pseudo="TestPlayer2", mail="test2@example.com", mdp="pass", age=30
        )
        self.id_table = 2001

        # Nettoyage initial au cas où un test précédent aurait échoué avant son tearDown
        self.tearDown()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Créer une table de poker de test
                    cursor.execute(
                        "INSERT INTO table_poker (id_table, nom, nb_sieges, blind_initial) VALUES (%(id)s, 'Test Table', 6, 10) ON CONFLICT (id_table) DO NOTHING;",
                        {"id": self.id_table},
                    )
                    # Créer des joueurs de test
                    cursor.execute(
                        "INSERT INTO joueur (id_joueur, pseudo, mail, mdp, age, credit) VALUES (%(id)s, %(pseudo)s, %(mail)s, 'hash', %(age)s, 1000) ON CONFLICT (id_joueur) DO NOTHING;",
                        {
                            "id": self.joueur1.id_joueur,
                            "pseudo": self.joueur1.pseudo,
                            "mail": self.joueur1.mail,
                            "age": self.joueur1.age,
                        },
                    )
                    cursor.execute(
                        "INSERT INTO joueur (id_joueur, pseudo, mail, mdp, age, credit) VALUES (%(id)s, %(pseudo)s, %(mail)s, 'hash', %(age)s, 1000) ON CONFLICT (id_joueur) DO NOTHING;",
                        {
                            "id": self.joueur2.id_joueur,
                            "pseudo": self.joueur2.pseudo,
                            "mail": self.joueur2.mail,
                            "age": self.joueur2.age,
                        },
                    )
                connection.commit()
        except Exception as e:
            self.fail(f"La configuration de la base de données a échoué: {e}")

        # Créer une première partie pour les tests
        joueur_partie1 = JoueurPartie(
            joueur=self.joueur1, siege=Siege(id_siege=1), solde_partie=500
        )
        self.partie1 = Partie(
            joueurs=[joueur_partie1],
            pot=Pot(100),
            id_table=self.id_table,
            date_debut=datetime.now(),
        )
        self.partie_dao.creer(self.partie1)

        # Créer une deuxième partie (terminée) pour les tests de listing
        joueur_partie2 = JoueurPartie(
            joueur=self.joueur2, siege=Siege(id_siege=2), solde_partie=500
        )
        self.partie2 = Partie(
            joueurs=[joueur_partie2],
            pot=Pot(200),
            id_table=self.id_table,
            date_debut=datetime.now() - timedelta(days=1),
        )
        self.partie_dao.creer(self.partie2)
        self.partie2.date_fin = datetime.now()
        self.partie_dao.modifier(self.partie2)

    def tearDown(self):
        """Nettoie la base de données après chaque test."""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM partie_joueur WHERE id_joueur IN (1001, 1002, 1003);")
                    cursor.execute("DELETE FROM partie WHERE id_table = 2001;")
                    cursor.execute("DELETE FROM joueur WHERE id_joueur IN (1001, 1002, 1003);")
                    cursor.execute("DELETE FROM table_poker WHERE id_table = 2001;")
                connection.commit()
        except Exception as e:
            # Ne pas faire échouer le test si le nettoyage échoue, mais l'afficher
            print(f"Avertissement: Le nettoyage a échoué: {e}")

    def test_creer(self):
        """Teste la création d'une nouvelle partie."""
        # Arrange
        joueur3 = Joueur(
            id_joueur=1003, pseudo="TestPlayer3", mail="test3@example.com", mdp="pass", age=40
        )
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO joueur (id_joueur, pseudo, mail, mdp, age, credit) VALUES (%(id)s, %(pseudo)s, %(mail)s, 'hash', %(age)s, 1000) ON CONFLICT (id_joueur) DO NOTHING;",
                    {
                        "id": joueur3.id_joueur,
                        "pseudo": joueur3.pseudo,
                        "mail": joueur3.mail,
                        "age": joueur3.age,
                    },
                )
            connection.commit()
            
        jp = JoueurPartie(joueur=joueur3, siege=Siege(id_siege=3), solde_partie=1000)
        jp.statut = "Actif"
        jp.mise_tour = Monnaie(50)

        nouvelle_partie = Partie(
            joueurs=[jp],
            pot=Pot(50),
            id_table=self.id_table,
            date_debut=datetime.now(),
        )

        # Act
        created = self.partie_dao.creer(nouvelle_partie)

        # Assert
        self.assertTrue(created)
        self.assertIsNotNone(nouvelle_partie.id_partie)

        # Vérifier en base
        partie_trouvee = self.partie_dao.trouver_par_id(nouvelle_partie.id_partie)
        self.assertIsNotNone(partie_trouvee)
        self.assertEqual(len(partie_trouvee.joueurs), 1)
        self.assertEqual(partie_trouvee.joueurs[0].joueur.id_joueur, joueur3.id_joueur)
        self.assertEqual(partie_trouvee.pot.valeur, 50)

    def test_trouver_par_id(self):
        """Teste la recherche d'une partie par son ID."""
        # Arrange
        id_partie_existante = self.partie1.id_partie
        id_partie_inexistante = 99999

        # Act
        partie_trouvee = self.partie_dao.trouver_par_id(id_partie_existante)
        partie_non_trouvee = self.partie_dao.trouver_par_id(id_partie_inexistante)

        # Assert
        self.assertIsNotNone(partie_trouvee)
        self.assertEqual(partie_trouvee.id_partie, id_partie_existante)
        self.assertEqual(len(partie_trouvee.joueurs), 1)
        self.assertEqual(partie_trouvee.joueurs[0].joueur.id_joueur, self.joueur1.id_joueur)
        self.assertIsNone(partie_non_trouvee)

    def test_lister_toutes(self):
        """Teste la récupération de toutes les parties."""
        # Act
        liste_parties = self.partie_dao.lister_toutes()

        # Assert
        self.assertIsInstance(liste_parties, list)
        # On s'attend à trouver les 2 parties créées dans setUp
        self.assertGreaterEqual(len(liste_parties), 2)
        ids_trouves = [p.id_partie for p in liste_parties]
        self.assertIn(self.partie1.id_partie, ids_trouves)
        self.assertIn(self.partie2.id_partie, ids_trouves)

    def test_modifier(self):
        """Teste la modification d'une partie existante."""
        # Arrange
        partie_a_modifier = self.partie_dao.trouver_par_id(self.partie1.id_partie)
        nouveau_pot = 550
        nouvelle_date_fin = datetime.now()
        nouveau_statut_joueur = "Couché"
        
        partie_a_modifier.pot.valeur = nouveau_pot
        partie_a_modifier.date_fin = nouvelle_date_fin
        partie_a_modifier.joueurs[0].statut = nouveau_statut_joueur
        partie_a_modifier.joueurs[0].solde_partie.valeur = 400

        # Act
        success = self.partie_dao.modifier(partie_a_modifier)

        # Assert
        self.assertTrue(success)
        partie_modifiee_db = self.partie_dao.trouver_par_id(self.partie1.id_partie)
        self.assertEqual(partie_modifiee_db.pot.valeur, nouveau_pot)
        self.assertIsNotNone(partie_modifiee_db.date_fin)
        self.assertEqual(partie_modifiee_db.joueurs[0].statut, nouveau_statut_joueur)
        self.assertEqual(partie_modifiee_db.joueurs[0].solde_partie.valeur, 400)

    def test_supprimer(self):
        """Teste la suppression d'une partie."""
        # Arrange
        partie_a_supprimer = self.partie1

        # Act
        success = self.partie_dao.supprimer(partie_a_supprimer)

        # Assert
        self.assertTrue(success)
        partie_supprimee = self.partie_dao.trouver_par_id(partie_a_supprimer.id_partie)
        self.assertIsNone(partie_supprimee)

    def test_lister_par_table(self):
        """Teste la récupération des parties pour une table donnée."""
        # Act
        parties_table = self.partie_dao.lister_par_table(self.id_table)
        parties_table_inexistante = self.partie_dao.lister_par_table(9999)

        # Assert
        self.assertIsInstance(parties_table, list)
        self.assertEqual(len(parties_table), 2)
        self.assertEqual(len(parties_table_inexistante), 0)

    def test_lister_actives(self):
        """Teste la récupération des parties actives (non terminées)."""
        # Act
        parties_actives = self.partie_dao.lister_actives()

        # Assert
        self.assertIsInstance(parties_actives, list)
        # Seule partie1 doit être active
        self.assertEqual(len(parties_actives), 1)
        self.assertEqual(parties_actives[0].id_partie, self.partie1.id_partie)
        self.assertIsNone(parties_actives[0].date_fin)

    def test_trouver_par_joueur(self):
        """Teste la recherche des parties auxquelles un joueur a participé."""
        # Arrange
        # Ajouter joueur1 à partie2 pour qu'il ait participé à 2 parties
        partie2_mod = self.partie_dao.trouver_par_id(self.partie2.id_partie)
        jp_supp = JoueurPartie(joueur=self.joueur1, siege=Siege(id_siege=3), solde_partie=200)
        
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO partie_joueur (id_partie, id_joueur, mise_tour, solde_partie, statut, id_siege) "
                    "VALUES (%(id_partie)s, %(id_joueur)s, 0, 200, 'Terminé', 3)",
                    {
                        "id_partie": partie2_mod.id_partie,
                        "id_joueur": self.joueur1.id_joueur,
                    },
                )
            connection.commit()

        # Act
        parties_joueur1 = self.partie_dao.trouver_par_joueur(self.joueur1.id_joueur)
        parties_joueur2 = self.partie_dao.trouver_par_joueur(self.joueur2.id_joueur)

        # Assert
        self.assertEqual(len(parties_joueur1), 2)
        self.assertEqual(len(parties_joueur2), 1)
        self.assertEqual(parties_joueur2[0].id_partie, self.partie2.id_partie)


if __name__ == "__main__":
    unittest.main()