from InquirerPy import inquirer
from tabulate import tabulate

from src.view.vue_abstraite import VueAbstraite
from src.view.session import Session
from src.service.admin_service import AdminService
from src.service.joueur_service import JoueurService


class GestionJoueursVue(VueAbstraite):
    """Vue pour la gestion des joueurs et des bannissements."""

    def choisir_menu(self):
        session = Session()
        admin = session.admin

        if not admin:
            print("Acces non autorise.")
            from view.accueil.accueil_vue import AccueilVue
            return AccueilVue()

        print("\n" + "-" * 50 + "\nGestion des Joueurs\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Que souhaitez-vous faire ?",
            choices=[
                "Voir tous les joueurs",
                "Voir les joueurs bannis",
                "Bannir un joueur",
                "Debannir un joueur",
                "Consulter les stats d'un joueur",
                "Retour au menu admin",
            ],
        ).execute()

        admin_service = AdminService()
        joueur_service = JoueurService()

        match choix:
            case "Voir tous les joueurs":
                self._afficher_tous_joueurs(joueur_service)

            case "Voir les joueurs bannis":
                self._afficher_joueurs_bannis(admin_service)

            case "Bannir un joueur":
                self._bannir_joueur(admin_service, joueur_service, admin.admin_id)

            case "Debannir un joueur":
                self._debannir_joueur(admin_service)

            case "Consulter les stats d'un joueur":
                self._consulter_stats_joueur(admin_service, joueur_service)

            case "Retour au menu admin":
                from view.admin.menu_admin_vue import MenuAdminVue
                return MenuAdminVue()

        from view.admin.gestion_joueurs_vue import GestionJoueursVue
        return GestionJoueursVue()

    def _afficher_tous_joueurs(self, joueur_service: JoueurService):
        """Affiche la liste de tous les joueurs."""
        print("\n--- Liste des joueurs ---\n")
        joueurs = joueur_service.lister_tous()

        if joueurs:
            table_data = []
            for joueur in joueurs:
                table_data.append([
                    joueur.id_joueur,
                    joueur.pseudo,
                    joueur.mail,
                    joueur.age,
                    f"{joueur.credit.get() if hasattr(joueur.credit, 'get') else joueur.credit:.2f}",
                ])
            headers = ["ID", "Pseudo", "Email", "Age", "Credit"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print("Aucun joueur trouve.")

        input("\nAppuyez sur Entree pour continuer...")

    def _afficher_joueurs_bannis(self, admin_service: AdminService):
        """Affiche la liste des joueurs bannis."""
        print("\n--- Joueurs bannis ---\n")
        bannis = admin_service.lister_joueurs_banis()

        if bannis:
            table_data = []
            for ban in bannis:
                date_fin = ban.get("date_fin_ban")
                fin_str = str(date_fin)[:16] if date_fin else "Permanent"
                table_data.append([
                    ban.get("id_ban", "N/A"),
                    ban.get("id_joueur", "N/A"),
                    ban.get("pseudo", "N/A"),
                    ban.get("raison_ban", "N/A")[:30],
                    str(ban.get("date_ban", "N/A"))[:16],
                    fin_str,
                ])
            headers = ["ID Ban", "ID Joueur", "Pseudo", "Raison", "Date ban", "Fin"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print("Aucun joueur banni.")

        input("\nAppuyez sur Entree pour continuer...")

    def _bannir_joueur(self, admin_service: AdminService, joueur_service: JoueurService, admin_id: int):
        """Bannit un joueur."""
        print("\n--- Bannir un joueur ---\n")

        # Afficher la liste des joueurs
        joueurs = joueur_service.lister_tous()
        if not joueurs:
            print("Aucun joueur a bannir.")
            input("\nAppuyez sur Entree pour continuer...")
            return

        table_data = [[j.id_joueur, j.pseudo, j.mail] for j in joueurs]
        headers = ["ID", "Pseudo", "Email"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()

        id_joueur_str = inquirer.text(
            message="ID du joueur a bannir (ou 'annuler') : "
        ).execute()

        if id_joueur_str.lower() == "annuler":
            return

        try:
            id_joueur = int(id_joueur_str)

            # Vérifier que le joueur existe
            joueur = joueur_service.trouver_par_id(id_joueur)
            if not joueur:
                print("Joueur non trouve.")
                input("\nAppuyez sur Entree pour continuer...")
                return

            raison = inquirer.text(
                message=f"Raison du bannissement de {joueur.pseudo} : "
            ).execute()

            if not raison.strip():
                print("La raison ne peut pas etre vide.")
                input("\nAppuyez sur Entree pour continuer...")
                return

            confirmation = inquirer.confirm(
                message=f"Confirmer le bannissement de {joueur.pseudo} ?",
                default=False
            ).execute()

            if confirmation:
                succes = admin_service.banir_joueur(id_joueur, admin_id, raison)
                if succes:
                    print(f"Le joueur {joueur.pseudo} a ete banni.")
                else:
                    print("Erreur lors du bannissement.")
            else:
                print("Bannissement annule.")

        except ValueError:
            print("ID invalide.")

        input("\nAppuyez sur Entree pour continuer...")

    def _debannir_joueur(self, admin_service: AdminService):
        """Débannit un joueur."""
        print("\n--- Debannir un joueur ---\n")

        bannis = admin_service.lister_joueurs_banis()
        if not bannis:
            print("Aucun joueur banni.")
            input("\nAppuyez sur Entree pour continuer...")
            return

        # Afficher les joueurs bannis
        table_data = []
        for ban in bannis:
            table_data.append([
                ban.get("id_joueur", "N/A"),
                ban.get("pseudo", "N/A"),
                ban.get("raison_ban", "N/A")[:40],
            ])
        headers = ["ID Joueur", "Pseudo", "Raison"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()

        id_joueur_str = inquirer.text(
            message="ID du joueur a debannir (ou 'annuler') : "
        ).execute()

        if id_joueur_str.lower() == "annuler":
            return

        try:
            id_joueur = int(id_joueur_str)

            confirmation = inquirer.confirm(
                message=f"Confirmer le debannissement du joueur {id_joueur} ?",
                default=False
            ).execute()

            if confirmation:
                succes = admin_service.debannir_joueur(id_joueur)
                if succes:
                    print(f"Le joueur {id_joueur} a ete debanni.")
                else:
                    print("Erreur lors du debannissement.")
            else:
                print("Debannissement annule.")

        except ValueError:
            print("ID invalide.")

        input("\nAppuyez sur Entree pour continuer...")

    def _consulter_stats_joueur(self, admin_service: AdminService, joueur_service: JoueurService):
        """Consulte les statistiques d'un joueur spécifique."""
        print("\n--- Consulter les stats d'un joueur ---\n")

        # Afficher la liste des joueurs
        joueurs = joueur_service.lister_tous()
        if joueurs:
            table_data = [[j.id_joueur, j.pseudo] for j in joueurs]
            headers = ["ID", "Pseudo"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            print()

        id_joueur_str = inquirer.text(
            message="ID du joueur (ou 'annuler') : "
        ).execute()

        if id_joueur_str.lower() == "annuler":
            return

        try:
            id_joueur = int(id_joueur_str)
            stats = admin_service.obtenir_statistiques_joueur(id_joueur)

            if stats:
                print(f"\n--- Statistiques de {stats.get('pseudo', 'N/A')} ---\n")
                print(f"Age : {stats.get('age', 'N/A')} ans")
                print(f"Credit actuel : {stats.get('credit_actuel', 0):.2f}")
                print(f"Parties jouees : {stats.get('nb_parties_jouees', 0)}")
                print(f"Victoires : {stats.get('nb_victoires', 0)}")
                print(f"Taux de victoire : {stats.get('taux_victoire', 0):.1f}%")
                print(f"Gains totaux : {stats.get('total_gains', 0):.2f}")
                print(f"Gain moyen : {stats.get('gain_moyen_partie', 0):.2f}")
                print(f"Mise moyenne : {stats.get('mise_moyenne', 0):.2f}")
                print(f"Inscrit depuis : {stats.get('date_inscription', 'N/A')}")
            else:
                print("Impossible de recuperer les statistiques.")

        except ValueError:
            print("ID invalide.")

        input("\nAppuyez sur Entree pour continuer...")
