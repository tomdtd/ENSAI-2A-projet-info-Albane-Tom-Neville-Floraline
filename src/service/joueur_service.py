from tabulate import tabulate

from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao


class JoueurService:
    def creer(self, pseudo, mdp, age, mail, fan_pokemon) -> Joueur:
        """Service de création d'un joueur"""

        nouveau_joueur = Joueur(pseudo, mdp, age, mail, fan_pokemon)
        JoueurDao().creer(nouveau_joueur)

        return nouveau_joueur

    def lister_tous(self) -> list[Joueur]:
        """Lister tous les joueurs"""
        return JoueurDao().lister_tous()

    def trouver_par_id(self, id_joueur) -> Joueur:
        """Trouver un joueur à partir de son id"""
        return JoueurDao().trouver_par_id(id_joueur)

    def supprimer(self, joueur) -> bool:
        """Supprimer le compte d'un joueur"""
        return JoueurDao().supprimer(joueur)

    def afficher_tous(self) -> str:
        entetes = ["pseudo", "age", "mail", "est fan de Pokemon"]

        joueurs = JoueurDao().lister_tous()
        joueurs_as_list = [j.as_list() for j in joueurs]

        str_joueurs = "-" * 100
        str_joueurs += "\nListe des joueurs \n"
        str_joueurs += "-" * 100
        str_joueurs += "\n"
        str_joueurs += tabulate(
            tabular_data=joueurs_as_list,
            headers=entetes,
            tablefmt="psql",
            floatfmt=".2f",
        )
        str_joueurs += "\n"

        print(str_joueurs)

        return str_joueurs

    def se_connecter(self, pseudo, mdp) -> Joueur:
        """Se connecter à partir de pseudo et mdp"""
        joueur = JoueurDao().se_connecter(pseudo, mdp)
        if not joueur:
            print(f"Connexion {pseudo} refusée")
        else:
            print(f"Joueur {joueur.pseudo} connecté")
        print("*" * 100)
        return joueur
