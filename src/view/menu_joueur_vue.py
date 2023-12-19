from InquirerPy import prompt

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

    def __init__(self, message="") -> None:
        super().__init__(message)
        self.questions = [
            {
                "type": "list",
                "name": "choix",
                "message": "Faites votre choix",
                "choices": [
                    "Afficher les joueurs de la base de données",
                    "Afficher des pokemons (par appel à un Webservice)",
                    "Se déconnecter",
                ],
            }
        ]

    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur

        Return
        ------
        vue
            Retourne la vue choisi par l'utilisateur dans le terminal
        """
        reponse = prompt(self.questions)

        if reponse["choix"] == "Se déconnecter":
            from view.accueil_vue import AccueilVue

            return AccueilVue()

        elif reponse["choix"] == "Afficher les joueurs de la base de données":
            joueurs_str = JoueurService().afficher_tous()
            return MenuJoueurVue(joueurs_str)

        elif reponse["choix"] == "Afficher des pokemons (par appel à un Webservice)":
            from view.pokemon_vue import PokemonVue

            return PokemonVue()
