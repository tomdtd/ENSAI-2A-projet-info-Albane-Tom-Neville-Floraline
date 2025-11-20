from datetime import datetime
from typing import Optional


class Transaction:
    """
    Représente une transaction financière pour un joueur.
    Attributs
    ----------
    id_transaction : int
        Identifiant unique de la transaction.
    id_joueur : int
        Identifiant du joueur associé à la transaction.
    solde : int
        Montant de la transaction (positif pour un crédit, négatif pour un débit).
    date : datetime
        Date et heure de la transaction.
    statut : str
        Statut de la transaction ('en_attente', 'validee', 'rejetee').
    id_admin : int, optional
        Identifiant de l'administrateur qui a validé/rejeté la transaction.
    date_validation : datetime, optional
        Date de validation/rejet de la transaction.
    """

    def __init__(self, solde: int, date: datetime, id_joueur: int=None, id_transaction: int=None,
                 statut: str='en_attente', id_admin: Optional[int]=None,
                 date_validation: Optional[datetime]=None):
        if not id_transaction is None and not isinstance(id_transaction, int):
            raise TypeError("id_transaction doit être un entier.")
        if not id_joueur is None and not isinstance(id_joueur, int):
            raise TypeError("id_joueur doit être un entier.")
        if not isinstance(solde, int):
            raise TypeError("solde doit être un entier.")
        if not isinstance(date, datetime):
            raise TypeError("date doit être un objet datetime.")
        if not isinstance(statut, str):
            raise TypeError("statut doit être une chaîne de caractères.")
        if statut not in ['en_attente', 'validee', 'rejetee']:
            raise ValueError("statut doit être 'en_attente', 'validee' ou 'rejetee'.")
        if id_admin is not None and not isinstance(id_admin, int):
            raise TypeError("id_admin doit être un entier ou None.")
        if date_validation is not None and not isinstance(date_validation, datetime):
            raise TypeError("date_validation doit être un objet datetime ou None.")

        self.__id_transaction = id_transaction
        self.__id_joueur = id_joueur
        self.__solde = solde
        self.__date = date
        self.__statut = statut
        self.__id_admin = id_admin
        self.__date_validation = date_validation

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

    @property
    def statut(self):
        return self.__statut

    @property
    def id_admin(self):
        return self.__id_admin

    @property
    def date_validation(self):
        return self.__date_validation

    def __str__(self):
        return (f"Transaction {self.__id_transaction} : Joueur {self.__id_joueur}, "
                f"montant = {self.__solde}, date = {self.__date.strftime('%Y-%m-%d %H:%M:%S')}, "
                f"statut = {self.__statut}")

    def __repr__(self):
        return (f"Transaction(id_transaction={self.__id_transaction!r}, "
                f"id_joueur={self.__id_joueur!r}, solde={self.__solde!r}, date={self.__date!r}, "
                f"statut={self.__statut!r}, id_admin={self.__id_admin!r}, "
                f"date_validation={self.__date_validation!r})")

    @id_transaction.setter
    def id_transaction(self, value):
        """Setter pour permettre à la DAO d'assigner l'ID généré par la base."""
        if not isinstance(value, int):
            raise TypeError("id_transaction doit être un entier.")
        self.__id_transaction = value

    @statut.setter
    def statut(self, value):
        """Setter pour permettre la modification du statut."""
        if not isinstance(value, str):
            raise TypeError("statut doit être une chaîne de caractères.")
        if value not in ['en_attente', 'validee', 'rejetee']:
            raise ValueError("statut doit être 'en_attente', 'validee' ou 'rejetee'.")
        self.__statut = value

    @id_admin.setter
    def id_admin(self, value):
        """Setter pour permettre d'assigner l'ID de l'admin."""
        if value is not None and not isinstance(value, int):
            raise TypeError("id_admin doit être un entier ou None.")
        self.__id_admin = value

    @date_validation.setter
    def date_validation(self, value):
        """Setter pour permettre d'assigner la date de validation."""
        if value is not None and not isinstance(value, datetime):
            raise TypeError("date_validation doit être un objet datetime ou None.")
        self.__date_validation = value