class Croupier:
    """
    Représente le croupier, qui gère le déroulement du jeu.
    
    Attributes:
    ----------      
    pioche : Pioche
        La pioche de cartes utilisée par le croupier.   
    Methods:
    -------         
    distribuer(joueurs_partie: List[JoueurPartie], nb_cartes: int) -> None
        Distribue un nombre de cartes à chaque joueur.

    """
    def __init__(self):
        self.pioche = Pioche()

    def distribuer(self, joueurs_partie: List[JoueurPartie], nb_cartes: int):
        """Distribue un nombre de cartes à chaque joueur."""
        for _ in range(nb_cartes):
            for jp in joueurs_partie:
                carte = self.pioche.piocher()
                if carte:
                    jp.main.ajouter_carte(carte)