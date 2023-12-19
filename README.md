# ENSAI-projet-info-2A-template

Template du projet informatique de 2e année de l'ENSAI.
Cette application très simple comporte quelques éléments qui peuvent aider pour le projet info 2A :

* programmation en couche (DAO, service, business_object)
* connexion à une base de données
* interface dans le terminal (couche view) avec inquirerPy
* Appel d'un Webservice
* Création d'un Webservice

## :arrow_forward: Cloner le dépôt

```bash
git clone https://github.com/ludo2ne/ENSAI-2A-projet-info-template.git

# ou si vous avez une clé ssh :
git clone git@github.com:ludo2ne/ENSAI-2A-projet-info-template.git
```

## :arrow_forward: Ouvrir le code avec Visual Studio Code

* File > Open Folder > ENSAI-2A-projet-info-template
* :warning: Si le dossier parent dans l'explorer VScode n'est pas `ENSAI-2A-projet-info-template`, l'application ne fonctionnera pas

## :arrow_forward: Installer les packages nécessaires

```bash
pip install -r requirements.txt
pip list
```

## :arrow_forward: Variables d'environnement

Modifier à la racine du projet le fichier `.env` qui contient :

```
HOST_WEBSERVICE=https://pokeapi.co/api/v2

HOST=sgbd-eleves.domensai.ecole
PORT=5432
DATABASE=idxxxx
USER=idxxxx
PASSWORD=idxxxx
```

## :arrow_forward: Lancer les tests unitaires

* `python -m unittest`

## :arrow_forward: Lancer le programme

* `python src/__main__.py`
* au premier lancement, choisissez **Ré-initialiser la base de données**
  * cela appelle le programme `src/utils/reset_database.py`
  * qui lui même va exécuter les scripts SQL du dossier `data`
  
## :arrow_forward: Lancer le webservice

* `python src/app.py`
* Exemples de endpoints :
  * `GET http://localhost/docs` (swagger)
  * `GET http://localhost/hello/you`
  * `GET http://localhost/joueur`
  * `GET http://localhost/joueur/3`
  * ```
    POST http://localhost/joueur/
    JSON body :
      {
        "pseudo": "patapouf",
      	 "mdp": "9999",
        "age": "95",
        "mail": "patapouf@mail.fr",
        "fan_pokemon": true
      }
    ```
