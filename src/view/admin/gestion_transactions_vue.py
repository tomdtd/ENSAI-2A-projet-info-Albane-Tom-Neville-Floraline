from InquirerPy import inquirer
from tabulate import tabulate

from src.view.vue_abstraite import VueAbstraite
from src.view.session import Session
from src.service.admin_service import AdminService
from src.service.joueur_service import JoueurService


class GestionTransactionsVue(VueAbstraite):
    """Vue pour la gestion des transactions par l'administrateur."""

    def choisir_menu(self):
        session = Session()
        admin = session.admin

        if not admin:
            print("Acces non autorise.")
            from view.accueil.accueil_vue import AccueilVue
            return AccueilVue()

        print("\n" + "-" * 50 + "\nGestion des Transactions\n" + "-" * 50 + "\n")

        admin_service = AdminService()

        choix = inquirer.select(
            message="Que souhaitez-vous faire ?",
            choices=[
                "Voir les transactions en attente",
                "Voir toutes les transactions",
                "Valider une transaction",
                "Rejeter une transaction",
                "Retour au menu admin",
            ],
        ).execute()

        match choix:
            case "Voir les transactions en attente":
                self._afficher_transactions_en_attente(admin_service)

            case "Voir toutes les transactions":
                self._afficher_toutes_transactions(admin_service)

            case "Valider une transaction":
                self._valider_transaction(admin_service, admin.admin_id)

            case "Rejeter une transaction":
                self._rejeter_transaction(admin_service, admin.admin_id)

            case "Retour au menu admin":
                from view.admin.menu_admin_vue import MenuAdminVue
                return MenuAdminVue()

        from view.admin.gestion_transactions_vue import GestionTransactionsVue
        return GestionTransactionsVue()

    def _afficher_transactions_en_attente(self, admin_service: AdminService):
        """Affiche les transactions en attente de validation."""
        print("\n--- Transactions en attente ---\n")
        transactions = admin_service.lister_transactions_en_attente()

        if transactions:
            self._afficher_tableau_transactions(transactions)
        else:
            print("Aucune transaction en attente.")

        input("\nAppuyez sur Entree pour continuer...")

    def _afficher_toutes_transactions(self, admin_service: AdminService):
        """Affiche toutes les transactions."""
        print("\n--- Toutes les transactions ---\n")

        filtre = inquirer.select(
            message="Filtrer par statut ?",
            choices=["Toutes", "en_attente", "validee", "rejetee"],
        ).execute()

        statut = None if filtre == "Toutes" else filtre
        transactions = admin_service.lister_toutes_transactions(statut)

        if transactions:
            self._afficher_tableau_transactions(transactions)
        else:
            print("Aucune transaction trouvee.")

        input("\nAppuyez sur Entree pour continuer...")

    def _afficher_tableau_transactions(self, transactions: list):
        """Affiche un tableau de transactions."""
        joueur_service = JoueurService()
        table_data = []

        for trans in transactions:
            joueur = joueur_service.trouver_par_id(trans.get("id_joueur"))
            pseudo = joueur.pseudo if joueur else "Inconnu"
            montant = trans.get("solde", 0)
            signe = "+" if montant >= 0 else ""

            table_data.append([
                trans.get("id_transaction", "N/A"),
                pseudo,
                f"{signe}{montant}",
                trans.get("statut", "N/A"),
                str(trans.get("date", "N/A"))[:16],
            ])

        headers = ["ID", "Joueur", "Montant", "Statut", "Date"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def _valider_transaction(self, admin_service: AdminService, admin_id: int):
        """Valide une transaction."""
        transactions = admin_service.lister_transactions_en_attente()

        if not transactions:
            print("Aucune transaction en attente a valider.")
            input("\nAppuyez sur Entree pour continuer...")
            return

        self._afficher_tableau_transactions(transactions)

        id_trans = inquirer.text(
            message="ID de la transaction a valider (ou 'annuler') : "
        ).execute()

        if id_trans.lower() == "annuler":
            return

        try:
            id_transaction = int(id_trans)
            succes = admin_service.valider_transaction(id_transaction, admin_id)
            if succes:
                print(f"Transaction {id_transaction} validee avec succes.")
            else:
                print("Erreur lors de la validation.")
        except ValueError:
            print("ID invalide.")

        input("\nAppuyez sur Entree pour continuer...")

    def _rejeter_transaction(self, admin_service: AdminService, admin_id: int):
        """Rejette une transaction."""
        transactions = admin_service.lister_transactions_en_attente()

        if not transactions:
            print("Aucune transaction en attente a rejeter.")
            input("\nAppuyez sur Entree pour continuer...")
            return

        self._afficher_tableau_transactions(transactions)

        id_trans = inquirer.text(
            message="ID de la transaction a rejeter (ou 'annuler') : "
        ).execute()

        if id_trans.lower() == "annuler":
            return

        try:
            id_transaction = int(id_trans)
            succes = admin_service.rejeter_transaction(id_transaction, admin_id)
            if succes:
                print(f"Transaction {id_transaction} rejetee.")
            else:
                print("Erreur lors du rejet.")
        except ValueError:
            print("ID invalide.")

        input("\nAppuyez sur Entree pour continuer...")
