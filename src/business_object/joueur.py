class Joueur:
    """
    Classe représentant un Joueur

    Attributs
    ----------
    id_joueur : int
        identifiant
    pseudo : str
        pseudo du joueur
    mdp : str
        le mot de passe du joueur
    credit : int
        nombre de crédits du joueur
    mail : str
        adresse mail du joueur 
    age : int
        age du joueur
    solde : Monnaie
        solde du joueur 
    """

    def __init__(self, pseudo, mail, credit, mdp, id_joueur, age, date_creation):
        """Constructeur"""
        self.id_joueur = id_joueur
        self.pseudo = pseudo
        self.mdp = mdp
        self.mail = mail
        self.credit = credit
        self.age = age  

    def __str__(self):
        """Permet d'afficher les informations du joueur"""
        return f"Joueur({self.pseudo}, {self.mail} ans)"
    
    def __repr__(self) -> str:
        return f"Joueur(id={self.id_joueur}, pseudo='{self.pseudo}', solde={self.solde.get()})"

    def crediter(self, montant: int):
        """Crédite le solde du joueur."""
        self.solde.crediter(montant)

    def debiter(self, montant: int):
        """Débite le solde du joueur."""
        self.solde.debiter(montant)

    def jouer_partie(self):
        """Action pour qu'un joueur rejoigne ou démarre une partie."""
        print(f"Le joueur {self.pseudo} entre dans une partie.")

    def changer_mdp(self, last_mdp, new_mdp: str) -> None:
        """Permet à l'administrateur de changer son mot de passe."""
        if self.mdp != last_mdp: 
            print("Mot de passe actuel incorrect.")
        else : 
            self.mdp = new_mdp
            print(f"Le mot de passe de l'administrateur {self.name} a été changé.")

