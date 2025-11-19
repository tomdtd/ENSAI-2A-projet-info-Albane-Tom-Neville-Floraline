from typing import Optional, List
from src.utils.log_decorator import log
from src.dao.joueur_partie_dao import JoueurPartieDao
from src.business_object.joueur_partie import JoueurPartie
from src.business_object.joueur import Joueur
from src.business_object.siege import Siege
from src.business_object.monnaie import Monnaie
from src.business_object.liste_cartes import ListeCartes

class JoueurPartieService:
    """Classe contenant les méthodes de service pour les joueurs dans une partie."""

    @log
    def ajouter_joueur_a_partie(self, joueur: Joueur, siege: Siege, solde_partie: int, id_table: int) -> Optional[JoueurPartie]:
        """Ajoute un joueur à une partie.
        Parameters
        ----------
        joueur : Joueur
            Le joueur à ajouter à la partie.
        siege : Siege
            Le siège occupé par le joueur dans la partie.
        solde_partie : int
            Le solde initial du joueur pour cette partie.
        id_table : int
            L'identifiant de la partie.
        Returns
        -------
        joueur_partie : JoueurPartie
            L'objet JoueurPartie créé si l'ajout est un succès.
            None sinon.
        """
        if not joueur or not joueur.id_joueur:
            raise ValueError("Le joueur doit avoir un identifiant valide.")
        # if not siege or not siege.id_siege:
        #     raise ValueError("Le siège doit avoir un identifiant valide.")
        if solde_partie < 0:
            raise ValueError("Le solde de la partie ne peut pas être négatif.")

        joueur_partie = JoueurPartie(joueur=joueur, siege=siege, solde_partie=solde_partie)
        if JoueurPartieDao().creer(joueur_partie, id_table):
            return joueur_partie
        return None

    @log
    def retirer_joueur_de_partie(self, id_joueur: int) -> bool:
        """Retire un joueur d'une partie.
        Parameters
        ----------
        id_joueur : int
            L'identifiant du joueur à retirer de la partie.
        Returns
        -------
        deleted : bool
            True si le joueur a bien été retiré.
            False sinon.
        """
        if not id_joueur:
            raise ValueError("L'identifiant du joueur ne peut pas être vide.")

        return JoueurPartieDao().supprimer(id_joueur)

    @log
    def miser(self, id_joueur: int, montant: int) -> bool:
        """Permet à un joueur de miser un certain montant.
        Parameters
        ----------
        id_joueur : int
            L'identifiant du joueur.
        montant : int
            Le montant à miser.
        Returns
        -------
        success : bool
            True si la mise a été effectuée avec succès.
            False sinon.
        """
        if montant <= 0:
            raise ValueError("Le montant de la mise doit être positif.")

        joueur_partie = self._trouver_joueur_partie_par_id_joueur(id_joueur)
        if not joueur_partie:
            raise ValueError("Joueur non trouvé dans la partie.")

        joueur_partie.miser(montant)
        return True

    @log
    def se_coucher(self, id_joueur: int) -> bool:
        """Permet à un joueur de se coucher.
        Parameters
        ----------
        id_joueur : int
            L'identifiant du joueur.
        Returns
        -------
        success : bool
            True si le joueur s'est couché avec succès.
            False sinon.
        """
        joueur_partie = self._trouver_joueur_partie_par_id_joueur(id_joueur)
        if not joueur_partie:
            raise ValueError("Joueur non trouvé dans la partie.")

        joueur_partie.se_coucher()
        return True

    def _trouver_joueur_partie_par_id_joueur(self, id_joueur: int) -> Optional[JoueurPartie]:
        """Trouve un JoueurPartie par l'identifiant du joueur.
        Parameters
        ----------
        id_joueur : int
            L'identifiant du joueur.
        Returns
        -------
        joueur_partie : JoueurPartie
            L'objet JoueurPartie trouvé.
            None sinon.
        """
        # Note: Cette méthode est un placeholder. En réalité, il faudrait interroger la base de données
        # pour récupérer le JoueurPartie correspondant à l'id_joueur.
        # Pour l'instant, on retourne None pour indiquer que cette méthode n'est pas implémentée.
        return None
    
    def lister_joueurs_selon_table(self, id_table: int) -> list[int]:
        """Liste tous les JoueurPartie sur une table.
        Parameters
        ----------
        id_table : int
            L'identifiant de la table.
        Returns
        -------
        joueur_table : lst[int]
            Liste des id des JoueurPartie trouvé.
            Liste vide sinon.
        """
        joueurs = JoueurPartieDao().trouver_par_table(id_table)
        return joueurs if joueurs else []
    
    @log
    def recuperer_cartes_main_joueur(self, id_table: int, id_joueur: int) -> ListeCartes:
        """Récupère la main d'un joueur pour une partie spécifique.
        Parameters
        ----------
        id_table : int
            L'identifiant de la table/partie
        id_joueur : int
            L'identifiant du joueur
        Returns
        -------
        main : ListeCartes
            La main du joueur, vide si non trouvée.
        """
        return JoueurPartieDao().trouver_cartes_main_joueur(id_table, id_joueur)
    
    @log
    def attribuer_cartes_main_joueur(self, id_table: int, id_joueur: int, main: ListeCartes) -> bool:
        """Attribue une main de cartes à un joueur pour une partie spécifique.
        Parameters
        ----------
        id_table : int
            L'identifiant de la table/partie
        id_joueur : int
            L'identifiant du joueur
        main : ListeCartes
            La main à attribuer
        Returns
        -------
        success : bool
            True si l'attribution a réussi, False sinon.
        """
        if not isinstance(main, ListeCartes):
            raise ValueError("main doit être un objet ListeCartes.")
        return JoueurPartieDao().donner_cartes_main_joueur(id_table, id_joueur, main)
    
    @log
    def mettre_a_jour_statut(self, id_joueur: int, id_table: int, statut: str) -> bool:
        """Met à jour le statut d'un joueur dans une partie.

        Parameters
        ----------
        id_joueur : int
            L'identifiant du joueur.
        id_table : int
            L'identifiant de la table.
        statut : str
            Nouveau statut : 'en attente', 'tour de blinde', 'tour petite blinde', 'en jeu', 's'est couché', ...

        Returns
        -------
        success : bool
            True si la mise à jour a été effectuée avec succès.
        """
        if not id_joueur or not id_table:
            raise ValueError("id_joueur et id_table sont requis.")
        if statut not in ['en attente', 'tour de blinde', 'tour petite blinde', 'en jeu', "s'est couché"]:
            raise ValueError(f"Statut invalide : {statut}")
        return JoueurPartieDao().modifier_statut(id_joueur, id_table, statut)
    
    @log
    def obtenir_statut(self, id_joueur: int, id_table: int) -> str:
        """Retourne le statut actuel d'un joueur dans une partie.

        Parameters
        ----------
        id_joueur : int
            L'identifiant du joueur.
        id_table : int
            L'identifiant de la table.

        Returns
        -------
        statut : str
            Statut du joueur, ou None si non trouvé.
        """
        if not id_joueur or not id_table:
            raise ValueError("id_joueur et id_table sont requis.")
        return JoueurPartieDao().recuperer_statut(id_joueur, id_table)
