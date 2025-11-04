-- =====================================================================
--- INSERTION DES DONNÉES D'EXEMPLE
-- =====================================================================

-- -----------------------------------------------------
-- Insertion de 100 joueurs avec des noms français
-- -----------------------------------------------------
INSERT INTO joueur (pseudo, mdp, credit) VALUES
('jean.dupont', 'hash_placeholder', 150.00), ('marie.curie', 'hash_placeholder', 2500.50), ('pierre.martin', 'hash_placeholder', 75.25),
('sophie.bernard', 'hash_placeholder', 500.00), ('luc.dubois', 'hash_placeholder', 1200.00), ('camille.robert', 'hash_placeholder', 300.00),
('antoine.richard', 'hash_placeholder', 950.75), ('emilie.petit', 'hash_placeholder', 45.00), ('julien.durand', 'hash_placeholder', 880.00),
('laura.leroy', 'hash_placeholder', 2100.00), ('nicolas.moreau', 'hash_placeholder', 100.00), ('claire.simon', 'hash_placeholder', 650.00),
('alexandre.laurent', 'hash_placeholder', 320.50), ('manon.lefevre', 'hash_placeholder', 1500.00), ('thomas.roux', 'hash_placeholder', 50.00),
('chloe.david', 'hash_placeholder', 180.00), ('quentin.morel', 'hash_placeholder', 730.00), ('lea.fournier', 'hash_placeholder', 999.00),
('hugo.girard', 'hash_placeholder', 120.00), ('eva.lambert', 'hash_placeholder', 470.00), ('louis.bonnet', 'hash_placeholder', 250.00),
('emma.francois', 'hash_placeholder', 1100.00), ('gabriel.martinez', 'hash_placeholder', 80.00), ('alice.legrand', 'hash_placeholder', 540.00),
('raphael.garnier', 'hash_placeholder', 1350.00), ('juliette.faure', 'hash_placeholder', 220.00), ('arthur.rousseau', 'hash_placeholder', 680.00),
('sarah.vincent', 'hash_placeholder', 920.00), ('adam.muller', 'hash_placeholder', 170.00), ('ines.lemoine', 'hash_placeholder', 2000.00),
('paul.andre', 'hash_placeholder', 340.00), ('adele.mercier', 'hash_placeholder', 490.00), ('victor.brun', 'hash_placeholder', 760.00),
('louise.gauthier', 'hash_placeholder', 1400.00), ('leo.masson', 'hash_placeholder', 90.00), ('zoe.blanc', 'hash_placeholder', 610.00),
('mohamed.guichard', 'hash_placeholder', 270.00), ('lina.perez', 'hash_placeholder', 1600.00), ('enzo.robin', 'hash_placeholder', 400.00),
('helena.clement', 'hash_placeholder', 820.00), ('sacha.morin', 'hash_placeholder', 110.00), ('anna.nicolas', 'hash_placeholder', 700.00),
('tim.henry', 'hash_placeholder', 1900.00), ('rose.gaudin', 'hash_placeholder', 30.00), ('clement.michel', 'hash_placeholder', 580.00),
('maya.mathieu', 'hash_placeholder', 1250.00), ('maxime.guerin', 'hash_placeholder', 200.00), ('amelie.leclerc', 'hash_placeholder', 780.00),
('theo.poulain', 'hash_placeholder', 420.00), ('agathe.dumont', 'hash_placeholder', 930.00), ('gaspard.perrin', 'hash_placeholder', 150.00),
('elise.dufour', 'hash_placeholder', 1700.00), ('augustin.joly', 'hash_placeholder', 60.00), ('romane.lecomte', 'hash_placeholder', 630.00),
('noah.boucher', 'hash_placeholder', 360.00), ('lola.jacquet', 'hash_placeholder', 850.00), ('valentin.renard', 'hash_placeholder', 1300.00),
('margot.meunier', 'hash_placeholder', 240.00), ('samuel.brunet', 'hash_placeholder', 510.00), ('alix.schmitt', 'hash_placeholder', 1050.00),
('oscar.da-silva', 'hash_placeholder', 190.00), ('jeanne.leroux', 'hash_placeholder', 710.00), ('yannis.colin', 'hash_placeholder', 440.00),
('capucine.barbier', 'hash_placeholder', 970.00), ('basile.vidal', 'hash_placeholder', 140.00), ('celia.caron', 'hash_placeholder', 1800.00),
('felix.charles', 'hash_placeholder', 80.00), ('diane.renaud', 'hash_placeholder', 660.00), ('marius.gomez', 'hash_placeholder', 380.00),
('elena.lopes', 'hash_placeholder', 890.00), ('nathan.roger', 'hash_placeholder', 1150.00), ('iris.marchand', 'hash_placeholder', 280.00),
('ismael.roy', 'hash_placeholder', 560.00), ('leonore.picard', 'hash_placeholder', 1000.00), ('elie.philippe', 'hash_placeholder', 160.00),
('romy.duval', 'hash_placeholder', 740.00), ('milan.lucas', 'hash_placeholder', 460.00), ('victoria.deschamps', 'hash_placeholder', 940.00),
('aaron.baron', 'hash_placeholder', 130.00), ('olivia.bertin', 'hash_placeholder', 1650.00), ('edouard.boulanger', 'hash_placeholder', 70.00),
('constance.gerard', 'hash_placeholder', 690.00), ('noé.lamy', 'hash_placeholder', 390.00), ('marion.le-roux', 'hash_placeholder', 860.00),
('robin.maillard', 'hash_placeholder', 1200.00), ('adele.barre', 'hash_placeholder', 260.00), ('hippolyte.denis', 'hash_placeholder', 530.00),
('thea.royer', 'hash_placeholder', 1100.00), ('martin.fabre', 'hash_placeholder', 210.00), ('lea.aubert', 'hash_placeholder', 790.00),
('simon.carpentier', 'hash_placeholder', 430.00), ('lou.guillot', 'hash_placeholder', 960.00), ('gabin.lucas', 'hash_placeholder', 180.00),
('celestine.ferreira', 'hash_placeholder', 1950.00), ('baptiste.morvan', 'hash_placeholder', 95.00), ('anouk.fleury', 'hash_placeholder', 620.00);

