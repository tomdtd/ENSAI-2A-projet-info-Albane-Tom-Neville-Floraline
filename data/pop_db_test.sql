INSERT INTO joueur(id_joueur, pseudo, mdp, mail, age, credit)
OVERRIDING SYSTEM VALUE
VALUES
(999, 'admin',    '82ec27c3e05e57a62a5a1a5b3907e4836f693a1df70e59b03e20433b2a60c6df', 'admin@projet.fr', 0, 0),
(998, 'a',        '961b6dd3ede3cb8ecbaacbd68de040cd78eb2ed5889130cceb4c49268ea4d506', 'a@ensai.fr',      20, 10),
(997, 'maurice',  '2b9ff2caf3872dda673847ec75ff6ae0968fc0c24a2b7e4bb6aeb21288ba462e', 'maurice@ensai.fr',20, 50),
(996, 'batricia', 'e99bf7ce2b5216ff9811d3518cfe4499ddb9cb398e01600046a8f556d3e0b358', 'bat@projet.fr',   25, 30),
(995, 'miguel',   'c3b9d2196e24f68d35091ecc3615bb8b3cd12b127e06e86b64e533f9844d6c2e', 'miguel@projet.fr',23, 15),
(994, 'gilbert',  '968356512a7c3c61686eaabe4e6bce327a4f3937bcc7dd7f97498b505a1d4119', 'gilbert@projet.fr',21, 40),
(993, 'junior',   '9d6ecb35e514a49d7ea1df9dca7ac74d05fae531081f5860153697957fa66bc4', 'junior@projet.fr', 15, 20);