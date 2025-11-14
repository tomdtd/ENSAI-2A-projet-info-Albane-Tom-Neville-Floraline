from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite
from view.session import Session
from service.joueur_partie_service import JoueurPartieService

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
            return RejoindrePartie()
        
        siege_libre = self.table.nb_joueurs + 1

        joueur_partie_service = JoueurPartieService()
        joueur_partie = joueur_partie_service.ajouter_joueur_a_partie(joueur, siege_libre, solde_initial_partie, self.table.id_table)

        if joueur_partie:
            print(f"{joueur.pseudo} a été ajouté à la partie {id_partie} sur le siège {siege.id_siege}.")
        else:
            print("Impossible d'ajouter le joueur à la partie.")
