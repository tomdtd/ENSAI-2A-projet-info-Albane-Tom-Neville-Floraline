-- =====================================================================
--- CRÉATION DES TABLES DE LA BASE DE DONNÉES
-- =====================================================================

-- Pour faciliter les tests, on supprime les tables si elles existent déjà.
DROP TABLE IF EXISTS partie_joueur;
DROP TABLE IF EXISTS partie;
DROP TABLE IF EXISTS table_joueur;
DROP TABLE IF EXISTS table_poker;
DROP TABLE IF EXISTS portefeuille;
DROP TABLE IF EXISTS utilisateur;


-- -----------------------------------------------------
-- Table `utilisateur`
-- Stocke les informations sur les joueurs inscrits.
-- -----------------------------------------------------
CREATE TABLE utilisateur (
  id_utilisateur INT PRIMARY KEY AUTO_INCREMENT,
  pseudo VARCHAR(50) NOT NULL UNIQUE,
  -- On utilise VARCHAR(255) pour stocker un hash du mot de passe, jamais le mot de passe en clair.
  mot_de_passe VARCHAR(255) NOT NULL,
  credit DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
  date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------
-- Table `portefeuille`
-- Gère le solde de chaque utilisateur. Relation 1-1 avec utilisateur.
-- -----------------------------------------------------
CREATE TABLE portefeuille (
  id_portefeuille INT PRIMARY KEY AUTO_INCREMENT,
  -- Clé étrangère vers l'utilisateur
  id_utilisateur INT NOT NULL UNIQUE,
  solde DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
  -- La contrainte UNIQUE sur id_utilisateur garantit la relation 1-1
  CONSTRAINT fk_portefeuille_utilisateur
    FOREIGN KEY (id_utilisateur)
    REFERENCES utilisateur(id_utilisateur)
    ON DELETE CASCADE -- Si un utilisateur est supprimé, son portefeuille l'est aussi.
);

-- -----------------------------------------------------
-- Table `table_poker`
-- Décrit les tables de jeu disponibles.
-- -----------------------------------------------------
CREATE TABLE table_poker (
  id_table INT PRIMARY KEY AUTO_INCREMENT,
  nom_table VARCHAR(100) NOT NULL,
  nb_sieges INT NOT NULL,
  blind_initial DECIMAL(10, 2) NOT NULL,
  -- nb_joueurs est une donnée dénormalisée pour un accès rapide.
  -- Elle devra être mise à jour par l'application.
  nb_joueurs INT NOT NULL DEFAULT 0
);

-- -----------------------------------------------------
-- Table `table_joueur` (TABLE DE JONCTION)
-- Lie les utilisateurs aux tables sur lesquelles ils sont assis. Relation N-N.
-- -----------------------------------------------------
CREATE TABLE table_joueur (
  id_table INT NOT NULL,
  id_utilisateur INT NOT NULL,
  date_arrivee TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  -- Clé primaire composite pour s'assurer qu'un joueur n'est assis qu'une fois à la même table.
  PRIMARY KEY (id_table, id_utilisateur),
  CONSTRAINT fk_tablejoueur_table
    FOREIGN KEY (id_table)
    REFERENCES table_poker(id_table)
    ON DELETE CASCADE, -- Si la table est supprimée, les joueurs sont retirés.
  CONSTRAINT fk_tablejoueur_utilisateur
    FOREIGN KEY (id_utilisateur)
    REFERENCES utilisateur(id_utilisateur)
    ON DELETE CASCADE -- Si le joueur est supprimé, il est retiré de la table.
);

-- -----------------------------------------------------
-- Table `partie`
-- Représente une main de poker qui s'est déroulée sur une table.
-- -----------------------------------------------------
CREATE TABLE partie (
  id_partie INT PRIMARY KEY AUTO_INCREMENT,
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
-- Lie les utilisateurs aux parties auxquelles ils ont participé. Relation N-N.
-- -----------------------------------------------------
CREATE TABLE partie_joueur (
  id_partie INT NOT NULL,
  id_utilisateur INT NOT NULL,
  -- On pourrait ajouter des informations comme la mise du joueur, ses cartes, etc.
  -- mise_joueur DECIMAL(10, 2),
  PRIMARY KEY (id_partie, id_utilisateur),
  CONSTRAINT fk_partiejoueur_partie
    FOREIGN KEY (id_partie)
    REFERENCES partie(id_partie)
    ON DELETE CASCADE,
  CONSTRAINT fk_partiejoueur_utilisateur
    FOREIGN KEY (id_utilisateur)
    REFERENCES utilisateur(id_utilisateur)
    ON DELETE CASCADE
);
