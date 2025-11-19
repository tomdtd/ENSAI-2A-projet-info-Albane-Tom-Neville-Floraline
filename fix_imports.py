#!/usr/bin/env python3
"""Script pour corriger tous les imports du projet"""

import os
import re
from pathlib import Path

def fix_imports_in_file(filepath):
    """Corrige les imports dans un fichier donné"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Remplacer les imports
    replacements = [
        (r'^from dao\.', 'from src.dao.'),
        (r'^from business_object\.', 'from src.business_object.'),
        (r'^from service\.', 'from src.service.'),
        (r'^from view\.', 'from src.view.'),
    ]

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Parcourt tous les fichiers Python et corrige les imports"""
    src_dir = Path('src')
    modified_files = []

    for py_file in src_dir.rglob('*.py'):
        if fix_imports_in_file(py_file):
            modified_files.append(str(py_file))

    print(f"✅ {len(modified_files)} fichiers modifiés")
    if modified_files:
        print("\nFichiers modifiés:")
        for f in sorted(modified_files):
            print(f"  - {f}")

if __name__ == '__main__':
    main()
