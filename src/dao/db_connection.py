import os
import logging
import dotenv
import psycopg2

from psycopg2.extras import RealDictCursor
from utils.singleton import Singleton


class DBConnection(metaclass=Singleton):
    """
    Classe de connexion à la base de données
    Elle permet de n'ouvrir qu'une seule et unique connexion
    """

    def __init__(self):
        dotenv.load_dotenv()

        # Ouvrir la connexion
        self.__connection = psycopg2.connect(
            host=os.environ["HOST"],
            port=os.environ["PORT"],
            database=os.environ["DATABASE"],
            user=os.environ["USER"],
            password=os.environ["PASSWORD"],
            options=f"-c search_path={os.environ['SCHEMA']}",
            cursor_factory=RealDictCursor,
        )

    @property
    def connection(self):
        return self.__connection
