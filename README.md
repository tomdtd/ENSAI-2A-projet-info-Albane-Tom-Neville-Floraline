# ENSAI-2A-projet-info-Albane-Tom-Neville-Floraline

Recommandations pour l’application de poker

Cette application intègre plusieurs éléments utiles pour notre projet Informatique :

- Programmation en couches (DAO, service, view, business_object)
- Connexion à une base de données
- Interface terminal (couche view) avec [inquirerPy](https://inquirerpy.readthedocs.io/en/latest/)
- Appel d'un Webservice
- Création d'un webservice


## :arrow_forward: Logiciels et outils

- [Visual Studio Code](https://code.visualstudio.com/)
- [Python 3.13](https://www.python.org/)
- [Git](https://git-scm.com/)
- Une base de données [PostgreSQL](https://www.postgresql.org/)


## :arrow_forward: Clone the repository

- [ ] Ouvrir VSCode
- [ ] Ouvrir **Git Bash**
- [ ] Cloner le dépôt :
  - `git clone https://github.com/tomdtd/ENSAI-2A-projet-info-Albane-Tom-Neville-Floraline.git`


### Open Folder

- [ ] Ouvrir **Visual Studio Code** via Onyxia SSPLAB
- [ ] Dans Visual Studio Code : File > Open Folder
- [ ] Sélectionner le dossier   *ENSAI-2A-projet-info-Albane-Tom-Neville-Floraline*
  - *ENSAI-2A-projet-info-Albane-Tom-Neville-Floraline* Ce dossier doit être la racine de l’Explorer
  - :warning: Sinon l’application ne se lancera pas correctement


## :arrow_forward: Structure du dépôt


| Item                       | Description                                                              |
| -------------------------- | ------------------------------------------------------------------------ |
| `README.md`                | Informations pour présenter, installer et utiliser l’application |
| `LICENSE`                  | Droits d’utilisation et termes de licence du dépôt        |

### Fichiers de configuration

Le dépôt contient de nombreux fichiers de configuration pour paramétrer les outils utilisés.

 En pratique, seuls `.env`, `.env_test` et `requirements.txt` doivent être modifiés pour le projet.


| Élément                      | Description                                                              |
| -------------------------- | ------------------------------------------------------------------------ |
| `.github/workflows/ci.yml` | Workflow CI automatisé (tests, linting, déploiement) |
| `.vscode/settings.json`    | Paramètres VSCode spécifiques au projet                      |
| `.coveragerc`              | Configuration de la couverture de tests                                                  |
| `.gitignore`               | Liste des fichiers/dossiers ignorés par Git            |
| `logging_config.yml`       | Configuration du logging                                                        |
| `requirements.txt`         | Liste des dépendances Python nécessaires                   |

  Vous aurez aussi besoin du fichier `.env`. Voir ci-dessous.


### Dossiers

| Élément               | Description                                                              |
| -------------------------- | ------------------------------------------------------------------------ |
| `data`                     | Scripts SQL contenant les jeux de données                                        |
| `doc`                      | Diagrammes UML, suivi du projet...                                          |
| `logs`                     | Fichiers de logs générés après lancement de l’application        |
| `src`                      | Code source Python, organisé selon une architecture en couches   |



### Documents de paramétrages

Le dépôt contient de nombreux fichiers de configuration pour paramétrer les outils utilisés.

En pratique, seuls `.env`, `.env_test` et `requirements.txt`doivent être modifiés pour le projet.


## :arrow_forward: Installation des dépendances

- [ ] Dans le terminal Git Bash, faire tourner les lignes de codes suivantes:


```bash
pip install -r requirements.txt
pip list
```
  - Cela permet d'installer le contenu de `requirements.txt`
  - affiche la liste de tous les packages chargés

## :arrow_forward: Variables d'environnement

Définir les variables d’environnement pour connecter l’application Python à la base et au webservice.

À la racine du projet :

- [ ] Créer un fichier`.env`


Si vous passez directement par le lien copier coller dans onyxia pas besoin des variables export VAULT_ADDR et export VAULT_TOKEN

```default
WEBSERVICE_HOST=https://pickpoker.com/api

POSTGRES_HOST=sgbd-eleves.domensai.ecole
POSTGRES_PORT=5432
POSTGRES_DATABASE=prod_poker
POSTGRES_USER=idxxxx
POSTGRES_PASSWORD=idxxxx
POSTGRES_SCHEMA=projet
POSTGRES_SCHEMA=public

export VAULT_ADDR=https://vault.lab.sspcloud.fr #voir pour changer l'endroit
export VAULT_TOKEN=********

API_URL = "url_de_l'api"
```


 À la racine du projet:

- [ ] Créer un fichier `.env_test`
- [ ] Coller les éléments suivants:

```default
WEBSERVICE_HOST=https://pickpoker.com/api

POSTGRES_HOST=sgbd-eleves.domensai.ecole
POSTGRES_PORT=5432
POSTGRES_DATABASE=idxxxx
POSTGRES_USER=idxxxx
POSTGRES_PASSWORD=idxxxx
POSTGRES_SCHEMA=projet
```

## Création de la base de donnée prod_poker et des tables associées

Executer le script creation_db_pord_poker.py

## :arrow_forward: Tests unitaires

- [ ] Dans Git Bash: `pytest -v` 
  - ou `python -m pytest -v` si *pytest* n'a pas été ajouté à *PATH*


### Tests unitaires DAO

Les tests DAO utilisent un schéma dédié `projet_test_dao` afin de ne pas polluer la base réelle.

Les données proviennent du fichier `data/pop_db_test.sql`.



### Couverture de tests

Générer la couverture avec [Coverage](https://coverage.readthedocs.io/en/7.4.0/index.html)

:bulb: Le fichier `.coveragerc` peut être utilisé pour modifier les paramètres

- [ ] `coverage run -m pytest`
- [ ] `coverage report -m`
- [ ] `coverage html`
  - Télécharger et ouvrir coverage_report/index.html



## :arrow_forward: Lancer l'application CLI 

- [ ] Dans Git Bash: `python src/main.py`
- [ ] Au premier lancement, choisir **Reset database** pour exécuter `src/utils/reset_database.py` et et charger les scripts SQL du dossier `data`.



## :arrow_forward: Lancer le webservice

- [ ] `python src/api.py`

Documentation :

- https://en.wikipedia.org/wiki/Texas_hold_%27em
- https://oag.ca.gov/sites/all/files/agweb/pdfs/gambling/BGC_texas.pdf

### Endpoints

Examples d'endpoints (à tester avec *Insomnia* or a moteur de recherche):


- `GET http://localhost:8000/joueur`
- `GET http://localhost:8000/joueur/997`
- ```
POST http://localhost:8000/joueur
Content-Type: application/json

{
  "pseudo": "charlotte",
  "mdp": "azerty",
  "mail": "charlotte@ensai.fr",
  "age": 28,
  "credit": 100.00
}
  ```
- ```
  PUT http://localhost/joueur/3
  JSON body :
    {
       "pseudo": "marie.curie",
       "mdp": 12345,
       "credit": "2500.50" 
    }
  ```
- `DELETE http://localhost/joueur/2`



## :arrow_forward: Logs

Initialisés dans `src/utils/log_init.py`avec la configuration : `logging_config.yml`.
Un décorateur `src/utils/log_decorator.py`permet de tracer les entrées/sorties des méthodes.

Les fichiers de logs sont stockés dans le dossier `logs`:

Exemples of logs :

```
22/11/2025 09:07:07 - INFO     - ConnexionVue
22/11/2025 09:07:08 - INFO     -     JoueurService.se_connecter('a', '*****') - DEBUT
22/11/2025 09:07:08 - INFO     -         hash_password('*****', 'a') - DEBUT
22/11/2025 09:07:08 - INFO     -         hash_password('*****', 'a') - FIN
22/11/2025 09:07:08 - INFO     -         JoueurDao.se_connecter('a', 'hashed_*****') - DEBUT
22/11/2025 09:07:08 - INFO     -         JoueurDao.se_connecter('a', 'hashed_*****') - FIN
22/11/2025 09:07:08 - INFO     -            └─> Sortie : Joueur(a, 20 ans)
22/11/2025 09:07:08 - INFO     -     JoueurService.se_connecter('a', '*****') - FIN
22/11/2025 09:07:08 - INFO     -        └─> Sortie : Joueur(a, 20 ans)
22/11/2025 09:07:08 - INFO     -     JoueurService.pseudo_deja_utilise('a') - DEBUT
22/11/2025 09:07:08 - INFO     -         JoueurDao.lister_tous() - DEBUT
22/11/2025 09:07:08 - INFO     -         JoueurDao.lister_tous() - FIN
22/11/2025 09:07:08 - INFO     -            └─> Sortie : [Joueur(a), Joueur(b), Joueur(c)]
22/11/2025 09:07:08 - INFO     -     JoueurService.pseudo_deja_utilise('a') - FIN
22/11/2025 09:07:08 - INFO     -        └─> Sortie : True
22/11/2025 09:07:08 - INFO     - MenuJoueurVue
```



## :arrow_forward: Continuous integration (CI)

Le dépôt contient un workflow GitHub Actions`.github/workflow/main.yml'.

À chaque *push*, une pipeline est déclenchée :

- Création d’un conteneur Ubuntu
- Installation de Python et des dépendances
- Exécution des tests unitaires (services uniquement)
- Installation des packages requis
- Exécution des tests unitaires (services uniquement)
- Analyse du code avec *pylint*
  - Échec si score < 7.5

Le suivi du pipeline est visible dans l’onglet Actions du dépôt GitHub.