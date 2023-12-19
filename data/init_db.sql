DROP SCHEMA IF EXISTS projet CASCADE;
CREATE SCHEMA projet;


-----------------------------------------------------
-- Joueur
-----------------------------------------------------
DROP TABLE IF EXISTS projet.joueur CASCADE ;
CREATE TABLE projet.joueur(
    id_joueur    SERIAL PRIMARY KEY,
    pseudo       TEXT UNIQUE,
    mdp          TEXT,
    age          INTEGER,
    mail         TEXT,
    fan_pokemon  BOOLEAN
);
