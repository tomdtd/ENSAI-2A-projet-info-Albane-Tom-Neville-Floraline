#!/bin/bash
# Script pour exécuter les tests avec le bon PYTHONPATH

# Définir le répertoire racine du projet
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Définir PYTHONPATH
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH}"

# Exécuter pytest avec les arguments passés au script
python -m pytest "$@"
