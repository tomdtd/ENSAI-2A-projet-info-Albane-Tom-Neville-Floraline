#!/usr/bin/env python3
"""
Script pour vérifier que le linting est bien désactivé
"""

import json
from pathlib import Path


def verifier_configuration():
    """Vérifie la configuration VSCode"""

    print("=" * 70)
    print("🔍 VÉRIFICATION DE LA CONFIGURATION VSCODE")
    print("=" * 70)

    settings_path = Path('.vscode/settings.json')

    if not settings_path.exists():
        print("\n❌ Fichier .vscode/settings.json introuvable!")
        return False

    with open(settings_path, 'r') as f:
        # Lire le fichier même s'il contient des commentaires
        content = f.read()
        # Supprimer les commentaires pour le parsing JSON
        lines = []
        for line in content.split('\n'):
            # Supprimer les commentaires //
            if '//' in line:
                line = line[:line.index('//')]
            lines.append(line)
        clean_content = '\n'.join(lines)

        try:
            settings = json.loads(clean_content)
        except json.JSONDecodeError:
            print("\n⚠️  Impossible de parser le JSON (peut-être des commentaires)")
            # Vérifier manuellement
            settings = {}

    print("\n📋 État du Linting :")
    print("-" * 70)

    # Vérifications
    checks = {
        "python.linting.enabled": False,
        "python.linting.flake8Enabled": False,
        "python.linting.pylintEnabled": False,
    }

    all_ok = True

    for key, expected in checks.items():
        actual = settings.get(key, "non défini")
        status = "✅" if actual == expected else "❌"
        print(f"{status} {key}: {actual} (attendu: {expected})")
        if actual != expected:
            all_ok = False

    print("\n" + "=" * 70)

    if all_ok or 'python.linting.enabled": false' in content.lower():
        print("✅ CONFIGURATION CORRECTE - Le linting est désactivé!")
        print("\n📝 Prochaine étape :")
        print("   → Rechargez VSCode : Ctrl+Shift+P → 'Reload Window'")
        return True
    else:
        print("❌ PROBLÈME DÉTECTÉ - Le linting est encore activé")
        print("\n🔧 Solution :")
        print("   1. Ouvrez .vscode/settings.json")
        print('   2. Ajoutez : "python.linting.enabled": false')
        print("   3. Rechargez VSCode")
        return False


if __name__ == '__main__':
    verifier_configuration()
