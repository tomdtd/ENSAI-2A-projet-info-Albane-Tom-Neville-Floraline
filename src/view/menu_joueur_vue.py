from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from service.joueur_service import JoueurService


class MenuJoueurVue(VueAbstraite):
    """Vue du menu du joueur

    Attributes
    ----------
    message=''
        str

    Returns
    ------
    view
        retourne la prochaine vue, celle qui est choisi par l'utilisateur de l'application
    """

    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur

        Return
        ------
        vue
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Afficher les joueurs de la base de données",
                "Afficher des pokemons (par appel à un Webservice)",
                "Se déconnecter",
            ],
        ).execute()

        match choix:
            case "Se déconnecter":
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Afficher les joueurs de la base de données":
                joueurs_str = JoueurService().afficher_tous()
                return MenuJoueurVue(joueurs_str)

            case "Afficher des pokemons (par appel à un Webservice)":
                from view.pokemon_vue import PokemonVue

                return PokemonVue()
