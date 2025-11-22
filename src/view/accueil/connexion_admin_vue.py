from InquirerPy import inquirer

from src.view.vue_abstraite import VueAbstraite
from src.view.session import Session
from src.service.admin_service import AdminService


class ConnexionAdminVue(VueAbstraite):
    """Vue de connexion pour les administrateurs."""

    def choisir_menu(self):
        print("\n" + "-" * 50 + "\nConnexion Administrateur\n" + "-" * 50 + "\n")

        nom = inquirer.text(message="Nom administrateur : ").execute()
        mdp = inquirer.secret(message="Mot de passe : ").execute()

        admin_service = AdminService()
        admin = admin_service.verifier_identifiants(nom, mdp)

        if admin:
            # Stocker l'admin dans la session
            session = Session()
            session.admin = admin
            print(f"\nBienvenue {admin.nom} !")

            from view.admin.menu_admin_vue import MenuAdminVue
            return MenuAdminVue()
        else:
            print("\nIdentifiants incorrects.")
            from view.accueil.accueil_vue import AccueilVue
            return AccueilVue("Echec de connexion administrateur.")
