from datetime import datetime
class Transaction:
    """
    Représente une transaction financière pour un joueur.
    Attributs
    ----------  
    id_transaction : int
        Identifiant unique de la transaction.
    joueur_id : str
        Identifiant du joueur associé à la transaction.
    solde : int
        Montant de la transaction (positif pour un crédit, négatif pour un débit).
    date : datetime
        Date et heure de la transaction.


    """

    def __init__(self, id_transaction: int, joueur_id: str, solde: int, date: datetime):
        if not isinstance(id_transaction, int):
            raise TypeError("id_transaction doit être un entier.")
        if not isinstance(joueur_id, str):
            raise TypeError("joueur_id doit être une chaîne de caractères.")
        if not isinstance(solde, int):
            raise TypeError("solde doit être un entier.")
        if not isinstance(date, datetime):
            raise TypeError("date doit être un objet datetime.")
        self.__id_transaction = id_transaction
        self.__id_joueur = joueur_id
        self.__solde = solde
        self.__date = date

    @property
    def id_transaction(self):
        return self.__id_transaction

    @property
    def id_joueur(self):
        return self.__id_joueur

    @property
    def solde(self):
        return self.__solde

    @property
    def date(self):
        return self.__date

    def __str__(self):
        return f"Transaction {self.__id_transaction} : Joueur {self.__id_joueur}, montant = {self.__solde}, date = {self.__date.strftime('%Y-%m-%d %H:%M:%S')}"

    def __repr__(self):
        return (f"Transaction(id_transaction={self.__id_transaction!r}, "
                f"joueur_id={self.__id_joueur!r}, solde={self.__solde!r}, date={self.__date!r})")