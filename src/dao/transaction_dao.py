import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.transaction import Transaction


class TransactionDao(metaclass=Singleton):
    pass