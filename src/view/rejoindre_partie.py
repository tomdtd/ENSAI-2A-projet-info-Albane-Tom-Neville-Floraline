from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite
from view.session import Session
from service.table_service import TableService

class RejoindrePartie(VueAbstraite):
    """Vue pour rejoindre une partie en tant que joueur connecté."""

    def choisir_menu(self):
        session = Session()
        joueur = session.joueur


        table_service = TableService()
        tables_disponibles = table_service.lister_tables_disponibles()

        print("\n" + "-" * 50 + "\nRejoindre une partie\n" + "-" * 50 + "\n")

        choix_tables = [f"Table {t.id_table}" for t in tables_disponibles]
        choix_tables.append("Créer une nouvelle table")
        choix_tables.append("Retour au menu")

        choix = inquirer.select(
            message="Que voulez-vous faire ?",
            choices=choix_tables,
        ).execute()

        if choix_table == "Retour au menu":
            from view.menu_joueur_vue import MenuJoueurVue
            return MenuJoueurVue()
        
        elif choix == "Créer une nouvelle table":
            # Crée une nouvelle table via le service
            nouvelle_table = table_service.creer_table(joueur)
            if nouvelle_table:
                print(f"Nouvelle table créée ! Table {nouvelle_table.id_table}")
            else:
                print("Erreur lors de la création de la table.")

        else:        
            table_choisie = next(t for t in tables_disponibles if f"Table {t.id_table}" == choix_table)
            success = table_service.rejoindre_table(joueur, table_choisie.id_table)

            if success:
                print(f"Vous avez rejoint la Table {table_choisie.id_table} !")
            else:
                print("Impossible de rejoindre cette table, elle est peut-être pleine.") #mettre une condition du nb tables

        from view.menu_joueur_vue import MenuJoueurVue
        return MenuJoueurVue()
