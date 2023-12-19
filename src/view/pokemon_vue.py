from InquirerPy import prompt

from view.vue_abstraite import VueAbstraite
from client.pokemon_client import PokemonClient


class PokemonVue(VueAbstraite):
    def __init__(self, message="") -> None:
        super().__init__(message)

    def choisir_menu(self):
        pokemon_client = PokemonClient()

        pokemon_types = pokemon_client.get_pokemon_types()
        pokemon_types.append("Retour au Menu Joueur")

        self.questions = [
            {
                "type": "list",
                "name": "choix",
                "message": "Choisissez un type de Pokemon",
                "choices": pokemon_types,
            }
        ]

        reponse = prompt(self.questions)

        if reponse["choix"] == "Retour au Menu Joueur":
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        else:
            from view.menu_joueur_vue import MenuJoueurVue

            pokemons = pokemon_client.get_all_pokemon_by_types(reponse["choix"])
            return MenuJoueurVue(pokemons)
