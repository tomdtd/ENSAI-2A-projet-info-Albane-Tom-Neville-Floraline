-----------------------------------------------------
-- Joueur
-----------------------------------------------------
DROP TABLE IF EXISTS projet.joueur CASCADE ;
CREATE TABLE projet.joueur(
    id_joueur    SERIAL PRIMARY KEY,
    pseudo       VARCHAR(30) UNIQUE,
    mdp          VARCHAR(256),
    age          INTEGER,
    mail         VARCHAR(50),
    fan_pokemon  BOOLEAN
);
