import os

import regex
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator, PasswordValidator
from prompt_toolkit.validation import ValidationError, Validator

from service.joueur_service import JoueurService
from business_object.monnaie import Monnaie
from view.vue_abstraite import VueAbstraite

import requests
API_URL = "https://user-arouille-170474-0.user.lab.sspcloud.fr/proxy/9876" #a changer...

class InscriptionVue(VueAbstraite):
    def choisir_menu(self):
        # Demande à l'utilisateur de saisir pseudo, mot de passe...
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()

        VAULT_TOKEN = os.environ.get("VAULT_TOKEN")  # récupère le token depuis ton .env

        headers = {"Authorization": f"Bearer {VAULT_TOKEN}"}

        response = requests.get(f"{API_URL}/joueurs/", headers=headers)

        # Ensuite tu récupères la liste des joueurs
        joueurs = response.json().get("joueurs", [])
        #joueurs = requests.get(f"{API_URL}/joueurs/").json()["joueurs"]
        if pseudo in [j["pseudo"] for j in joueurs]: 
        #if JoueurService().pseudo_deja_utilise(pseudo): #ne plus utiliser les services et passer par l'api...
            from view.accueil.accueil_vue import AccueilVue

            return AccueilVue(f"Le pseudo {pseudo} est déjà utilisé.")

        mdp = inquirer.secret(
            message="Entrez votre mot de passe : ",
            validate=PasswordValidator(
                length=8, #os.environ["PASSWORD_LENGTH"],
                cap=True,
                number=True,
                message="Au moins 8 caractères, incluant une majuscule et un chiffre",
            ),
        ).execute()

        age = int(inquirer.number(
            message="Entrez votre age : ",
            min_allowed=0,
            max_allowed=120,
            validate=EmptyInputValidator(),
        ).execute())

        mail = inquirer.text(message="Entrez votre mail : ", validate=MailValidator()).execute()

        # Appel du service pour créer le joueur
        joueur = JoueurService().creer(pseudo, mdp, mail, age, credit=Monnaie(0))

        # Si le joueur a été créé
        if joueur:
            message = (
                f"Votre compte {joueur.pseudo} a été créé. Vous pouvez maintenant vous connecter."
            )
        else:
            message = "Erreur de connexion (pseudo ou mot de passe invalide)"

        from view.accueil.accueil_vue import AccueilVue

        return AccueilVue(message)


class MailValidator(Validator):
    """La classe MailValidator verifie si la chaine de caractères
    que l'on entre correspond au format de l'email"""

    def validate(self, document) -> None:
        ok = regex.match(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$", document.text)
        if not ok:
            raise ValidationError(
                message="Entrez un mail valide", cursor_position=len(document.text)
            )
