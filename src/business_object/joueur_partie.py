
from src.business_object.main import Main
from src.business_object.joueur import Joueur
from src.business_object.siege import Siege
from src.business_object.monnaie import Monnaie

class JoueurPartie:
    """
    Classe d'association liant un Joueur à une Partie.
    
    Attributs:
    ----------
    joueur : Joueur
        Le joueur associé à cette partie.
    siege : Siege
        Le siège occupé par le joueur dans la partie.       
    main : Main
        La main de cartes du joueur dans cette partie.
    solde_partie : Monnaie
        Le solde d'argent du joueur pour cette partie.             
    statut : str
        Le statut actuel du joueur dans la partie (ex: "actif", "couché", "all-in").
    mise_tour : Monnaie
        La mise actuelle du joueur pour le tour de mise en cours.
    
    Méthodes:
    ---------
    miser(montant: int) -> None
        Permet au joueur de miser un certain montant.       
    se_coucher() -> None
        Permet au joueur de se coucher.
    """
    def __init__(self, joueur: Joueur, siege: Siege, solde_partie: int):
        self.joueur = joueur
        self.siege = siege
        self.main = Main()
        self.solde_partie = Monnaie(solde_partie) 
        self.statut = "en attente" 
        self.mise_tour = Monnaie(0) 

    def miser(self, montant: int):
        """Le joueur mise un certain montant"""
        if montant <= 0:
            return  # Ne rien faire si montant négatif ou nul
        
        if montant > self.solde_partie.valeur  :
            # Ajuster au solde maximum disponible
            montant = self.solde_partie.valeur
        
        self.solde_partie.debiter(montant)
        self.mise_tour.crediter(montant)
        print(f"{self.joueur.pseudo} mise {montant}.")

    def se_coucher(self):
        """Le joueur se couche."""
        self.statut = "couché"
        print(f"{self.joueur.pseudo} se couche.")