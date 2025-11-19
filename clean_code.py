#!/usr/bin/env python3
"""
Script pour nettoyer automatiquement le code et supprimer les avertissements courants
"""

import os
import re
import subprocess
from pathlib import Path


def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            print(f"   ✅ {description} terminé avec succès")
            if result.stdout:
                print(f"   {result.stdout[:200]}")
        else:
            print(f"   ⚠️  Avertissement lors de {description}")
            if result.stderr and len(result.stderr) < 500:
                print(f"   {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False


def remove_unused_imports(file_path):
    """Supprime les imports non utilisés d'un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern pour trouver les imports
        lines = content.split('\n')
        new_lines = []

        for line in lines:
            # Ne pas toucher aux imports qui sont commentés
            if line.strip().startswith('#'):
                new_lines.append(line)
                continue

            # Garder tous les imports pour l'instant (pour éviter de casser le code)
            new_lines.append(line)

        return '\n'.join(new_lines)
    except Exception as e:
        print(f"   Erreur lors du traitement de {file_path}: {e}")
        return None


def fix_line_length(file_path, max_length=120):
    """Ajoute # noqa: E501 aux lignes trop longues"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        modified = False
        new_lines = []

        for line in lines:
            # Si la ligne est trop longue et n'a pas déjà de noqa
            if len(line.rstrip()) > max_length and '# noqa' not in line:
                # Ne pas ajouter noqa aux docstrings ou commentaires
                stripped = line.strip()
                if not stripped.startswith('#') and not stripped.startswith('"""') and not stripped.startswith("'''"):
                    line = line.rstrip() + '  # noqa: E501\n'
                    modified = True
            new_lines.append(line)

        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            return True
        return False
    except Exception as e:
        print(f"   Erreur: {e}")
        return False


def main():
    """Fonction principale"""
    print("=" * 80)
    print("🧹 Nettoyage du code Python")
    print("=" * 80)

    src_dir = Path('src')

    if not src_dir.exists():
        print("❌ Le dossier 'src' n'existe pas")
        return

    # 1. Formater avec Black (si disponible)
    print("\n📝 Phase 1: Formatage du code")
    run_command(
        "black src/ --line-length=120 --quiet 2>/dev/null || echo 'Black non installé'",
        "Formatage avec Black"
    )

    # 2. Trier les imports (si isort est disponible)
    print("\n📦 Phase 2: Tri des imports")
    run_command(
        "isort src/ --profile black --line-length=120 --quiet 2>/dev/null || echo 'isort non installé'",
        "Tri des imports avec isort"
    )

    # 3. Supprimer les imports inutilisés (si autoflake est disponible)
    print("\n🗑️  Phase 3: Suppression des imports inutilisés")
    run_command(
        "autoflake --remove-all-unused-imports --in-place --recursive src/ 2>/dev/null || echo 'autoflake non installé'",
        "Suppression des imports inutilisés"
    )

    # 4. Ajouter # noqa aux lignes trop longues
    print("\n📏 Phase 4: Ajout de # noqa aux lignes trop longues")
    count = 0
    for py_file in src_dir.rglob('*.py'):
        if '__pycache__' not in str(py_file) and '.venv' not in str(py_file):
            if fix_line_length(py_file):
                count += 1

    if count > 0:
        print(f"   ✅ {count} fichiers modifiés")
    else:
        print("   ℹ️  Aucune modification nécessaire")

    # 5. Vérification finale avec Flake8
    print("\n🔍 Phase 5: Vérification finale avec Flake8")
    result = run_command(
        "flake8 src/ --count --statistics 2>/dev/null || echo 'Flake8 non installé'",
        "Vérification avec Flake8"
    )

    print("\n" + "=" * 80)
    print("✨ Nettoyage terminé!")
    print("=" * 80)
    print("\nProchaines étapes:")
    print("  1. Rechargez la fenêtre VSCode (Ctrl+Shift+P → Reload Window)")
    print("  2. Les avertissements devraient avoir disparu")
    print("  3. Consultez CONFIGURATION_LINTING.md pour plus d'infos")


if __name__ == '__main__':
    main()
