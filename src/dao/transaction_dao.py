import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.transaction import Transaction


class TransactionDao(metaclass=Singleton):
    @log
    def creer(self, transaction) -> bool:
        """Creation d'une transaction dans la base de données

        Parameters
        ----------
        transaction : Transaction

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO transaction (id_transaction, id_joueur, solde, date)"
                        "VALUES (%(id_transaction)s, %(id_joueur)s, %(solde)s, %(date)s)"
                        "RETURNING id_transaction;                                              ",
                        {
                            "id_transaction": transaction.id_transaction,
                            "id_joueur": transaction.id_joueur,
                            "solde": transaction.solde,
                            "date": transaction.date
                        },
                    )
                    res = cursor.fetchone()
                connection.commit() 
        except Exception as e:
            #logging.info(e)
            logging.exception("Erreur lors de la création du joueur")

        created = False
        if res:
            transaction.id_transaction = res["id_transaction"]
            created = True

        return created
    
    @log
    def lister_par_joueur(self, joueur_id: int) -> list[Transaction]:
        """Retourne toutes les transactions d’un joueur depuis la base"""
        transactions = []
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_transaction, id_joueur, solde, date "
                        "FROM transaction WHERE id_joueur = %(id_joueur)s "
                        "ORDER BY date ASC;",
                        {"id_joueur": joueur_id}
                    )
                    rows = cursor.fetchall()
                    for row in rows:
                        transactions.append(Transaction(
                            id_transaction=row["id_transaction"],
                            id_joueur=row["id_joueur"],
                            solde=row["solde"],
                            date=row["date"]
                        ))
        except Exception as e:
            logging.exception("Erreur lors de la récupération des transactions")
        return transactions