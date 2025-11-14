from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite
from view.session import Session
from service.table_service import TableService
from business_object.monnaie import Monnaie
from view.menu_partie import MenuPartie
import traceback

class RejoindrePartie(VueAbstraite):
    """Vue pour rejoindre une partie en tant que joueur connecté."""

    def choisir_menu(self):
        try:
            # Récupérer le joueur connecté
            session = Session()
            joueur = session.joueur
            if joueur is None:
                print("Aucun joueur connecté.")
                from view.menu_joueur_vue import MenuJoueurVue
                return MenuJoueurVue()

            # Créer le service de table
            table_service = TableService()

            # Lister les tables disponibles
            try:
                tables_disponibles = table_service.lister_tables_disponibles()
            except Exception as e:
                print("Impossible de récupérer les tables :", e)
                tables_disponibles = []

            print("\n" + "-" * 50 + "\nRejoindre une partie\n" + "-" * 50 + "\n")

            # Construire le menu
            choix_tables = [f"Table {t.id_table}" for t in tables_disponibles]
            choix_tables.append("Créer une nouvelle table")
            choix_tables.append("Retour au menu")

            # Demander le choix à l'utilisateur
            choix = inquirer.select(
                message="Que voulez-vous faire ?",
                choices=choix_tables,
            ).execute()

            # Retour au menu
            if choix == "Retour au menu":
                from view.menu_joueur_vue import MenuJoueurVue
                return MenuJoueurVue()

            # Créer une nouvelle table
            elif choix == "Créer une nouvelle table":
                try:
                    # Voir quels parametres par defaut on met
                    nouvelle_table = table_service.creer_table(nb_sieges=8, blind_initial=Monnaie(10))
                    if nouvelle_table:
                        print(f"Nouvelle table créée ! Table {nouvelle_table.id_table}")
                        tables_disponibles.append(nouvelle_table)  # Ajouter à la liste locale
                        choix = f"Table {nouvelle_table.id_table}"
                        print(f"Vous avez rejoint la Table {nouvelle_table.id_table} !")
                        return MenuPartie(table_choisie).choisir_menu()
                    else:
                        print("Erreur lors de la création de la table.")
                        from view.menu_joueur_vue import MenuJoueurVue
                        return MenuJoueurVue()
                except Exception as e:
                    print("Erreur lors de la création de la table :", e)
                    traceback.print_exc()
                    from view.menu_joueur_vue import MenuJoueurVue
                    return MenuJoueurVue()

            # Rejoindre une table existante
            table_choisie = next((t for t in tables_disponibles if f"Table {t.id_table}" == choix), None)
            if table_choisie is None:
                print("Cette table n'existe pas ou n'est plus disponible.")
            else:
                try:
                    success = table_service.rejoindre_table(joueur, table_choisie.id_table)
                    if success:
                        print(f"Vous avez rejoint la Table {table_choisie.id_table} !")
                        return MenuPartie(table_choisie).choisir_menu()
                    else:
                        print("Impossible de rejoindre cette table, elle est peut-être pleine.")
                except Exception as e:
                    print("Erreur en rejoignant la table :", e)
                    traceback.print_exc()

        except Exception as e:
            print("Une erreur est survenue dans le menu rejoindre partie :")
            traceback.print_exc()

        # Retour au menu joueur
        from view.menu_joueur_vue import MenuJoueurVue
        return MenuJoueurVue()
