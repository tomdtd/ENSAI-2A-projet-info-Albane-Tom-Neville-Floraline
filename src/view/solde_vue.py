from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from client.poker_client import PokerClient
from view.session import Session
from service.joueur_service import JoueurService

class SoldeVue(VueAbstraite):
    """Vue pour consulter et gérer le solde du joueur connecté."""

    def choisir_menu(self):
        session = Session()
        joueur = session.joueur

        if not joueur:
            print("Aucun joueur connecté. Retour au menu principal.")
            from view.menu_joueur_vue import MenuJoueurVue
            return MenuJoueurVue("Aucun joueur connecté.")

        solde = getattr(joueur, "credit", getattr(joueur, "solde", None))
        print("\n" + "-" * 50 + "\nGestion du solde\n" + "-" * 50 + "\n")
        print(f"Pseudo : {joueur.pseudo}")
        print(f"Solde actuel : {solde:.2f}" if solde is not None else "Solde non disponible")

        choix = inquirer.select(
            message="Que souhaitez-vous faire ?",
            choices=[
                "Ajouter des crédits",
                "Retirer des crédits",
                "Retour au menu joueur",
            ],
        ).execute()

        if choix == "Ajouter des crédits":
            montant = inquirer.number(
                message="Montant à ajouter :",
                min_allowed=0,
            ).execute()

            joueur.credit = (solde or 0) + float(montant)
            try:
                JoueurService().modifier(joueur)
                print(f"Crédit ajouté avec succès. Nouveau solde : {joueur.credit:.2f}")
            except Exception as e:
                logging.exception(e)
                print("Erreur lors de la mise à jour du solde.")

            from view.menu_joueur_vue import MenuJoueurVue
            return MenuJoueurVue("Retour du menu solde.")

        elif choix == "Retirer des crédits":
            montant = inquirer.number(
                message="Montant à retirer : ",
                min_allowed=0,
            ).execute()

            if solde is None or solde < float(montant):
                print("Solde insuffisant.")
            else:
                joueur.credit = solde - float(montant)
                try:
                    JoueurService().modifier(joueur)
                    print(f"Crédit retiré avec succès. Nouveau solde : {joueur.credit:.2f}")
                except Exception as e:
                    logging.exception(e)
                    print("Erreur lors de la mise à jour du solde.")

            from view.menu_joueur_vue import MenuJoueurVue
            return MenuJoueurVue("Retour du menu solde.")

        else:
            from view.menu_joueur_vue import MenuJoueurVue
            return MenuJoueurVue("Retour du menu solde.")
