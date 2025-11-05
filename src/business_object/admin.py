class Admin:
    """ 
    Classe des administrateurs du serveur de poker 
    
    Parameters:
    ----------
    admin_id : int
        L'identifiant unique de l'administrateur.               
    name : str
        Le nom de l'administrateur.
    mdp : str
        Le mot de passe de l'administrateur.
    mail : str
        L'adresse e-mail de l'administrateur.
    Méthodes:
    ---------       
    """
    def __init__(self, admin_id, name, mdp, mail):

        self.admin_id = admin_id
        self.name = name
        self.mdp = mdp
        self.mail = mail

    def changer_mdp(self, last_mdp, new_mdp: str) -> None:
        """Permet à l'administrateur de changer son mot de passe."""
        if self.mdp != last_mdp: 
            print("Mot de passe actuel incorrect.")
        else : 
            self.mdp = new_mdp
            print(f"Le mot de passe de l'administrateur {self.name} a été changé.")