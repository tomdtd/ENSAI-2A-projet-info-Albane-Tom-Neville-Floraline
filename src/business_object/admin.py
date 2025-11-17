class Admin:
    """ 
    Classe des administrateurs du serveur de poker 
    
    Parameters:
    ----------
    nom : str
        Le nom de l'administrateur.
    mdp : str
        Le mot de passe de l'administrateur.
    mail : str
        L'adresse e-mail de l'administrateur.
    admin_id : int, optional
        L'identifiant unique de l'administrateur (auto-généré par la base de données).
        
    Méthodes:
    ---------       
    """
    def __init__(self, nom: str, mdp: str, mail: str, admin_id: int = None):
        self.admin_id = admin_id  # Peut être None pour les nouvelles créations
        self.nom = nom
        self.mdp = mdp
        self.mail = mail

    def __str__(self):
        """Permet d'afficher les informations de l'administrateur"""
        return f"Admin(id={self.admin_id}, nom='{self.nom}', mail='{self.mail}')"
    
    def __repr__(self) -> str:
        return f"Admin(admin_id={self.admin_id}, nom='{self.nom}', mail='{self.mail}')"

    def changer_mdp(self, last_mdp: str, new_mdp: str) -> bool:
        """Permet à l'administrateur de changer son mot de passe.
        
        Parameters:
        ----------
        last_mdp : str
            L'ancien mot de passe
        new_mdp : str
            Le nouveau mot de passe
            
        Returns:
        -------
        bool
            True si le changement a réussi, False sinon
        """
        if self.mdp != last_mdp: 
            print("Mot de passe actuel incorrect.")
            return False
        else: 
            self.mdp = new_mdp
            print(f"Le mot de passe de l'administrateur {self.nom} a été changé.")
            return True