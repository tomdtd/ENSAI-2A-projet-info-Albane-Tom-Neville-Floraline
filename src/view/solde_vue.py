from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from client.poker_client import PokerClient
from view.session import Session
from service.joueur_service import JoueurService
from service.transaction_service import TransactionService
from business_object.monnaie import Monnaie

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
        print(f"Solde actuel : {solde.get():.2f}" if solde is not None else "Solde non disponible")

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
            valeur_solde = solde.get() if solde else 0
            nouveau_solde = valeur_solde + int(montant)
            joueur.credit = Monnaie(nouveau_solde)
            try:
                JoueurService().modifier_credit(joueur.id_joueur, int(joueur.credit.get()))
                TransactionService().enregistrer_transaction(joueur.id_joueur, int(montant))
                print(f"Crédit ajouté avec succès. Nouveau solde : {joueur.credit.get():.2f}")
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

            valeur_solde = solde.get() if solde else 0

            if valeur_solde is None or valeur_solde < int(montant):
                print("Solde insuffisant.")
            else:
                joueur.credit = Monnaie(valeur_solde - int(montant))
                try:
                    JoueurService().modifier_credit(joueur.id_joueur, int(joueur.credit.get()))
                    TransactionService().enregistrer_transaction(joueur.id_joueur, - int(montant))
                    print(f"Crédit retiré avec succès. Nouveau solde : {joueur.credit.get():.2f}")
                except Exception as e:
                    logging.exception(e)
                    print("Erreur lors de la mise à jour du solde.")

            from view.menu_joueur_vue import MenuJoueurVue
            return MenuJoueurVue("Retour du menu solde.")

        else:
            from view.menu_joueur_vue import MenuJoueurVue
            return MenuJoueurVue("Retour du menu solde.")
