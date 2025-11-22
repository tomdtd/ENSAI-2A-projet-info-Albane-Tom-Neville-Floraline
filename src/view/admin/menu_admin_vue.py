from InquirerPy import inquirer

from src.view.vue_abstraite import VueAbstraite
from src.view.session import Session


class MenuAdminVue(VueAbstraite):
    """Vue du menu principal administrateur."""

    def choisir_menu(self):
        session = Session()
        admin = session.admin

        if not admin:
            print("Aucun administrateur connecte.")
            from view.accueil.accueil_vue import AccueilVue
            return AccueilVue()

        print("\n" + "-" * 50 + f"\nMenu Administrateur - {admin.nom}\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Que souhaitez-vous faire ?",
            choices=[
                "Gerer les transactions",
                "Voir les statistiques globales",
                "Gerer les joueurs (bannissement)",
                "Se deconnecter",
            ],
        ).execute()

        match choix:
            case "Gerer les transactions":
                from view.admin.gestion_transactions_vue import GestionTransactionsVue
                return GestionTransactionsVue()

            case "Voir les statistiques globales":
                from view.admin.statistiques_globales_vue import StatistiquesGlobalesVue
                return StatistiquesGlobalesVue()

            case "Gerer les joueurs (bannissement)":
                from view.admin.gestion_joueurs_vue import GestionJoueursVue
                return GestionJoueursVue()

            case "Se deconnecter":
                session.deconnexion_admin()
                print("Deconnexion reussie.")
                from view.accueil.accueil_vue import AccueilVue
                return AccueilVue()
