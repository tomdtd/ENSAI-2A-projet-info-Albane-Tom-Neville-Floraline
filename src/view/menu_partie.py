from InquirerPy import inquirer
from src.view.vue_abstraite import VueAbstraite
from src.view.session import Session
from src.service.joueur_partie_service import JoueurPartieService
from src.service.table_service import TableService
from src.service.joueur_service import JoueurService
from src.business_object.siege import Siege
from src.business_object.croupier import Croupier
from src.business_object.liste_cartes import ListeCartes
from src.business_object.monnaie import Monnaie
from src.business_object.main_joueur_complete import MainJoueurComplete
from src.business_object.combinaison import Combinaison
from src.service.transaction_service import TransactionService
import time

COMBINAISON_LABELS = {
    Combinaison.CarteHaute: "Carte haute",
    Combinaison.Paire: "Paire",
    Combinaison.DoublePaire: "Double paire",
    Combinaison.Brelan: "Brelan",
    Combinaison.Quinte: "Quinte",
    Combinaison.Flush: "Couleur",
    Combinaison.Full: "Full",
    Combinaison.Carre: "Carré",
    Combinaison.QuinteFlush: "Quinte flush",
    Combinaison.QuinteRoyale: "Quinte royale",
}


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

        siege_libre = Siege(
            self.table.nb_joueurs + 1
        )  # faire en sorte de modifier nb_joueurs avant pour ne pas mettre 0 a tout le monde...
        siege_libre.est_occupe()

        joueur_partie_service = JoueurPartieService()
        joueur_partie = joueur_partie_service.ajouter_joueur_a_partie(
            joueur, siege_libre, self.solde_initial_partie, self.table.id_table
        )

        if joueur_partie:
            print(f"{joueur.pseudo} a été ajouté à la table {self.table.id_table}.")
            table_service = TableService()
            table_service.ajouter_joueur_table(self.table.id_table)

        else:
            print("Impossible d'ajouter le joueur à la partie.")
            from view.rejoindre_partie import RejoindrePartie

            return RejoindrePartie().choisir_menu()

        liste_joueurs_dans_partie = joueur_partie_service.lister_joueurs_selon_table(self.table.id_table)

        joueurs_obj = [JoueurService().trouver_par_id(id_joueur) for id_joueur in liste_joueurs_dans_partie]
        joueurs = ", ".join([j.pseudo for j in joueurs_obj])
        print(f"Joueurs présents : {joueurs}")

        num_tour_joueur = 0

        quitter_partie = False
        while not quitter_partie:

            # Système d'attende de d'autres joueurs
            while len(liste_joueurs_dans_partie) < 2:
                print(f"En attente d'autres joueurs... ({len(liste_joueurs_dans_partie)} joueur(s) présent(s))")

                action_attente = inquirer.select(
                    message="Voulez-vous continuer à attendre ou quitter la partie ?",
                    choices=["Continuer à attendre", "Quitter la partie"],
                    default="Continuer à attendre",
                ).execute()

                if action_attente == "Quitter la partie":
                    quitter_partie = True
                    break

                time.sleep(5)  # attente de 5 secondes avant de re-vérifier
                liste_joueurs_dans_partie = joueur_partie_service.lister_joueurs_selon_table(self.table.id_table)

            if quitter_partie == True:
                break

            statut = joueur_partie_service.obtenir_statut(joueur.id_joueur, self.table.id_table)

            # Sas d'attente pour les joueurs pour la distribution des carte et l'attibution des blindes
            if not (joueur.id_joueur == liste_joueurs_dans_partie[0]):
                while len(joueur_partie_service.recuperer_cartes_main_joueur(self.table.id_table, joueur.id_joueur)) == 0:
                    print(f"En attente de la distribution des cartes...")

                    action_attente = inquirer.select(
                        message="Voulez-vous continuer à attendre ou quitter la partie ?",
                        choices=["Continuer à attendre", "Quitter la partie"],
                        default="Continuer à attendre",
                    ).execute()

                    if action_attente == "Quitter la partie":
                        quitter_partie = True
                        break

                    time.sleep(5)  # attente de 5 secondes avant de re-vérifier



            ### Partie de code executée une seule fois
            if joueur.id_joueur == liste_joueurs_dans_partie[0]:
                # Identifier le bouton du croupier (ici le premier joueur stocké dans la table)
                id_bouton = TableService().get_id_joueur_bouton(self.table.id_table)

                # Si le bouton n'est pas défini ou plus dans la liste, choisir le premier joueur
                if id_bouton not in liste_joueurs_dans_partie:
                    id_bouton = liste_joueurs_dans_partie[0]
                    TableService().set_id_joueur_bouton(self.table.id_table, id_bouton)

                bouton_index = liste_joueurs_dans_partie.index(id_bouton)
                nb_joueurs = len(liste_joueurs_dans_partie)

                # Indices des blindes
                indice_petite_blinde = (bouton_index + 1) % nb_joueurs
                indice_grosse_blinde = (bouton_index + 2) % nb_joueurs

                id_petite_blinde = liste_joueurs_dans_partie[indice_petite_blinde]
                id_grosse_blinde = liste_joueurs_dans_partie[indice_grosse_blinde]

                # Mettre à jour les statuts
                joueur_partie_service.mettre_a_jour_statut(id_petite_blinde, self.table.id_table, "tour petite blinde")
                joueur_partie_service.mettre_a_jour_statut(id_grosse_blinde, self.table.id_table, "tour de blinde")

                # determiner le premier indice a jouer
                indice_grosse_blinde = liste_joueurs_dans_partie.index(id_grosse_blinde)
                indice_premier_a_jouer = (indice_grosse_blinde + 1) % len(liste_joueurs_dans_partie)
                id_premier_joueur = liste_joueurs_dans_partie[indice_premier_a_jouer]
                TableService().set_id_joueur_tour(self.table.id_table, id_premier_joueur)
                print(f"Premier joueur à parler : {JoueurService().trouver_par_id(id_premier_joueur).pseudo}")

            # Stocker dans l'environnement de tous les joueurs l'id du premier a jouer
            id_bouton = TableService().get_id_joueur_bouton(self.table.id_table)
            bouton_index = liste_joueurs_dans_partie.index(id_bouton)
            nb_joueurs = len(liste_joueurs_dans_partie)
            indice_grosse_blinde = (bouton_index + 2) % nb_joueurs
            id_grosse_blinde = liste_joueurs_dans_partie[indice_grosse_blinde]
            indice_grosse_blinde = liste_joueurs_dans_partie.index(id_grosse_blinde)
            indice_premier_a_jouer = (indice_grosse_blinde + 1) % len(liste_joueurs_dans_partie)
            id_premier_joueur = liste_joueurs_dans_partie[indice_premier_a_jouer]

            if joueur_partie_service.obtenir_statut(joueur.id_joueur, self.table.id_table) == "tour petite blinde":
                # Débiter automatiquement les blindes et alimenter le pot
                credit_pb = JoueurService().recuperer_credit(joueur.id_joueur)
                montant_a_donner_blinde = float(credit_pb.get()) - float(self.table.blind_initial.get() / 2)
                if montant_a_donner_blinde < 0:
                    print("Solde insufisant pour payer la blinde")
                    quitter_partie = True
                    break
                else:
                    JoueurService().modifier_credit(
                        joueur.id_joueur, float(credit_pb.get()) - float(self.table.blind_initial.get() / 2)
                    )
                    TransactionService().enregistrer_transaction(joueur.id_joueur, - int(float(self.table.blind_initial.get() / 2)))

                TableService().alimenter_pot(self.table.id_table, self.table.blind_initial.get() / 2)

            if joueur_partie_service.obtenir_statut(joueur.id_joueur, self.table.id_table) == "tour de blinde":
                credit_gb = JoueurService().recuperer_credit(joueur.id_joueur)
                montant_a_donner_petite_blinde = float(credit_gb.get()) - float(self.table.blind_initial.get())
                if montant_a_donner_petite_blinde < 0:
                    print("Solde insufisant pour payer la blinde")
                    quitter_partie = True
                    break
                else:
                    JoueurService().modifier_credit(
                        joueur.id_joueur, float(credit_gb.get()) - float(self.table.blind_initial.get())
                    )
                    TransactionService().enregistrer_transaction(joueur.id_joueur, - int(float(self.table.blind_initial.get())))

                TableService().alimenter_pot(self.table.id_table, self.table.blind_initial.get())

            ### partie de code executée une seule fois
            if joueur.id_joueur == liste_joueurs_dans_partie[0]:
                # executera le tirage dans le script d'un seul joueur
                pioche = ListeCartes()
                croupier = Croupier(pioche)
                liste_joueurs_dans_partie = joueur_partie_service.lister_joueurs_selon_table(self.table.id_table)
                mains_distribuees = croupier.distribuer2(liste_joueurs_dans_partie, 2)
                for id_joueur_partie in liste_joueurs_dans_partie:
                    main = mains_distribuees[id_joueur_partie]
                    joueur_partie_service.attribuer_cartes_main_joueur(
                        id_table=self.table.id_table, id_joueur=id_joueur_partie, main=main
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
            cartes = main_joueur.get_cartes()
            main_joueur_join = ", ".join(str(carte) for carte in cartes)
            print(f"Ta main est : {main_joueur_join}")

            tours_de_mise = ["Pré-flop", "Flop", "Turn", "River"]
            for tour in tours_de_mise:

                # Reinitialiser la derniere mise à 0 pour le premier joueur a joueur le tour -> ne fonctionne pas
                # if joueur.id_joueur == id_premier_joueur:
                #     TableService().set_val_derniere_mise(self.table.id_table, 0.0)

                liste_joueurs_en_jeu = []
                statuts_en_jeu = {"tour de blinde", "tour petite blinde", "en jeu"}
                for id_j in liste_joueurs_dans_partie:
                    statut_joueur = joueur_partie_service.obtenir_statut(id_j, self.table.id_table)
                    if statut_joueur in statuts_en_jeu:
                        liste_joueurs_en_jeu.append(id_j)

                while not TableService().get_id_joueur_tour(self.table.id_table) == joueur.id_joueur:
                    print("En attente du tour des autres joueurs...")
                    time.sleep(2)

                    action_attente = inquirer.select(
                        message="Voulez-vous continuer à attendre ou quitter la partie ?",
                        choices=["Continuer à attendre", "Quitter la partie"],
                        default="Continuer à attendre",
                    ).execute()

                    if action_attente == "Quitter la partie":
                        quitter_partie = True
                        break

                    # Vérifier que les joueurs ne sont pas partis pendant l'attente
                    liste_joueurs_en_jeu = []
                    for id_j in liste_joueurs_dans_partie:
                        statut_joueur = joueur_partie_service.obtenir_statut(id_j, self.table.id_table)
                        if statut_joueur in statuts_en_jeu:
                            liste_joueurs_en_jeu.append(id_j)
                    if len(liste_joueurs_en_jeu) == 1:
                        print("Tous les autres joueurs on quitté la partie")
                        break
                if len(liste_joueurs_en_jeu) == 1:
                    break

                if quitter_partie:
                    break

                print("C'est ton tour")

                liste_joueurs_dans_partie = joueur_partie_service.lister_joueurs_selon_table(self.table.id_table)
                joueurs_obj = [JoueurService().trouver_par_id(id_joueur) for id_joueur in liste_joueurs_dans_partie]
                noms_joueurs_presents = ", ".join([j.pseudo for j in joueurs_obj])
                print(f"Joueurs présents : {noms_joueurs_presents}")

                print(f"Votre credit actuel : {joueur.credit}")

                print(f"Valeur actuelle de la blinde : {self.table.blind_initial}")

                if tour == "Pré-flop":
                    if joueur_partie_service.obtenir_statut(joueur.id_joueur, self.table.id_table) == "tour de blinde":
                        print("C'est ton tour de grosse blinde")
                    if (
                        joueur_partie_service.obtenir_statut(joueur.id_joueur, self.table.id_table)
                        == "tour petite blinde"
                    ):
                        print("C'est ton tour de petite blinde")

                pot_actuel = TableService().get_pot(id_table)
                print(f"Pot actuel : {pot_actuel}")

                cartes_communes = table_service.get_cartes_communes(id_table)
                flop = cartes_communes["flop"]
                flop_cartes = flop.get_cartes()
                flop_affichage = ", ".join(str(c) for c in flop_cartes)
                turn = cartes_communes["turn"]
                turn_carte = turn.get_cartes()
                turn_affichage = ", ".join(str(c) for c in turn_carte)
                river = cartes_communes["river"]
                river_carte = river.get_cartes()
                river_affichage = ", ".join(str(c) for c in river_carte)
                if tour == "Flop":
                    print(f"Le flop est : {flop_affichage}")
                elif tour == "Turn":
                    print(f"Le flop est : {flop_affichage}")
                    print(f"La turn est : {turn_affichage}")
                elif tour == "River":
                    print(f"Le flop est : {flop_affichage}")
                    print(f"La turn est : {turn_affichage}")
                    print(f"La river est : {river_affichage}")
                print(f"Ta main est : {main_joueur_join}")

                if not joueur_partie_service.obtenir_statut(joueur.id_joueur, self.table.id_table) in {
                    "tour de blinde",
                    "tour petite blinde",
                } and tour == "Pré-flop":
                    montant_pour_suivre = float(self.table.blind_initial.valeur) + float(
                        TableService().get_val_derniere_mise(self.table.id_table)
                    )
                    print(f"La valeur a payer pour suivre est : {montant_pour_suivre}")
                elif (
                    joueur_partie_service.obtenir_statut(joueur.id_joueur, self.table.id_table) == "tour petite blinde"
                ) and tour == "Pré-flop":
                    montant_pour_suivre = float(self.table.blind_initial.valeur) / 2 + float(
                        TableService().get_val_derniere_mise(self.table.id_table)
                    )
                    print(f"La valeur a payer pour suivre est : {montant_pour_suivre}")
                else:
                    montant_pour_suivre = float(TableService().get_val_derniere_mise(self.table.id_table))
                    print(f"La valeur a payer pour suivre est : {montant_pour_suivre}")

                action = inquirer.select(
                    message="Que voulez-vous faire ?",
                    choices=["Miser", "Suivre", "Se coucher", "Quitter la partie"],
                ).execute()

                if action == "Miser":
                    montant = int(inquirer.text(message="Montant à miser : ").execute())

                    if tour == "Pré-flop" and (
                        not joueur_partie_service.obtenir_statut(joueur.id_joueur, self.table.id_table)
                        in {"tour de blinde", "tour petite blinde"}
                    ):
                        valeur_totale_paye = (
                            float(montant)
                            + float(TableService().get_val_derniere_mise(self.table.id_table))
                            + float(self.table.blind_initial.valeur)
                        )

                    elif (
                        joueur_partie_service.obtenir_statut(joueur.id_joueur, self.table.id_table)
                        == "tour petite blinde"
                    ):
                        valeur_totale_paye = float(montant) + float(
                            TableService().get_val_derniere_mise(self.table.id_table)
                            + float(self.table.blind_initial.valeur / 2)
                        )

                    else:
                        valeur_totale_paye = (
                            float(montant)
                            + float(TableService().get_val_derniere_mise(self.table.id_table))
                            + float(self.table.blind_initial.valeur)
                        )

                    if joueur.credit.valeur < valeur_totale_paye:
                        print("Votre solde est insufisant")
                        JoueurPartieService().mettre_a_jour_statut(
                            joueur.id_joueur, self.table.id_table, "s'est couché"
                        )
                        print(f"{joueur.pseudo} s'est couché.")
                    else:
                        TableService().set_val_derniere_mise(
                            self.table.id_table, montant + TableService().get_val_derniere_mise(self.table.id_table)
                        )

                        # retirer le solde du joueur
                        solde = getattr(joueur, "credit", getattr(joueur, "solde", None))
                        valeur_solde = solde.get()
                        joueur.credit = Monnaie(float(valeur_solde) - float(valeur_totale_paye))
                        JoueurService().modifier_credit(joueur.id_joueur, float(joueur.credit.get()))
                        TransactionService().enregistrer_transaction(joueur.id_joueur, - int(valeur_totale_paye))
                        # ajouter au pot
                        TableService().alimenter_pot(self.table.id_table, valeur_totale_paye)

                        print(f"{joueur.pseudo} a misé {montant}.")

                elif action == "Suivre":

                    if tour == "Pré-flop" and (
                        not joueur_partie_service.obtenir_statut(joueur.id_joueur, self.table.id_table)
                        in {"tour de blinde", "tour petite blinde"}
                    ):
                        valeur_totale_paye = float(TableService().get_val_derniere_mise(self.table.id_table)) + float(
                            self.table.blind_initial.valeur
                        )

                    elif (
                        joueur_partie_service.obtenir_statut(joueur.id_joueur, self.table.id_table)
                        == "tour petite blinde"
                    ):
                        valeur_totale_paye = float(TableService().get_val_derniere_mise(self.table.id_table)) + float(
                            self.table.blind_initial.valeur / 2
                        )

                    else:
                        valeur_totale_paye = float(TableService().get_val_derniere_mise(self.table.id_table)) + float(
                            self.table.blind_initial.valeur
                        )

                    if joueur.credit.valeur < valeur_totale_paye:
                        print("Votre solde est insufisant")
                        JoueurPartieService().mettre_a_jour_statut(
                            joueur.id_joueur, self.table.id_table, "s'est couché"
                        )
                        print(f"{joueur.pseudo} s'est couché.")
                    else:
                        # retirer le solde du joueur
                        solde = getattr(joueur, "credit", getattr(joueur, "solde", None))
                        valeur_solde = solde.get()
                        joueur.credit = Monnaie(float(valeur_solde) - float(valeur_totale_paye))
                        JoueurService().modifier_credit(joueur.id_joueur, float(joueur.credit.get()))
                        TransactionService().enregistrer_transaction(joueur.id_joueur, - int(valeur_totale_paye))
                        # ajouter au pot
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
                            choices=["Continuer à attendre", "Quitter la partie"],
                            default="Continuer à attendre",
                        ).execute()

                        if action_attente == "Quitter la partie":
                            quitter_partie = True
                            break
                    if quitter_partie:
                        break

                # mise a jour du joueur dont c'est le tour

                # recharger la liste des joueurs et filtrer les joueurs actifs
                liste_joueurs_dans_partie = joueur_partie_service.lister_joueurs_selon_table(self.table.id_table)
                statuts_en_jeu = {"tour de blinde", "tour petite blinde", "en jeu"}
                liste_joueurs_en_jeu = [
                    jid
                    for jid in liste_joueurs_dans_partie
                    if joueur_partie_service.obtenir_statut(jid, self.table.id_table) in statuts_en_jeu
                ]

                if len(liste_joueurs_en_jeu) == 0:
                    # plus personne en jeu (sécurité) : rien à faire
                    print("Aucun joueur en jeu pour passer le tour.")
                else:
                    # id courant (celui qui venait de jouer) stocké en DB
                    id_courant = TableService().get_id_joueur_tour(self.table.id_table)

                    # s'assurer que id_courant est dans la liste (même type !)
                    try:
                        idx = liste_joueurs_en_jeu.index(id_courant)
                    except ValueError:
                        # si l'id courant n'est pas présent (ex : il s'est couché), on prend
                        # l'indice du premier joueur en jeu (ou le joueur suivant de num_tour_joueur si tu préfères)
                        idx = 0

                    prochain_idx = (idx + 1) % len(liste_joueurs_en_jeu)
                    prochain_id = liste_joueurs_en_jeu[prochain_idx]

                    # écrire en base : c'est cette écriture qui permettra aux autres clients de voir le changement
                    TableService().set_id_joueur_tour(self.table.id_table, prochain_id)

                    print(f"Tour passé de {JoueurService().trouver_par_id(id_courant).pseudo} à {JoueurService().trouver_par_id(prochain_id).pseudo}")

                if len(liste_joueurs_en_jeu) <= 1:
                    break

                # recalcul du nombre de joueurs en jeu
                liste_joueurs_en_jeu = []
                for id_j in liste_joueurs_dans_partie:
                    statut_joueur = joueur_partie_service.obtenir_statut(id_j, self.table.id_table)
                    if statut_joueur in statuts_en_jeu:
                        liste_joueurs_en_jeu.append(id_j)

                if joueur.id_joueur == liste_joueurs_en_jeu[-1]:  # dernier joueur à avoir joué
                    # gestion des cas de relance
                    # ---------- Début : gestion stricte de la clôture du tour ----------
                    # Initialisation des contributions pour ce tour
                    liste_joueurs_dans_partie = joueur_partie_service.lister_joueurs_selon_table(self.table.id_table)
                    statuts_en_jeu = {"tour de blinde", "tour petite blinde", "en jeu"}
                    joueurs_actifs = [
                        jid
                        for jid in liste_joueurs_dans_partie
                        if joueur_partie_service.obtenir_statut(jid, self.table.id_table) in statuts_en_jeu
                    ]

                    contribution_joueur = {jid: 0.0 for jid in joueurs_actifs}
                    mise_tour_courant = 0.0

                    def tour_clos():
                        for jid in list(contribution_joueur.keys()):
                            statut = joueur_partie_service.obtenir_statut(jid, self.table.id_table)
                            if statut == "s'est couché":
                                continue
                            credit = float(JoueurService().recuperer_credit(jid).get())
                            if credit <= 0:
                                continue
                            if contribution_joueur[jid] < mise_tour_courant:
                                return False
                        return True

                    # Boucle de clôture
                    securite = 0
                    max_securite = 1000
                    while not tour_clos():
                        securite += 1
                        if securite > max_securite:
                            print("Arrêt sécurité : trop d'itérations dans la phase de clôture.")
                            break

                        liste_joueurs_dans_partie = joueur_partie_service.lister_joueurs_selon_table(
                            self.table.id_table
                        )
                        joueurs_actifs = [
                            jid
                            for jid in liste_joueurs_dans_partie
                            if joueur_partie_service.obtenir_statut(jid, self.table.id_table) in statuts_en_jeu
                        ]

                        joueur_courant = TableService().get_id_joueur_tour(self.table.id_table)
                        if joueur_courant not in joueurs_actifs:
                            if joueurs_actifs:
                                joueur_courant = joueurs_actifs[0]
                                TableService().set_id_joueur_tour(self.table.id_table, joueur_courant)
                            else:
                                break  # plus personne d'actif

                        if joueur_courant == joueur.id_joueur:
                            montant_a_suivre = mise_tour_courant - contribution_joueur.get(joueur.id_joueur, 0.0)
                            if montant_a_suivre < 0:
                                montant_a_suivre = 0.0

                            print(f"Montant à suivre : {montant_a_suivre} | Ton crédit : {joueur.credit}")

                            action = inquirer.select(
                                message="Phase de clôture : que fais-tu ?",
                                choices=["Miser (relance)", "Suivre", "Se coucher", "Quitter la partie"],
                            ).execute()

                            if action == "Quitter la partie":
                                quitter_partie = True
                                break
                            elif action == "Se coucher":
                                joueur_partie_service.mettre_a_jour_statut(
                                    joueur.id_joueur, self.table.id_table, "s'est couché"
                                )
                                if joueur.id_joueur in contribution_joueur:
                                    del contribution_joueur[joueur.id_joueur]
                            elif action == "Suivre":
                                to_pay = min(float(joueur.credit), montant_a_suivre)
                                JoueurService().modifier_credit(joueur.id_joueur, float(joueur.credit) - to_pay)
                                TransactionService().enregistrer_transaction(joueur.id_joueur, - int(to_pay))
                                TableService().alimenter_pot(self.table.id_table, to_pay)
                                contribution_joueur[joueur.id_joueur] += to_pay
                            else:  # Miser / Relance
                                montant = float(inquirer.text(message="Montant à relancer (additionnel) : ").execute())
                                to_pay = min(float(joueur.credit), montant)
                                JoueurService().modifier_credit(joueur.id_joueur, float(joueur.credit) - to_pay)
                                TransactionService().enregistrer_transaction(joueur.id_joueur, - int(to_pay))
                                TableService().alimenter_pot(self.table.id_table, to_pay)
                                contribution_joueur[joueur.id_joueur] += to_pay
                                if contribution_joueur[joueur.id_joueur] > mise_tour_courant:
                                    mise_tour_courant = contribution_joueur[joueur.id_joueur]
                                    print(f"Nouvelle mise à égaler : {mise_tour_courant}")

                            # Passer le tour au prochain joueur actif
                            if joueurs_actifs:
                                try:
                                    idx = joueurs_actifs.index(joueur_courant)
                                    prochain_idx = (idx + 1) % len(joueurs_actifs)
                                    prochain_joueur = joueurs_actifs[prochain_idx]
                                except ValueError:
                                    prochain_joueur = joueurs_actifs[0]
                                TableService().set_id_joueur_tour(self.table.id_table, prochain_joueur)
                        else:
                            print("En attente du tour des autres joueurs...")
                            time.sleep(2)

                    # ---------- Fin : gestion stricte de la clôture ----------

                if quitter_partie:
                    break

                # Gestion de la fin de la main -> partie du code executé dans le script d'un seul joueur pour qu'il s'execute une fois

                # recalcul du nombre de joueurs en jeu
                liste_joueurs_en_jeu = []
                for id_j in liste_joueurs_dans_partie:
                    statut_joueur = joueur_partie_service.obtenir_statut(id_j, self.table.id_table)
                    if statut_joueur in statuts_en_jeu:
                        liste_joueurs_en_jeu.append(id_j)

            if (
                joueur.id_joueur == liste_joueurs_en_jeu[0]
            ):  # premier joueur de la liste pris arbitrairement pour que le code s'execute une seule fois
                # Cas ou il reste un seul joueur : il remporte le pot
                if len(liste_joueurs_en_jeu) == 1:
                    id_gagnant = liste_joueurs_en_jeu[0]

                    pot = TableService().get_pot(self.table.id_table)
                    print(f"Fin de la main : le gagnant remporte le pot : {pot}")

                    nouveau_solde_du_gagnant = JoueurService().recuperer_credit(id_gagnant)
                    JoueurService().modifier_credit(id_gagnant, int(nouveau_solde_du_gagnant.get()))
                    TransactionService().enregistrer_transaction(id_gagnant, int(pot))
                    TableService().retirer_pot(self.table.id_table, pot)

            # Cas ou il reste plusieur joueur : le joueur avec la combinaison la plus haute remporte le pot

            # Recuperer les mains des joueurs en jeu
            dict_id_cartes = {}
            for id_en_jeu in liste_joueurs_en_jeu:
                dict_id_cartes[id_en_jeu] = JoueurPartieService().recuperer_cartes_main_joueur(
                    id_table=id_table, id_joueur=id_en_jeu
                )

            # Comparer les mains
            dict_id_combinaison = {}
            # aplatir en UNE LISTE de cartes (et non pas liste de listes)
            flop_complet = (
                (flop.get_cartes() if hasattr(flop, "get_cartes") else list(flop))
                + (turn.get_cartes() if hasattr(turn, "get_cartes") else list(turn))
                + (river.get_cartes() if hasattr(river, "get_cartes") else list(river))
            )

            for id, main_obj in dict_id_cartes.items():
                main_list = main_obj.get_cartes() if hasattr(main_obj, "get_cartes") else list(main_obj)
                main_complete = MainJoueurComplete(main_list + flop_complet)
                dict_id_combinaison[id] = main_complete.combinaison()
            # Trouver la valeur maximale
            max_val = max(dict_id_combinaison.values())
            combinaison_max = Combinaison(max_val)
            id_max = [
                k for k, v in dict_id_combinaison.items() if v == max_val
            ]  # recupere les id avec la combinaison la plus haute

            id_gagnant = id_max[0]
            if not len(id_max) == 1:
                # Creer dico
                dict_comb_complete = {}
                for id in id_max:
                    dict_comb_complete[id] = (dict_id_cartes[id].get_cartes() if hasattr(dict_id_cartes[id], "get_cartes") else list(dict_id_cartes[id])) + flop_complet
                    #dict_comb_complete[id] = dict_id_cartes[id] + ListeCartes(flop_complet)
                id_gagnant = MainJoueurComplete([]).gagnants_avec_meme_combinaison(dict_comb_complete, combinaison_max)

            # Créditer le gagnant
            if isinstance(id_gagnant, list):
                noms = ", ".join([JoueurService().trouver_par_id(i).pseudo for i in id_gagnant])
                print(f"Les gagnants sont : {noms} avec une {COMBINAISON_LABELS.get(combinaison_max)}")
                # Cas plusieurs gagnant il faut diviser le pot
                if joueur.id_joueur == liste_joueurs_en_jeu[0]:
                    pot = int(TableService().get_pot(self.table.id_table))
                    repartition_pot = int(pot / len(id_gagnant))

                    for id in id_gagnant:
                        nouveau_solde_du_gagnant = JoueurService().recuperer_credit(id)
                        JoueurService().modifier_credit(id, float(repartition_pot + int(nouveau_solde_du_gagnant.get())))
                        TransactionService().enregistrer_transaction(id, int(repartition_pot))

                    TableService().retirer_pot(self.table.id_table, pot)

            else:
                print(
                    f"Le gagnant est : {JoueurService().trouver_par_id(id_gagnant).pseudo} avec une {COMBINAISON_LABELS.get(combinaison_max)}"
                )

                pot = TableService().get_pot(self.table.id_table)
                print(f"Fin de la main : le gagnant remporte le pot : {pot}")

                if joueur.id_joueur == liste_joueurs_en_jeu[0]:
                    nouveau_solde_du_gagnant = JoueurService().recuperer_credit(id_gagnant)
                    JoueurService().modifier_credit(id_gagnant, float(pot + int(nouveau_solde_du_gagnant.get())))
                    TransactionService().enregistrer_transaction(id_gagnant, int(pot))
                    TableService().retirer_pot(self.table.id_table, pot)

            # Mettre le statut couché a tous les joueurs pour eviter qu'il passent a l'étape suivante de la boucle
            # avant que tous les joueurs n'ai consulté le resultat de la partie en cours
            # (montre le résultat de la partie suivante à certains utilisateurs sans cette etape...)
            joueur_partie_service.mettre_a_jour_statut(joueur.id_joueur, self.table.id_table, "s'est couché")
            while len(liste_joueurs_en_jeu) != 0:
                print("Attente que les joueurs consultent le resultat de la main...")

                action_attente = inquirer.select(
                    message="Voulez-vous continuer à attendre ou quitter la partie ?",
                    choices=["Continuer à attendre", "Quitter la partie"],
                    default="Continuer à attendre",
                ).execute()

                if action_attente == "Quitter la partie":
                    quitter_partie = True
                    break

                time.sleep(5)  # attente de 5 secondes avant de re-vérifier
                liste_joueurs_dans_partie = joueur_partie_service.lister_joueurs_selon_table(self.table.id_table)

                # recalcul du nombre de joueurs en jeu
                liste_joueurs_en_jeu = []
                for id_j in liste_joueurs_dans_partie:
                    statut_joueur = joueur_partie_service.obtenir_statut(id_j, self.table.id_table)
                    if statut_joueur in statuts_en_jeu:
                        liste_joueurs_en_jeu.append(id_j)

            # lister joueurs dans partie
            liste_joueurs_dans_partie = joueur_partie_service.lister_joueurs_selon_table(self.table.id_table)
            if joueur.id_joueur == liste_joueurs_dans_partie[0]:
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

        # faire quitter la partie au joueur
        TableService().retirer_joueur_table(self.table.id_table)  # retirer le nb de joueurs dans la table table_poker
        joueur_partie_service.retirer_joueur_de_partie(joueur.id_joueur)  # retirer le joueur de la partie à la fin
        print(f"{joueur.pseudo} a quitté la partie.")

        from view.menu_joueur_vue import MenuJoueurVue

        return MenuJoueurVue().choisir_menu()
