from datetime import datetime
class Transaction:
    """
    Représente une transaction financière pour un joueur.
    Attributs
    ----------  
    id_transaction : int
        L'identifiant unique de la transaction.
    id_joueur : int
        L'identifiant du joueur associé à la transaction.
    montant : int
        Le montant de la transaction.   
    date : datetime
        La date et l'heure de la transaction.
    Méthodes    
    ---------  
    __repr__() -> str       
        Retourne une représentation textuelle d'une transaction.
    """
    def __init__(self, id_transaction: int, id_joueur: int, montant: int):
        self.id_transaction = id_transaction
        self.id_joueur = id_joueur
        self.solde = solde
        self.date = datetime.now()

    def __repr__(self) -> str:
        return f"Transaction(id={self.id_transaction}, joueur={self.id_joueur}, solde={self.solde})"
