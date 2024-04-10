# ENSAI-2A-projet-info-template

Template du projet informatique de 2e année de l'ENSAI.
Cette application très simple comporte quelques éléments qui peuvent aider pour le projet info 2A :

- programmation en couche (DAO, service, dto)
- connexion à une base de données
- interface dans le terminal (couche view) avec inquirerPy
- Appel d'un Webservice
- Création d'un Webservice

## :arrow_forward: Cloner le dépôt

- [ ] Créez un dossier `P:/Cours2A/UE3-Projet-info`
- [ ] Allez dans ce dossier
- [ ] Clic droit > `Git Bash here`
- [ ] Clonez ce dépôt : `git clone https://github.com/ludo2ne/ENSAI-2A-projet-info-template.git`

---

## :arrow_forward: Ouvrir le dépôt avec VS Code

- [ ] Ouvrez Visual Studio Code
- [ ] File > Open Folder 
- [ ] Retrouvez dans l'arborescence le clone
- [ ] Cliquez une fois sur *ENSAI-2A-projet-info-template* et cliquez sur `Sélectionner un dossier`
  - :warning: Si le dossier parent dans l'explorer VScode (à gauche) n'est pas *ENSAI-2A-projet-info-template*, l'application ne fonctionnera pas

### Paramètres VScode

Pour information, ce dépôt contient un fichier `.vscode/settings.xml` qui définit des paramètres pour ce projet. Par exemple :

- **Black formatter** permet de mettre en forme automatiquement un fichier python
  - `editor.formatOnSave` : à chaque savegarde de fichier, le code est automatiquement mis en forme
- **Flake** est un Linter
  - il vérifie que le code est propre et affiche un message si ce n'est pas le cas
- **Path** : indique les dossiers dans lesquels sont les modules python 
  - `"PYTHONPATH": "${workspaceFolder}/src"` : src est le dossier racine des imports


---

## :arrow_forward: Installer les packages nécessaires

Dans Visual Studio Code :

- [ ] ouvrez un terminal *Git Bash*
- [ ] exécutez les commandes suivantes

```bash
pip install -r requirements.txt
pip list
```

---

## :arrow_forward: Variables d'environnement

Vous allez maintenant définir des variables d'environnement pour déclarer la base de données et le webservice auquels vous allez connecter votre application python.

À la racine du projet le fichier :

- [ ] Créez un fichier nommé `.env` 
- [ ] Collez-y et complétez les éléments ci-dessous

```
HOST_WEBSERVICE=https://pokeapi.co/api/v2

HOST=sgbd-eleves.domensai.ecole
PORT=5432
DATABASE=idxxxx
USER=idxxxx
PASSWORD=idxxxx
SCHEMA=projet
```

---

## :arrow_forward: Lancer les tests unitaires

- [ ] Dans Git Bash : `pytest -v` 
  - ou `python -m pytest -v` si *pytest* n'a pas été ajouté au *PATH*

Il est également possible de générer la couverture de tests avec [Coverage](https://coverage.readthedocs.io/en/7.4.0/index.html)
:bulb: Le fichier `.coveragerc` permet de modifier le paramétrage

- [ ] `coverage run -m pytest`
- [ ] `coverage html`
- [ ] Ouvrir le fichier coverage_report/index.html

Les tests unitaires de la DAO utilisent les données du fichier `data/pop_db_test.sql`.
Ces données sont chargées dans un schéma à part (projet_test_dao) pour ne pas polluer les autres données.

---

## :arrow_forward: Lancer le programme

Cette application propose une interface graphique très basique pour naviguer entre différents menus.

- [ ] Dans Git Bash : `python src/__main__.py`
- [ ] au premier lancement, choisissez **Ré-initialiser la base de données**
  - cela appelle le programme `src/utils/reset_database.py`
  - qui lui même va exécuter les scripts SQL du dossier `data`

---

## :arrow_forward: Lancer le webservice

Cette application permet également de créer un webservice.

- [ ] `python src/app.py`
- Exemples de endpoints (à tester par exemple avec *Insomnia* ou éventuellement un navigateur):
  - `GET http://localhost/docs` (swagger)
  - `GET http://localhost/hello/you`
  - `GET http://localhost/joueur`
  - `GET http://localhost/joueur/3`
  - ```
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
  - ```
    PUT http://localhost/joueur/3
    JSON body :
      {
         "pseudo": "maurice_new",
         "mdp": null,
         "age": 20,
         "mail": "maurice@ensai.fr",
         "fan_pokemon": true
      }
    ```
  - `DELETE http://localhost/joueur/5`

---

## :arrow_forward: Les logs

- le fichier `logging_config.yml` permet de définir les paramètres de logs
- un décorateur a été créé dans `src/utils/log_decorator.py`
  - appliqué à une méthode, il permettra d'afficher dans les logs :
    - les paramétres d'entrée
    - la sortie
- les logs sont consultables dans le dossier `logs`

---

## :arrow_forward: Intégration continue

Le dépôt contient un fichier `.github/workflow/main.yml`.

Lorsque vous faîtes un *push* sur GitHub, cela déclanche un pipeline qui va effectuer les les étapes suivantes :

- Création d'un conteneur à partir d'une image Ubuntu (Linux)
  - Autrement dit, cela crée une machine virtuelle avec simplement un noyau Linux
- Installation de Python
- Installation des packages requis
- Lancement des tests unitaires (uniquement les tests de service car plus compliqué de lancer les tests dao)
- Analyse du code avec *pylint*
  - Si la note est inférieure à 7.5, l'étape sera en échec

Vous pouvez consulter le bon déroulement de ce pipeline sur la page GitHub de votre dépôt, onglet *Actions*.