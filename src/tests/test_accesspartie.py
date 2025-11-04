import pytest
import sqlite3
from src.business_object.accesspartie import AccessPartie
from src.business_object.table import Table
from src.business_object.joueur import Joueur
from src.business_object.monnaie import Monnaie


def charger_base_test():
    conn = sqlite3.connect(":memory:")
    with open("data/pop_db.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()
    conn.executescript(sql_script)
    return conn


def extraire_joueurs(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, pseudo, 30 AS age, 'mail@example.com' AS mail, credit, 'hash_placeholder' AS mdp FROM utilisateur")
    return [
        Joueur(pseudo=pseudo, age=age, mail=mail, credit=credit, mdp=mdp, id_joueur=rowid)
        for rowid, pseudo, age, mail, credit, mdp in cursor.fetchall()
    ]


def extraire_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT nb_sieges, blind_initial FROM table_poker")
    return [(nb_sieges, blind_initial) for nb_sieges, blind_initial in cursor.fetchall()]


def test_access_partie_depuis_sql():
    conn = charger_base_test()
    joueurs = extraire_joueurs(conn)
    tables_info = extraire_tables(conn)

    partie = AccessPartie()

    # Créer les tables
    for nb_sieges, blind in tables_info:
        partie.creer_table(nb_sieges, Monnaie(blind))

    # Assigner les joueurs
    for joueur in joueurs:
        success = partie.rejoindre_table(joueur)
        print(f"{joueur.pseudo} rejoint une table : {'✔️' if success else '❌'}")

    # Afficher l’état des tables
    for table in partie.tables:
        occupes = sum(1 for s in table.sieges if s.est_occupe())
        print(f"Table {table.id_table} - Blind {table.blind_initial} - Sièges occupés : {occupes}/{len(table.sieges)}")


if __name__ == "__main__":
    test_access_partie_depuis_sql()
