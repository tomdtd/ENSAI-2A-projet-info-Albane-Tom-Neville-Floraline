# Guide d'exécution des tests

## Configuration du projet

Ce projet utilise une structure d'imports absolus avec le préfixe `src.`.

### Prérequis

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Exécution des tests

### Méthode 1 : Script automatique (recommandé)

Utilisez le script `run_tests.sh` qui configure automatiquement le PYTHONPATH :

```bash
# Tous les tests
./run_tests.sh

# Tests d'un dossier spécifique
./run_tests.sh src/tests/test_dao/

# Un fichier de test spécifique
./run_tests.sh src/tests/test_dao/test_admin_dao.py

# Un test spécifique
./run_tests.sh src/tests/test_dao/test_admin_dao.py::TestAdminDao::test_creer_admin_success
```

### Méthode 2 : Commande manuelle

Si vous préférez exécuter pytest manuellement, définissez le PYTHONPATH :

```bash
PYTHONPATH=. python -m pytest src/tests/test_dao/ -v
```

### Méthode 3 : Depuis l'IDE

Si vous utilisez un IDE (PyCharm, VSCode, etc.), configurez le working directory sur la racine du projet et ajoutez `.` au PYTHONPATH.

## Configuration pytest

Le fichier `pytest.ini` à la racine configure automatiquement :
- Le PYTHONPATH
- Les répertoires de tests
- Les options d'affichage

## Structure des imports

Tous les imports dans le projet doivent utiliser le préfixe `src.` :

✅ **Correct :**
```python
from src.dao.joueur_dao import JoueurDao
from src.business_object.joueur import Joueur
from src.utils.securite import hash_password
```

❌ **Incorrect :**
```python
from dao.joueur_dao import JoueurDao
from business_object.joueur import Joueur
from utils.securite import hash_password
```

## Résolution des problèmes courants

### Erreur : "ModuleNotFoundError: No module named 'src'"

**Solution :** Assurez-vous que le PYTHONPATH inclut le répertoire racine :
```bash
export PYTHONPATH=/chemin/vers/projet:$PYTHONPATH
```

Ou utilisez le script `run_tests.sh` qui le fait automatiquement.

### Erreur : "ModuleNotFoundError: No module named 'dao'"

**Solution :** Vos imports utilisent l'ancien format. Utilisez le script `fix_imports.py` :
```bash
python fix_imports.py
```

### Erreur : "ModuleNotFoundError: No module named 'psycopg2'"

**Solution :** Installez les dépendances :
```bash
pip install -r requirements.txt
```
