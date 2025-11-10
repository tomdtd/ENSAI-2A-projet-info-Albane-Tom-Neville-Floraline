from typing import Dict, List, Optional, Tuple
from datetime import datetime

from src.business_object.deroulement_partie import DeroulementPartie
from src.business_object.joueur import Joueur
from src.business_object.joueur_partie import JoueurPartie
from src.business_object.transaction import Transaction
from src.business_object.pot import Pot
from src.business_object.partie import Partie
from src.business_object.monnaie import Monnaie


class DeroulementPartieDao:
    """
    DAO pour gérer le déroulement d'une partie.
    """

    def __init__(self):
        self._sessions: Dict[int, DeroulementPartie] = {}
        self._next_id: int = 1

    # --- Création et récupération de session ---
    def creer_session(self, joueurs: List[Joueur], big_blind: int, small_blind: int) -> int:
        """Crée et enregistre une nouvelle session DeroulementPartie. Retourne l'id de session."""
        session = DeroulementPartie(joueurs=joueurs, big_blind=big_blind, small_blind=small_blind)
        session_id = self._next_id
        self._sessions[session_id] = session
        self._next_id += 1
        return session_id

    def get_session(self, session_id: int) -> Optional[DeroulementPartie]:
        """Retourne la session si elle existe, sinon None."""
        return self._sessions.get(session_id)

    def supprimer_session(self, session_id: int) -> bool:
        """Supprime une session et retourne True si succès."""
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def lister_sessions(self) -> List[Tuple[int, DeroulementPartie]]:
        """Liste toutes les sessions avec leur id."""
        return list(self._sessions.items())

    # --- Contrôle de la partie ---
    def lancer_partie(self, session_id: int) -> bool:
        """Lance la partie pour une session donnée."""
        session = self.get_session(session_id)
        if not session:
            return False
        session.lancer_partie()
        return True

    def terminer_partie(self, session_id: int) -> bool:
        """Termine la partie si elle est en cours."""
        session = self.get_session(session_id)
        if not session or not session.partie:
            return False
        session.partie.finir_partie()
        return True

    # --- Accès aux entités ---
    def get_partie(self, session_id: int) -> Optional[Partie]:
        """Retourne l'objet Partie courant."""
        session = self.get_session(session_id)
        return session.partie if session else None

    def get_pot(self, session_id: int) -> Optional[Pot]:
        """Retourne le pot de la session."""
        session = self.get_session(session_id)
        return session.pot if session else None

    def get_transactions(self, session_id: int) -> List[Transaction]:
        """Liste les transactions de la session."""
        session = self.get_session(session_id)
        return session.transactions[:] if session else []

    def get_joueurs_partie(self, session_id: int) -> List[JoueurPartie]:
        """Liste les JoueurPartie de la session."""
        session = self.get_session(session_id)
        return session.joueurs_partie[:] if session else []

    # --- Mises à jour contrôlées ---
    def collecter_blinds(self, session_id: int) -> bool:
        """Déclenche la collecte des blinds sur la session."""
        session = self.get_session(session_id)
        if not session:
            return False
        session._collecter_blinds()
        return True

    def tour_de_table(self, session_id: int, phase: str) -> bool:
        """Exécute un tour de table pour la phase donnée (Pré-flop, Flop, Turn, River)."""
        session = self.get_session(session_id)
        if not session:
            return False
        session._tour_de_table(phase)
        return True

    def enregistrer_transaction(self, session_id: int, transaction: Transaction) -> bool:
        """Ajoute une transaction manuelle à la session (utile pour tests, rake, ajustements)."""
        session = self.get_session(session_id)
        if not session:
            return False
        session.transactions.append(transaction)
        # Alimente le pot si solde négatif (mise), crédite si positif (gain)
        solde = transaction.solde
        if isinstance(solde, Monnaie):
            montant = solde.get()
        else:
            montant = solde
        if montant < 0:
            session.pot.ajouter_mise(-montant)
        return True

    # --- Requêtes utilitaires ---
    def get_montant_pot(self, session_id: int) -> Optional[int]:
        """Retourne le montant numérique du pot."""
        session = self.get_session(session_id)
        if not session:
            return None
        montant = session.pot.get_montant()
        return montant.get() if hasattr(montant, "get") else montant

    def get_blinds(self, session_id: int) -> Optional[Tuple[int, int]]:
        """Retourne (small_blind, big_blind) en entier."""
        session = self.get_session(session_id)
        if not session:
            return None
        sb = session.small_blind.get() if hasattr(session.small_blind, "get") else session.small_blind
        bb = session.big_blind.get() if hasattr(session.big_blind, "get") else session.big_blind
        return sb, bb

    def get_gagnant_apres_showdown(self, session_id: int) -> Optional[JoueurPartie]:
        """Retourne le gagnant si le showdown a été effectué (approche simple: dernier crédité)."""
        session = self.get_session(session_id)
        if not session or not session.transactions:
            return None
        # Heuristique: la dernière transaction positive correspond au gain du pot par le gagnant
        for tr in reversed(session.transactions):
            solde = tr.solde.get() if hasattr(tr.solde, "get") else tr.solde
            if solde > 0:
                # Map id_joueur -> JoueurPartie
                for jp in session.joueurs_partie:
                    if jp.joueur.id_joueur == tr.id_joueur:
                        return jp
        return None
