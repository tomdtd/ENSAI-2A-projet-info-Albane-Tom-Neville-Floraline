import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os

#Récupération des informations de connection
load_dotenv(".env_test")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

# Connexion à PostgreSQL sur la base par défaut
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)


# Important : on doit activer l'autocommit pour CREATE DATABASE
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = conn.cursor()

# Création de la base de donnée 
try:
    cur.execute(f"CREATE DATABASE prod_poker;")
    print(f"Base de données 'prod_poker' créée avec succès !")
except psycopg2.errors.DuplicateDatabase:
    print(f"La base 'prod_poker' existe déjà.")

cur.close()
conn.close()
print("Base de données 'prod_poker' créée avec succès !")

# Création des tables
conn = psycopg2.connect(
    dbname="prod_poker",
    user=user,
    password=password,
    host=host,
    port=port
)
cur = conn.cursor()

with open("data/init_db.sql", "r", encoding="utf-8") as f:
    sql_file = f.read()

# Séparer les commandes SQL par ';' et exécuter une par une
sql_commands = sql_file.split(";")
for command in sql_commands:
    command = command.strip()
    if command:  # Ignorer les commandes vides
        cur.execute(command)

conn.commit()
cur.close()
conn.close()
print(f"Tables créées avec succès dans la base 'prod_poker' !")