```mermaid
erDiagram
    %% Titre du diagramme
    %% Modèle Physique de Données (MPD) - Serveur de Poker

    %% Définition des Tables
    T_JOUEURS {
        INTEGER id_joueur PK "AUTO_INCREMENT"
        VARCHAR pseudo "UNIQUE"
        VARCHAR mot_de_passe_hash
        VARCHAR email "UNIQUE"
        DECIMAL credit
        BOOLEAN est_admin
        TIMESTAMP date_creation
    }

    T_TABLES {
        INTEGER id_table PK "AUTO_INCREMENT"
        VARCHAR nom_table
        INTEGER nb_sieges_max
        DECIMAL blind_initial
    }

    T_PARTIES {
        INTEGER id_partie PK "AUTO_INCREMENT"
        INTEGER id_table FK
        TIMESTAMP date_debut
        TIMESTAMP date_fin
        VARCHAR statut_partie
        DECIMAL pot_total
        VARCHAR cartes_communes
    }

    T_JOUEURS_PARTIES {
        INTEGER id_joueur PK FK
        INTEGER id_partie PK FK
        VARCHAR main_joueur
        DECIMAL montant_mise_total
        INTEGER numero_siege
        VARCHAR statut_dans_la_partie
        DECIMAL gain_perte
        VARCHAR combinaison_finale
    }

    T_TRANSACTIONS {
        INTEGER id_transaction PK "AUTO_INCREMENT"
        INTEGER id_joueur FK
        VARCHAR type_transaction
        DECIMAL montant
        TIMESTAMP date_transaction
    }

    %% Définition des Relations
    T_JOUEURS ||--o{ T_TRANSACTIONS : "a pour"
    T_TABLES ||--o{ T_PARTIES : "accueille"
    T_JOUEURS }|--|| T_JOUEURS_PARTIES : "participe à"
    T_PARTIES }|--|| T_JOUEURS_PARTIES : "comprend"