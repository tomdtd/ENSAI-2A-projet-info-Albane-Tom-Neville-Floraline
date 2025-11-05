"""Implementation de la classe Transaction."""

from datetime import datetime

class Transaction :
    """
    La classe Transaction modélise une opération financière
    (crédit ou débit) effectuée par un joueur.

    Parameters
    ----------
    id_transaction : int
        Identifiant unique de la transaction.
    id_joueur : str
        Identifiant du joueur associé à la transaction.
    solde : int
        Montant de la transaction (positif pour un crédit, négatif pour un débit).
    date : datetime
        Date et heure de la transaction.


    """

    def __init__(self, id_joueur: str, solde: int, date: datetime, id_transaction: int = None):
        if id_transaction is not None and not isinstance(id_transaction, int):
            raise TypeError("id_transaction doit être un entier.")
        if not isinstance(id_joueur, int):
            raise TypeError("id_joueur doit être un entier.")
        if not isinstance(solde, int):
            raise TypeError("solde doit être un entier.")
        if not isinstance(date, datetime):
            raise TypeError("date doit être un objet datetime.")
        self.__id_transaction = id_transaction
        self.__id_joueur = id_joueur
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

    @id_transaction.setter
    def id_transaction(self, value):
        """Setter pour permettre à la DAO d'assigner l'ID généré par la base."""
        if not isinstance(value, int):
            raise TypeError("id_transaction doit être un entier.")
        self.__id_transaction = value
