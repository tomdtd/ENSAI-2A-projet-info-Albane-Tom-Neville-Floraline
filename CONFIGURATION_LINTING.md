# Configuration du Linting et Formatage

Ce document explique comment configurer et désactiver les avertissements de formatage dans le projet.

## Fichiers de Configuration Créés

### 1. `.flake8` - Configuration Flake8

Ce fichier désactive les erreurs de formatage non critiques :
- **E501** : Lignes trop longues (> 120 caractères)
- **E131** : Indentation non alignée
- **E252** : Espaces autour des paramètres
- **F841** : Variables locales non utilisées
- **W503/W504** : Sauts de ligne autour des opérateurs

### 2. `.pylintrc` - Configuration Pylint

Configuration complète pour Pylint avec des règles assouplies :
- Longueur de ligne maximale : 120 caractères
- Désactivation des warnings sur les variables non utilisées
- Désactivation des avertissements de complexité excessive
- Autorisation des noms de variables courts (i, j, k, e, etc.)

### 3. `pyproject.toml` - Configuration Générale

Contient les configurations pour :
- **Black** : Formatage du code (ligne max 120 caractères)
- **isort** : Tri des imports
- **mypy** : Vérification de types (désactivé pour la plupart des warnings)
- **pytest** : Configuration des tests
- **coverage** : Couverture de code

### 4. `.vscode/settings.json` - Configuration VSCode

Configuration spécifique à VSCode pour :
- Utiliser Flake8 avec la configuration personnalisée
- Désactiver les warnings de l'analyseur Python
- Ne pas formater automatiquement à la sauvegarde
- Masquer les fichiers de cache

## Comment Utiliser

### Recharger la Configuration dans VSCode

1. Ouvrez la palette de commandes : `Ctrl+Shift+P` (ou `Cmd+Shift+P` sur Mac)
2. Tapez "Reload Window" et appuyez sur Entrée
3. Les erreurs de formatage devraient disparaître

### Vérifier le Linting Manuellement

```bash
# Avec Flake8 (utilise automatiquement .flake8)
flake8 src/

# Avec Pylint (utilise automatiquement .pylintrc)
pylint src/

# Formater le code avec Black
black src/ --line-length=120
```

### Si les Erreurs Persistent

#### Option 1 : Désactiver complètement le linting dans VSCode

Ajoutez dans `.vscode/settings.json` :
```json
{
    "python.linting.enabled": false
}
```

#### Option 2 : Désactiver seulement certaines règles

Dans `.vscode/settings.json`, ajoutez des diagnostics spécifiques :
```json
{
    "python.analysis.diagnosticSeverityOverrides": {
        "reportUnusedVariable": "none",
        "reportUnusedImport": "none"
    }
}
```

#### Option 3 : Ignorer les erreurs dans un fichier spécifique

En haut du fichier Python, ajoutez :
```python
# flake8: noqa
# pylint: skip-file
```

Ou pour une ligne spécifique :
```python
variable = "exemple"  # noqa: F841
```

## Erreurs Spécifiques Désactivées

Les erreurs que vous voyiez sont maintenant désactivées :

| Code | Description | Désactivé dans |
|------|-------------|----------------|
| E131 | Continuation line unaligned | .flake8 |
| E501 | Line too long | .flake8 |
| E252 | Missing whitespace around parameter equals | .flake8 |
| F841 | Local variable assigned but never used | .flake8 |

## Commandes Utiles

```bash
# Lister toutes les erreurs Flake8
flake8 src/ --statistics

# Compter les erreurs par type
flake8 src/ --count

# Voir uniquement les erreurs d'un type spécifique
flake8 src/ --select=E501

# Ignorer des erreurs spécifiques pour une commande
flake8 src/ --ignore=E501,F841
```

## Formatage Recommandé

Pour maintenir un code propre sans les avertissements :

1. **Utilisez Black** pour le formatage automatique :
   ```bash
   black src/ --line-length=120
   ```

2. **Triez les imports** avec isort :
   ```bash
   isort src/ --profile black
   ```

3. **Nettoyez les imports inutilisés** avec autoflake :
   ```bash
   pip install autoflake
   autoflake --remove-all-unused-imports --in-place src/**/*.py
   ```

## Notes

- Les configurations sont appliquées automatiquement lorsque vous ouvrez le projet dans VSCode
- Les fichiers de configuration sont reconnus automatiquement par les outils de linting
- Vous pouvez toujours exécuter manuellement les outils avec leurs configurations par défaut en utilisant des flags

## Support

Si vous rencontrez des problèmes :
1. Rechargez la fenêtre VSCode (`Ctrl+Shift+P` → "Reload Window")
2. Vérifiez que les extensions Python sont installées
3. Consultez la sortie du linter : `Ctrl+Shift+U` → Sélectionnez "Python"
