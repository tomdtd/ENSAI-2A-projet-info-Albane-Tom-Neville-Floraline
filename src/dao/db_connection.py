import os
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
        """Ouverture de la connexion"""
        dotenv.load_dotenv()

        self.__connection = psycopg2.connect(
                host=os.environ["POSTGRES_HOST"],
                port=os.environ["POSTGRES_PORT"],
                database=os.environ["POSTGRES_DATABASE"],
                user=os.environ["POSTGRES_USER"],
                password=os.environ["POSTGRES_PASSWORD"],
                cursor_factory=RealDictCursor,
            )

    # @property
    # def connection(self):
    #     return self.__connection
    @property
    def connection(self):
        try:
            # Test rapide pour voir si la connexion est encore valide
            self.__connection.cursor().execute("SELECT 1")
        except (psycopg2.InterfaceError, psycopg2.OperationalError):
            # Reconnecte si la connexion est fermée ou perdue
            self.__connection = psycopg2.connect(
                host=os.environ["POSTGRES_HOST"],
                port=os.environ["POSTGRES_PORT"],
                database=os.environ["POSTGRES_DATABASE"],
                user=os.environ["POSTGRES_USER"],
                password=os.environ["POSTGRES_PASSWORD"],
                cursor_factory=RealDictCursor,
            )
        return self.__connection