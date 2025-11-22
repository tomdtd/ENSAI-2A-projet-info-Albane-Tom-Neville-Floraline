from InquirerPy import inquirer
from tabulate import tabulate

from src.view.vue_abstraite import VueAbstraite
from src.view.session import Session
from src.dao.statistiques_dao import StatistiquesDao


class StatistiquesJoueurVue(VueAbstraite):
    """Vue pour afficher les statistiques du joueur connecté."""

    def choisir_menu(self):
        session = Session()
        joueur = session.joueur

        if not joueur:
            print("Aucun joueur connecté.")
            from view.menu_joueur_vue import MenuJoueurVue
            return MenuJoueurVue()

        print("\n" + "-" * 50 + "\nMes Statistiques\n" + "-" * 50 + "\n")

        stats_dao = StatistiquesDao()
        stats = stats_dao.obtenir_stats_joueur(joueur.id_joueur)

        if stats:
            print(f"Pseudo : {stats['pseudo']}")
            print(f"Age : {stats['age']} ans")
            print(f"Credit actuel : {stats['credit_actuel']:.2f}")
            print(f"Date d'inscription : {stats['date_inscription']}")
            print()
            print("--- Performances ---")
            print(f"Parties jouees : {stats['nb_parties_jouees']}")
            print(f"Victoires : {stats['nb_victoires']}")
            print(f"Taux de victoire : {stats['taux_victoire']:.1f}%")
            print(f"Gains totaux : {stats['total_gains']:.2f}")
            print(f"Gain moyen par partie : {stats['gain_moyen_partie']:.2f}")
            print(f"Mise moyenne : {stats['mise_moyenne']:.2f}")
        else:
            print("Impossible de recuperer les statistiques.")

        print()

        choix = inquirer.select(
            message="Que souhaitez-vous consulter ?",
            choices=[
                "Historique des parties",
                "Evolution du credit",
                "Statistiques par table",
                "Retour au menu joueur",
            ],
        ).execute()

        if choix == "Historique des parties":
            self._afficher_historique_parties(joueur.id_joueur, stats_dao)
        elif choix == "Evolution du credit":
            self._afficher_evolution_credit(joueur.id_joueur, stats_dao)
        elif choix == "Statistiques par table":
            self._afficher_stats_par_table(joueur.id_joueur, stats_dao)

        from view.menu_joueur_vue import MenuJoueurVue
        return MenuJoueurVue()

    def _afficher_historique_parties(self, id_joueur: int, stats_dao: StatistiquesDao):
        """Affiche l'historique des dernières parties."""
        print("\n--- Historique des 10 dernieres parties ---\n")
        historique = stats_dao.obtenir_historique_parties_joueur(id_joueur, limite=10)

        if historique:
            table_data = []
            for partie in historique:
                table_data.append([
                    partie.get("id_partie", "N/A"),
                    partie.get("id_table", "N/A"),
                    f"{partie.get('pot_total', 0):.2f}",
                    f"{partie.get('resultat', 0):.2f}",
                    partie.get("statut", "N/A"),
                    str(partie.get("date_debut", "N/A"))[:16]
                ])
            headers = ["Partie", "Table", "Pot", "Resultat", "Statut", "Date"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print("Aucune partie trouvee.")

        input("\nAppuyez sur Entree pour continuer...")

    def _afficher_evolution_credit(self, id_joueur: int, stats_dao: StatistiquesDao):
        """Affiche l'évolution du crédit."""
        print("\n--- Evolution du credit ---\n")
        evolution = stats_dao.obtenir_evolution_credit_joueur(id_joueur)

        if evolution:
            table_data = []
            for trans in evolution:
                montant = trans.get("montant", 0)
                signe = "+" if montant >= 0 else ""
                table_data.append([
                    str(trans.get("date", "N/A"))[:16],
                    f"{signe}{montant}",
                    f"{trans.get('solde_cumule', 0):.2f}"
                ])
            headers = ["Date", "Montant", "Solde cumule"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print("Aucune transaction trouvee.")

        input("\nAppuyez sur Entree pour continuer...")

    def _afficher_stats_par_table(self, id_joueur: int, stats_dao: StatistiquesDao):
        """Affiche les statistiques par table."""
        print("\n--- Statistiques par table ---\n")
        stats_tables = stats_dao.obtenir_statistiques_par_table(id_joueur)

        if stats_tables:
            table_data = []
            for stat in stats_tables:
                table_data.append([
                    stat.get("id_table", "N/A"),
                    stat.get("nb_sieges", "N/A"),
                    f"{stat.get('blind_initial', 0):.2f}",
                    stat.get("nb_parties", 0),
                    stat.get("victoires", 0),
                    f"{stat.get('taux_victoire', 0):.1f}%",
                    f"{stat.get('gain_total', 0):.2f}"
                ])
            headers = ["Table", "Places", "Blind", "Parties", "Victoires", "Taux", "Gains"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print("Aucune statistique par table trouvee.")

        input("\nAppuyez sur Entree pour continuer...")
