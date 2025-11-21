from InquirerPy import inquirer

from src.view.vue_abstraite import VueAbstraite
from src.view.session import Session
from src.view.rejoindre_partie import RejoindrePartie

from src.service.joueur_service import JoueurService


class MenuJoueurVue(VueAbstraite):
    """Vue du menu du joueur

    Attributes
    ----------
    message=''
        str

    Returns
    ------
    view
        retourne la prochaine vue, celle qui est choisie par l'utilisateur
    """

    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur

        Return
        ------
        vue
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nMenu Joueur\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Rejoindre une partie",
                "Gerer son solde",
                "Se déconnecter",
            ],
        ).execute()

        match choix:
            case "Se déconnecter":
                Session().deconnexion()
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Rejoindre une partie":
                return MenuJoueurVue(RejoindrePartie().choisir_menu())

            case "Gerer son solde":
                from view.solde_vue import SoldeVue

                return SoldeVue()
