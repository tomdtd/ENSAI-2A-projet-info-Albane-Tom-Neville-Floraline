from typing import List, Optional
from src.utils.log_decorator import log
from src.dao.joueur_dao import JoueurDao
from src.business_object.joueur import Joueur
from src.utils.securite import hash_password
from src.business_object.monnaie import Monnaie

class JoueurService:
    """Classe contenant les méthodes de service pour les joueurs."""

    @log
    def creer(self, pseudo: str, mdp: str, mail: str, age: int, credit: Monnaie) -> Optional[Joueur]:
        """Crée un nouveau joueur.
        Parameters
        ----------
        pseudo : str
            Pseudo du joueur.
        mdp : str
            Mot de passe du joueur.
        mail : str
            Adresse mail du joueur.
        age : int
            Âge du joueur.
        credit : Monnaie
            Crédit initial du joueur.
        Returns
        -------
        joueur : Joueur
            Le joueur créé si la création est un succès.
            None sinon.
        """
        if not pseudo or not mdp or not mail or age < 0 or credit.get() < 0:
            raise ValueError("Les paramètres ne sont pas valides.")
        mdp_hashe = hash_password(mdp, pseudo)
        joueur = Joueur(pseudo=pseudo, mail=mail, credit=credit, mdp=mdp_hashe, age=age)
        if JoueurDao().creer(joueur):
            return joueur
        return None

    @log
    def trouver_par_id(self, id_joueur: int) -> Optional[Joueur]:
        """Trouve un joueur par son identifiant.
        Parameters
        ----------
        id_joueur : int
            Identifiant du joueur.
        Returns
        -------
        joueur : Joueur
            Le joueur trouvé si l'identifiant est valide.
            None sinon.
        """
        if id_joueur is None:
            raise ValueError("L'identifiant du joueur ne peut pas être vide.")

        return JoueurDao().trouver_par_id(id_joueur)

    @log
    def lister_tous(self, inclure_mdp=False) -> List[Joueur]:
        """Liste tous les joueurs.
        Si tous les mots de passe sont à True, ils sont renvoyés également
        Returns
        -------
        joueurs : List[Joueur]
            Liste de tous les joueurs.
        """
        joueurs = JoueurDao().lister_tous()
        if not inclure_mdp:
            for j in joueurs:
                j.mdp = None
        return joueurs

    @log
    def modifier(self, joueur: Joueur) -> Optional[Joueur]:
        """Modifie les informations d'un joueur.
        Parameters
        ----------
        joueur : Joueur
            Le joueur à modifier.
        Returns
        -------
        joueur : Joueur
            Le joueur modifié si la modification est un succès.
            None sinon.
        """
        if joueur is None or not joueur.id_joueur:
            raise ValueError("Le joueur ou son identifiant ne peut pas être vide.")

        joueur.mdp = hash_password(joueur.mdp, joueur.pseudo)
        return joueur if JoueurDao().modifier(joueur) else None

     
    @log
    def supprimer(self, joueur: Joueur) -> bool:
        if joueur is None or not joueur.id_joueur:
            raise ValueError("Le joueur ou son identifiant ne peut pas être vide.")
        return JoueurDao().supprimer(joueur)
        
    @log
    def se_connecter(self, pseudo: str, mdp: str) -> Optional[Joueur]:
        """Connecte un joueur avec son pseudo et son mot de passe.
        Parameters
        ----------
        pseudo : str
            Pseudo du joueur.
        mdp : str
            Mot de passe du joueur.
        Returns
        -------
        joueur : Joueur
            Le joueur connecté si les identifiants sont corrects.
            None sinon.
        """
        if not pseudo or not mdp:
            raise ValueError("Le pseudo et le mot de passe ne peuvent pas être vides.")

        mdp_hashe = hash_password(mdp, pseudo)
        return JoueurDao().se_connecter(pseudo, mdp_hashe)

    @log
    def changer_mot_de_passe(self, joueur: Joueur, ancien_mdp: str, nouveau_mdp: str) -> bool:
        """Change le mot de passe d'un joueur.
        Parameters
        ----------
        joueur : Joueur
            Le joueur dont le mot de passe doit être changé.
        ancien_mdp : str
            L'ancien mot de passe.
        nouveau_mdp : str
            Le nouveau mot de passe.
        Returns
        -------
        success : bool
            True si le changement de mot de passe est un succès.
            False sinon.
        """
        if not joueur or not ancien_mdp or not nouveau_mdp:
            raise ValueError("Le joueur, l'ancien mot de passe et le nouveau mot de passe ne peuvent pas être vides.")

        if joueur.mdp != hash_password(ancien_mdp, joueur.pseudo):
            raise ValueError("L'ancien mot de passe est incorrect.")

        joueur.mdp = hash_password(nouveau_mdp, joueur.pseudo)
        return JoueurDao().modifier(joueur)
    
    @log
    def pseudo_deja_utilise(self, pseudo) -> bool:
        """Vérifie si le pseudo est déjà utilisé
        Retourne True si le pseudo existe déjà en BDD"""
        joueurs = JoueurDao().lister_tous()
        return pseudo in [j.pseudo for j in joueurs]

    @log
    def modifier_credit(self, id_joueur: int, credit: int) -> bool:
        """Modifie le crédit (valeur absolue) d'un joueur.
        
        Parameters
        ----------
        id_joueur : int
            Identifiant du joueur.
        credit : int
            Nouvelle valeur du crédit (valeur absolue).
        
        Returns
        -------
        bool
            True si la mise à jour a réussi, False sinon.
        """
        if id_joueur is None:
            raise ValueError("L'identifiant du joueur ne peut pas être vide.")
        if credit < 0:
            raise ValueError("Le crédit ne peut pas être négatif.")
        # créer un objet Monnaie si ton DAO attend .get() sur Monnaie ; sinon on peut envoyer Decimal/str
        credit_bo = Monnaie(credit)
        return JoueurDao().modifier_credit(id_joueur, credit_bo)
    
    @log
    def recuperer_credit(self, id_joueur: int) -> Monnaie():
        """Récupère le crédit d'un joueur par son identifiant.

        Parameters
        ----------
        id_joueur : int
            Identifiant du joueur.

        Returns
        -------
        Monnaie | None
            Le crédit du joueur si trouvé, sinon None.
        """
        if id_joueur is None:
            raise ValueError("L'identifiant du joueur ne peut pas être vide.")

        return JoueurDao().recuperer_credit(id_joueur)