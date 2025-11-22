from InquirerPy import inquirer
from tabulate import tabulate

from src.view.vue_abstraite import VueAbstraite
from src.view.session import Session
from src.dao.statistiques_dao import StatistiquesDao


class StatistiquesGlobalesVue(VueAbstraite):
    """Vue pour afficher les statistiques globales de la plateforme."""

    def choisir_menu(self):
        session = Session()
        admin = session.admin

        if not admin:
            print("Acces non autorise.")
            from view.accueil.accueil_vue import AccueilVue
            return AccueilVue()

        print("\n" + "-" * 50 + "\nStatistiques Globales\n" + "-" * 50 + "\n")

        stats_dao = StatistiquesDao()

        choix = inquirer.select(
            message="Que souhaitez-vous consulter ?",
            choices=[
                "Vue d'ensemble",
                "Classement des joueurs",
                "Statistiques des parties",
                "Statistiques des mises",
                "Distribution par age",
                "Joueurs les plus actifs",
                "Statistiques par table",
                "Rapport complet",
                "Retour au menu admin",
            ],
        ).execute()

        match choix:
            case "Vue d'ensemble":
                self._afficher_vue_ensemble(stats_dao)

            case "Classement des joueurs":
                self._afficher_classement(stats_dao)

            case "Statistiques des parties":
                self._afficher_stats_parties(stats_dao)

            case "Statistiques des mises":
                self._afficher_stats_mises(stats_dao)

            case "Distribution par age":
                self._afficher_distribution_age(stats_dao)

            case "Joueurs les plus actifs":
                self._afficher_joueurs_actifs(stats_dao)

            case "Statistiques par table":
                self._afficher_stats_tables(stats_dao)

            case "Rapport complet":
                self._afficher_rapport_complet(stats_dao)

            case "Retour au menu admin":
                from view.admin.menu_admin_vue import MenuAdminVue
                return MenuAdminVue()

        from view.admin.statistiques_globales_vue import StatistiquesGlobalesVue
        return StatistiquesGlobalesVue()

    def _afficher_vue_ensemble(self, stats_dao: StatistiquesDao):
        """Affiche une vue d'ensemble des statistiques."""
        print("\n--- Vue d'ensemble de la plateforme ---\n")
        stats = stats_dao.obtenir_stats_globales()

        if stats:
            print(f"Nombre total de joueurs : {stats['nb_joueurs_total']}")
            print(f"Nombre total de parties : {stats['nb_parties_total']}")
            print(f"Nombre de tables actives : {stats['nb_tables_actives']}")
            print(f"Credit total sur la plateforme : {stats['credit_total_plateforme']:.2f}")
            print(f"Credit moyen par joueur : {stats['credit_moyen_joueur']:.2f}")
            print(f"Age moyen des joueurs : {stats['age_moyen_joueurs']:.1f} ans")
        else:
            print("Impossible de recuperer les statistiques.")

        input("\nAppuyez sur Entree pour continuer...")

    def _afficher_classement(self, stats_dao: StatistiquesDao):
        """Affiche le classement des joueurs."""
        print("\n--- Classement des joueurs ---\n")

        critere = inquirer.select(
            message="Classer par :",
            choices=["credit", "victoires", "parties_jouees"],
        ).execute()

        classement = stats_dao.obtenir_classement_joueurs(critere=critere, limite=10)

        if classement:
            table_data = []
            for joueur in classement:
                table_data.append([
                    joueur.get("rang", "N/A"),
                    joueur.get("pseudo", "N/A"),
                    f"{joueur.get('credit', 0):.2f}",
                    joueur.get("nb_parties", 0),
                    joueur.get("nb_victoires", 0),
                    f"{joueur.get('taux_victoire', 0):.1f}%",
                ])
            headers = ["Rang", "Pseudo", "Credit", "Parties", "Victoires", "Taux"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print("Aucun classement disponible.")

        input("\nAppuyez sur Entree pour continuer...")

    def _afficher_stats_parties(self, stats_dao: StatistiquesDao):
        """Affiche les statistiques des parties."""
        print("\n--- Statistiques des parties ---\n")
        stats = stats_dao.obtenir_stats_parties()

        if stats:
            print(f"Nombre total de parties : {stats['nb_parties_total']}")
            print(f"Pot moyen : {stats['pot_moyen']:.2f}")
            print(f"Ecart-type du pot : {stats['ecart_type_pot']:.2f}")
            print(f"Pot median : {stats['mediane_pot']:.2f}")
            print(f"Pot minimum : {stats['pot_min']:.2f}")
            print(f"Pot maximum : {stats['pot_max']:.2f}")
            print(f"Somme totale des pots : {stats['somme_totale_pots']:.2f}")
        else:
            print("Impossible de recuperer les statistiques.")

        input("\nAppuyez sur Entree pour continuer...")

    def _afficher_stats_mises(self, stats_dao: StatistiquesDao):
        """Affiche les statistiques des mises."""
        print("\n--- Statistiques des mises ---\n")
        stats = stats_dao.obtenir_stats_mises()

        if stats:
            print(f"Nombre total de mises : {stats['nb_mises_total']}")
            print(f"Mise moyenne : {stats['mise_moyenne']:.2f}")
            print(f"Ecart-type : {stats['ecart_type_mise']:.2f}")
            print(f"Mise mediane : {stats['mediane_mise']:.2f}")
            print(f"Mise minimum : {stats['mise_min']:.2f}")
            print(f"Mise maximum : {stats['mise_max']:.2f}")
            print(f"Somme totale des mises : {stats['somme_totale_mises']:.2f}")
        else:
            print("Impossible de recuperer les statistiques.")

        input("\nAppuyez sur Entree pour continuer...")

    def _afficher_distribution_age(self, stats_dao: StatistiquesDao):
        """Affiche la distribution des joueurs par âge."""
        print("\n--- Distribution par tranche d'age ---\n")
        distribution = stats_dao.obtenir_distribution_age()

        if distribution:
            table_data = []
            for tranche in distribution:
                table_data.append([
                    tranche.get("tranche_age", "N/A"),
                    tranche.get("nb_joueurs", 0),
                    f"{tranche.get('credit_moyen', 0):.2f}",
                    f"{tranche.get('age_moyen_tranche', 0):.1f}",
                ])
            headers = ["Tranche", "Nb joueurs", "Credit moyen", "Age moyen"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print("Aucune donnee disponible.")

        input("\nAppuyez sur Entree pour continuer...")

    def _afficher_joueurs_actifs(self, stats_dao: StatistiquesDao):
        """Affiche les joueurs les plus actifs."""
        print("\n--- Top 10 des joueurs les plus actifs ---\n")
        joueurs = stats_dao.obtenir_joueurs_plus_actifs(limite=10)

        if joueurs:
            table_data = []
            for i, joueur in enumerate(joueurs, 1):
                derniere = str(joueur.get("derniere_partie", "N/A"))[:16]
                table_data.append([
                    i,
                    joueur.get("pseudo", "N/A"),
                    joueur.get("nb_parties", 0),
                    f"{joueur.get('total_mises', 0):.2f}",
                    f"{joueur.get('mise_moyenne', 0):.2f}",
                    derniere,
                ])
            headers = ["#", "Pseudo", "Parties", "Total mises", "Mise moy.", "Derniere partie"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print("Aucun joueur actif trouve.")

        input("\nAppuyez sur Entree pour continuer...")

    def _afficher_stats_tables(self, stats_dao: StatistiquesDao):
        """Affiche les statistiques par table."""
        print("\n--- Statistiques par table ---\n")
        stats = stats_dao.obtenir_stats_tables()

        if stats:
            table_data = []
            for table in stats:
                table_data.append([
                    table.get("id_table", "N/A"),
                    table.get("nb_sieges", 0),
                    f"{table.get('blind_initial', 0):.2f}",
                    f"{table.get('nb_joueurs_actuels', 0)}/{table.get('nb_sieges', 0)}",
                    f"{table.get('taux_occupation', 0):.1f}%",
                    table.get("nb_parties_jouees", 0),
                    f"{table.get('pot_moyen', 0):.2f}",
                ])
            headers = ["Table", "Places", "Blind", "Occup.", "Taux", "Parties", "Pot moy."]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print("Aucune table trouvee.")

        input("\nAppuyez sur Entree pour continuer...")

    def _afficher_rapport_complet(self, stats_dao: StatistiquesDao):
        """Affiche un rapport complet."""
        print("\n" + "=" * 60)
        print("           RAPPORT COMPLET DE LA PLATEFORME")
        print("=" * 60 + "\n")

        rapport = stats_dao.obtenir_rapport_complet()

        if rapport:
            # Stats globales
            stats_g = rapport.get("stats_globales", {})
            if stats_g:
                print(">>> STATISTIQUES GENERALES")
                print(f"    Joueurs: {stats_g.get('nb_joueurs_total', 0)}")
                print(f"    Parties: {stats_g.get('nb_parties_total', 0)}")
                print(f"    Tables: {stats_g.get('nb_tables_actives', 0)}")
                print(f"    Credit total: {stats_g.get('credit_total_plateforme', 0):.2f}")
                print()

            # Stats parties
            stats_p = rapport.get("stats_parties", {})
            if stats_p:
                print(">>> STATISTIQUES DES PARTIES")
                print(f"    Pot moyen: {stats_p.get('pot_moyen', 0):.2f}")
                print(f"    Pot max: {stats_p.get('pot_max', 0):.2f}")
                print()

            # Taux abandon
            taux = rapport.get("taux_abandon", {})
            if taux:
                print(">>> TAUX D'ABANDON")
                print(f"    Taux abandon: {taux.get('taux_abandon', 0):.1f}%")
                print(f"    Taux victoire global: {taux.get('taux_victoire_global', 0):.1f}%")
                print()

            # Top joueurs
            top = rapport.get("top_10_joueurs", [])
            if top:
                print(">>> TOP 3 JOUEURS (par credit)")
                for i, j in enumerate(top[:3], 1):
                    print(f"    {i}. {j.get('pseudo', 'N/A')} - {j.get('credit', 0):.2f}")
                print()

        else:
            print("Impossible de generer le rapport.")

        input("\nAppuyez sur Entree pour continuer...")
