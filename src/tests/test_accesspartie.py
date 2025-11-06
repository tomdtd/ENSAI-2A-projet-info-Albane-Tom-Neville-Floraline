import sqlite3
from src.business_object.accesspartie import AccessPartie
from src.business_object.joueur import Joueur
from src.business_object.joueur_partie import JoueurPartie
from src.business_object.monnaie import Monnaie


def charger_base_test():
    conn = sqlite3.connect(":memory:")
    with open("data/pop_db_test.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()
    conn.executescript(sql_script)
    return conn


def extraire_joueurs(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_joueur, pseudo, age, mail, credit, mdp
        FROM joueur
    """)
    return [
        Joueur(pseudo=pseudo, age=age, mail=mail, credit=credit, mdp=mdp, id_joueur=id_joueur)
        for id_joueur, pseudo, age, mail, credit, mdp in cursor.fetchall()
    ]


def extraire_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_table, nom_table, nb_sieges, blind_initial, nb_joueurs
        FROM table_poker
    """)
    return [
        (id_table, nom_table, nb_sieges, blind_initial, nb_joueurs)
        for id_table, nom_table, nb_sieges, blind_initial, nb_joueurs in cursor.fetchall()
    ]


def test_access_partie_depuis_sql(capfd):
    conn = charger_base_test()
    joueurs = extraire_joueurs(conn)
    tables_info = extraire_tables(conn)

    partie = AccessPartie()

    # Créer les tables
    for id_table, nom_table, nb_sieges, blind, nb_joueurs in tables_info:
        partie.creer_table(nb_sieges, Monnaie(int(blind)))

    # Assigner les joueurs
    for joueur in joueurs:
        success = partie.rejoindre_table(joueur)
        if success:
            # Trouver le siège correspondant
            for table in partie.tables:
                for siege in table.sieges:
                    if siege.id_joueur == joueur.id_joueur:
                        jp = JoueurPartie(joueur=joueur, siege=siege,
                                          solde_partie=int(joueur.credit))
                        print(
                            f"{jp.joueur.pseudo} rejoint une table avec "
                            f"{jp.solde_partie.get()} jetons."
                        )
                break
        else:
            print(f"{joueur.pseudo} n'a pas pu rejoindre une table")

    # Afficher l’état des tables
    for table in partie.tables:
        occupes = sum(1 for s in table.sieges if s.est_occupe())
        print(
            f"Table {table.id_table} - Blind {table.blind_initial.get()} "
            f"- Sièges occupés : {occupes}/{len(table.sieges)}"
        )

    out, _ = capfd.readouterr()
    assert "rejoint une table" in out
    assert "Table" in out
