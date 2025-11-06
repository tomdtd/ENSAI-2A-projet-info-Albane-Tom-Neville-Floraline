from typing import List, Optional
from datetime import datetime
from dao.db_connection import DBConnection
from src.business_object.partie import Partie
from src.business_object.pot import Pot
from src.business_object.carte import Carte

class PartieDao:
    def __init__(self):
        self.connection = DBConnection()

    def creer(self, partie: Partie) -> Partie:
        """Crée une nouvelle partie dans la base de données"""
        try:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Parties (id_table, date_debut, pot_total)
                        VALUES (%s, %s, %s)
                        RETURNING id_partie
                    """, (partie.id_table, partie.date_debut, partie.pot.get_montant()))
                    
                    result = cursor.fetchone()
                    partie.id_partie = result[0]
                    
                    # Sauvegarder les cartes communes
                    for i, carte in enumerate(partie.carte_communes):
                        cursor.execute("""
                            INSERT INTO Cartes_Communes (id_partie, valeur, couleur, ordre)
                            VALUES (%s, %s, %s, %s)
                        """, (partie.id_partie, carte.valeur, carte.couleur, i))
                    
                    return partie
                    
        except Exception as e:
            raise ValueError(f"Erreur lors de la création de la partie: {e}")

    def trouver_par_id(self, id_partie: int) -> Optional[Partie]:
        """Récupère une partie par son ID"""
        try:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    # Récupérer la partie
                    cursor.execute("""
                        SELECT id_partie, id_table, date_debut, date_fin, pot_total
                        FROM Parties WHERE id_partie = %s
                    """, (id_partie,))
                    
                    row = cursor.fetchone()
                    if not row:
                        return None
                    
                    partie = Partie(
                        id_partie=row[0],
                        joueurs=[],  # À charger séparément
                        pot=Pot(),
                        id_table=row[1],
                        date_debut=row[2],
                        carte_communes=[]
                    )
                    
                    if row[3]:
                        partie.date_fin = row[3]
                    
                    partie.pot.ajouter_mise(row[4])
                    
                    # Récupérer les cartes communes
                    cursor.execute("""
                        SELECT valeur, couleur FROM Cartes_Communes
                        WHERE id_partie = %s ORDER BY ordre
                    """, (id_partie,))
                    
                    for carte_row in cursor.fetchall():
                        partie.carte_communes.append(Carte(carte_row[0], carte_row[1]))
                    
                    return partie
                    
        except Exception as e:
            raise ValueError(f"Erreur lors de la recherche de la partie: {e}")

    def mettre_a_jour(self, partie: Partie) -> bool:
        """Met à jour les informations d'une partie"""
        try:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE Parties 
                        SET date_fin = %s, pot_total = %s
                        WHERE id_partie = %s
                    """, (partie.date_fin, partie.pot.get_montant(), partie.id_partie))
                    
                    # Mettre à jour les cartes communes
                    cursor.execute("DELETE FROM Cartes_Communes WHERE id_partie = %s", (partie.id_partie,))
                    
                    for i, carte in enumerate(partie.carte_communes):
                        cursor.execute("""
                            INSERT INTO Cartes_Communes (id_partie, valeur, couleur, ordre)
                            VALUES (%s, %s, %s, %s)
                        """, (partie.id_partie, carte.valeur, carte.couleur, i))
                    
                    return cursor.rowcount > 0
                    
        except Exception as e:
            raise ValueError(f"Erreur lors de la mise à jour de la partie: {e}")

    def trouver_parties_par_statut(self, statut: str) -> List[Partie]:
        """Récupère les parties par statut"""
        try:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    if statut == "en_cours":
                        cursor.execute("SELECT id_partie FROM Parties WHERE date_fin IS NULL")
                    elif statut == "terminee":
                        cursor.execute("SELECT id_partie FROM Parties WHERE date_fin IS NOT NULL")
                    
                    parties = []
                    for row in cursor.fetchall():
                        partie = self.trouver_par_id(row[0])
                        if partie:
                            parties.append(partie)
                    
                    return parties
                    
        except Exception as e:
            raise ValueError(f"Erreur lors de la recherche des parties par statut: {e}")

    def trouver_parties_par_joueur(self, id_joueur: int) -> List[Partie]:
        """Récupère l'historique des parties d'un joueur"""
        try:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT DISTINCT p.id_partie
                        FROM Parties p
                        JOIN Joueurs_Parties jp ON p.id_partie = jp.id_partie
                        WHERE jp.id_joueur = %s
                    """, (id_joueur,))
                    
                    parties = []
                    for row in cursor.fetchall():
                        partie = self.trouver_par_id(row[0])
                        if partie:
                            parties.append(partie)
                    
                    return parties
                    
        except Exception as e:
            raise ValueError(f"Erreur lors de la recherche des parties du joueur: {e}")

    def trouver_derniere_partie_sur_table(self, id_table: int) -> Optional[Partie]:
        """Récupère la dernière partie sur une table"""
        try:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id_partie FROM Parties 
                        WHERE id_table = %s 
                        ORDER BY date_debut DESC 
                        LIMIT 1
                    """, (id_table,))
                    
                    row = cursor.fetchone()
                    if row:
                        return self.trouver_par_id(row[0])
                    return None
                    
        except Exception as e:
            raise ValueError(f"Erreur lors de la recherche de la dernière partie: {e}")

    def lister_parties_par_periode(self, debut: datetime, fin: datetime) -> List[Partie]:
        """Récupère les parties dans une période donnée"""
        try:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id_partie FROM Parties 
                        WHERE date_debut BETWEEN %s AND %s
                    """, (debut, fin))
                    
                    parties = []
                    for row in cursor.fetchall():
                        partie = self.trouver_par_id(row[0])
                        if partie:
                            parties.append(partie)
                    
                    return parties
                    
        except Exception as e:
            raise ValueError(f"Erreur lors du listage des parties par période: {e}")