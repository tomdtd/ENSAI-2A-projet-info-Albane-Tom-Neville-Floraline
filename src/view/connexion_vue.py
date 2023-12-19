from InquirerPy import prompt

from view.vue_abstraite import VueAbstraite
from service.joueur_service import JoueurService


class ConnexionVue(VueAbstraite):
    def __init__(self, message=""):
        super().__init__(message)
        self.questions = [
            {"type": "input", "name": "pseudo", "message": "Entrez votre pseudo :"},
            {"type": "input", "name": "mdp", "message": "Entrez votre mot de passe :"},
        ]

    def afficher(self):
        self.nettoyer_console()
        print("Connexion à l'application")
        print()

    def choisir_menu(self):
        answers = prompt(self.questions)

        # On appelle le service pour trouver le joueur
        joueur = JoueurService().se_connecter(answers["pseudo"], answers["mdp"])

        message = ""

        if joueur:
            message = f"Vous êtes connecté sous le pseudo {joueur.pseudo}"
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue(message)

        else:
            message = "erreur de connexion"
            from view.accueil_vue import AccueilVue

            return AccueilVue(message)
