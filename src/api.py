from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from src.service.joueur_service import JoueurService
from src.service.table_service import TableService
from src.business_object.joueur import Joueur
from src.business_object.table import Table

app = FastAPI(title="pickpoker")


# --- ✅ Page d'accueil ---
@app.get("/")
def accueil():
    return {
        "message": "Bienvenue sur l’API PickPoker 🎲",
        "endpoints_disponibles": [
            "/joueurs/ (GET, POST)",
            "/joueurs/{id_joueur} (GET)",
            "/joueurs/connexion (POST)",
            "/tables/ (GET, POST)",
            "/tables/{id_table}/rejoindre (POST)",
            "/tables/{id_table}/quitter (POST)",
            "/docs (Swagger UI)"
        ]
    }


# Instancie tes services
joueur_service = JoueurService()
table_service = TableService()

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to the API documentation"""
    return RedirectResponse(url="/docs")

#Les différents modèles    
# Créer un joueur
class JoueurCreate(BaseModel):
    pseudo: str
    mdp: str
    mail: str
    age: int
    credit: int

class TableCreate(BaseModel):
    nb_sieges: int
    blind_initial: float

class RejoindreTableRequest(BaseModel):
    id_joueur: int

class QuitterTableRequest(BaseModel):
    id_joueur: int

class CartesCommunesRequest(BaseModel):
    cartes: List[str]

class PotRequest(BaseModel):
    montant: float

class DerniereMiseRequest(BaseModel):
    montant: float

@app.post("/joueurs/")
async def creer_joueur(joueur: JoueurCreate):
    joueur_obj = joueur_service.creer(joueur.pseudo, joueur.mdp, joueur.mail, joueur.age, Monnaie(joueur.credit))
    if joueur_obj:
        return {"message": "Joueur créé avec succès", "joueur": joueur_obj}
    raise HTTPException(status_code=400, detail="Échec de la création du joueur")

# Lister tous les joueurs
@app.get("/joueurs/")
async def lister_joueurs():
    joueurs = joueur_service.lister_tous()
    return {"joueurs": joueurs}

# Trouver un joueur par ID
@app.get("/joueurs/{id_joueur}")
async def trouver_joueur(id_joueur: int):
    joueur = joueur_service.trouver_par_id(id_joueur)
    if joueur:
        return {"joueur": joueur}
    raise HTTPException(status_code=404, detail="Joueur non trouvé")

# Se connecter
@app.post("/joueurs/connexion")
async def se_connecter(pseudo: str, mdp: str):
    joueur = joueur_service.se_connecter(pseudo, mdp)
    if joueur:
        return {"message": "Connexion réussie", "joueur": joueur}
    raise HTTPException(status_code=401, detail="Pseudo ou mot de passe incorrect")

# Modifier un joueur
@app.put("/joueurs/{id_joueur}")
async def modifier_joueur(id_joueur: int, pseudo: str = None, mail: str = None, age: int = None, credit: int = None):
    joueur = joueur_service.trouver_par_id(id_joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    if pseudo:
        joueur.pseudo = pseudo
    if mail:
        joueur.mail = mail
    if age:
        joueur.age = age
    if credit is not None:
        joueur.credit = Monnaie(credit)

    joueur_modifie = joueur_service.modifier(joueur)
    if joueur_modifie:
        return {"message": "Joueur modifié avec succès", "joueur": joueur_modifie}
    raise HTTPException(status_code=500, detail="Erreur lors de la modification du joueur")

# Supprimer un joueur
@app.delete("/joueurs/{id_joueur}")
async def supprimer_joueur(id_joueur: int):
    joueur = joueur_service.trouver_par_id(id_joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    success = joueur_service.supprimer(joueur)
    if success:
        return {"message": "Joueur supprimé avec succès"}
    raise HTTPException(status_code=500, detail="Erreur lors de la suppression du joueur")


# Créer une table
@app.post("/tables/")
async def creer_table(nb_sieges: int, blind_initial: float):
    table = table_service.creer_table(nb_sieges, blind_initial)
    if table:
        return {"message": "Table créée avec succès", "table": table}
    raise HTTPException(status_code=400, detail="Échec de la création de la table")

# Lister les tables disponibles
@app.get("/tables/")
async def lister_tables():
    tables = table_service.lister_tables_disponibles()
    return {"tables": tables}

# Rejoindre une table
@app.post("/tables/{id_table}/rejoindre")
async def rejoindre_table(id_table: int, joueur_id: int):
    joueur = joueur_service.trouver_par_id(joueur_id)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    success = table_service.rejoindre_table(joueur, id_table)
    if success:
        return {"message": f"Joueur {joueur.pseudo} a rejoint la table {id_table}"}
    raise HTTPException(status_code=400, detail="Impossible de rejoindre la table")

# Quitter une table
@app.post("/tables/{id_table}/quitter")
async def quitter_table(id_table: int, joueur_id: int):
    joueur = joueur_service.trouver_par_id(joueur_id)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    success = table_service.quitter_table(joueur, id_table)
    if success:
        return {"message": f"Joueur {joueur.pseudo} a quitté la table {id_table}"}
    raise HTTPException(status_code=400, detail="Impossible de quitter la table")

@app.put("/tables/{id_table}/joueur-tour")
def set_id_joueur_tour(id_table: int, id_joueur_tour: Optional[int] = None):
    try:
        success = table_service.set_id_joueur_tour(id_table, id_joueur_tour)
        if success:
            return {"message": "ID du joueur dont c'est le tour mis à jour avec succès"}
        raise HTTPException(status_code=400, detail="Impossible de mettre à jour l'ID du joueur dont c'est le tour")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.put("/tables/{id_table}/flop")
def set_flop(id_table: int, request: CartesCommunesRequest):
    try:
        flop = ListeCartes(request.cartes)
        success = table_service.set_flop(id_table, flop)
        if success:
            return {"message": "Flop mis à jour avec succès"}
        raise HTTPException(status_code=400, detail="Impossible de mettre à jour le flop")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.put("/tables/{id_table}/turn")
def set_turn(id_table: int, request: CartesCommunesRequest):
    try:
        turn = ListeCartes(request.cartes)
        success = table_service.set_turn(id_table, turn)
        if success:
            return {"message": "Turn mis à jour avec succès"}
        raise HTTPException(status_code=400, detail="Impossible de mettre à jour le turn")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.put("/tables/{id_table}/river")
def set_river(id_table: int, request: CartesCommunesRequest):
    try:
        river = ListeCartes(request.cartes)
        success = table_service.set_river(id_table, river)
        if success:
            return {"message": "River mis à jour avec succès"}
        raise HTTPException(status_code=400, detail="Impossible de mettre à jour la river")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.get("/tables/{id_table}/cartes-communes")
def get_cartes_communes(id_table: int):
    try:
        cartes_communes = table_service.get_cartes_communes(id_table)
        return {
            "flop": cartes_communes.get("flop", []),
            "turn": cartes_communes.get("turn", []),
            "river": cartes_communes.get("river", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.post("/tables/{id_table}/alimenter-pot")
def alimenter_pot(id_table: int, request: PotRequest):
    try:
        success = table_service.alimenter_pot(id_table, request.montant)
        if success:
            return {"message": f"Pot alimenté de {request.montant} avec succès"}
        raise HTTPException(status_code=400, detail="Impossible d'alimenter le pot")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.post("/tables/{id_table}/retirer-pot")
def retirer_pot(id_table: int, request: PotRequest):
    try:
        success = table_service.retirer_pot(id_table, request.montant)
        if success:
            return {"message": f"Pot réduit de {request.montant} avec succès"}
        raise HTTPException(status_code=400, detail="Impossible de retirer du pot")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.get("/tables/{id_table}/pot")
def get_pot(id_table: int):
    try:
        montant = table_service.get_pot(id_table)
        return {"montant": montant}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.put("/tables/{id_table}/derniere-mise")
def set_val_derniere_mise(id_table: int, request: DerniereMiseRequest):
    try:
        success = table_service.set_val_derniere_mise(id_table, request.montant)
        if success:
            return {"message": f"Valeur de la dernière mise mise à jour à {request.montant} avec succès"}
        raise HTTPException(status_code=400, detail="Impossible de mettre à jour la valeur de la dernière mise")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.get("/tables/{id_table}/derniere-mise")
def get_val_derniere_mise(id_table: int):
    try:
        montant = table_service.get_val_derniere_mise(id_table)
        return {"montant": montant}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9678)

    logging.info("Arret du Webservice")