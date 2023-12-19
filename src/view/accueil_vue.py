from InquirerPy import prompt

from view.vue_abstraite import VueAbstraite
from view.connexion_vue import ConnexionVue
from utils.reset_database import ResetDatabase


class AccueilVue(VueAbstraite):
    """Vue de l'accueil de l'application du Jeu de Rôle.

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
                    "Ré-initialiser la base de données",
                    "Se connecter",
                    "Quitter",
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

        if reponse["choix"] == "Quitter":
            pass
        elif reponse["choix"] == "Se connecter":
            return ConnexionVue()
        elif reponse["choix"] == "Ré-initialiser la base de données":
            succes = ResetDatabase().lancer()
            message = (
                "Ré-initilisation de la base de données terminée" if succes else None
            )
            return AccueilVue(message)
