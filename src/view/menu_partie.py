from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite
from view.session import Session
from service.joueur_partie_service import JoueurPartieService
from service.table_service import TableService
from business_object.siege import Siege
import time

class MenuPartie(VueAbstraite):

    def __init__(self, table):
        self.table = table
        self.solde_initial_partie = self.table.blind_initial.get()

    def choisir_menu(self):
        session = Session()
        joueur = session.joueur

        if self.table.nb_joueurs >= self.table.nb_sieges:
            print("La table est pleine !")
            from view.rejoindre_partie import RejoindrePartie
            return RejoindrePartie().choisir_menu()
        
        siege_libre = Siege(self.table.nb_joueurs + 1) # faire en sorte de modifier nb_joueurs avant pour ne pas mettre 0 a tout le monde...
        siege_libre.est_occupe()
        
        joueur_partie_service = JoueurPartieService()
        joueur_partie = joueur_partie_service.ajouter_joueur_a_partie(joueur, siege_libre, self.solde_initial_partie, self.table.id_table)

        if joueur_partie:
            print(f"{joueur.pseudo} a été ajouté à la table {self.table.id_table} sur le siège {siege_libre.id_siege}.")
            table_service = TableService()
            table_service.ajouter_joueur_table(self.table.id_table)

        else:
            print("Impossible d'ajouter le joueur à la partie.")
            from view.rejoindre_partie import RejoindrePartie
            return RejoindrePartie().choisir_menu()
        

        liste_joueurs_dans_partie = joueur_partie_service.lister_joueurs_selon_table(self.table.id_table)

        print(f"Joueurs présents : {liste_joueurs_dans_partie}")

        num_tour_joueur = 0

        quitter_partie = False
        while not quitter_partie:
            if num_tour_joueur >= len(liste_joueurs_dans_partie):
                num_tour_joueur = 0
            id_tour_joueur = liste_joueurs_dans_partie[num_tour_joueur]
            num_tour_joueur += 1

            TableService().set_id_joueur_tour(self.table.id_table, id_tour_joueur)

            while not TableService().get_id_joueur_tour(self.table.id_table, id_tour_joueur) == joueur.id_joueur: 
                print("En attente du tour des autres joueurs...")
                time.sleep(2) 
                # peut etre mettre un break ou autre pour quitter la partie
            
            print("C'est ton tour")
            liste_joueurs = joueur_partie_service.lister_joueurs_selon_table(self.table.id_table)
            print(f"Joueurs présents : {[j['pseudo'] for j in liste_joueurs]}")
            print(f"Votre credit actuel : {joueur.credit}")

            #trouver un moyen de monter les cartes le flop si besoin ect

            action = inquirer.select(
                message="Que voulez-vous faire ?",
                choices=[
                    "Miser",
                    "Se coucher",
                    "Quitter la partie"
                ],
            ).execute()

            if action == "Miser":
                pass # a voir
                # montant = int(inquirer.text(message="Montant à miser : ").execute())
                # try:
                #     self.joueur_partie_service.miser(joueur.id_joueur, montant)
                #     print(f"{joueur.pseudo} a misé {montant}.")
                # except ValueError as e:
                #     print(e)
            
            elif action == "Se coucher":
                pass # a voir
                # try:
                #     self.joueur_partie_service.se_coucher(joueur.id_joueur)
                #     print(f"{joueur.pseudo} s'est couché.")
                # except ValueError as e:
                #     print(e)
            
            elif action == "Quitter la partie":
                quitter_partie = True

        #faire quitter la partie au joueur
        # trouver un moyen de retirer le nb de joueurs dans la table table_poker -1
        #penser a retirer le joueur de joueur partie à la fin
        joueur_partie_service.retirer_joueur_de_partie(joueur.id_joueur)
        print(f"{joueur.pseudo} a quitté la partie.")

        from view.menu_joueur_vue import MenuJoueurVue
        return MenuJoueurVue()
