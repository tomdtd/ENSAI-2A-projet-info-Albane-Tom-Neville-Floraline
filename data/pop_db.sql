-- =====================================================================
--- INSERTION DES DONNÉES D'EXEMPLE
-- =====================================================================

-- -----------------------------------------------------
-- Insertion de 100 joueurs avec des noms français
-- -----------------------------------------------------
INSERT INTO joueur (id_joueur, pseudo, mdp, mail, age, credit) VALUES
(NULL, 'jean.dupont', 'hash_placeholder', 'jean.dupont@mail.com', 28, 150.00),
(NULL, 'marie.curie', 'hash_placeholder', 'marie.curie@mail.com', 35, 2500.50),
(NULL, 'pierre.martin', 'hash_placeholder', 'pierre.martin@mail.com', 31, 75.25),
(NULL, 'sophie.bernard', 'hash_placeholder', 'sophie.bernard@mail.com', 26, 500.00),
(NULL, 'luc.dubois', 'hash_placeholder', 'luc.dubois@mail.com', 29, 1200.00),
(NULL, 'camille.robert', 'hash_placeholder', 'camille.robert@mail.com', 32, 300.00),
(NULL, 'antoine.richard', 'hash_placeholder', 'antoine.richard@mail.com', 27, 950.75),
(NULL, 'emilie.petit', 'hash_placeholder', 'emilie.petit@mail.com', 24, 45.00),
(NULL, 'julien.durand', 'hash_placeholder', 'julien.durand@mail.com', 30, 880.00),
(NULL, 'laura.leroy', 'hash_placeholder', 'laura.leroy@mail.com', 33, 2100.00),
(NULL, 'nicolas.moreau', 'hash_placeholder', 'nicolas.moreau@mail.com', 22, 100.00),
(NULL, 'claire.simon', 'hash_placeholder', 'claire.simon@mail.com', 29, 650.00),
(NULL, 'alexandre.laurent', 'hash_placeholder', 'alexandre.laurent@mail.com', 34, 320.50),
(NULL, 'manon.lefevre', 'hash_placeholder', 'manon.lefevre@mail.com', 25, 1500.00),
(NULL, 'thomas.roux', 'hash_placeholder', 'thomas.roux@mail.com', 23, 50.00),
(NULL, 'chloe.david', 'hash_placeholder', 'chloe.david@mail.com', 27, 180.00),
(NULL, 'quentin.morel', 'hash_placeholder', 'quentin.morel@mail.com', 26, 730.00),
(NULL, 'lea.fournier', 'hash_placeholder', 'lea.fournier@mail.com', 24, 999.00),
(NULL, 'hugo.girard', 'hash_placeholder', 'hugo.girard@mail.com', 28, 120.00),
(NULL, 'eva.lambert', 'hash_placeholder', 'eva.lambert@mail.com', 30, 470.00),
(NULL, 'louis.bonnet', 'hash_placeholder', 'louis.bonnet@mail.com', 29, 250.00),
(NULL, 'emma.francois', 'hash_placeholder', 'emma.francois@mail.com', 27, 1100.00),
(NULL, 'gabriel.martinez', 'hash_placeholder', 'gabriel.martinez@mail.com', 33, 80.00),
(NULL, 'alice.legrand', 'hash_placeholder', 'alice.legrand@mail.com', 26, 540.00),
(NULL, 'raphael.garnier', 'hash_placeholder', 'raphael.garnier@mail.com', 31, 1350.00),
(NULL, 'juliette.faure', 'hash_placeholder', 'juliette.faure@mail.com', 22, 220.00),
(NULL, 'arthur.rousseau', 'hash_placeholder', 'arthur.rousseau@mail.com', 29, 680.00),
(NULL, 'sarah.vincent', 'hash_placeholder', 'sarah.vincent@mail.com', 25, 920.00),
(NULL, 'adam.muller', 'hash_placeholder', 'adam.muller@mail.com', 24, 170.00),
(NULL, 'ines.lemoine', 'hash_placeholder', 'ines.lemoine@mail.com', 28, 2000.00),
(NULL, 'paul.andre', 'hash_placeholder', 'paul.andre@mail.com', 30, 340.00),
(NULL, 'adele.mercier', 'hash_placeholder', 'adele.mercier@mail.com', 27, 490.00),
(NULL, 'victor.brun', 'hash_placeholder', 'victor.brun@mail.com', 26, 760.00),
(NULL, 'louise.gauthier', 'hash_placeholder', 'louise.gauthier@mail.com', 25, 1400.00),
(NULL, 'leo.masson', 'hash_placeholder', 'leo.masson@mail.com', 23, 90.00),
(NULL, 'zoe.blanc', 'hash_placeholder', 'zoe.blanc@mail.com', 28, 610.00),
(NULL, 'mohamed.guichard', 'hash_placeholder', 'mohamed.guichard@mail.com', 29, 270.00),
(NULL, 'lina.perez', 'hash_placeholder', 'lina.perez@mail.com', 24, 1600.00),
(NULL, 'enzo.robin', 'hash_placeholder', 'enzo.robin@mail.com', 31, 400.00),
(NULL, 'helena.clement', 'hash_placeholder', 'helena.clement@mail.com', 30, 820.00),
(NULL, 'sacha.morin', 'hash_placeholder', 'sacha.morin@mail.com', 22, 110.00),
(NULL, 'anna.nicolas', 'hash_placeholder', 'anna.nicolas@mail.com', 26, 700.00),
(NULL, 'tim.henry', 'hash_placeholder', 'tim.henry@mail.com', 27, 1900.00),
(NULL, 'rose.gaudin', 'hash_placeholder', 'rose.gaudin@mail.com', 21, 30.00),
(NULL, 'clement.michel', 'hash_placeholder', 'clement.michel@mail.com', 29, 580.00),
(NULL, 'maya.mathieu', 'hash_placeholder', 'maya.mathieu@mail.com', 25, 1250.00),
(NULL, 'maxime.guerin', 'hash_placeholder', 'maxime.guerin@mail.com', 28, 200.00),
(NULL, 'amelie.leclerc', 'hash_placeholder', 'amelie.leclerc@mail.com', 24, 780.00),
(NULL, 'theo.poulain', 'hash_placeholder', 'theo.poulain@mail.com', 30, 420.00),
(NULL, 'agathe.dumont', 'hash_placeholder', 'agathe.dumont@mail.com', 27, 930.00),
(NULL, 'gaspard.perrin', 'hash_placeholder', 'gaspard.perrin@mail.com', 28, 150.00),
(NULL, 'elise.dufour', 'hash_placeholder', 'elise.dufour@mail.com', 23, 1700.00),
(NULL, 'augustin.joly', 'hash_placeholder', 'augustin.joly@mail.com', 29, 60.00),
(NULL, 'romane.lecomte', 'hash_placeholder', 'romane.lecomte@mail.com', 25, 630.00),
(NULL, 'noah.boucher', 'hash_placeholder', 'noah.boucher@mail.com', 27, 360.00),
(NULL, 'lola.jacquet', 'hash_placeholder', 'lola.jacquet@mail.com', 24, 850.00),
(NULL, 'valentin.renard', 'hash_placeholder', 'valentin.renard@mail.com', 29, 1300.00),
(NULL, 'margot.meunier', 'hash_placeholder', 'margot.meunier@mail.com', 26, 240.00),
(NULL, 'samuel.brunet', 'hash_placeholder', 'samuel.brunet@mail.com', 30, 510.00),
(NULL, 'alix.schmitt', 'hash_placeholder', 'alix.schmitt@mail.com', 25, 1050.00),
(NULL, 'oscar.da-silva', 'hash_placeholder', 'oscar.da-silva@mail.com', 27, 190.00),
(NULL, 'jeanne.leroux', 'hash_placeholder', 'jeanne.leroux@mail.com', 26, 710.00),
(NULL, 'yannis.colin', 'hash_placeholder', 'yannis.colin@mail.com', 28, 440.00),
(NULL, 'capucine.barbier', 'hash_placeholder', 'capucine.barbier@mail.com', 22, 970.00),
(NULL, 'basile.vidal', 'hash_placeholder', 'basile.vidal@mail.com', 23, 140.00),
(NULL, 'celia.caron', 'hash_placeholder', 'celia.caron@mail.com', 25, 1800.00),
(NULL, 'felix.charles', 'hash_placeholder', 'felix.charles@mail.com', 29, 80.00),
(NULL, 'diane.renaud', 'hash_placeholder', 'diane.renaud@mail.com', 30, 660.00),
(NULL, 'marius.gomez', 'hash_placeholder', 'marius.gomez@mail.com', 28, 380.00),
(NULL, 'elena.lopes', 'hash_placeholder', 'elena.lopes@mail.com', 27, 890.00),
(NULL, 'nathan.roger', 'hash_placeholder', 'nathan.roger@mail.com', 25, 1150.00),
(NULL, 'iris.marchand', 'hash_placeholder', 'iris.marchand@mail.com', 24, 280.00),
(NULL, 'ismael.roy', 'hash_placeholder', 'ismael.roy@mail.com', 26, 560.00),
(NULL, 'leonore.picard', 'hash_placeholder', 'leonore.picard@mail.com', 27, 1000.00),
(NULL, 'elie.philippe', 'hash_placeholder', 'elie.philippe@mail.com', 29, 160.00),
(NULL, 'romy.duval', 'hash_placeholder', 'romy.duval@mail.com', 25, 740.00),
(NULL, 'milan.lucas', 'hash_placeholder', 'milan.lucas@mail.com', 28, 460.00),
(NULL, 'victoria.deschamps', 'hash_placeholder', 'victoria.deschamps@mail.com', 26, 940.00),
(NULL, 'aaron.baron', 'hash_placeholder', 'aaron.baron@mail.com', 23, 130.00),
(NULL, 'olivia.bertin', 'hash_placeholder', 'olivia.bertin@mail.com', 30, 1650.00),
(NULL, 'edouard.boulanger', 'hash_placeholder', 'edouard.boulanger@mail.com', 27, 70.00),
(NULL, 'constance.gerard', 'hash_placeholder', 'constance.gerard@mail.com', 29, 690.00),
(NULL, 'noe.lamy', 'hash_placeholder', 'noe.lamy@mail.com', 22, 390.00),
(NULL, 'marion.le-roux', 'hash_placeholder', 'marion.le-roux@mail.com', 25, 860.00),
(NULL, 'robin.maillard', 'hash_placeholder', 'robin.maillard@mail.com', 28, 1200.00),
(NULL, 'adele.barre', 'hash_placeholder', 'adele.barre@mail.com', 26, 260.00),
(NULL, 'hippolyte.denis', 'hash_placeholder', 'hippolyte.denis@mail.com', 30, 530.00),
(NULL, 'thea.royer', 'hash_placeholder', 'thea.royer@mail.com', 25, 1100.00),
(NULL, 'martin.fabre', 'hash_placeholder', 'martin.fabre@mail.com', 29, 210.00),
(NULL, 'lea.aubert', 'hash_placeholder', 'lea.aubert@mail.com', 27, 790.00),
(NULL, 'simon.carpentier', 'hash_placeholder', 'simon.carpentier@mail.com', 28, 430.00),
(NULL, 'lou.guillot', 'hash_placeholder', 'lou.guillot@mail.com', 23, 960.00),
(NULL, 'gabin.lucas', 'hash_placeholder', 'gabin.lucas@mail.com', 24, 180.00),
(NULL, 'celestine.ferreira', 'hash_placeholder', 'celestine.ferreira@mail.com', 30, 1950.00),
(NULL, 'baptiste.morvan', 'hash_placeholder', 'baptiste.morvan@mail.com', 26, 95.00),
(NULL, 'anouk.fleury', 'hash_placeholder', 'anouk.fleury@mail.com', 25, 620.00);

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
