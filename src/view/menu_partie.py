from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite
from view.session import Session
from service.joueur_partie_service import JoueurPartieService
from business_object.siege import Siege

class MenuPartie(VueAbstraite):

    def __init__(self, table):
        self.table = table
        self.solde_initial_partie = self.table.blind_initial.get()

    def choisir_menu(self):
        session = Session()
        joueur = session.joueur

        if self.table.nb_sieges >= self.table.nb_sieges:
            print("La table est pleine !")
            from view.rejoindre_partie import RejoindrePartie
            return RejoindrePartie().choisir_menu()
        
        siege_libre = Siege(self.table.nb_sieges + 1)
        siege_libre.est_occupe()
        
        joueur_partie_service = JoueurPartieService()
        joueur_partie = joueur_partie_service.ajouter_joueur_a_partie(joueur, siege_libre, self.solde_initial_partie, self.table.id_table)

        if joueur_partie:
            print(f"{joueur.pseudo} a été ajouté à la table {self.table.id_table} sur le siège {siege_libre.id_siege}.")
        else:
            print("Impossible d'ajouter le joueur à la partie.")
