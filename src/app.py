from fastapi import FastAPI
from pydantic import BaseModel

from dto.joueur import Joueur
from service.joueur_service import JoueurService

app = FastAPI()

joueur_service = JoueurService()


# List all pokemons
# GET http://localhost/joueur
@app.get("/joueur/")
async def lister_tous_joueurs():
    liste_joueurs = joueur_service.lister_tous()

    # Convert all pokemons using the model
    liste_model = []
    for joueur in liste_joueurs:
        liste_model.append(joueur)

    return liste_model


# Trouver un joueur à partir de son id
@app.get("/joueur/{id_joueur}")
async def joueur_par_nom(id_joueur: int):
    return joueur_service.trouver_par_id(id_joueur)


# Définir un modèle Pydantic pour les Joueurs
class JoueurModel(BaseModel):
    pseudo: str
    mdp: str
    age: int
    mail: str
    fan_pokemon: bool


# Créer un joueur
@app.post("/joueur/")
async def creer_joueur(j: JoueurModel):
    return joueur_service.creer(j.pseudo, j.mdp, j.age, j.mail, j.fan_pokemon)


# Afficher Hello
@app.get("/hello/{name}")
async def get_hello_name(name: str):
    return {"message": "Hello {}".format(name)}


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