-- -----------------------------------------------------
-- Création des portefeuilles pour chaque joueur
-- On copie simplement le crédit initial dans le solde du portefeuille.
-- -----------------------------------------------------
INSERT INTO portefeuille (id_joueur, solde)
SELECT id_joueur, credit FROM joueur;

-- -----------------------------------------------------
-- Insertion de 20 tables de poker
-- -----------------------------------------------------
INSERT INTO table_poker (nom_table, nb_sieges, blind_initial) VALUES
('Débutants - Paris', 9, 0.02), ('Micro Limite - Lyon', 6, 0.05), ('Petite Limite - Marseille', 6, 0.10),
('Cash Game NL10 - Lille', 9, 0.10), ('Cash Game NL25 - Bordeaux', 6, 0.25), ('Cash Game NL50 - Nice', 6, 0.50),
('Cash Game NL100 - Toulouse', 6, 1.00), ('High Roller - Monaco', 6, 10.00), ('Heads Up - Nantes', 2, 0.50),
('Heads Up Pro - Strasbourg', 2, 5.00), ('Table Rapide - Rennes', 6, 0.25), ('Table Lente - Montpellier', 9, 0.05),
('Le Colisée', 9, 2.00), ('Le Vélodrome', 9, 0.10), ('La Croisette', 6, 5.00),
('Tour Eiffel Express', 6, 1.00), ('Mont Blanc Sommet', 6, 2.00), ('Brocéliande Magique', 9, 0.25),
('Canal du Midi', 9, 0.50), ('Champs-Élysées', 6, 10.00);

-- -----------------------------------------------------
-- Ajout de joueurs à quelques tables
-- -----------------------------------------------------
-- Table 1 (Débutants - Paris), 5 joueurs
INSERT INTO table_joueur (id_table, id_joueur) VALUES (1, 1), (1, 4), (1, 8), (1, 15), (1, 22);
-- Table 2 (Micro Limite - Lyon), 6 joueurs (pleine)
INSERT INTO table_joueur (id_table, id_joueur) VALUES (2, 2), (2, 5), (2, 10), (2, 11), (2, 20), (2, 30);
-- Table 5 (Cash Game NL25 - Bordeaux), 3 joueurs
INSERT INTO table_joueur (id_table, id_joueur) VALUES (5, 3), (5, 6), (5, 9);
-- Table 9 (Heads Up - Nantes), 2 joueurs
INSERT INTO table_joueur (id_table, id_joueur) VALUES (9, 7), (9, 14);

-- -----------------------------------------------------
-- Mise à jour du compteur de joueurs sur les tables peuplées
-- Dans une vraie application, cela serait géré par des triggers ou la logique applicative.
-- -----------------------------------------------------
UPDATE table_poker SET nb_joueurs = 5 WHERE id_table = 1;
UPDATE table_poker SET nb_joueurs = 6 WHERE id_table = 2;
UPDATE table_poker SET nb_joueurs = 3 WHERE id_table = 5;
UPDATE table_poker SET nb_joueurs = 2 WHERE id_table = 9;

-- -----------------------------------------------------
-- Création de quelques parties (mains) et ajout des joueurs
-- -----------------------------------------------------
-- Une partie sur la table 2 avec tous les joueurs
INSERT INTO partie (id_table, pot) VALUES (2, 5.75);
SET @last_partie_id = LAST_INSERT_ID();
INSERT INTO partie_joueur (id_partie, id_joueur) VALUES
(@last_partie_id, 2), (@last_partie_id, 5), (@last_partie_id, 10),
(@last_partie_id, 11), (@last_partie_id, 20), (@last_partie_id, 30);

-- Une autre partie sur la table 2
INSERT INTO partie (id_table, pot) VALUES (2, 12.50);
SET @last_partie_id = LAST_INSERT_ID();
INSERT INTO partie_joueur (id_partie, id_joueur) VALUES
(@last_partie_id, 2), (@last_partie_id, 5), (@last_partie_id, 10),
(@last_partie_id, 11), (@last_partie_id, 20), (@last_partie_id, 30);

-- Une partie sur la table 9 (Heads Up)
INSERT INTO partie (id_table, pot) VALUES (9, 22.00);
SET @last_partie_id = LAST_INSERT_ID();
INSERT INTO partie_joueur (id_partie, id_joueur) VALUES
(@last_partie_id, 7), (@last_partie_id, 14);
