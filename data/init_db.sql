-- =====================================================================
--- CRÉATION DES TABLES DE LA BASE DE DONNÉES
-- =====================================================================

-- Pour faciliter les tests, on supprime les tables si elles existent déjà.
DROP TABLE IF EXISTS partie_joueur;
DROP TABLE IF EXISTS partie;
DROP TABLE IF EXISTS table_joueur;
DROP TABLE IF EXISTS table_poker;
DROP TABLE IF EXISTS portefeuille;
DROP TABLE IF EXISTS joueur;


-- -----------------------------------------------------
-- Table `joueur`
-- Stocke les informations sur les joueurs inscrits.
-- -----------------------------------------------------
CREATE TABLE joueur (
  id_joueur INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  pseudo VARCHAR(50) NOT NULL UNIQUE,
  -- On utilise VARCHAR(255) pour stocker un hash du mot de passe, jamais le mot de passe en clair.
  mdp VARCHAR(255) NOT NULL,
  mail VARCHAR(255) NOT NULL,
  age INT NOT NULL,
  credit DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
  date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- Table `portefeuille`
-- Gère le solde de chaque joueur. Relation 1-1 avec joueur.
-- -----------------------------------------------------
CREATE TABLE portefeuille (
  id_portefeuille INT PRIMARY KEY,
  -- Clé étrangère vers l'joueur
  id_joueur INT NOT NULL UNIQUE,
  solde DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
  -- La contrainte UNIQUE sur id_joueur garantit la relation 1-1
  CONSTRAINT fk_portefeuille_joueur
    FOREIGN KEY (id_joueur)
    REFERENCES joueur(id_joueur)
    ON DELETE CASCADE -- Si un joueur est supprimé, son portefeuille l'est aussi.
);

-- -----------------------------------------------------
-- Table `table_poker`
-- Décrit les tables de jeu disponibles.
-- -----------------------------------------------------
CREATE TABLE table_poker (
  id_table INT PRIMARY KEY,
  nom_table VARCHAR(100) NOT NULL,
  nb_sieges INT NOT NULL,
  blind_initial DECIMAL(10, 2) NOT NULL,
  -- nb_joueurs est une donnée dénormalisée pour un accès rapide.
  -- Elle devra être mise à jour par l'application.
  nb_joueurs INT NOT NULL DEFAULT 0
);

-- -----------------------------------------------------
-- Table `table_joueur` (TABLE DE JONCTION)
-- Lie les joueurs aux tables sur lesquelles ils sont assis. Relation N-N.
-- -----------------------------------------------------
CREATE TABLE table_joueur (
  id_table INT NOT NULL,
  id_joueur INT NOT NULL,
  date_arrivee TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  -- Clé primaire composite pour s'assurer qu'un joueur n'est assis qu'une fois à la même table.
  PRIMARY KEY (id_table, id_joueur),
  CONSTRAINT fk_tablejoueur_table
    FOREIGN KEY (id_table)
    REFERENCES table_poker(id_table)
    ON DELETE CASCADE, -- Si la table est supprimée, les joueurs sont retirés.
  CONSTRAINT fk_tablejoueur_joueur
    FOREIGN KEY (id_joueur)
    REFERENCES joueur(id_joueur)
    ON DELETE CASCADE -- Si le joueur est supprimé, il est retiré de la table.
);

-- -----------------------------------------------------
-- Table `partie`
-- Représente une main de poker qui s'est déroulée sur une table.
-- -----------------------------------------------------
CREATE TABLE partie (
  id_partie INT PRIMARY KEY,
  id_table INT NOT NULL,
  pot DECIMAL(12, 2) NOT NULL,
  date_debut TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_partie_table
    FOREIGN KEY (id_table)
    REFERENCES table_poker(id_table)
    -- On ne veut pas supprimer les parties si une table est supprimée,
    -- on pourrait vouloir garder l'historique. ON DELETE SET NULL est une option.
    -- Ici, on va supposer que l'historique est lié à la table.
    ON DELETE CASCADE
);

-- -----------------------------------------------------
-- Table `partie_joueur` (TABLE DE JONCTION)
-- Lie les joueurs aux parties auxquelles ils ont participé. Relation N-N.
-- -----------------------------------------------------
CREATE TABLE partie_joueur (
  id_partie INT NOT NULL,
  id_joueur INT NOT NULL,
  mise_tour INT DEFAULT 0,
  solde_partie DECIMAL(10,2) DEFAULT 0.00,
  statut VARCHAR(50) DEFAULT 'en attente',
  id_siege INT NULL,
  PRIMARY KEY (id_partie, id_joueur),
  CONSTRAINT fk_partiejoueur_partie
    FOREIGN KEY (id_partie)
    REFERENCES partie(id_partie)
    ON DELETE CASCADE,
  CONSTRAINT fk_partiejoueur_joueur
    FOREIGN KEY (id_joueur)
    REFERENCES joueur(id_joueur)
    ON DELETE CASCADE
);


-- -----------------------------------------------------
-- Table `transaction` 
-- Gere les transaction.
-- -----------------------------------------------------
CREATE TABLE transaction (
  id_transaction INT NOT NULL, 
  joueur_id INT NOT NULL, 
  solde: INT DEFAULT 0,
  date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_transaction),
  CONSTRAINT fk_transaction_joueur
        FOREIGN KEY (joueur_id)
        REFERENCES joueur(id_joueur)
        ON DELETE CASCADE
);
