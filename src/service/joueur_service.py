from typing import List, Optional
from utils.log_decorator import log
from dao.joueur_dao import JoueurDao
from business_object.joueur import Joueur
from utils.securite import hash_password

class JoueurService:
    """Classe contenant les méthodes de service pour les joueurs."""

    @log
    def creer(self, pseudo: str, mdp: str, mail: str, age: int, credit: int) -> Optional[Joueur]:
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
        credit : int
            Crédit initial du joueur.
        Returns
        -------
        joueur : Joueur
            Le joueur créé si la création est un succès.
            None sinon.
        """
        if not pseudo or not mdp or not mail or age < 0 or credit < 0:
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
        if not id_joueur:
            raise ValueError("L'identifiant du joueur ne peut pas être vide.")

        return JoueurDao().trouver_par_id(id_joueur)

    @log
    def lister_tous(self) -> List[Joueur]:
        """Liste tous les joueurs.
        Returns
        -------
        joueurs : List[Joueur]
            Liste de tous les joueurs.
        """
        return JoueurDao().lister_tous()

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
        if not joueur or not joueur.id_joueur:
            raise ValueError("Le joueur ou son identifiant ne peut pas être vide.")

        if JoueurDao().modifier(joueur):
            return joueur
        return None

    @log
    def supprimer(self, joueur: Joueur) -> bool:
        """Supprime un joueur.
        Parameters
        ----------
        joueur : Joueur
            Le joueur à supprimer.
        Returns
        -------
        success : bool
            True si la suppression est un succès.
            False sinon.
        """
        if not joueur or not joueur.id_joueur:
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
