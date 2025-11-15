from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite
from view.session import Session
from service.joueur_partie_service import JoueurPartieService
from service.table_service import TableService
from service.joueur_service import JoueurService
from business_object.siege import Siege
from business_object.croupier import Croupier
from business_object.liste_cartes import ListeCartes
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
        
        joueurs_obj = [JoueurService().trouver_par_id(id_joueur) for id_joueur in liste_joueurs_dans_partie]
        print(f"Joueurs présents : {[j.pseudo for j in joueurs_obj]}")

        num_tour_joueur = 0

        quitter_partie = False
        while not quitter_partie:

            statut = joueur_partie_service.obtenir_statut(joueur.id_joueur, self.table.id_table)
            
            pioche = ListeCartes()
            croupier = Croupier(pioche)
            liste_joueurs_dans_partie = joueur_partie_service.lister_joueurs_selon_table(self.table.id_table)
            mains_distribuees = croupier.distribuer2(liste_joueurs_dans_partie,2)
            for id_joueur_partie in liste_joueurs_dans_partie:
                main = mains_distribuees[id_joueur_partie]
                joueur_partie_service.attribuer_cartes_main_joueur(
                    id_table=self.table.id_table,
                    id_joueur=id_joueur_partie,
                    main=main
                )
            flop = croupier.distribuer_flop()
            turn = ListeCartes([croupier.distribuer_turn()])      
            river = ListeCartes([croupier.distribuer_river()]) 

            TableService().set_flop(self.table.id_table, flop)
            TableService().set_turn(self.table.id_table, turn)
            TableService().set_river(self.table.id_table, river)

            id_table = self.table.id_table
            id_joueur = joueur_partie.joueur.id_joueur 
            main_joueur = joueur_partie_service.recuperer_cartes_main_joueur(id_table=id_table, id_joueur=id_joueur)
            print(f'Ta main est : {main_joueur}')

            tours_de_mise = ['Pré-flop', 'Flop', 'Turn', 'River']
            for tour in tours_de_mise:

                if num_tour_joueur >= len(liste_joueurs_dans_partie):
                    num_tour_joueur = 0
                id_tour_joueur = liste_joueurs_dans_partie[num_tour_joueur]
                num_tour_joueur += 1
                TableService().set_id_joueur_tour(self.table.id_table, id_tour_joueur)

                while not TableService().get_id_joueur_tour(self.table.id_table) == joueur.id_joueur: 
                    print("En attente du tour des autres joueurs...")
                    time.sleep(2) 

                    action_attente = inquirer.select(
                        message="Voulez-vous continuer à attendre ou quitter la partie ?",
                        choices=[
                            "Continuer à attendre",
                            "Quitter la partie"
                        ],
                        default="Continuer à attendre"
                    ).execute()

                    if action_attente == "Quitter la partie":
                        quitter_partie = True
                        break
                if quitter_partie:
                    break
                
                print("C'est ton tour")

                liste_joueurs_dans_partie = joueur_partie_service.lister_joueurs_selon_table(self.table.id_table)
                joueurs_obj = [JoueurService().trouver_par_id(id_joueur) for id_joueur in liste_joueurs_dans_partie]
                print(f"Joueurs présents : {[j.pseudo for j in joueurs_obj]}")

                print(f"Votre credit actuel : {joueur.credit}")

                print(f"Valeur actuelle de la blinde : {self.table.blind_initial}")

                pot_actuel = TableService().get_pot(id_table)
                print(f"Pot actuel : {pot_actuel}") # garder dans un coin : TableService().alimenter_pot(id_table, 50) et TableService().retirer_pot(id_table, 100)

                cartes_communes = table_service.get_cartes_communes(id_table)
                flop = cartes_communes["flop"]
                turn = cartes_communes["turn"]
                river = cartes_communes["river"]
                if tours_de_mise == 'Flop':
                    print(f'Le flop est : {flop}')
                elif tours_de_mise == 'Turn':
                    print(f'Le flop est : {flop}')
                    print(f'La turn est : {turn}')
                elif tours_de_mise == 'River':
                    print(f'Le flop est : {flop}')
                    print(f'La turn est : {turn}')
                    print(f'La river est : {river}')

                montant_pour_suivre = self.table.blind_initial.valeur + TableService().get_val_derniere_mise(self.table.id_table)
                print(f"La valeur a payer pour suivre est : {montant_pour_suivre}")

                action = inquirer.select(
                    message="Que voulez-vous faire ?",
                    choices=[
                        "Miser",
                        "Suivre",
                        "Se coucher",
                        "Quitter la partie"
                    ],
                ).execute()

                if action == "Miser":
                    montant = int(inquirer.text(message="Montant à miser : ").execute())
                    TableService().set_val_derniere_mise(self.table.id_table, montant + TableService().get_val_derniere_mise(self.table.id_table))
                    valeur_totale_paye = montant + TableService().get_val_derniere_mise(self.table.id_table) + self.table.blind_initial.valeur
                    
                    #retirer le solde du joueur
                    solde = getattr(joueur, "credit", getattr(joueur, "solde", None))
                    valeur_solde = solde.get()
                    joueur.credit = Monnaie(valeur_solde - valeur_totale_paye)
                    #ajouter au pot
                    TableService().alimenter_pot(self.table.id_table, valeur_totale_paye)
                    
                    print(f"{joueur.pseudo} a misé {montant}.")

                elif action == "Suivre":
                    valeur_totale_paye = TableService().get_val_derniere_mise(self.table.id_table) + self.table.blind_initial.valeur

                    #retirer le solde du joueur
                    solde = getattr(joueur, "credit", getattr(joueur, "solde", None))
                    valeur_solde = solde.get()
                    joueur.credit = Monnaie(valeur_solde - valeur_totale_paye)
                    #ajouter au pot
                    TableService().alimenter_pot(self.table.id_table, valeur_totale_paye)

                    print(f"{joueur.pseudo} a suivi.")

                elif action == "Se coucher":
                    JoueurPartieService().mettre_a_jour_statut(joueur.id_joueur, self.table.id_table, "s'est couché")
                    print(f"{joueur.pseudo} s'est couché.")

                    while JoueurPartieService().obtenir_statut(joueur.id_joueur, self.table.id_table) == "s'est couché":
                        print("En attente de la fin de la main des autres joueurs...")
                        time.sleep(2) 

                        action_attente = inquirer.select(
                            message="Voulez-vous continuer à attendre ou quitter la partie ?",
                            choices=[
                                "Continuer à attendre",
                                "Quitter la partie"
                            ],
                            default="Continuer à attendre"
                        ).execute()

                        if action_attente == "Quitter la partie":
                            quitter_partie = True
                            break
                    if quitter_partie:
                        break
                    #monter que joueur a gagné
                
                if action == "Quitter la partie":
                    quitter_partie = True
            
            if quitter_partie:
                    break

        #faire quitter la partie au joueur
        # trouver un moyen de retirer le nb de joueurs dans la table table_poker -1
        joueur_partie_service.retirer_joueur_de_partie(joueur.id_joueur) #penser a retirer le joueur de joueur partie à la fin
        print(f"{joueur.pseudo} a quitté la partie.")

        from view.menu_joueur_vue import MenuJoueurVue
        return MenuJoueurVue().choisir_menu()
