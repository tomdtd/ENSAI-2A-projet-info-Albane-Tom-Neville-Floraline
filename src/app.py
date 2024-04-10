import os
import logging
import yaml

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from service.joueur_service import JoueurService

app = FastAPI(title="Mon webservice")

# On charge le fichier de config des logs
os.makedirs("logs", exist_ok=True)
stream = open("logging_config.yml", encoding="utf-8")
config = yaml.load(stream, Loader=yaml.FullLoader)
logging.config.dictConfig(config)
logging.info("-" * 50)
logging.info("Lancement du Webservice                        ")
logging.info("-" * 50)

joueur_service = JoueurService()


# Lister tous les joueurs
# GET http://localhost/joueur
@app.get("/joueur/", tags=["Joueurs"])
async def lister_tous_joueurs():
    logging.info("Lister tous les joueurs")
    liste_joueurs = joueur_service.lister_tous()

    liste_model = []
    for joueur in liste_joueurs:
        liste_model.append(joueur)

    return liste_model


# Trouver un joueur à partir de son id
# GET http://localhost/joueur/3
@app.get("/joueur/{id_joueur}", tags=["Joueurs"])
async def joueur_par_id(id_joueur: int):
    logging.info("Trouver un joueur à partir de son id")
    return joueur_service.trouver_par_id(id_joueur)


# Définir un modèle Pydantic pour les Joueurs
class JoueurModel(BaseModel):
    id_joueur: int | None = None  # Champ optionnel
    pseudo: str
    mdp: str
    age: int
    mail: str
    fan_pokemon: bool


# Créer un joueur
@app.post("/joueur/", tags=["Joueurs"])
async def creer_joueur(j: JoueurModel):
    logging.info("Créer un joueur")
    if joueur_service.pseudo_deja_utilise(j.pseudo):
        raise HTTPException(status_code=404, detail="Pseudo déjà utilisé")
    else:
        joueur = joueur_service.creer(j.pseudo, j.mdp, j.age, j.mail, j.fan_pokemon)
        if not joueur:
            raise HTTPException(
                status_code=404, detail="Erreur lors de la création du joueur"
            )
        else:
            return joueur


# Modifier un joueur
@app.put("/joueur/{id_joueur}", tags=["Joueurs"])
def modifier_joueur(id_joueur: int, j: JoueurModel):
    logging.info("Modifier un joueur")
    joueur = joueur_service.trouver_par_id(id_joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")
    else:
        joueur.pseudo = j.pseudo
        joueur.mdp = j.mdp
        joueur.age = j.age
        joueur.mail = j.mail
        joueur.fan_pokemon = j.fan_pokemon
        joueur = joueur_service.modifier(joueur)
        if not joueur:
            raise HTTPException(
                status_code=404, detail="Erreur lors de la modification du joueur"
            )
        else:
            return f"Joueur {j.pseudo} modifié"


# Supprimer un joueur
@app.delete("/joueur/{id_joueur}", tags=["Joueurs"])
def supprimer_joueur(id_joueur: int):
    logging.info("Supprimer un joueur")
    joueur = joueur_service.trouver_par_id(id_joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")
    else:
        joueur_service.supprimer(joueur)
        return f"Joueur {joueur.pseudo} supprimé"


# Afficher Hello
@app.get("/hello/{name}")
async def hello_name(name: str):
    logging.info("Afficher Hello")
    return f"message : Hello {name}"


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)

    logging.info("Arret du Webservice")
