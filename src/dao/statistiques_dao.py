"""
Module DAO pour la gestion des statistiques du jeu de poker.

Ce module fournit des méthodes pour extraire des statistiques descriptives
individuelles et collectives sur les joueurs et les parties.
"""

from src.dao.db_connection import DBConnection
from src.utils.singleton import Singleton
from src.utils.log_decorator import log


class StatistiquesDao(metaclass=Singleton):
    """Classe DAO pour gérer les statistiques du jeu de poker."""

    # =========================================================================
    # STATISTIQUES INDIVIDUELLES PAR JOUEUR
    # =========================================================================

    @log
    def obtenir_stats_joueur(self, id_joueur: int) -> dict:
        """
        Récupère les statistiques complètes d'un joueur.
        
        Parameters
        ----------
        id_joueur : int
            Identifiant du joueur
            
        Returns
        -------
        dict
            Dictionnaire contenant toutes les statistiques du joueur
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 
                            j.pseudo,
                            j.credit,
                            j.age,
                            COUNT(DISTINCT pp.id_table) as nb_parties_jouees,
                            COALESCE(SUM(pp.solde_partie), 0) as total_gains,
                            COALESCE(AVG(pp.solde_partie), 0) as gain_moyen_partie,
                            COALESCE(AVG(pp.mise_tour), 0) as mise_moyenne,
                            COALESCE(SUM(CASE WHEN pp.statut = 'gagnant' THEN 1 ELSE 0 END), 0) as nb_victoires,
                            j.date_creation
                        FROM joueur j
                        LEFT JOIN partie_joueur pp ON j.id_joueur = pp.id_joueur
                        WHERE j.id_joueur = %(id_joueur)s
                        GROUP BY j.id_joueur, j.pseudo, j.credit, j.age, j.date_creation
                        """,
                        {"id_joueur": id_joueur}
                    )
                    result = cursor.fetchone()
                    
                    if result:
                        nb_parties = result["nb_parties_jouees"] or 0
                        nb_victoires = result["nb_victoires"] or 0
                        
                        return {
                            "pseudo": result["pseudo"],
                            "credit_actuel": float(result["credit"]),
                            "age": result["age"],
                            "nb_parties_jouees": nb_parties,
                            "nb_victoires": nb_victoires,
                            "taux_victoire": (nb_victoires / nb_parties * 100) if nb_parties > 0 else 0,
                            "total_gains": float(result["total_gains"]),
                            "gain_moyen_partie": float(result["gain_moyen_partie"]),
                            "mise_moyenne": float(result["mise_moyenne"]),
                            "date_inscription": result["date_creation"]
                        }
                    return None
        except Exception as e:
            print(f"Erreur lors de la récupération des stats du joueur: {e}")
            return None

    @log
    def obtenir_historique_parties_joueur(self, id_joueur: int, limite: int = 10) -> list[dict]:
        """
        Récupère l'historique des dernières parties d'un joueur.
        
        Parameters
        ----------
        id_joueur : int
            Identifiant du joueur
        limite : int
            Nombre de parties à récupérer (défaut: 10)
            
        Returns
        -------
        list[dict]
            Liste des parties avec leurs détails
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 
                            p.id_partie,
                            p.id_table,
                            p.pot as pot_total,
                            p.date_debut,
                            pp.solde_partie as resultat,
                            pp.mise_tour as mise_finale,
                            pp.statut,
                            tp.blind_initial
                        FROM partie p
                        JOIN partie_joueur pp ON p.id_table = pp.id_table
                        JOIN table_poker tp ON p.id_table = tp.id_table
                        WHERE pp.id_joueur = %(id_joueur)s
                        ORDER BY p.date_debut DESC
                        LIMIT %(limite)s
                        """,
                        {"id_joueur": id_joueur, "limite": limite}
                    )
                    return cursor.fetchall()
        except Exception as e:
            print(f"Erreur lors de la récupération de l'historique: {e}")
            return []

    @log
    def obtenir_evolution_credit_joueur(self, id_joueur: int) -> list[dict]:
        """
        Récupère l'évolution du crédit d'un joueur via les transactions.
        
        Parameters
        ----------
        id_joueur : int
            Identifiant du joueur
            
        Returns
        -------
        list[dict]
            Liste chronologique des transactions
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 
                            id_transaction,
                            solde as montant,
                            date,
                            SUM(solde) OVER (ORDER BY date) as solde_cumule
                        FROM transaction
                        WHERE id_joueur = %(id_joueur)s
                        ORDER BY date ASC
                        """,
                        {"id_joueur": id_joueur}
                    )
                    return cursor.fetchall()
        except Exception as e:
            print(f"Erreur lors de la récupération de l'évolution du crédit: {e}")
            return []

    @log
    def obtenir_statistiques_par_table(self, id_joueur: int) -> list[dict]:
        """
        Récupère les performances d'un joueur par table.
        
        Parameters
        ----------
        id_joueur : int
            Identifiant du joueur
            
        Returns
        -------
        list[dict]
            Statistiques par table
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 
                            pp.id_table,
                            tp.nb_sieges,
                            tp.blind_initial,
                            COUNT(*) as nb_parties,
                            SUM(CASE WHEN pp.statut = 'gagnant' THEN 1 ELSE 0 END) as victoires,
                            AVG(pp.solde_partie) as gain_moyen,
                            SUM(pp.solde_partie) as gain_total
                        FROM partie_joueur pp
                        JOIN table_poker tp ON pp.id_table = tp.id_table
                        WHERE pp.id_joueur = %(id_joueur)s
                        GROUP BY pp.id_table, tp.nb_sieges, tp.blind_initial
                        ORDER BY nb_parties DESC
                        """,
                        {"id_joueur": id_joueur}
                    )
                    results = cursor.fetchall()
                    
                    # Calcul du taux de victoire pour chaque table
                    for result in results:
                        nb_parties = result["nb_parties"]
                        result["taux_victoire"] = (result["victoires"] / nb_parties * 100) if nb_parties > 0 else 0
                    
                    return results
        except Exception as e:
            print(f"Erreur lors de la récupération des stats par table: {e}")
            return []

    # =========================================================================
    # STATISTIQUES COLLECTIVES
    # =========================================================================

    @log
    def obtenir_stats_globales(self) -> dict:
        """
        Récupère les statistiques globales de la plateforme.
        
        Returns
        -------
        dict
            Statistiques générales
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 
                            (SELECT COUNT(*) FROM joueur) as nb_joueurs_total,
                            (SELECT COUNT(*) FROM partie) as nb_parties_total,
                            (SELECT COUNT(*) FROM table_poker) as nb_tables_actives,
                            COALESCE((SELECT SUM(credit) FROM joueur), 0) as credit_total_plateforme,
                            COALESCE((SELECT AVG(credit) FROM joueur), 0) as credit_moyen_joueur,
                            COALESCE((SELECT AVG(age) FROM joueur), 0) as age_moyen_joueurs
                        """
                    )
                    result = cursor.fetchone()
                    
                    if result:
                        return {
                            "nb_joueurs_total": result["nb_joueurs_total"],
                            "nb_parties_total": result["nb_parties_total"],
                            "nb_tables_actives": result["nb_tables_actives"],
                            "credit_total_plateforme": float(result["credit_total_plateforme"]),
                            "credit_moyen_joueur": float(result["credit_moyen_joueur"]),
                            "age_moyen_joueurs": float(result["age_moyen_joueurs"])
                        }
                    return None
        except Exception as e:
            print(f"Erreur lors de la récupération des stats globales: {e}")
            return None

    @log
    def obtenir_classement_joueurs(self, critere: str = "credit", limite: int = 10) -> list[dict]:
        """
        Récupère le classement des joueurs selon un critère.
        
        Parameters
        ----------
        critere : str
            Critère de classement: 'credit', 'victoires', 'parties_jouees'
        limite : int
            Nombre de joueurs à retourner
            
        Returns
        -------
        list[dict]
            Classement des joueurs
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    if critere == "credit":
                        order_by = "j.credit DESC"
                    elif critere == "victoires":
                        order_by = "nb_victoires DESC"
                    elif critere == "parties_jouees":
                        order_by = "nb_parties DESC"
                    else:
                        order_by = "j.credit DESC"
                    
                    cursor.execute(
                        f"""
                        SELECT 
                            j.id_joueur,
                            j.pseudo,
                            j.credit,
                            COUNT(DISTINCT pp.id_table) as nb_parties,
                            SUM(CASE WHEN pp.statut = 'gagnant' THEN 1 ELSE 0 END) as nb_victoires,
                            COALESCE(SUM(pp.solde_partie), 0) as gains_totaux
                        FROM joueur j
                        LEFT JOIN partie_joueur pp ON j.id_joueur = pp.id_joueur
                        GROUP BY j.id_joueur, j.pseudo, j.credit
                        ORDER BY {order_by}
                        LIMIT %(limite)s
                        """,
                        {"limite": limite}
                    )
                    results = cursor.fetchall()
                    
                    # Ajout du rang
                    for i, result in enumerate(results, 1):
                        result["rang"] = i
                        nb_parties = result["nb_parties"] or 0
                        nb_victoires = result["nb_victoires"] or 0
                        result["taux_victoire"] = (
                            nb_victoires / nb_parties * 100 
                            if nb_parties > 0 else 0
                        )
                    
                    return results
        except Exception as e:
            print(f"Erreur lors de la récupération du classement: {e}")
            return []

    @log
    def obtenir_distribution_age(self) -> list[dict]:
        """
        Récupère la distribution des joueurs par tranche d'âge.
        
        Returns
        -------
        list[dict]
            Distribution par tranche d'âge
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 
                            CASE 
                                WHEN age < 18 THEN 'Moins de 18'
                                WHEN age BETWEEN 18 AND 25 THEN '18-25'
                                WHEN age BETWEEN 26 AND 35 THEN '26-35'
                                WHEN age BETWEEN 36 AND 50 THEN '36-50'
                                ELSE 'Plus de 50'
                            END as tranche_age,
                            COUNT(*) as nb_joueurs,
                            AVG(credit) as credit_moyen,
                            AVG(age) as age_moyen_tranche
                        FROM joueur
                        GROUP BY 
                            CASE 
                                WHEN age < 18 THEN 'Moins de 18'
                                WHEN age BETWEEN 18 AND 25 THEN '18-25'
                                WHEN age BETWEEN 26 AND 35 THEN '26-35'
                                WHEN age BETWEEN 36 AND 50 THEN '36-50'
                                ELSE 'Plus de 50'
                            END
                        ORDER BY 
                            CASE 
                                WHEN CASE 
                                    WHEN age < 18 THEN 'Moins de 18'
                                    WHEN age BETWEEN 18 AND 25 THEN '18-25'
                                    WHEN age BETWEEN 26 AND 35 THEN '26-35'
                                    WHEN age BETWEEN 36 AND 50 THEN '36-50'
                                    ELSE 'Plus de 50'
                                END = 'Moins de 18' THEN 1
                                WHEN CASE 
                                    WHEN age < 18 THEN 'Moins de 18'
                                    WHEN age BETWEEN 18 AND 25 THEN '18-25'
                                    WHEN age BETWEEN 26 AND 35 THEN '26-35'
                                    WHEN age BETWEEN 36 AND 50 THEN '36-50'
                                    ELSE 'Plus de 50'
                                END = '18-25' THEN 2
                                WHEN CASE 
                                    WHEN age < 18 THEN 'Moins de 18'
                                    WHEN age BETWEEN 18 AND 25 THEN '18-25'
                                    WHEN age BETWEEN 26 AND 35 THEN '26-35'
                                    WHEN age BETWEEN 36 AND 50 THEN '36-50'
                                    ELSE 'Plus de 50'
                                END = '26-35' THEN 3
                                WHEN CASE 
                                    WHEN age < 18 THEN 'Moins de 18'
                                    WHEN age BETWEEN 18 AND 25 THEN '18-25'
                                    WHEN age BETWEEN 26 AND 35 THEN '26-35'
                                    WHEN age BETWEEN 36 AND 50 THEN '36-50'
                                    ELSE 'Plus de 50'
                                END = '36-50' THEN 4
                                ELSE 5
                            END
                        """
                    )
                    return cursor.fetchall()
        except Exception as e:
            print(f"Erreur lors de la récupération de la distribution d'âge: {e}")
            return []

    @log
    def obtenir_joueurs_plus_actifs(self, limite: int = 10) -> list[dict]:
        """
        Récupère les joueurs les plus actifs (nombre de parties jouées).
        
        Parameters
        ----------
        limite : int
            Nombre de joueurs à retourner
            
        Returns
        -------
        list[dict]
            Liste des joueurs les plus actifs
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 
                            j.id_joueur,
                            j.pseudo,
                            COUNT(DISTINCT pp.id_table) as nb_parties,
                            SUM(pp.mise_tour) as total_mises,
                            AVG(pp.mise_tour) as mise_moyenne,
                            MAX(p.date_debut) as derniere_partie
                        FROM joueur j
                        JOIN partie_joueur pp ON j.id_joueur = pp.id_joueur
                        JOIN partie p ON pp.id_table = p.id_table
                        GROUP BY j.id_joueur, j.pseudo
                        ORDER BY nb_parties DESC
                        LIMIT %(limite)s
                        """,
                        {"limite": limite}
                    )
                    return cursor.fetchall()
        except Exception as e:
            print(f"Erreur lors de la récupération des joueurs actifs: {e}")
            return []

    # =========================================================================
    # STATISTIQUES SUR LES PARTIES
    # =========================================================================

    @log
    def obtenir_stats_parties(self) -> dict:
        """
        Récupère les statistiques sur les parties.
        
        Returns
        -------
        dict
            Statistiques agrégées sur les parties
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 
                            COUNT(*) as nb_parties_total,
                            COALESCE(AVG(pot), 0) as pot_moyen,
                            COALESCE(STDDEV(pot), 0) as ecart_type_pot,
                            COALESCE(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY pot), 0) as mediane_pot,
                            COALESCE(MIN(pot), 0) as pot_min,
                            COALESCE(MAX(pot), 0) as pot_max,
                            COALESCE(SUM(pot), 0) as somme_totale_pots
                        FROM partie
                        """
                    )
                    result = cursor.fetchone()
                    
                    if result:
                        return {
                            "nb_parties_total": result["nb_parties_total"],
                            "pot_moyen": float(result["pot_moyen"] or 0),
                            "ecart_type_pot": float(result["ecart_type_pot"] or 0),
                            "mediane_pot": float(result["mediane_pot"] or 0),
                            "pot_min": float(result["pot_min"] or 0),
                            "pot_max": float(result["pot_max"] or 0),
                            "somme_totale_pots": float(result["somme_totale_pots"] or 0)
                        }
                    return None
        except Exception as e:
            print(f"Erreur lors de la récupération des stats des parties: {e}")
            return None

    @log
    def obtenir_stats_mises(self) -> dict:
        """
        Récupère les statistiques sur les mises des joueurs.
        
        Returns
        -------
        dict
            Statistiques agrégées sur les mises
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 
                            COUNT(*) as nb_mises_total,
                            COALESCE(AVG(mise_tour), 0) as mise_moyenne,
                            COALESCE(STDDEV(mise_tour), 0) as ecart_type_mise,
                            COALESCE(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY mise_tour), 0) as mediane_mise,
                            COALESCE(MIN(mise_tour), 0) as mise_min,
                            COALESCE(MAX(mise_tour), 0) as mise_max,
                            COALESCE(SUM(mise_tour), 0) as somme_totale_mises
                        FROM partie_joueur
                        WHERE mise_tour > 0
                        """
                    )
                    result = cursor.fetchone()
                    
                    if result:
                        return {
                            "nb_mises_total": result["nb_mises_total"],
                            "mise_moyenne": float(result["mise_moyenne"] or 0),
                            "ecart_type_mise": float(result["ecart_type_mise"] or 0),
                            "mediane_mise": float(result["mediane_mise"] or 0),
                            "mise_min": float(result["mise_min"] or 0),
                            "mise_max": float(result["mise_max"] or 0),
                            "somme_totale_mises": float(result["somme_totale_mises"] or 0)
                        }
                    return None
        except Exception as e:
            print(f"Erreur lors de la récupération des stats des mises: {e}")
            return None

    @log
    def obtenir_stats_tables(self) -> list[dict]:
        """
        Récupère les statistiques par table.
        
        Returns
        -------
        list[dict]
            Statistiques par table
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 
                            tp.id_table,
                            tp.nb_sieges,
                            tp.blind_initial,
                            tp.nb_joueurs as nb_joueurs_actuels,
                            COUNT(DISTINCT p.id_partie) as nb_parties_jouees,
                            COALESCE(AVG(p.pot), 0) as pot_moyen,
                            COALESCE(MAX(p.pot), 0) as pot_max,
                            COUNT(DISTINCT pp.id_joueur) as nb_joueurs_differents
                        FROM table_poker tp
                        LEFT JOIN partie p ON tp.id_table = p.id_table
                        LEFT JOIN partie_joueur pp ON tp.id_table = pp.id_table
                        GROUP BY tp.id_table, tp.nb_sieges, tp.blind_initial, tp.nb_joueurs
                        ORDER BY nb_parties_jouees DESC
                        """
                    )
                    results = cursor.fetchall()
                    
                    for result in results:
                        taux_occupation = (result["nb_joueurs_actuels"] / result["nb_sieges"] * 100) if result["nb_sieges"] > 0 else 0
                        result["taux_occupation"] = taux_occupation
                    
                    return results
        except Exception as e:
            print(f"Erreur lors de la récupération des stats des tables: {e}")
            return []

    @log
    def obtenir_activite_par_periode(self, periode: str = "jour") -> list[dict]:
        """
        Récupère l'activité (nombre de parties) par période.
        
        Parameters
        ----------
        periode : str
            'jour', 'semaine' ou 'mois'
            
        Returns
        -------
        list[dict]
            Activité par période
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    if periode == "jour":
                        date_trunc = "day"
                    elif periode == "semaine":
                        date_trunc = "week"
                    else:
                        date_trunc = "month"
                    
                    cursor.execute(
                        f"""
                        SELECT 
                            DATE_TRUNC('{date_trunc}', date_debut) as periode,
                            COUNT(*) as nb_parties,
                            COUNT(DISTINCT id_table) as nb_tables_utilisees,
                            AVG(pot) as pot_moyen,
                            SUM(pot) as pot_total
                        FROM partie
                        GROUP BY periode
                        ORDER BY periode DESC
                        LIMIT 30
                        """
                    )
                    return cursor.fetchall()
        except Exception as e:
            print(f"Erreur lors de la récupération de l'activité par période: {e}")
            return []

    @log
    def obtenir_taux_abandon(self) -> dict:
        """
        Calcule les taux d'abandon (joueurs qui se couchent).
        
        Returns
        -------
        dict
            Statistiques sur les abandons
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 
                            COUNT(*) as total_participations,
                            SUM(CASE WHEN statut = 'couché' THEN 1 ELSE 0 END) as nb_abandons,
                            SUM(CASE WHEN statut = 'gagnant' THEN 1 ELSE 0 END) as nb_victoires,
                            SUM(CASE WHEN statut = 'actif' THEN 1 ELSE 0 END) as nb_actifs,
                            AVG(CASE WHEN statut = 'couché' THEN mise_tour ELSE NULL END) as mise_moyenne_avant_abandon
                        FROM partie_joueur
                        """
                    )
                    result = cursor.fetchone()
                    
                    if result and result["total_participations"] > 0:
                        total = result["total_participations"]
                        return {
                            "total_participations": total,
                            "nb_abandons": result["nb_abandons"],
                            "nb_victoires": result["nb_victoires"],
                            "nb_actifs": result["nb_actifs"],
                            "taux_abandon": (result["nb_abandons"] / total * 100),
                            "taux_victoire_global": (result["nb_victoires"] / total * 100),
                            "mise_moyenne_avant_abandon": float(result["mise_moyenne_avant_abandon"] or 0)
                        }
                    return None
        except Exception as e:
            print(f"Erreur lors du calcul du taux d'abandon: {e}")
            return None

    @log
    def obtenir_rapport_complet(self) -> dict:
        """
        Génère un rapport complet avec toutes les statistiques principales.
        
        Returns
        -------
        dict
            Rapport complet des statistiques
        """
        return {
            "stats_globales": self.obtenir_stats_globales(),
            "stats_parties": self.obtenir_stats_parties(),
            "stats_mises": self.obtenir_stats_mises(),
            "top_10_joueurs": self.obtenir_classement_joueurs(limite=10),
            "joueurs_actifs": self.obtenir_joueurs_plus_actifs(limite=10),
            "distribution_age": self.obtenir_distribution_age(),
            "taux_abandon": self.obtenir_taux_abandon(),
            "stats_tables": self.obtenir_stats_tables()
        }