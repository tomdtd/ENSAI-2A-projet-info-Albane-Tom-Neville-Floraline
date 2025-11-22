from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from src.service.joueur_service import JoueurService
from src.service.table_service import TableService
from src.service.partie_service import PartieService
from src.service.joueur_partie_service import JoueurPartieService
from src.business_object.joueur import Joueur
from src.business_object.table import Table
from src.business_object.monnaie import Monnaie
from src.service.transaction_service import TransactionService


# --- Page d'accueil ---
ROOT_PATH = "/proxy/9876"

app = FastAPI(root_path=ROOT_PATH, title="PickPoker")


# Instancie tes services
joueur_service = JoueurService()
table_service = TableService()
partie_service = PartieService()
transaction_service = TransactionService()
joueur_partie_service = JoueurPartieService()

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to the API documentation"""
    return RedirectResponse(url="/docs")

#Les différents modèles : on crée des classes pydantic de sorte )à utiliser un json correct et plus simple  
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

class JoueurRequest(BaseModel):
    id_joueur: int

class LancerPartieRequest(BaseModel):
    joueurs: List[JoueurRequest]
    dealer_id: int

# Modèles pour PartieService
class PartieCreateRequest(BaseModel):
    joueurs: List[int]  # Liste des IDs des joueurs
    dealer_id: int

class PartieUpdateRequest(BaseModel):
    id_table: Optional[int] = None
    pot: Optional[float] = None
    date_debut: Optional[datetime] = None

class PeriodeRequest(BaseModel):
    debut: datetime
    fin: datetime    

#Les classes pour les transactions
class TransactionRequest(BaseModel):
    joueur_id: int
    montant: int
class TransactionResponse(BaseModel):
    id_transaction: int
    id_joueur: int
    solde: int
    date: datetime
class AjouterJoueurPartieRequest(BaseModel):
    id_joueur: int
    id_siege: int
    solde_partie: int
    id_table: int

# Modèles pour JoueurPartieService
class AjouterJoueurPartieRequest(BaseModel):
    id_joueur: int
    id_siege: int
    solde_partie: int
    id_table: int

class RetirerJoueurPartieRequest(BaseModel):
    id_joueur: int

class MiserRequest(BaseModel):
    id_joueur: int
    montant: int

class SeCoucherRequest(BaseModel):
    id_joueur: int

class RecupererCartesMainRequest(BaseModel):
    id_table: int
    id_joueur: int

class CartesMainResponse(BaseModel):
    cartes: List[str]

class AttribuerCartesMainRequest(BaseModel):
    id_table: int
    id_joueur: int
    cartes: List[str]

class MettreAJourStatutRequest(BaseModel):
    id_joueur: int
    id_table: int
    statut: str

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
    blind_initial_monnaie = Monnaie(blind_initial)

    table = table_service.creer_table(nb_sieges, blind_initial_monnaie)

    if table:
        return {"message": "Table créée avec succès", "table": table}

    raise HTTPException(status_code=400, detail="Échec de la création de la table, une table n'est pas complète")

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

@app.post("/parties/lancer")
def lancer_partie(request: LancerPartieRequest):
    try:
        joueurs = []
        for joueur_req in request.joueurs:
            joueur = joueur_service.trouver_par_id(joueur_req.id_joueur)
            if not joueur:
                raise HTTPException(status_code=404, detail=f"Joueur {joueur_req.id_joueur} non trouvé")
            joueurs.append(joueur)

        dealer = joueur_service.trouver_par_id(request.dealer_id)
        if not dealer:
            raise HTTPException(status_code=404, detail=f"Dealer {request.dealer_id} non trouvé")

        result = partie_service.lancer_partie(joueurs, dealer.id_joueur)
        if "Erreur" in result:
            raise HTTPException(status_code=400, detail=result)
        return {"message": "Partie lancée avec succès", "id_partie": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.post("/parties/")
def creer_partie(request: PartieCreateRequest):
    try:
        joueurs = []
        for joueur_id in request.joueurs:
            joueur = joueur_service.trouver_par_id(joueur_id)
            if not joueur:
                raise HTTPException(status_code=404, detail=f"Joueur {joueur_id} non trouvé")
            joueurs.append(joueur)

        dealer = joueur_service.trouver_par_id(request.dealer_id)
        if not dealer:
            raise HTTPException(status_code=404, detail=f"Dealer {request.dealer_id} non trouvé")

        result = partie_service.lancer_partie(joueurs, dealer.id_joueur)
        if "Erreur" in result:
            raise HTTPException(status_code=400, detail=result)

        return {"message": "Partie créée avec succès"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.get("/parties/{id_partie}")
def trouver_partie_par_id(id_partie: int):
    try:
        partie = PartieDao().trouver_par_id(id_partie)
        if partie:
            return {"partie": partie}
        raise HTTPException(status_code=404, detail="Partie non trouvée")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.get("/parties/")
def lister_parties():
    try:
        parties = PartieDao().lister_toutes()
        return {"parties": parties}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.put("/parties/{id_partie}")
def modifier_partie(id_partie: int, request: PartieUpdateRequest):
    try:
        partie = PartieDao().trouver_par_id(id_partie)
        if not partie:
            raise HTTPException(status_code=404, detail="Partie non trouvée")

        if request.id_table is not None:
            partie.id_table = request.id_table
        if request.pot is not None:
            partie.pot = Pot(request.pot)
        if request.date_debut is not None:
            partie.date_debut = request.date_debut

        success = PartieDao().modifier(partie)
        if success:
            return {"message": "Partie modifiée avec succès"}
        raise HTTPException(status_code=500, detail="Erreur lors de la modification de la partie")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.delete("/parties/{id_partie}")
def supprimer_partie(id_partie: int):
    try:
        success = PartieDao().supprimer(id_partie)
        if success:
            return {"message": "Partie supprimée avec succès"}
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression de la partie")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.get("/parties/statut/{statut}")
def trouver_parties_par_statut(statut: str):
    try:
        parties = PartieDao().trouver_parties_par_statut(statut)
        return {"parties": parties}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.get("/tables/{id_table}/derniere-partie")
def trouver_derniere_partie_sur_table(id_table: int):
    try:
        partie = PartieDao().trouver_derniere_partie_sur_table(id_table)
        if partie:
            return {"partie": partie}
        raise HTTPException(status_code=404, detail="Aucune partie trouvée sur cette table")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.post("/parties/periode")
def lister_parties_par_periode(request: PeriodeRequest):
    try:
        parties = PartieDao().lister_parties_par_periode(request.debut, request.fin)
        return {"parties": parties}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.post("/transactions/", response_model=TransactionResponse)
def enregistrer_transaction(request: TransactionRequest):
    try:
        transaction = transaction_service.enregistrer_transaction(request.joueur_id, request.montant)
        if transaction:
            return transaction
        raise HTTPException(status_code=400, detail="Échec de l'enregistrement de la transaction")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.get("/transactions/joueur/{joueur_id}", response_model=List[TransactionResponse])
def historique_joueur(joueur_id: int):
    try:
        historique = transaction_service.historique_joueur(joueur_id)
        return historique
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.post("/joueurs-partie/ajouter")
def ajouter_joueur_a_partie(request: AjouterJoueurPartieRequest):
    try:
        joueur = joueur_service.trouver_par_id(request.id_joueur)
        if not joueur:
            raise HTTPException(status_code=404, detail=f"Joueur {request.id_joueur} non trouvé")

        siege = Siege(id_siege=request.id_siege)
        joueur_partie = joueur_partie_service.ajouter_joueur_a_partie(joueur, siege, request.solde_partie, request.id_table)
        if joueur_partie:
            return {"message": "Joueur ajouté à la partie avec succès", "joueur_partie": joueur_partie}
        raise HTTPException(status_code=400, detail="Échec de l'ajout du joueur à la partie")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.post("/joueurs-partie/ajouter")
def ajouter_joueur_a_partie(request: AjouterJoueurPartieRequest):
    try:
        joueur = joueur_service.trouver_par_id(request.id_joueur)
        if not joueur:
            raise HTTPException(status_code=404, detail=f"Joueur {request.id_joueur} non trouvé")

        siege = Siege(id_siege=request.id_siege)
        joueur_partie = joueur_partie_service.ajouter_joueur_a_partie(joueur, siege, request.solde_partie, request.id_table)
        if joueur_partie:
            return {"message": "Joueur ajouté à la partie avec succès", "joueur_partie": joueur_partie}
        raise HTTPException(status_code=400, detail="Échec de l'ajout du joueur à la partie")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.delete("/joueurs-partie/retirer")
def retirer_joueur_de_partie(request: RetirerJoueurPartieRequest):
    try:
        success = joueur_partie_service.retirer_joueur_de_partie(request.id_joueur)
        if success:
            return {"message": f"Joueur {request.id_joueur} retiré de la partie avec succès"}
        raise HTTPException(status_code=400, detail=f"Échec du retrait du joueur {request.id_joueur} de la partie")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.post("/joueurs-partie/miser")
def miser(request: MiserRequest):
    try:
        success = joueur_partie_service.miser(request.id_joueur, request.montant)
        if success:
            return {"message": f"Mise de {request.montant} effectuée avec succès par le joueur {request.id_joueur}"}
        raise HTTPException(status_code=400, detail=f"Échec de la mise pour le joueur {request.id_joueur}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.post("/joueurs-partie/se-coucher")
def se_coucher(request: SeCoucherRequest):
    try:
        success = joueur_partie_service.se_coucher(request.id_joueur)
        if success:
            return {"message": f"Joueur {request.id_joueur} s'est couché avec succès"}
        raise HTTPException(status_code=400, detail=f"Échec du coucher pour le joueur {request.id_joueur}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.get("/joueurs-partie/table/{id_table}")
def lister_joueurs_selon_table(id_table: int):
    try:
        joueurs = joueur_partie_service.lister_joueurs_selon_table(id_table)
        return {"joueurs": joueurs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.get("/joueurs-partie/cartes-main")
def recuperer_cartes_main_joueur(id_table: int, id_joueur: int):
    try:
        cartes = joueur_partie_service.recuperer_cartes_main_joueur(id_table, id_joueur)
        return {"cartes": cartes.cartes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.post("/joueurs-partie/attribuer-cartes-main")
def attribuer_cartes_main_joueur(request: AttribuerCartesMainRequest):
    try:
        cartes = ListeCartes(request.cartes)
        success = joueur_partie_service.attribuer_cartes_main_joueur(request.id_table, request.id_joueur, cartes)
        if success:
            return {"message": f"Cartes attribuées avec succès au joueur {request.id_joueur}"}
        raise HTTPException(status_code=400, detail=f"Échec de l'attribution des cartes au joueur {request.id_joueur}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.put("/joueurs-partie/statut")
def mettre_a_jour_statut(request: MettreAJourStatutRequest):
    try:
        success = joueur_partie_service.mettre_a_jour_statut(request.id_joueur, request.id_table, request.statut)
        if success:
            return {"message": f"Statut du joueur {request.id_joueur} mis à jour avec succès"}
        raise HTTPException(status_code=400, detail=f"Échec de la mise à jour du statut pour le joueur {request.id_joueur}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@app.get("/joueurs-partie/statut")
def obtenir_statut(id_joueur: int, id_table: int):
    try:
        statut = joueur_partie_service.obtenir_statut(id_joueur, id_table)
        return {"statut": statut}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9876)

    logging.info("Arret du Webservice")