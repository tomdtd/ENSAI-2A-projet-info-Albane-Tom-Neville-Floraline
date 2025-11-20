from src.utils.log_decorator import log
from src.utils.securite import hash_password

from src.business_object.table import Table
from src.business_object.joueur import Joueur
from src.business_object.accesspartie import AccessPartie
from src.business_object.liste_cartes import ListeCartes
from src.dao.table_dao import TableDao

class TableService :
    """Classe contenant les méthodes de service des tables"""

    @log
    def creer_table(self, nb_sieges: int, blind_initial: 'Monnaie') -> Table:
        """Crée une nouvelle table avec un nombre de sièges et un blind initial."""
        nouvelle_table = AccessPartie().creer_table(nb_sieges, blind_initial)
        if TableDao().creer(nouvelle_table):
            return nouvelle_table
        return None

    @log 
    def rejoindre_table(self, joueur: Joueur, id_table: int) -> bool:
        """Un joueur rejoint une table s'il y a un siège disponible."""
        table = TableDao().trouver_par_id(id_table)
        if table:
            for siege in table.sieges:
                if not siege.est_occupe():
                    siege.occupe = True
                    siege.id_joueur = joueur.id_joueur  
                    return TableDao().modifier(table)
        return False

    @log
    def lister_tables_disponibles(self) -> list[Table]:
        """Liste toutes les tables qui ont au moins un siège disponible."""
        tables = TableDao().lister_toutes()
        return [table for table in tables if not table.table_remplie()]

    @log
    def quitter_table(self, joueur: Joueur, id_table: int) -> bool:
        """Un joueur quitte une table et libère son siège."""
        table = TableDao().trouver_par_id(id_table)
        if table:
            for siege in table.sieges:
                if siege.id_joueur == joueur.id_joueur:
                    siege.occupe = False
                    siege.id_joueur = None
                    return TableDao().modifier(table)
        return False
    
    @log
    def ajouter_joueur_table(self, id_table: int) -> bool:
        """Incrémente le nb_joueurs de la table dans la DB"""
        return TableDao().incrementer_nb_joueurs(id_table)
    
    @log
    def retirer_joueur_table(self, id_table: int) -> bool:
        """Décrémente le nb_joueurs de la table dans la DB"""
        return TableDao().decrementer_nb_joueurs(id_table)
    
    @log
    def get_id_joueur_tour(self, id_table: int) -> int:
        """
        Retourne l'id du joueur dont c'est le tour pour la table donnée.
        Renvoie None si aucune information disponible.
        """
        if not id_table:
            raise ValueError("id_table requis.")
        return TableDao().get_id_joueur_tour(id_table)
    
    @log
    def set_id_joueur_tour(self, id_table: int, id_joueur_tour: int=None) -> bool:
        """
        Met à jour l'id du joueur dont c'est le tour pour la table donnée.
        id_joueur_tour peut être None (aucun joueur).
        Retourne True si la mise à jour a réussi.
        """
        if not id_table:
            raise ValueError("id_table requis.")
        return TableDao().set_id_joueur_tour(id_table, id_joueur_tour)
    
    @log
    def set_flop(self, id_table: int, flop: ListeCartes) -> bool:
        """Met à jour le flop pour une table donnée"""
        return TableDao().set_flop(id_table, flop)

    @log
    def set_turn(self, id_table: int, turn: ListeCartes) -> bool:
        """Met à jour le turn pour une table donnée"""
        return TableDao().set_turn(id_table, turn)

    @log
    def set_river(self, id_table: int, river: ListeCartes) -> bool:
        """Met à jour la river pour une table donnée"""
        return TableDao().set_river(id_table, river)

    @log
    def get_cartes_communes(self, id_table: int) -> dict:
        """
        Récupère le flop, turn et river d'une table.
        Renvoie un dictionnaire avec des objets ListeCartes pour chaque étape.
        """
        return TableDao().get_cartes_communess(id_table)

    @log
    def alimenter_pot(self, id_table: int, montant: float) -> bool:
        """Ajoute une somme au pot de la table."""
        if montant <= 0:
            raise ValueError("Le montant doit être positif pour alimenter le pot.")
        return TableDao().alimenter_pot(id_table, montant)

    @log
    def retirer_pot(self, id_table: int, montant: float) -> bool:
        """Retire une somme du pot de la table."""
        if montant < 0:
            raise ValueError("Le montant doit être positif pour retirer du pot.")
        return TableDao().retirer_pot(id_table, montant)

    @log
    def get_pot(self, id_table: int) -> float:
        """Récupère le montant actuel du pot de la table."""
        return TableDao().get_pot(id_table)
    
    @log
    def set_val_derniere_mise(self, id_table: int, montant: float) -> bool:
        """Met à jour la valeur de la dernière mise pour la table.
        Vérifie les arguments puis délègue au DAO.
        """
        if id_table is None:
            raise ValueError("id_table requis.")
        if montant is None or montant < 0:
            raise ValueError("montant doit être >= 0.")
        return TableDao().set_val_derniere_mise(id_table, montant)

    @log
    def get_val_derniere_mise(self, id_table: int) -> float:
        """Récupère la valeur de la dernière mise pour la table."""
        if id_table is None:
            raise ValueError("id_table requis.")
        return TableDao().get_val_derniere_mise(id_table)
    
    @log
    def get_id_joueur_bouton(self, id_table: int) -> int:
        """Retourne l'id du joueur qui a le bouton"""
        if not id_table:
            raise ValueError("id_table requis.")
        return TableDao().get_id_joueur_bouton(id_table)

    @log
    def set_id_joueur_bouton(self, id_table: int, id_joueur_bouton: int=None) -> bool:
        """Met à jour l'id du joueur qui a le bouton"""
        if not id_table:
            raise ValueError("id_table requis.")
        return TableDao().set_id_joueur_bouton(id_table, id_joueur_bouton)


