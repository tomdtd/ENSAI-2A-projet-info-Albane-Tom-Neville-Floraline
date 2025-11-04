INSERT INTO joueur(id_joueur, pseudo, mdp, mail, age, credit)
OVERRIDING SYSTEM VALUE
VALUES
(999, 'admin',    '0000', 'admin@projet.fr', 0, 0),
(998, 'a',        'a',    'a@ensai.fr',      20, 10),
(997, 'maurice',  '1234', 'maurice@ensai.fr',20, 50),
(996, 'batricia', '9876', 'bat@projet.fr',   25, 30),
(995, 'miguel',   'abcd', 'miguel@projet.fr',23, 15),
(994, 'gilbert',  'toto', 'gilbert@projet.fr',21, 40),
(993, 'junior',   'aaaa', 'junior@projet.fr', 15, 20);