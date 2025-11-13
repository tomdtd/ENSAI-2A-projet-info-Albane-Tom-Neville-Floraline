import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connexion à PostgreSQL sur la base par défaut (ex: defautdb) # a changer pour que ca aille chercher dans le .env_test
conn = psycopg2.connect(
    dbname="defaultdb",
    user="user-arouille",
    password="9r8fyvvwc6d7dh4fen8q",
    host="postgresql-163390.user-arouille",
    port="5432"
)

# Important : on doit activer l'autocommit pour CREATE DATABASE
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = conn.cursor()

# Création de la base de donnée 
cur.execute("CREATE DATABASE prod_poker;")

cur.close()
conn.close()
print("Base de données 'prod_poker' créée avec succès !")
