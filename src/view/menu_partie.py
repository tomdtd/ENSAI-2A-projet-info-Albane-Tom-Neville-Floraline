from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite
from view.session import Session
from service.joueur_partie_service import JoueurPartieService
from service.table_service import TableService
from service.joueur_service import JoueurService
from business_object.siege import Siege
from business_object.croupier import Croupier
from business_object.liste_cartes import ListeCartes
from business_object.monnaie import Monnaie
from business_object.main_joueur_complete import MainJoueurComplete
from business_object.combinaison import Combinaison
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


            # Identifier le bouton du croupier (ici le premier joueur ou stocké dans la table)
            bouton_index = liste_joueurs_dans_partie.index(table_service.get_id_joueur_bouton(self.table.id_table))
            nb_joueurs = len(liste_joueurs_dans_partie)

            # Indices des blindes
            indice_petite_blinde = (bouton_index + 1) % nb_joueurs
            indice_grosse_blinde = (bouton_index + 2) % nb_joueurs

            id_petite_blinde = liste_joueurs_dans_partie[indice_petite_blinde]
            id_grosse_blinde = liste_joueurs_dans_partie[indice_grosse_blinde]

            # Mettre à jour les statuts
            joueur_partie_service.mettre_a_jour_statut(id_petite_blinde, self.table.id_table, "tour petite blinde")
            joueur_partie_service.mettre_a_jour_statut(id_grosse_blinde, self.table.id_table, "tour de blinde")

            # Débiter automatiquement les blindes et alimenter le pot
            credit_pb = JoueurService().recuperer_credit(id_petite_blinde)
            JoueurService().modifier_credit(id_petite_blinde, credit_pb.get() - self.table.blind_initial.get()/2)
            TableService().alimenter_pot(self.table.id_table, self.table.blind_initial.get()/2)

            credit_gb = JoueurService().recuperer_credit(id_grosse_blinde)
            JoueurService().modifier_credit(id_grosse_blinde, credit_gb.get() - self.table.blind_initial.get())
            TableService().alimenter_pot(self.table.id_table, self.table.blind_initial.get())


            tours_de_mise = ['Pré-flop', 'Flop', 'Turn', 'River', 'Fin de la main']
            for tour in tours_de_mise:

                if num_tour_joueur >= len(liste_joueurs_dans_partie):
                    num_tour_joueur = 0
                id_tour_joueur = liste_joueurs_dans_partie[num_tour_joueur]
                num_tour_joueur += 1
                TableService().set_id_joueur_tour(self.table.id_table, id_tour_joueur)


                liste_joueurs_en_jeu = []
                statuts_en_jeu = {"tour de blinde", "tour petite blinde", "en jeu"}
                for id_j in liste_joueurs_dans_partie:
                    statut_joueur = joueur_partie_service.obtenir_statut(id_j, self.table.id_table)
                    if statut_joueur in statuts_en_jeu:
                        liste_joueurs_en_jeu.append(id_j)
                
                while (not len(liste_joueurs_en_jeu) == 1) or (tour == 'Fin de la main'):

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

                    if tour == 'Pré-flop':
                        if joueur_partie_service.obtenir_statut(joueur.id_joueur, self.table.id_table) == 'tour de blinde':
                            print("C'est ton tour de grosse blinde")
                        if joueur_partie_service.obtenir_statut(joueur.id_joueur, self.table.id_table) == 'tour petite blinde':
                            print("C'est ton tour de petite blinde")


                    pot_actuel = TableService().get_pot(id_table)
                    print(f"Pot actuel : {pot_actuel}")

                    cartes_communes = table_service.get_cartes_communes(id_table)
                    flop = cartes_communes["flop"]
                    turn = cartes_communes["turn"]
                    river = cartes_communes["river"]
                    if tour == 'Flop':
                        print(f'Le flop est : {flop}')
                    elif tour == 'Turn':
                        print(f'Le flop est : {flop}')
                        print(f'La turn est : {turn}')
                    elif tour == 'River':
                        print(f'Le flop est : {flop}')
                        print(f'La turn est : {turn}')
                        print(f'La river est : {river}')

                    montant_pour_suivre = float(self.table.blind_initial.valeur) + float(TableService().get_val_derniere_mise(self.table.id_table))
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

                        if tour == 'Pré-flop' and (not joueur_partie_service.obtenir_statut(joueur.id_joueur, self.table.id_table) in {"tour de blinde", "tour petite blinde"}):
                            valeur_totale_paye = float(montant) + float(TableService().get_val_derniere_mise(self.table.id_table) + self.table.blind_initial.valeur)

                        elif joueur_partie_service.obtenir_statut(joueur.id_joueur, self.table.id_table) == "tour petite blinde":
                            valeur_totale_paye = float(montant) + float(TableService().get_val_derniere_mise(self.table.id_table) + (self.table.blind_initial.valeur/2))

                        else:
                            valeur_totale_paye = float(montant) + float(TableService().get_val_derniere_mise(self.table.id_table) + self.table.blind_initial.valeur)
                            
                        if joueur.credit.valeur < valeur_totale_paye:
                            print("Votre solde est insufisant")
                            JoueurPartieService().mettre_a_jour_statut(joueur.id_joueur, self.table.id_table, "s'est couché")
                            print(f"{joueur.pseudo} s'est couché.")
                        else :
                            TableService().set_val_derniere_mise(self.table.id_table, montant + TableService().get_val_derniere_mise(self.table.id_table))
                        
                            #retirer le solde du joueur
                            solde = getattr(joueur, "credit", getattr(joueur, "solde", None))
                            valeur_solde = solde.get()
                            joueur.credit = Monnaie(float(valeur_solde) - float(valeur_totale_paye))
                            #ajouter au pot
                            TableService().alimenter_pot(self.table.id_table, valeur_totale_paye)
                            
                            print(f"{joueur.pseudo} a misé {montant}.")

                    elif action == "Suivre":

                        if tour == 'Pré-flop' and (not joueur_partie_service.obtenir_statut(joueur.id_joueur, self.table.id_table) in {"tour de blinde", "tour petite blinde"}):
                            valeur_totale_paye = float(TableService().get_val_derniere_mise(self.table.id_table)) + float(self.table.blind_initial.valeur)

                        elif joueur_partie_service.obtenir_statut(joueur.id_joueur, self.table.id_table) == "tour petite blinde":
                            valeur_totale_paye = float(TableService().get_val_derniere_mise(self.table.id_table) + (self.table.blind_initial.valeur/2))

                        else:
                            valeur_totale_paye = float(TableService().get_val_derniere_mise(self.table.id_table) + self.table.blind_initial.valeur)
                        

                        if joueur.credit.valeur < valeur_totale_paye:
                            print("Votre solde est insufisant")
                            JoueurPartieService().mettre_a_jour_statut(joueur.id_joueur, self.table.id_table, "s'est couché")
                            print(f"{joueur.pseudo} s'est couché.")
                        else :
                            #retirer le solde du joueur
                            solde = getattr(joueur, "credit", getattr(joueur, "solde", None))
                            valeur_solde = solde.get()
                            joueur.credit = Monnaie(float(valeur_solde) - float(valeur_totale_paye))
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
                    
                    #recalcul du nombre de joueurs en jeu
                    liste_joueurs_en_jeu = []
                    for id_j in liste_joueurs_dans_partie:
                        statut_joueur = joueur_partie_service.obtenir_statut(id_j, self.table.id_table)
                        if statut_joueur in statuts_en_jeu:
                            liste_joueurs_en_jeu.append(id_j)
                
                if quitter_partie:
                        break
                
                #Gestion de la fin de la main

                #Cas ou il reste un seul joueur : il remporte le pot
                if len(liste_joueurs_en_jeu) == 1:
                    id_gagnant = liste_joueurs_en_jeu[0]
                
                    pot = TableService().get_pot(self.table.id_table)
                    print(f'Fin de la main : le gagnant remporte le pot : {pot}')
                    
                    nouveau_solde_du_gagnant = JoueurService().recuperer_credit(id_gagnant)
                    JoueurService().modifier_credit(id_gagnant, int(nouveau_solde_du_gagnant.get()))
                    TableService().retirer_pot(self.table.id_table, pot)

                #Cas ou il reste plusieur joueur : le joueur avec la combinaison la plus haute remporte le pot

                #Recuperer les mains des joueurs en jeu
                dict_id_cartes = {}
                for id_en_jeu in liste_joueurs_en_jeu:
                    dict_id_cartes[id_en_jeu] = JoueurPartieService().recuperer_cartes_main_joueur(id_table=id_table, id_joueur=id_en_jeu)
                
                #Comparer les mains
                dict_id_combinaison = {}
                flop_complet = flop + [turn, river] # ajouter turn et river
                for id in dict_id_cartes:
                    main_complete = MainJoueurComplete(dict_id_cartes[id] + flop_complet)
                    dict_id_combinaison[id] = main_complete.combinaison()
                #Trouver la valeur maximale
                max_val = max(dict_id_combinaison.values())
                combinaison_max = Combinaison(max_val)
                id_max = [k for k, v in d.items() if v == max_val] # recupere les id avec la combinaison la plus haute
                
                id_gagnant = id_max[0]
                if not len(id_max) == 1:
                    # Creer dico
                    dict_comb_complete = {}
                    for id in id_max:
                        dict_comb_complete[id] = dict_id_cartes[id] + flop_complet
                    id_gagnant = MainJoueurComplete().gagnants_avec_meme_combinaison(dict_comb_complete, combinaison_max)


                #Créditer le gagnant
                if isinstance(id_gagnant, list):
                    print(f"Les gagnants sont : {id_gagnant} avec une {combinaison_max}")

                    # Cas plusieurs gagnant il faut diviser le pot
                    pot = int(TableService().get_pot(self.table.id_table))
                    repartition_pot = int(pot/len(id_gagnant))

                    for id in id_gagnant:
                        nouveau_solde_du_gagnant = JoueurService().recuperer_credit(id)
                        JoueurService().modifier_credit(id, repartition_pot + int(nouveau_solde_du_gagnant.get()))
                    
                    TableService().retirer_pot(self.table.id_table, pot)

                else:
                    print(f"Le gagnant est : {id_gagnant} avec une {combinaison_max}")
                    
                    pot = TableService().get_pot(self.table.id_table)
                    print(f'Fin de la main : le gagnant remporte le pot : {pot}')
                    
                    nouveau_solde_du_gagnant = JoueurService().recuperer_credit(id_gagnant)
                    JoueurService().modifier_credit(id_gagnant, pot + int(nouveau_solde_du_gagnant.get()))
                    TableService().retirer_pot(self.table.id_table, pot)
                
                # Remet en jeu les joueurs couchés pour commencer une prochaine main
                liste_joueurs_dans_partie = joueur_partie_service.lister_joueurs_selon_table(self.table.id_table)
                for id_j in liste_joueurs_dans_partie:
                    statut_joueur = joueur_partie_service.obtenir_statut(id_j, self.table.id_table)
                    if statut_joueur == "s'est couché":
                        joueur_partie_service.mettre_a_jour_statut(id_j, self.table.id_table, "en jeu")
                
                # Faire tourner la blinde

                # Récupérer l'id du bouton actuel
                id_bouton_actuel = table_service.get_id_joueur_bouton(self.table.id_table)

                # Calculer le nouveau bouton (le joueur suivant dans la liste)
                index_actuel = liste_joueurs_dans_partie.index(id_bouton_actuel)
                nouveau_index_bouton = (index_actuel + 1) % len(liste_joueurs_dans_partie)
                nouveau_bouton = liste_joueurs_dans_partie[nouveau_index_bouton]

                # Mettre à jour dans la DB
                table_service.set_id_joueur_bouton(self.table.id_table, nouveau_bouton)

                # Changer les statuts des joueurs
                for id_j in liste_joueurs_dans_partie:
                    statut_joueur = joueur_partie_service.obtenir_statut(id_j, self.table.id_table)
                    if (statut_joueur == "tour de blinde") or (statut_joueur == "tour petite blinde"):
                        joueur_partie_service.mettre_a_jour_statut(id_j, self.table.id_table, "en jeu")
                
                    
            if quitter_partie:
                    break

        #faire quitter la partie au joueur
        TableService().retirer_joueur_table(self.table.id_table) # retirer le nb de joueurs dans la table table_poker
        joueur_partie_service.retirer_joueur_de_partie(joueur.id_joueur) # retirer le joueur de la partie à la fin
        print(f"{joueur.pseudo} a quitté la partie.")

        from view.menu_joueur_vue import MenuJoueurVue
        return MenuJoueurVue().choisir_menu()
