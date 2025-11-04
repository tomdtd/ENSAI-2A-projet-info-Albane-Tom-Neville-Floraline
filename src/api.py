from fastapi import FastAPI, HTTPException, Depends
from src.service.joueur_service import JoueurService
from src.service.table_service import TableService
from src.business_object.joueur import Joueur
from src.business_object.table import Table

app = FastAPI()

# Instancie tes services
joueur_service = JoueurService()
table_service = TableService()

# Créer un joueur
@app.post("/joueurs/")
def creer_joueur(pseudo: str, mdp: str, age: int, mail: str, credit: int):
    joueur = joueur_service.creer(pseudo, mdp, age, mail, credit)
    if joueur:
        return {"message": "Joueur créé avec succès", "joueur": joueur}
    raise HTTPException(status_code=400, detail="Échec de la création du joueur")

# Lister tous les joueurs
@app.get("/joueurs/")
def lister_joueurs():
    joueurs = joueur_service.lister_tous()
    return {"joueurs": joueurs}

# Trouver un joueur par ID
@app.get("/joueurs/{id_joueur}")
def trouver_joueur(id_joueur: int):
    joueur = joueur_service.trouver_par_id(id_joueur)
    if joueur:
        return {"joueur": joueur}
    raise HTTPException(status_code=404, detail="Joueur non trouvé")

# Se connecter
@app.post("/joueurs/connexion")
def se_connecter(pseudo: str, mdp: str):
    joueur = joueur_service.se_connecter(pseudo, mdp)
    if joueur:
        return {"message": "Connexion réussie", "joueur": joueur}
    raise HTTPException(status_code=401, detail="Pseudo ou mot de passe incorrect")

# Créer une table
@app.post("/tables/")
def creer_table(nb_sieges: int, blind_initial: float):
    table = table_service.creer_table(nb_sieges, blind_initial)
    if table:
        return {"message": "Table créée avec succès", "table": table}
    raise HTTPException(status_code=400, detail="Échec de la création de la table")

# Lister les tables disponibles
@app.get("/tables/")
def lister_tables():
    tables = table_service.lister_tables_disponibles()
    return {"tables": tables}

# Rejoindre une table
@app.post("/tables/{id_table}/rejoindre")
def rejoindre_table(id_table: int, joueur_id: int):
    joueur = joueur_service.trouver_par_id(joueur_id)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    success = table_service.rejoindre_table(joueur, id_table)
    if success:
        return {"message": f"Joueur {joueur.pseudo} a rejoint la table {id_table}"}
    raise HTTPException(status_code=400, detail="Impossible de rejoindre la table")

# Quitter une table
@app.post("/tables/{id_table}/quitter")
def quitter_table(id_table: int, joueur_id: int):
    joueur = joueur_service.trouver_par_id(joueur_id)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    success = table_service.quitter_table(joueur, id_table)
    if success:
        return {"message": f"Joueur {joueur.pseudo} a quitté la table {id_table}"}
    raise HTTPException(status_code=400, detail="Impossible de quitter la table")